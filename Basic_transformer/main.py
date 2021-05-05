import math
import time
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
corpus = data.Corpus(options["data_path"], options["tokenizer"])
eval_batch_size = 5

def batchify(data, batch_sz):
    n_batch = data.size(0) // batch_sz
    data = data.narrow(0, 0, n_batch * batch_sz)  # Resize to fit in batches
    data = data.view(batch_sz, -1).t().contiguous()
    return data.to(device)

train_data = batchify(corpus.train, options["batch_size"])
val_data = batchify(corpus.valid, eval_batch_size)
test_data = batchify(corpus.test, eval_batch_size)
n_tokens = len(corpus.dictionary)
model = model.TransformerModel(n_tokens,
                               options["embedding_size"],
                               options["num_of_heads"],
                               options["num_of_hidden"],
                               options["num_of_layers"],
                               options["dropout"]).to(device)


def get_loss_and_train_op(net, lr=0.001):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    return criterion, optimizer


criterion, optimizer = get_loss_and_train_op(model)
lr = options["learning_rate"]
best_val_loss = None


def get_batch(source, i):
    seq_len = min(options["seq_len"], len(source) - 1 - i)

    data = source[i:i + seq_len]

    target = source[i + 1:i + 1 + seq_len].view(-1)
    return data, target


def evaluate(data_source):
    model.eval()
    total_loss = 0.
    ntokens = len(corpus.dictionary)
    with torch.no_grad():
        for i in range(0, data_source.size(0) - 1, options["seq_len"]):
            data, targets = get_batch(data_source, i)
            output = model(data)
            output = output.view(-1, ntokens)
            total_loss += len(data) * criterion(output, targets).item()
    return total_loss / (len(data_source) - 1)


def train():
    model.train()

    total_loss = 0.
    start_time = time.time()
    n_tokens = len(corpus.dictionary)
    for batch, i in enumerate(range(0, train_data.size(0) - 1, options["seq_len"])):
        data, targets = get_batch(train_data, i)
        optimizer.zero_grad()
        output = model(data)
        output = output.view(-1, n_tokens)
        loss = criterion(output, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), options["grad_clip"])
        total_loss += loss.item()
        optimizer.step()

        if batch % 200 == 0 and batch > 0:
            print(optimizer)
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
    with open(options["save_path"], 'wb') as f:
        print("SAVING")
        torch.save(model, f)
        print("SAVED")

with open(options["save_path"], 'rb') as f:
    model = torch.load(f)
test_loss = evaluate(test_data)
