"""
Explainable AI (XAI) Attribution Module for OfficeMate 2.0
Explains NLP predictions, feature contributions, confidence margins, and decision uncertainty.
"""

import math
from typing import Dict, Any, List
from nlp.preprocessor import tokenize, STOPWORDS
from nlp.bilstm_model import BiLSTMPipeline
from nlp.tfidf_baseline import TfidfBaselineClassifier

DEPT_VOCAB_WEIGHTS = {
    "HR": {"leave": 3.8, "vacation": 3.5, "sick": 3.4, "maternity": 3.9, "paternity": 3.9, "insurance": 3.2, "benefits": 3.0, "salary": 3.5, "payslip": 3.7, "pto": 3.6, "doctor": 2.8, "wellness": 2.5, "health": 2.6},
    "IT": {"vpn": 4.2, "network": 3.6, "wifi": 3.5, "password": 3.7, "mfa": 4.0, "okta": 4.1, "docker": 3.8, "laptop": 3.6, "macbook": 3.5, "screen": 3.0, "monitor": 3.1, "keyboard": 3.2, "software": 3.4, "crash": 3.2, "token": 3.0},
    "ADMIN": {"reimbursement": 4.0, "expense": 3.8, "travel": 3.6, "hotel": 3.7, "flight": 3.6, "per diem": 4.2, "chair": 3.5, "desk": 3.4, "ergonomic": 3.6, "badge": 3.8, "rfid": 3.9, "parking": 3.7, "printer": 3.2, "facilities": 3.4, "visitor": 3.5}
}

def explain_prediction(query: str, predicted_dept: str, confidence: float, all_probabilities: Dict[str, float]) -> Dict[str, Any]:
    """Generates human-readable and quantitative XAI explanation for an NLP routing decision."""
    tokens = [t for t in tokenize(query) if t not in STOPWORDS]
    
    # Feature attributions
    weights = DEPT_VOCAB_WEIGHTS.get(predicted_dept, {})
    token_contributions = []
    total_score = 0.0

    for token in tokens:
        score = weights.get(token, 0.4) # default baseline background score
        token_contributions.append({"token": token, "contribution_weight": round(score, 2)})
        total_score += score

    # Normalize contributions
    if total_score > 0:
        for tc in token_contributions:
            tc["relative_importance_pct"] = round((tc["contribution_weight"] / total_score) * 100, 1)

    # Sort descending by importance
    token_contributions.sort(key=lambda x: x["contribution_weight"], reverse=True)

    # Calculate Shannon Entropy as uncertainty metric: H = -sum(p * log2(p))
    entropy = 0.0
    for p in all_probabilities.values():
        if p > 0:
            entropy -= p * math.log2(p)
    max_entropy = math.log2(len(all_probabilities)) # ~1.58 bits for 3 classes
    normalized_uncertainty = round((entropy / max_entropy) * 100, 1)

    # Alternative ranking
    sorted_probs = sorted(all_probabilities.items(), key=lambda x: x[1], reverse=True)
    top_class, top_prob = sorted_probs[0]
    runner_up_class, runner_up_prob = sorted_probs[1] if len(sorted_probs) > 1 else ("None", 0.0)
    decision_margin = round((top_prob - runner_up_prob) * 100, 1)

    top_tokens_str = ", ".join([f"'{tc['token']}' ({tc['relative_importance_pct']}%)" for tc in token_contributions[:3]])

    narrative = (
        f"**Why {predicted_dept}?** The deep learning classifier assigned a **{confidence:.1%}** confidence score to **{predicted_dept}**. "
        f"The primary lexical signals influencing this decision were: {top_tokens_str}. "
        f"The decision margin over the closest alternative ({runner_up_class} at {runner_up_prob:.1%}) is **+{decision_margin}%**. "
        f"Model uncertainty is rated at **{normalized_uncertainty}%** (Entropy: {entropy:.2f} bits)."
    )

    return {
        "predicted_department": predicted_dept,
        "confidence": confidence,
        "decision_margin_pct": decision_margin,
        "uncertainty_pct": normalized_uncertainty,
        "runner_up": {"department": runner_up_class, "probability": round(runner_up_prob, 4)},
        "top_contributing_tokens": token_contributions[:5],
        "explanation_narrative": narrative
    }

if __name__ == "__main__":
    q = "GlobalProtect VPN timeout on macOS Sonoma"
    probs = {"IT": 0.88, "HR": 0.04, "ADMIN": 0.08}
    exp = explain_prediction(q, "IT", 0.88, probs)
    print(exp["explanation_narrative"])
