#library imports
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import re
import spacy
import jovian
from collections import Counter
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
import string
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from sklearn.metrics import mean_squared_error
from spacy.lang.en.examples import sentences 


df = pd.read_csv("Help_Desk_Data_Cleaned_for_Category_Model.csv")

classes = {"Conditions": 0, "Conditions (Breach)" : 1, "Conditions (Essential Services)": 2, "Conditions (General)" : 3, "English" : 4, "Eviction" : 5, "Eviction (General)" : 6, "Eviction (Post-Filing)" : 7, "Eviction (Post-Judgment)": 8, "Eviction (Pre-Filing | Prevention)": 9, "Eviction (Pre-Filing)" :10, "Eviction (Sealing)": 11, "Foreclosure": 12, "Invalid Inquiry": 13, "Leases": 14, "Lockout": 15, "Lockout (Constructive)": 16, "Other" : 17, "Rental Assistance": 18, "Security Deposit": 19}
df['Answer Category'] = df['Answer Category'].apply(lambda x: classes[x])

#tokenization
tok = spacy.load("en_core_web_sm")
def tokenize (text):
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]') # remove punctuation and numbers
    nopunct = regex.sub(" ", text.lower())
    return [token.text for token in tok.tokenizer(nopunct)]

counts = Counter()
for index, row in df.iterrows():
    counts.update(tokenize(row['Inquiry']))



#deleting infrequent words
print("num_words before:",len(counts.keys()))
for word in list(counts):
    if counts[word] < 2:
        del counts[word]
print("num_words after:",len(counts.keys()))

#creating vocabulary
vocab2index = {"":0, "UNK":1}
words = ["", "UNK"]
for word in counts:
    vocab2index[word] = len(words)
    words.append(word)

def encode_sentence(text, vocab2index, N=70):
    tokenized = tokenize(text)
    encoded = np.zeros(N, dtype=int)
    enc1 = np.array([vocab2index.get(word, vocab2index["UNK"]) for word in tokenized])
    length = min(N, len(enc1))
    encoded[:length] = enc1[:length]
    return encoded, length

df['encoded'] = df['Inquiry'].apply(lambda x: np.array(encode_sentence(x,vocab2index )))
df.head()
Counter(df['Answer Category'])

X = list(df['encoded'])
y = list(df['Answer Category'])
from sklearn.model_selection import train_test_split
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2)

class DfDataset(Dataset):
    def __init__(self, X, Y):
        self.X = X
        self.y = Y
        
    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, idx):
        return torch.from_numpy(self.X[idx][0].astype(np.int32)), self.y[idx], self.X[idx][1]

train_ds = DfDataset(X_train, y_train)
valid_ds = DfDataset(X_valid, y_valid)


def train_model(model, epochs=10, lr=0.001):
    parameters = filter(lambda p: p.requires_grad, model.parameters())
    optimizer = torch.optim.Adam(parameters, lr=lr)
    for i in range(epochs):
        model.train()
        sum_loss = 0.0
        total = 0
        for x, y, l in train_dl:
            x = x.long()
            y = y.long()
            y_pred = model(x, l)
            optimizer.zero_grad()
            loss = F.cross_entropy(y_pred, y)
            loss.backward()
            optimizer.step()
            sum_loss += loss.item()*y.shape[0]
            total += y.shape[0]
        val_loss, val_acc, val_rmse = validation_metrics(model, val_dl)
        if i % 5 == 1:
            print("train loss %.3f, val loss %.3f, val accuracy %.3f, and val rmse %.3f" % (sum_loss/total, val_loss, val_acc, val_rmse))

def validation_metrics (model, valid_dl):
    model.eval()
    correct = 0
    total = 0
    sum_loss = 0.0
    sum_rmse = 0.0
    for x, y, l in valid_dl:
        x = x.long()
        y = y.long()
        y_hat = model(x, l)
        loss = F.cross_entropy(y_hat, y)
        pred = torch.max(y_hat, 1)[1]
        correct += (pred == y).float().sum()
        total += y.shape[0]
        sum_loss += loss.item()*y.shape[0]
        sum_rmse += np.sqrt(mean_squared_error(pred, y.unsqueeze(-1)))*y.shape[0]
    return sum_loss/total, correct/total, sum_rmse/total

batch_size = 5000
vocab_size = len(words)
train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
val_dl = DataLoader(valid_ds, batch_size=batch_size)


class LSTM_fixed_len(torch.nn.Module) :
    def __init__(self, vocab_size, embedding_dim, hidden_dim) :
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.linear = nn.Linear(hidden_dim, 20)
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, x, l):
        x = self.embeddings(x)
        x = self.dropout(x)
        lstm_out, (ht, ct) = self.lstm(x)
        return self.linear(ht[-1])


model_fixed =  LSTM_fixed_len(vocab_size, 50, 50)
# train_model(model_fixed, epochs=500, lr=0.1)
train_model(model_fixed, epochs=30, lr=0.060)
train_model(model_fixed, epochs=30, lr=0.060)

# x = torch.tensor([[1,2, 12,34, 56,78, 90,80],
#                  [12,45, 99,67, 6,23, 77,82],
#                  [3,24, 6,99, 12,56, 21,22]])

# model1 = nn.Embedding(100, 7, padding_idx=0)
# model2 = nn.LSTM(input_size=7, hidden_size=3, num_layers=1, batch_first=True)

# out1 = model1(x)
# out2 = model2(out1)

# print(out1.shape)
# print(out1)