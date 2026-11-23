"""
TF-IDF Baseline Classification Model for OfficeMate 2.0
CSE472 Deep Learning for NLP - Baseline Implementation
Uses Scikit-learn TF-IDF Vectorizer + Logistic Regression Classifier.
"""

import os
import pickle
from typing import Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from nlp.preprocessor import normalize
from nlp.dataset import get_train_val_test_splits

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
VECT_FILE = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
DEPT_MODEL_FILE = os.path.join(MODEL_DIR, "tfidf_dept_model.pkl")
INTENT_MODEL_FILE = os.path.join(MODEL_DIR, "tfidf_intent_model.pkl")

class TfidfBaselineClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=2500,
            sublinear_tf=True
        )
        self.dept_classifier = LogisticRegression(max_iter=1000, random_state=42, C=1.5)
        self.intent_classifier = LogisticRegression(max_iter=1000, random_state=42, C=1.5)
        self.is_trained = False

    def train(self, train_data, val_data=None):
        X_train_raw = [normalize(d["text"]) for d in train_data]
        y_train_dept = [d["dept"] for d in train_data]
        y_train_intent = [d["intent"] for d in train_data]

        X_train_vec = self.vectorizer.fit_transform(X_train_raw)
        self.dept_classifier.fit(X_train_vec, y_train_dept)
        self.intent_classifier.fit(X_train_vec, y_train_intent)
        self.is_trained = True

    def predict(self, text: str) -> Dict[str, Any]:
        if not self.is_trained:
            self.load()

        norm_text = normalize(text)
        vec = self.vectorizer.transform([norm_text])

        # Dept prediction & confidence
        dept_probs = self.dept_classifier.predict_proba(vec)[0]
        dept_idx = dept_probs.argmax()
        dept_pred = self.dept_classifier.classes_[dept_idx]
        dept_conf = float(dept_probs[dept_idx])

        # Intent prediction & confidence
        intent_probs = self.intent_classifier.predict_proba(vec)[0]
        intent_idx = intent_probs.argmax()
        intent_pred = self.intent_classifier.classes_[intent_idx]
        intent_conf = float(intent_probs[intent_idx])

        dept_prob_dict = {cls: float(prob) for cls, prob in zip(self.dept_classifier.classes_, dept_probs)}

        return {
            "department": dept_pred,
            "department_confidence": dept_conf,
            "department_probabilities": dept_prob_dict,
            "intent": intent_pred,
            "intent_confidence": intent_conf,
            "model": "TF-IDF + LogisticRegression Baseline"
        }

    def save(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        with open(VECT_FILE, "wb") as f:
            pickle.dump(self.vectorizer, f)
        with open(DEPT_MODEL_FILE, "wb") as f:
            pickle.dump(self.dept_classifier, f)
        with open(INTENT_MODEL_FILE, "wb") as f:
            pickle.dump(self.intent_classifier, f)

    def load(self):
        if not (os.path.exists(VECT_FILE) and os.path.exists(DEPT_MODEL_FILE)):
            # If not yet saved, train on the fly
            train, _, _ = get_train_val_test_splits()
            self.train(train)
            self.save()
            return

        with open(VECT_FILE, "rb") as f:
            self.vectorizer = pickle.load(f)
        with open(DEPT_MODEL_FILE, "rb") as f:
            self.dept_classifier = pickle.load(f)
        if os.path.exists(INTENT_MODEL_FILE):
            with open(INTENT_MODEL_FILE, "rb") as f:
                self.intent_classifier = pickle.load(f)
        self.is_trained = True

if __name__ == "__main__":
    train, val, test = get_train_val_test_splits()
    clf = TfidfBaselineClassifier()
    clf.train(train, val)
    clf.save()

    # Quick test
    test_q = "How do I setup GlobalProtect VPN on my Mac?"
    res = clf.predict(test_q)
    print(f"Sample query: '{test_q}' -> Dept: {res['department']} ({res['department_confidence']:.2%}) | Intent: {res['intent']}")
