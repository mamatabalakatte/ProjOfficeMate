"""
Page 12: Employee Impact Intelligence
Section 5 Requirement: Privacy-conscious workplace friction detection,
recurring ticket clusters, resolution latency, and policy confusion analytics.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from db.database import get_tickets
from agents.specialized_tools import analyze_cross_department_root_causes
from frontend.components.illustrations import render_banner_picture

st.set_page_config(page_title="Impact Intelligence | OfficeMate 2.0", page_icon="💡", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #059669 0%, #10B981 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">💡 Employee Impact &amp; Experience Intelligence</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.95;">
      Privacy-conscious aggregated telemetry identifying recurring workplace friction, policy friction, and resolution bottlenecks.
    </p>
  </div>
  <div>
    <span class="om-badge badge-success" style="background: white; color: #059669;">Aggregated Telemetry (Zero Surveillance)</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Impact Intelligence Hero Banner
render_banner_picture("impact_intelligence.png", caption="💡 Employee Impact & Experience Intelligence • Friction Diagnostics")
st.write("")

# Friction Index
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""
    <div class="stat-box">
      <div class="stat-value" style="color: #10B981;">2.4 / 10</div>
      <div class="stat-label">Workplace Friction Score (Low)</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="stat-box">
      <div class="stat-value" style="color: #4F46E5;">42 mins</div>
      <div class="stat-label">Average Resolution SLA</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="stat-box">
      <div class="stat-value" style="color: #F59E0B;">2 Clustered</div>
      <div class="stat-label">Correlated System Incidents</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown("""
    <div class="stat-box">
      <div class="stat-value" style="color: #10B981;">94.2%</div>
      <div class="stat-label">First-Contact Resolution</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🔥 Top Workplace Friction Drivers (By Frequency)")
    friction_data = {
        "Friction Driver": [
            "GlobalProtect VPN / MFA Timeout",
            "Maternity/Paternity Split Rules",
            "Missing Itemized Travel Receipts",
            "Docker License Key Expiration",
            "Floor 2 AC Temperature"
        ],
        "Incident Frequency": [14, 9, 8, 7, 5],
        "Department": ["IT", "HR", "ADMIN", "IT", "ADMIN"]
    }
    fig = px.bar(
        friction_data,
        x="Incident Frequency",
        y="Friction Driver",
        orientation='h',
        color="Department",
        color_discrete_map={"IT": "#4F46E5", "HR": "#EC4899", "ADMIN": "#F59E0B"},
        title="Employee Friction Frequency by Area"
    )
    fig.update_layout(height=280, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🧩 Cross-Department Root Cause Analyzer")
    findings = analyze_cross_department_root_causes()
    for f in findings:
        st.markdown(f"""
        <div class="om-card" style="border-left: 5px solid #F59E0B;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color: #B45309;">{f['incident_name']}</strong>
            <span class="om-badge badge-high">{f['severity']}</span>
          </div>
          <p style="font-size: 0.88rem; color: #475569; margin: 6px 0;"><strong>Probable Cause:</strong> {f['probable_cause']}</p>
          <div style="font-size: 0.82rem; color: #065F46; background: #ECFDF5; padding: 6px 10px; border-radius: 6px;">
            <strong>Fix:</strong> {f['recommended_action']}
          </div>
        </div>
        """, unsafe_allow_html=True)
