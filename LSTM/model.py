import torch.nn as nn
import torch.nn.functional as F


class RNNModel(nn.Module):

    def __init__(self, ntoken, emb_size, n_hidden, n_layers, dropout=0.1):
        super(RNNModel, self).__init__()
        self.ntoken = ntoken
        self.drop = nn.Dropout(dropout)
        self.encoder = nn.Embedding(ntoken, emb_size)
        self.rnn = getattr(nn, "LSTM")(emb_size, n_hidden, n_layers, dropout=dropout)
        self.decoder = nn.Linear(n_hidden, ntoken)
        self.init_weights()
        self.nhid = n_hidden
        self.nlayers = n_layers

    def init_weights(self):
        initrange = 0.1
        nn.init.uniform_(self.encoder.weight, -initrange, initrange)
        nn.init.zeros_(self.decoder.weight)
        nn.init.uniform_(self.decoder.weight, -initrange, initrange)

    def forward(self, input, hidden):
        emb = self.drop(self.encoder(input))
        output, hidden = self.rnn(emb, hidden)
        output = self.drop(output)
        decoded = self.decoder(output)
        decoded = decoded.view(-1, self.ntoken)
        return F.log_softmax(decoded, dim=1), hidden

    def init_hidden(self, bsz):
        weight = next(self.parameters())
        return (weight.new_zeros(self.nlayers, bsz, self.nhid),
                weight.new_zeros(self.nlayers, bsz, self.nhid))
