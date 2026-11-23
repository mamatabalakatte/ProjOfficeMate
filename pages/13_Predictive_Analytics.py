"""
Page 13: Predictive Analytics & Forecasting
Section 5 Requirement: Predictive Problem Detection
14-day ticket inflow forecast, seasonal surge curves, and early capacity alerts.
"""

import streamlit as st
import plotly.graph_objects as go
from simulation.predictive_engine import forecast_ticket_surges
from frontend.components.illustrations import render_banner_picture

st.set_page_config(page_title="Predictive Analytics | OfficeMate 2.0", page_icon="📈", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #4338CA 0%, #6366F1 50%, #4F46E5 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">📈 Predictive Problem Detection &amp; Forecasting</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      Early warning detection of ticket surges, seasonal SLA risks, and proactive staffing recommendations.
    </p>
  </div>
  <div>
    <span class="om-badge badge-it" style="background: white; color: #4338CA;">Seasonal Harmonic Forecaster</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Predictive AI Forecast Hero Banner
render_banner_picture("predictive_forecast.png", caption="📈 Predictive Analytics & 14-Day Inflow Forecaster • Early Warning Engine")
st.write("")

days_ahead = st.slider("Forecast Horizon (Days)", min_value=7, max_value=21, value=14)
fc = forecast_ticket_surges(days_ahead)

# Plot Forecast Lines
st.subheader("📊 Projected Daily Ticket Volume Inflow")
dates = fc["dates"]
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=dates,
    y=[d["forecast"] for d in fc["forecasts"]["IT"]],
    mode='lines+markers',
    name='IT Tickets (Projected)',
    line=dict(color='#4F46E5', width=3)
))
fig.add_trace(go.Scatter(
    x=dates,
    y=[d["forecast"] for d in fc["forecasts"]["HR"]],
    mode='lines+markers',
    name='HR Tickets (Projected)',
    line=dict(color='#EC4899', width=3)
))
fig.add_trace(go.Scatter(
    x=dates,
    y=[d["forecast"] for d in fc["forecasts"]["ADMIN"]],
    mode='lines+markers',
    name='Admin Tickets (Projected)',
    line=dict(color='#F59E0B', width=3)
))

fig.update_layout(
    height=340,
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis_title="Date",
    yaxis_title="Projected Daily Inflow",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# Early Warning Alerts
st.subheader("🚨 Proactive Capacity Alerts & Staffing Recommendations")
if not fc["alerts"]:
    st.success("All departments operating well within baseline capacity over the forecast horizon.")
else:
    for a in fc["alerts"]:
        badge_cls = "badge-critical" if a["severity"] == "HIGH" else "badge-high"
        st.markdown(f"""
        <div class="om-card" style="border-left: 5px solid {'#EF4444' if a['severity'] == 'HIGH' else '#F59E0B'};">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong>{a['department']} Capacity Alert — {a['date']}</strong>
            <span class="om-badge {badge_cls}">{a['severity']} RISK</span>
          </div>
          <p style="margin: 6px 0 0 0; color: #1E293B; font-size: 0.95rem;">{a['message']}</p>
        </div>
        """, unsafe_allow_html=True)
