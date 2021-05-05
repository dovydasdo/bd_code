import torch
from config import options
import data
from transformers import GPT2Tokenizer


device = torch.device("cuda")

with open(options["save_path"], 'rb') as f:
    model = torch.load(f).to(device)

model.eval()

if options["tokenizer"] == "char" or options["tokenizer"] == "word":
    corpus = data.Corpus(options["data_path"], options["tokenizer"])
    ntokens = len(corpus.dictionary)

if options["tokenizer"] == "bpe":
    corpus = GPT2Tokenizer.from_pretrained('gpt2')
    ntokens = len(corpus.get_vocab())

input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device)

with open(options["generated_path"], 'w', encoding="utf-8") as outf:
    with torch.no_grad():
        if options["tokenizer"] == "char":
            for i in range(1500):
                output = model(input, False)
                char_weights = output.squeeze().div(1).exp().cpu()

                char_idx = torch.multinomial(char_weights, 1)
                char_idx = char_idx[0]
                input.fill_(char_idx)
                char = corpus.dictionary.idx2char[char_idx]

                outf.write(char + ('\n' if i % 100 == 99 else ''))

                if i % 100 == 0:
                    print('| Generated {}/{} chars'.format(i, 1500))
        if options["tokenizer"] == "bpe":
            for i in range(1000):
                output = model(input, False)
                bpe_weights = output.squeeze().div(1).exp().cpu()

                bpe_idx = torch.multinomial(bpe_weights, 1)
                bpe_idx = bpe_idx[0]
                input.fill_(bpe_idx)
                bpe = corpus.decode(bpe_idx)

                outf.write(bpe + ('\n' if i % 100 == 99 else ''))

                if i % 100 == 0:
                    print('| Generated {}/{} pairs'.format(i, 1000))
        if options["tokenizer"] == "word":
            for i in range(500):
                output = model(input, False)
                word_weights = output.squeeze().div(1).exp().cpu()

                word_idx = torch.multinomial(word_weights, 1)
                word_idx = word_idx[0]
                input.fill_(word_idx)
                word = corpus.dictionary.idx2word[word_idx]

                outf.write(word + ('\n' if i % 100 == 99 else ''))

                if i % 100 == 0:
                    print('| Generated {}/{} words'.format(i, 1000))