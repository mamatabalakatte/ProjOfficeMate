"""
Bidirectional LSTM Deep Learning Architecture for OfficeMate 2.0
CSE472 Deep Learning for NLP - Deep Learning Neural Network
PyTorch Implementation with Bi-LSTM, Dropout, Batch Normalization, and Multi-head Output.
"""

import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from typing import Dict, Any, List, Tuple
from nlp.preprocessor import tokenize

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
WEIGHTS_FILE = os.path.join(MODEL_DIR, "bilstm_model.pt")
META_FILE = os.path.join(MODEL_DIR, "bilstm_meta.json")

class Vocabulary:
    def __init__(self, max_size=3000):
        self.max_size = max_size
        self.word2idx = {"<PAD>": 0, "<UNK>": 1}
        self.idx2word = {0: "<PAD>", 1: "<UNK>"}
        self.word_counts = {}

    def build_vocab(self, texts: List[str]):
        for text in texts:
            tokens = tokenize(text)
            for token in tokens:
                self.word_counts[token] = self.word_counts.get(token, 0) + 1

        sorted_words = sorted(self.word_counts.items(), key=lambda x: x[1], reverse=True)
        for word, _ in sorted_words[:self.max_size - 2]:
            idx = len(self.word2idx)
            self.word2idx[word] = idx
            self.idx2word[idx] = word

    def encode(self, text: str, max_len: int = 32) -> List[int]:
        tokens = tokenize(text)
        indices = [self.word2idx.get(t, 1) for t in tokens]
        if len(indices) < max_len:
            indices = indices + [0] * (max_len - len(indices))
        else:
            indices = indices[:max_len]
        return indices

    def to_dict(self):
        return {"word2idx": self.word2idx, "max_size": self.max_size}

    @classmethod
    def from_dict(cls, d):
        v = cls(max_size=d["max_size"])
        v.word2idx = d["word2idx"]
        v.idx2word = {int(v): k for k, v in d["word2idx"].items()}
        return v

class TextDataset(Dataset):
    def __init__(self, data: List[Dict[str, Any]], vocab: Vocabulary, dept_map: Dict[str, int], intent_map: Dict[str, int], max_len: int = 32):
        self.samples = []
        for item in data:
            enc = vocab.encode(item["text"], max_len)
            d_idx = dept_map[item["dept"]]
            i_idx = intent_map[item["intent"]]
            self.samples.append((torch.tensor(enc, dtype=torch.long), torch.tensor(d_idx, dtype=torch.long), torch.tensor(i_idx, dtype=torch.long)))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

class BiLSTMClassifier(nn.Module):
    def __init__(self, vocab_size: int, embedding_dim: int = 64, hidden_dim: int = 64, num_layers: int = 2,
                 num_depts: int = 3, num_intents: int = 8, dropout: float = 0.3):
        super(BiLSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.emb_dropout = nn.Dropout(dropout)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.fc_shared = nn.Sequential(
            nn.Linear(hidden_dim * 2, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        self.dept_head = nn.Linear(64, num_depts)
        self.intent_head = nn.Linear(64, num_intents)

    def forward(self, x):
        emb = self.emb_dropout(self.embedding(x))
        lstm_out, (hn, cn) = self.lstm(emb)
        # Global max pooling over sequence dimension
        pooled, _ = torch.max(lstm_out, dim=1)
        feat = self.fc_shared(pooled)
        dept_logits = self.dept_head(feat)
        intent_logits = self.intent_head(feat)
        return dept_logits, intent_logits

class BiLSTMPipeline:
    def __init__(self):
        self.device = torch.device("cpu")
        self.vocab = Vocabulary()
        self.dept_map = {"HR": 0, "IT": 1, "ADMIN": 2}
        self.inv_dept_map = {0: "HR", 1: "IT", 2: "ADMIN"}
        self.intent_map = {}
        self.inv_intent_map = {}
        self.model = None
        self.max_len = 32

    def train_model(self, train_data, val_data, epochs: int = 25, batch_size: int = 16, lr: float = 0.003):
        intents = sorted(list(set(d["intent"] for d in train_data)))
        self.intent_map = {intent: i for i, intent in enumerate(intents)}
        self.inv_intent_map = {i: intent for i, intent in enumerate(intents)}

        texts = [d["text"] for d in train_data]
        self.vocab.build_vocab(texts)

        train_ds = TextDataset(train_data, self.vocab, self.dept_map, self.intent_map, self.max_len)
        val_ds = TextDataset(val_data, self.vocab, self.dept_map, self.intent_map, self.max_len)

        train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

        self.model = BiLSTMClassifier(
            vocab_size=len(self.vocab.word2idx),
            embedding_dim=64,
            hidden_dim=64,
            num_layers=2,
            num_depts=len(self.dept_map),
            num_intents=len(self.intent_map),
            dropout=0.3
        ).to(self.device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.AdamW(self.model.parameters(), lr=lr, weight_decay=1e-4)

        best_val_loss = float("inf")
        history = {"train_loss": [], "val_loss": [], "val_acc": []}

        for epoch in range(epochs):
            self.model.train()
            total_train_loss = 0.0
            for x, y_d, y_i in train_loader:
                x, y_d, y_i = x.to(self.device), y_d.to(self.device), y_i.to(self.device)
                optimizer.zero_grad()
                d_logits, i_logits = self.model(x)
                loss = criterion(d_logits, y_d) + 0.5 * criterion(i_logits, y_i)
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()
                total_train_loss += loss.item()

            avg_train_loss = total_train_loss / len(train_loader)

            # Validation
            self.model.eval()
            total_val_loss = 0.0
            correct_dept = 0
            total_samples = 0
            with torch.no_grad():
                for x, y_d, y_i in val_loader:
                    x, y_d, y_i = x.to(self.device), y_d.to(self.device), y_i.to(self.device)
                    d_logits, i_logits = self.model(x)
                    loss = criterion(d_logits, y_d) + 0.5 * criterion(i_logits, y_i)
                    total_val_loss += loss.item()
                    preds = torch.argmax(d_logits, dim=1)
                    correct_dept += (preds == y_d).sum().item()
                    total_samples += y_d.size(0)

            avg_val_loss = total_val_loss / len(val_loader)
            val_acc = correct_dept / total_samples

            history["train_loss"].append(round(avg_train_loss, 4))
            history["val_loss"].append(round(avg_val_loss, 4))
            history["val_acc"].append(round(val_acc, 4))

            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                self.save()

        return history

    def predict(self, text: str) -> Dict[str, Any]:
        if self.model is None:
            self.load()

        self.model.eval()
        encoded = self.vocab.encode(text, self.max_len)
        x = torch.tensor([encoded], dtype=torch.long).to(self.device)

        with torch.no_grad():
            d_logits, i_logits = self.model(x)
            d_probs = torch.softmax(d_logits, dim=-1)[0].cpu().numpy()
            i_probs = torch.softmax(i_logits, dim=-1)[0].cpu().numpy()

        dept_idx = int(d_probs.argmax())
        dept = self.inv_dept_map[dept_idx]
        dept_conf = float(d_probs[dept_idx])

        intent_idx = int(i_probs.argmax())
        intent = self.inv_intent_map.get(intent_idx, "general_inquiry")
        intent_conf = float(i_probs[intent_idx])

        dept_prob_dict = {self.inv_dept_map[i]: float(prob) for i, prob in enumerate(d_probs)}

        return {
            "department": dept,
            "department_confidence": dept_conf,
            "department_probabilities": dept_prob_dict,
            "intent": intent,
            "intent_confidence": intent_conf,
            "model": "Bidirectional LSTM (Deep Learning Neural Network)"
        }

    def save(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        if self.model:
            torch.save(self.model.state_dict(), WEIGHTS_FILE)
        meta = {
            "vocab": self.vocab.to_dict(),
            "dept_map": self.dept_map,
            "inv_dept_map": {str(k): v for k, v in self.inv_dept_map.items()},
            "intent_map": self.intent_map,
            "inv_intent_map": {str(k): v for k, v in self.inv_intent_map.items()},
            "max_len": self.max_len
        }
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    def load(self):
        if not (os.path.exists(WEIGHTS_FILE) and os.path.exists(META_FILE)):
            from nlp.dataset import get_train_val_test_splits
            train, val, _ = get_train_val_test_splits()
            self.train_model(train, val, epochs=15)
            return

        with open(META_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.vocab = Vocabulary.from_dict(meta["vocab"])
        self.dept_map = meta["dept_map"]
        self.inv_dept_map = {int(k): v for k, v in meta["inv_dept_map"].items()}
        self.intent_map = meta["intent_map"]
        self.inv_intent_map = {int(k): v for k, v in meta["inv_intent_map"].items()}
        self.max_len = meta["max_len"]

        self.model = BiLSTMClassifier(
            vocab_size=len(self.vocab.word2idx),
            embedding_dim=64,
            hidden_dim=64,
            num_layers=2,
            num_depts=len(self.dept_map),
            num_intents=len(self.intent_map),
            dropout=0.3
        ).to(self.device)

        self.model.load_state_dict(torch.load(WEIGHTS_FILE, map_location=self.device, weights_only=True))
        self.model.eval()

if __name__ == "__main__":
    from nlp.dataset import get_train_val_test_splits
    train, val, test = get_train_val_test_splits()
    pipe = BiLSTMPipeline()
    hist = pipe.train_model(train, val, epochs=15)
    print("Bi-LSTM Trained Successfully! Final Val Acc:", hist["val_acc"][-1])
    test_q = "Need to submit doctor certificate for 3 days sick leave."
    out = pipe.predict(test_q)
    print(f"Sample prediction: '{test_q}' -> Dept: {out['department']} ({out['department_confidence']:.2%}) | Intent: {out['intent']}")
