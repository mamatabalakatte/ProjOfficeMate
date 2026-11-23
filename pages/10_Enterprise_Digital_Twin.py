"""
Page 10: Enterprise Digital Twin Dashboard
Real-time operational digital twin representing organizational departments,
support queues, staff utilization, and service telemetry.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from simulation.digital_twin import get_department_telemetry
from frontend.components.illustrations import render_banner_picture

st.set_page_config(page_title="Enterprise Digital Twin | OfficeMate 2.0", page_icon="🌐", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">🌐 Enterprise Digital Twin Telemetry</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      Live operational digital representation of company departments, support throughput, and resource bottlenecks.
    </p>
  </div>
  <div>
    <span class="om-badge badge-success">Telemetry Stream Synchronized</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Digital Twin Hero Banner
render_banner_picture("digital_twin.png", caption="🌐 Enterprise Digital Twin Telemetry • Live Queuing & Capacity Gauges")
st.write("")

telem = get_department_telemetry()
depts = telem["departments"]

# Top Overview Gauges
gc1, gc2, gc3 = st.columns([1, 1, 1])

with gc1:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=telem["overall_health_score"],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Twin Health Index", 'font': {'size': 18, 'family': 'Plus Jakarta Sans'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#4F46E5"},
            'steps': [
                {'range': [0, 50], 'color': "#FEE2E2"},
                {'range': [50, 75], 'color': "#FEF3C7"},
                {'range': [75, 100], 'color': "#D1FAE5"}
            ],
            'threshold': {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with gc2:
    labels = [d["name"] for d in depts.values()]
    open_counts = [d["open_tickets"] for d in depts.values()]
    fig_pie = px.pie(
        names=labels,
        values=open_counts,
        title="Workload Backlog Distribution",
        color_discrete_sequence=["#EC4899", "#4F46E5", "#F59E0B"],
        hole=0.45
    )
    fig_pie.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

with gc3:
    wait_times = [d["estimated_wait_time_min"] for d in depts.values()]
    fig_bar = px.bar(
        x=[d["code"] for d in depts.values()],
        y=wait_times,
        title="Estimated Wait Times (Minutes)",
        labels={'x': 'Department', 'y': 'Minutes'},
        color=[d["code"] for d in depts.values()],
        color_discrete_map={"HR": "#EC4899", "IT": "#4F46E5", "ADMIN": "#F59E0B"}
    )
    fig_bar.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# Department Cards
st.subheader("🏢 Department Operational Status")
dept_cols = st.columns(len(depts))
for i, (code, d) in enumerate(depts.items()):
    status_badge = "badge-success" if d["health_score"] >= 75 else ("badge-high" if d["health_score"] >= 50 else "badge-critical")
    with dept_cols[i]:
        st.markdown(f"""
        <div class="om-card">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-size: 1.1rem; color: #1E293B;">{d['name']} ({code})</strong>
            <span class="om-badge {status_badge}">{d['status']}</span>
          </div>
          <div style="font-size: 2rem; font-weight: 800; color: #4F46E5; margin: 10px 0;">{d['health_score']}% <span style="font-size: 0.9rem; color: #64748B;">Health</span></div>
          <div style="font-size: 0.88rem; color: #475569; line-height: 1.6;">
            • Active Staff: <strong>{d['staff_count']} agents</strong><br>
            • Open Requests: <strong>{d['open_tickets']}</strong> (Resolved: {d['resolved_tickets']})<br>
            • Critical Priority: <strong>{d['critical_tickets']}</strong><br>
            • Estimated Queue Wait: <strong>{d['estimated_wait_time_min']} mins</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)
