"""
Page 15: Model Evaluation Dashboard
CSE472 Deep Learning for NLP - Project 20 Mandatory Requirement
Presents actual evaluation results: Accuracy, Precision, Recall, F1,
Confusion Matrix, and side-by-side TF-IDF Baseline vs Bi-LSTM comparison.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from nlp.evaluator import get_latest_metrics, evaluate_models
from simulation.explainable_ai import explain_prediction
from nlp.bilstm_model import BiLSTMPipeline
from nlp.tfidf_baseline import TfidfBaselineClassifier
from frontend.components.illustrations import render_banner_picture

st.set_page_config(page_title="Model Evaluation | OfficeMate 2.0", page_icon="🧪", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">🧪 Deep Learning &amp; NLP Model Evaluation</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      CSE472 Project 20 Evaluation: Real metrics from trained models on held-out test partitions.
    </p>
  </div>
  <div>
    <span class="om-badge badge-success">Actual Evaluation Data (No Synthetic Metrics)</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Deep Learning Lab Hero Banner
render_banner_picture("model_evaluation.png", caption="🧪 Deep Learning & NLP Model Evaluation • Bi-LSTM vs TF-IDF Baseline")
st.write("")

metrics = get_latest_metrics()
tf = metrics["models"]["TF_IDF_Baseline"]
lstm = metrics["models"]["BiLSTM_DeepLearning"]
classes = metrics["dataset_summary"]["classes"]

# Model Comparison Metric Strip
st.subheader("📊 Primary Benchmark Comparison (Test Set)")
c1, c2, c3, c4 = st.columns(4)
with c1:
    delta_acc = round((lstm["accuracy"] - tf["accuracy"]) * 100, 2)
    delta_str = f"+{delta_acc}%" if delta_acc >= 0 else f"{delta_acc}%"
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{lstm['accuracy']:.1%}</div>
      <div class="stat-label">Bi-LSTM Test Accuracy ({delta_str} vs Base)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{lstm['f1_macro']:.1%}</div>
      <div class="stat-label">Bi-LSTM Macro F1-Score (Base: {tf['f1_macro']:.1%})</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{lstm['precision_macro']:.1%}</div>
      <div class="stat-label">Bi-LSTM Precision (Base: {tf['precision_macro']:.1%})</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{lstm['ticket_routing_accuracy']:.1%}</div>
      <div class="stat-label">Ticket Routing Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Side-by-Side Detailed Metrics Table
st.subheader("📋 Comprehensive Performance Breakdown")
comp_data = {
    "Evaluation Metric": [
        "Classification Accuracy",
        "Macro Precision",
        "Weighted Precision",
        "Macro Recall",
        "Weighted Recall",
        "Macro F1-Score",
        "Weighted F1-Score",
        "Fine-Grained Intent Accuracy",
        "Ticket-Routing Accuracy"
    ],
    "TF-IDF + Logistic Regression Baseline": [
        f"{tf['accuracy']:.2%}",
        f"{tf['precision_macro']:.2%}",
        f"{tf['precision_weighted']:.2%}",
        f"{tf['recall_macro']:.2%}",
        f"{tf['recall_weighted']:.2%}",
        f"{tf['f1_macro']:.2%}",
        f"{tf['f1_weighted']:.2%}",
        f"{tf['intent_accuracy']:.2%}",
        f"{tf['ticket_routing_accuracy']:.2%}"
    ],
    "Bidirectional LSTM Deep Learning Neural Network": [
        f"{lstm['accuracy']:.2%}",
        f"{lstm['precision_macro']:.2%}",
        f"{lstm['precision_weighted']:.2%}",
        f"{lstm['recall_macro']:.2%}",
        f"{lstm['recall_weighted']:.2%}",
        f"{lstm['f1_macro']:.2%}",
        f"{lstm['f1_weighted']:.2%}",
        f"{lstm['intent_accuracy']:.2%}",
        f"{lstm['ticket_routing_accuracy']:.2%}"
    ]
}
st.table(comp_data)

st.write("")
col_cm1, col_cm2 = st.columns(2)

with col_cm1:
    st.subheader("🔲 TF-IDF Confusion Matrix")
    cm_tf = tf["confusion_matrix"]
    fig_cm_tf = px.imshow(
        cm_tf, x=classes, y=classes,
        text_auto=True,
        color_continuous_scale='Blues',
        labels=dict(x="Predicted Class", y="Ground Truth", color="Count")
    )
    fig_cm_tf.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_cm_tf, use_container_width=True)

with col_cm2:
    st.subheader("🔲 Bi-LSTM Confusion Matrix")
    cm_lstm = lstm["confusion_matrix"]
    fig_cm_lstm = px.imshow(
        cm_lstm, x=classes, y=classes,
        text_auto=True,
        color_continuous_scale='Viridis',
        labels=dict(x="Predicted Class", y="Ground Truth", color="Count")
    )
    fig_cm_lstm.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_cm_lstm, use_container_width=True)

st.write("")
# Live Interactive Inference & XAI Sandbox
st.subheader("🔬 Live Inference & Explainable AI (XAI) Sandbox")
st.caption("Test real-time predictions and inspect feature token contributions and entropy.")

col_in, col_out = st.columns([1, 1])
with col_in:
    test_query = st.text_area(
        "Enter Inquiry to Classify & Explain",
        value="My GlobalProtect VPN keeps disconnecting every 10 minutes on WiFi",
        height=100
    )
    model_sel = st.radio("Choose Model", ["Bidirectional LSTM", "TF-IDF Baseline"], horizontal=True)

with col_out:
    if test_query:
        if "LSTM" in model_sel:
            pipe = BiLSTMPipeline()
            pipe.load()
            out = pipe.predict(test_query)
        else:
            clf = TfidfBaselineClassifier()
            clf.load()
            out = clf.predict(test_query)

        exp = explain_prediction(test_query, out["department"], out["department_confidence"], out["department_probabilities"])
        
        st.markdown(f"""
        <div class="om-card">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-size: 1.1rem; color: #4338CA;">Predicted: {out['department']}</strong>
            <span class="om-badge badge-it">Confidence: {out['department_confidence']:.1%}</span>
          </div>
          <div style="font-size: 0.88rem; color: #64748B; margin: 4px 0 8px 0;">Intent: <code>{out['intent']}</code></div>
          <div style="font-size: 0.9rem; line-height: 1.5; color: #1E293B;">
            {exp['explanation_narrative']}
          </div>
        </div>
        """, unsafe_allow_html=True)

if st.button("🔄 Re-Run Full Benchmark Evaluation On-Demand", use_container_width=True):
    with st.spinner("Evaluating models against test dataset..."):
        evaluate_models()
        st.success("Test evaluation re-calculated and saved!")
        st.rerun()
