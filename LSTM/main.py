import time
import math
import torch
import torch.nn as nn
import data
import model
from config import options

if torch.cuda.is_available():
    print("CUDA ON")
else:
    print("CUDA OFF")

device = torch.device("cuda")
print(str(device) + " --- DEVICE")
corpus = data.Corpus(options["data_path"])
eval_batch_size = 10


def batchify(data, batch_sz):
    nbatch = data.size(0) // batch_sz
    data = data.narrow(0, 0, nbatch * batch_sz)
    data = data.view(batch_sz, -1).t().contiguous()
    return data.to(device)


train_data = batchify(corpus.train, options["batch_size"])
val_data = batchify(corpus.valid, eval_batch_size)
test_data = batchify(corpus.test, eval_batch_size)

ntokens = len(corpus.dictionary)
model = model.RNNModel(ntokens,
                       options["embedding_size"],
                       options["num_of_hidden"],
                       options["num_of_layers"],
                       options["dropout"]).to(device)


def get_loss_and_train_op(net, lr=options["learning_rate"]):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=lr)

    return criterion, optimizer


criterion, optimizer = get_loss_and_train_op(model)

lr = options["learning_rate"]
best_val_loss = None


def repackage_hidden(h):
    if isinstance(h, torch.Tensor):
        return h.detach()
    else:
        return tuple(repackage_hidden(v) for v in h)


def get_batch(source, i):
    seq_len = min(options["seq_len"], len(source) - 1 - i)
    data = source[i:i + seq_len]
    target = source[i + 1:i + 1 + seq_len].view(-1)
    return data, target


def evaluate(data_source):
    model.eval()
    total_loss = 0.
    hidden = model.init_hidden(eval_batch_size)
    with torch.no_grad():
        for i in range(0, data_source.size(0) - 1, options["seq_len"]):
            data, targets = get_batch(data_source, i)
            output, hidden = model(data, hidden)
            hidden = repackage_hidden(hidden)
            total_loss += len(data) * criterion(output, targets).item()
    return total_loss / (len(data_source) - 1)


def train():
    model.train()
    total_loss = 0.
    start_time = time.time()
    hidden = model.init_hidden(options["batch_size"])
    for batch, i in enumerate(range(0, train_data.size(0) - 1, options["seq_len"])):
        data, targets = get_batch(train_data, i)
        optimizer.zero_grad()
        hidden = repackage_hidden(hidden)
        output, hidden = model(data, hidden)
        loss = criterion(output, targets)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), options["grad_clip"])

        total_loss += loss.item()
        optimizer.step()
        if batch % 200 == 0 and batch > 0:
            cur_loss = total_loss / 200
            elapsed = time.time() - start_time
            print('| epoch {:3d} | {:5d}/{:5d} batches | lr {:01.5f} | ms/batch {:5.2f} | '
                  'loss {:5.2f} | ppl {:8.2f}'.format(
                epoch, batch, len(train_data) // options["seq_len"], lr,
                              elapsed * 1000 / 200, cur_loss, math.exp(cur_loss)))
            total_loss = 0
            start_time = time.time()


for epoch in range(1, options["epochs"] + 1):
    epoch_start_time = time.time()
    train()
    val_loss = evaluate(val_data)
    print('-' * 89)
    print('| end of epoch {:3d} | time: {:5.2f}s | valid loss {:5.2f} | '
          'valid ppl {:8.2f}'.format(epoch, (time.time() - epoch_start_time),
                                     val_loss, math.exp(val_loss)))
    print('-' * 89)
    if not best_val_loss or val_loss < best_val_loss:
        with open(options["save_path"], 'wb') as f:
            torch.save(model, f)
        best_val_loss = val_loss
    else:
        lr /= 1.1
    with open(options["save_path"], 'wb') as f:
        torch.save(model, f)

with open(options["save_path"], 'rb') as f:
    model = torch.load(f)
    model.rnn.flatten_parameters()

test_loss = evaluate(test_data)
print('=' * 89)
print('| End of training | test loss {:5.2f} | test ppl {:8.2f}'.format(
    test_loss, math.exp(test_loss)))
print('=' * 89)
