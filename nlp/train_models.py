"""
Master Training Orchestrator for OfficeMate 2.0
CSE472 Deep Learning for NLP - Project 20
Trains TF-IDF Baseline & Bi-LSTM Neural Network, saves weights, and evaluates metrics.
"""

from nlp.dataset import get_train_val_test_splits
from nlp.tfidf_baseline import TfidfBaselineClassifier
from nlp.bilstm_model import BiLSTMPipeline
from nlp.evaluator import evaluate_models

def main():
    print(">>> 1. Loading and splitting dataset...")
    train, val, test = get_train_val_test_splits()
    print(f"Dataset ready: Train={len(train)}, Val={len(val)}, Test={len(test)}")

    print("\n>>> 2. Training TF-IDF Baseline (Scikit-Learn)...")
    tfidf = TfidfBaselineClassifier()
    tfidf.train(train, val)
    tfidf.save()
    print("TF-IDF Baseline trained & saved to models/.")

    print("\n>>> 3. Training Bidirectional LSTM (PyTorch Deep Learning)...")
    lstm = BiLSTMPipeline()
    hist = lstm.train_model(train, val, epochs=20, batch_size=16)
    print(f"Bi-LSTM trained & saved to models/. Final Validation Accuracy: {hist['val_acc'][-1]:.2%}")

    print("\n>>> 4. Computing true performance metrics on held-out test set...")
    metrics = evaluate_models()
    print("\n================ BENCHMARK RESULTS ================")
    for key, m in metrics["models"].items():
        print(f"Model: {m['name']}")
        print(f"  Test Accuracy:           {m['accuracy']:.2%}")
        print(f"  Macro F1-Score:          {m['f1_macro']:.2%}")
        print(f"  Ticket Routing Accuracy: {m['ticket_routing_accuracy']:.2%}")
        print(f"  Confusion Matrix:        {m['confusion_matrix']}")
        print()
    print("===================================================")

if __name__ == "__main__":
    main()
