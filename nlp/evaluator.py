"""
Comprehensive Model Evaluation Engine for OfficeMate 2.0
CSE472 Deep Learning for NLP - Model Evaluation
Evaluates TF-IDF Baseline vs Bi-LSTM Neural Network on Test Set.
Computes real Accuracy, Precision, Recall, F1, and Confusion Matrices.
"""

import os
import json
import numpy as np
from typing import Dict, Any, List
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from nlp.dataset import get_train_val_test_splits
from nlp.tfidf_baseline import TfidfBaselineClassifier
from nlp.bilstm_model import BiLSTMPipeline
from db.database import execute_insert

METRICS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "model_evaluation_metrics.json")

def evaluate_models() -> Dict[str, Any]:
    _, _, test_data = get_train_val_test_splits()
    y_true_dept = [d["dept"] for d in test_data]
    y_true_intent = [d["intent"] for d in test_data]
    test_texts = [d["text"] for d in test_data]

    classes = ["HR", "IT", "ADMIN"]

    # 1. Evaluate TF-IDF Baseline
    tfidf = TfidfBaselineClassifier()
    tfidf.load()

    y_pred_dept_tfidf = []
    y_pred_intent_tfidf = []
    for t in test_texts:
        res = tfidf.predict(t)
        y_pred_dept_tfidf.append(res["department"])
        y_pred_intent_tfidf.append(res["intent"])

    acc_tfidf = float(accuracy_score(y_true_dept, y_pred_dept_tfidf))
    p_macro_tf, r_macro_tf, f1_macro_tf, _ = precision_recall_fscore_support(y_true_dept, y_pred_dept_tfidf, average="macro", zero_division=0)
    p_weight_tf, r_weight_tf, f1_weight_tf, _ = precision_recall_fscore_support(y_true_dept, y_pred_dept_tfidf, average="weighted", zero_division=0)
    cm_tfidf = confusion_matrix(y_true_dept, y_pred_dept_tfidf, labels=classes).tolist()
    intent_acc_tfidf = float(accuracy_score(y_true_intent, y_pred_intent_tfidf))

    # 2. Evaluate Bi-LSTM Deep Learning Model
    bilstm = BiLSTMPipeline()
    bilstm.load()

    y_pred_dept_lstm = []
    y_pred_intent_lstm = []
    for t in test_texts:
        res = bilstm.predict(t)
        y_pred_dept_lstm.append(res["department"])
        y_pred_intent_lstm.append(res["intent"])

    acc_lstm = float(accuracy_score(y_true_dept, y_pred_dept_lstm))
    p_macro_lstm, r_macro_lstm, f1_macro_lstm, _ = precision_recall_fscore_support(y_true_dept, y_pred_dept_lstm, average="macro", zero_division=0)
    p_weight_lstm, r_weight_lstm, f1_weight_lstm, _ = precision_recall_fscore_support(y_true_dept, y_pred_dept_lstm, average="weighted", zero_division=0)
    cm_lstm = confusion_matrix(y_true_dept, y_pred_dept_lstm, labels=classes).tolist()
    intent_acc_lstm = float(accuracy_score(y_true_intent, y_pred_intent_lstm))

    results = {
        "dataset_summary": {
            "test_sample_count": len(test_data),
            "classes": classes
        },
        "models": {
            "TF_IDF_Baseline": {
                "name": "TF-IDF + Logistic Regression Baseline",
                "accuracy": round(acc_tfidf, 4),
                "precision_macro": round(float(p_macro_tf), 4),
                "precision_weighted": round(float(p_weight_tf), 4),
                "recall_macro": round(float(r_macro_tf), 4),
                "recall_weighted": round(float(r_weight_tf), 4),
                "f1_macro": round(float(f1_macro_tf), 4),
                "f1_weighted": round(float(f1_weight_tf), 4),
                "intent_accuracy": round(intent_acc_tfidf, 4),
                "ticket_routing_accuracy": round(acc_tfidf, 4),
                "confusion_matrix": cm_tfidf
            },
            "BiLSTM_DeepLearning": {
                "name": "Bidirectional LSTM (Deep Learning Neural Network)",
                "accuracy": round(acc_lstm, 4),
                "precision_macro": round(float(p_macro_lstm), 4),
                "precision_weighted": round(float(p_weight_lstm), 4),
                "recall_macro": round(float(r_macro_lstm), 4),
                "recall_weighted": round(float(r_weight_lstm), 4),
                "f1_macro": round(float(f1_macro_lstm), 4),
                "f1_weighted": round(float(f1_weight_lstm), 4),
                "intent_accuracy": round(intent_acc_lstm, 4),
                "ticket_routing_accuracy": round(acc_lstm, 4),
                "confusion_matrix": cm_lstm
            }
        }
    }

    # Save to disk
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Persist runs into SQLite DB
    try:
        execute_insert(
            """INSERT INTO model_eval_runs (model_name, accuracy, precision, recall, f1_score, confusion_matrix_json)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                results["models"]["TF_IDF_Baseline"]["name"],
                acc_tfidf, float(p_macro_tf), float(r_macro_tf), float(f1_macro_tf),
                json.dumps(cm_tfidf)
            )
        )
        execute_insert(
            """INSERT INTO model_eval_runs (model_name, accuracy, precision, recall, f1_score, confusion_matrix_json)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                results["models"]["BiLSTM_DeepLearning"]["name"],
                acc_lstm, float(p_macro_lstm), float(r_macro_lstm), float(f1_macro_lstm),
                json.dumps(cm_lstm)
            )
        )
    except Exception as e:
        print(f"Warning: could not write evaluation to DB: {e}")

    return results

def get_latest_metrics() -> Dict[str, Any]:
    if not os.path.exists(METRICS_FILE):
        return evaluate_models()
    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    res = evaluate_models()
    print("=== MODEL EVALUATION REPORT (Actual Metrics) ===")
    for k, m in res["models"].items():
        print(f"\nModel: {m['name']}")
        print(f"  Accuracy:                {m['accuracy']:.2%}")
        print(f"  F1-Score (Macro):        {m['f1_macro']:.2%}")
        print(f"  Precision (Macro):       {m['precision_macro']:.2%}")
        print(f"  Recall (Macro):          {m['recall_macro']:.2%}")
        print(f"  Ticket Routing Accuracy: {m['ticket_routing_accuracy']:.2%}")
        print(f"  Confusion Matrix:        {m['confusion_matrix']}")
