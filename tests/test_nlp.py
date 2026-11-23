"""
Unit Tests for NLP & Deep Learning Pipeline (CSE472 Project 20)
"""

import pytest
from nlp.preprocessor import clean_text, tokenize, normalize
from nlp.tfidf_baseline import TfidfBaselineClassifier
from nlp.bilstm_model import BiLSTMPipeline
from nlp.evaluator import get_latest_metrics

def test_text_preprocessing():
    raw = "Can't access https://portal.internal! Need 2 days off."
    cleaned = clean_text(raw)
    assert "https" not in cleaned
    assert "cannot" in cleaned # contraction expanded
    tokens = tokenize(raw)
    assert len(tokens) > 0
    norm = normalize(raw)
    assert isinstance(norm, str)

def test_tfidf_baseline_prediction():
    clf = TfidfBaselineClassifier()
    clf.load()
    res = clf.predict("How many vacation days can I take this year?")
    assert res["department"] in ["HR", "IT", "ADMIN"]
    assert res["department_confidence"] > 0.0
    assert "intent" in res

def test_bilstm_neural_network_prediction():
    pipe = BiLSTMPipeline()
    pipe.load()
    res = pipe.predict("GlobalProtect VPN authentication error on MacBook")
    assert res["department"] == "IT"
    assert res["department_confidence"] >= 0.50
    assert "department_probabilities" in res
    assert len(res["department_probabilities"]) == 3

def test_model_evaluation_metrics():
    metrics = get_latest_metrics()
    assert "models" in metrics
    tf = metrics["models"]["TF_IDF_Baseline"]
    lstm = metrics["models"]["BiLSTM_DeepLearning"]
    assert tf["accuracy"] > 0.80
    assert lstm["accuracy"] > 0.80
    assert "confusion_matrix" in tf
    assert len(tf["confusion_matrix"]) == 3
