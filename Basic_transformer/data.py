import os
from io import open
import torch
from transformers import GPT2Tokenizer

class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)


class CharDictionary(object):
    def __init__(self):
        self.char2idx = {}
        self.idx2char = []

    def add_char(self, char):
        if char not in self.char2idx:
            self.idx2char.append(char)
            self.char2idx[char] = len(self.idx2char) - 1
        return self.char2idx[char]

    def __len__(self):
        return len(self.idx2char)


class Corpus(object):
    def __init__(self, path, tokenizer):
        if tokenizer == "bpe":
            self.dictionary = GPT2Tokenizer.from_pretrained('gpt2')
            self.train = self.tokenize_bpe(os.path.join(path, 'train.txt'))
            self.valid = self.tokenize_bpe(os.path.join(path, 'valid.txt'))
            self.test = self.tokenize_bpe(os.path.join(path, 'test.txt'))
        elif tokenizer == "word":
            self.dictionary = Dictionary()
            self.train = self.tokenize(os.path.join(path, 'train.txt'))
            self.valid = self.tokenize(os.path.join(path, 'valid.txt'))
            self.test = self.tokenize(os.path.join(path, 'test.txt'))
        elif tokenizer == "char":
            self.dictionary = CharDictionary()
            self.train = self.tokenize_char(os.path.join(path, 'train.txt'))
            self.valid = self.tokenize_char(os.path.join(path, 'valid.txt'))
            self.test = self.tokenize_char(os.path.join(path, 'test.txt'))
        else:
            print("Wrong tokenizer name")
            exit()

    def tokenize(self, path):
        print(path)
        assert os.path.exists(path)
        with open(path, 'r', encoding="utf8") as f:
            data = f.read()
            comms = data.split("<EOS>")
            for line in comms:
                words = line.split()
                words.append("<EOS>")
                for word in words:
                    self.dictionary.add_word(word)

        with open(path, 'r', encoding="utf8") as f:
            idss = []
            data = f.read()
            comms = data.split("<EOS>")
            for line in comms:
                words = line.split()
                ids = []
                words.append("<EOS>")
                for word in words:
                    ids.append(self.dictionary.word2idx[word])
                idss.append(torch.tensor(ids).type(torch.int64))
                #idss.append(torch.tensor(self.dictionary(line)['input_ids']).type(torch.int64))
            ids = torch.cat(idss)
        return ids

    def tokenize_bpe(self, path):
        print(path)
        assert os.path.exists(path)
        with open(path, 'r', encoding="utf8") as f:
            idss = []
            data = f.read()
            comms = data.split("<EOS>")
            for line in comms:
                idss.append(torch.tensor(self.dictionary(line)['input_ids']).type(torch.int64))
            ids = torch.cat(idss)
        return ids

    def tokenize_char(self, path):
        print(path)
        assert os.path.exists(path)
        with open(path, 'r', encoding="utf8") as f:
            data = f.read()
            comms = data.split("<EOS>")
            for line in comms:
                line += "<EOS>"
                for char in line:
                    self.dictionary.add_char(char)
        with open(path, 'r', encoding="utf8") as f:
            idss = []
            data = f.read()
            comms = data.split("<EOS>")
            for line in comms:
                line += "<EOS>"
                ids = []
                for char in line:
                    ids.append(self.dictionary.char2idx[char])
                idss.append(torch.tensor(ids).type(torch.int64))
                # idss.append(torch.tensor(self.dictionary(line)['input_ids']).type(torch.int64))
            ids = torch.cat(idss)
        return ids
