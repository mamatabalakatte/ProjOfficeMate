"""
Page 11: What-If Scenario Simulator
Discrete-event queuing simulator modeling operational shocks,
resource bottlenecks, and comparative before/after impact.
"""

import streamlit as st
import plotly.graph_objects as go
from simulation.what_if_simulator import simulate_scenario
from frontend.components.illustrations import render_banner_picture

st.set_page_config(page_title="What-If Simulator | OfficeMate 2.0", page_icon="🔮", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #075985 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">🔮 What-If Scenario Simulator</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      SimPy discrete-event simulation of corporate operational shocks, queuing delays, and bottleneck diagnostics.
    </p>
  </div>
  <div>
    <span class="om-badge badge-it" style="background: white; color: #0284C7;">Discrete-Event M/M/c Engine</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual What-If Scenario Lab Hero Banner
render_banner_picture("what_if_lab.png", caption="🔮 What-If Scenario Stress Testing Lab • SimPy Discrete-Event Engine")
st.write("")

# Scenario Selector
st.subheader("⚙️ Scenario Selection & Parameters")
scenario_preset = st.selectbox(
    "Pre-Configured Enterprise Scenarios",
    [
        "40% Increase in IT Tickets (OS Upgrade / Patch Tuesday)",
        "50% HR Staff Shortage (Team Offsite / Flu Season)",
        "Company-wide Core Network & VPN Outage",
        "New Parental & Leave Policy Rollout Surge",
        "Custom Scenario (Manual Sliders)"
    ]
)

custom_params = None
if "Custom" in scenario_preset:
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        c_dept = st.selectbox("Target Department", ["IT", "HR", "ADMIN"])
    with col_c2:
        c_surge = st.slider("Arrival Surge Multiplier", 1.0, 3.5, 1.5, step=0.1)
    with col_c3:
        c_staff_delta = st.slider("Staff Modifier", -4, 4, 0)
    custom_params = {"dept": c_dept, "surge_mult": c_surge, "staff_delta": c_staff_delta}
    scenario_key = "custom"
else:
    scenario_key = {
        "40% Increase in IT Tickets (OS Upgrade / Patch Tuesday)": "it_surge_40",
        "50% HR Staff Shortage (Team Offsite / Flu Season)": "hr_shortage_50",
        "Company-wide Core Network & VPN Outage": "network_outage",
        "New Parental & Leave Policy Rollout Surge": "policy_rollout_surge"
    }[scenario_preset]

if st.button("🚀 Execute Discrete-Event Simulation", use_container_width=True):
    with st.spinner("Simulating thousands of workplace interactions with SimPy..."):
        res = simulate_scenario(scenario_key, custom_params)
        st.session_state["sim_results"] = res
else:
    if "sim_results" not in st.session_state:
        st.session_state["sim_results"] = simulate_scenario("it_surge_40")

res = st.session_state["sim_results"]

st.markdown("---")
st.subheader(f"📊 Simulation Results: {res['name']}")
st.caption(res["description"])

# Delta Stat Boxes
b = res["baseline"]
s = res["simulated"]
imp = res["impact"]

c1, c2, c3, c4 = st.columns(4)
with c1:
    delta_str = f"+{imp['wait_time_delta_min']}m" if imp['wait_time_delta_min'] >= 0 else f"{imp['wait_time_delta_min']}m"
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{s['avg_wait_minutes']}m</div>
      <div class="stat-label">Simulated Wait Time ({delta_str})</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{s['sla_breach_rate_pct']}%</div>
      <div class="stat-label">SLA Breach Rate (Base: {b['sla_breach_rate_pct']}%)</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{s['staff_utilization_pct']}%</div>
      <div class="stat-label">Staff Utilization (Base: {b['staff_utilization_pct']}%)</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{s['total_tickets_processed']}</div>
      <div class="stat-label">Total Workday Inflow (Base: {b['total_tickets_processed']})</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Comparative Chart
metrics_names = ["Avg Wait Time (min)", "Peak Queue Length", "SLA Breach Rate (%)", "Staff Utilization (%)"]
base_vals = [b["avg_wait_minutes"], b["peak_queue_length"], b["sla_breach_rate_pct"], b["staff_utilization_pct"]]
sim_vals = [s["avg_wait_minutes"], s["peak_queue_length"], s["sla_breach_rate_pct"], s["staff_utilization_pct"]]

fig = go.Figure(data=[
    go.Bar(name='Normal Baseline', x=metrics_names, y=base_vals, marker_color='#94A3B8'),
    go.Bar(name='Simulated Shock Scenario', x=metrics_names, y=sim_vals, marker_color='#EF4444')
])
fig.update_layout(barmode='group', title="Baseline vs Shock Scenario Comparison", height=320, margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig, use_container_width=True)

# Bottleneck & Strategic Recommendations
col_bot, col_rec = st.columns([1, 1])
with col_bot:
    st.markdown(f"""
    <div class="om-card" style="border-left: 6px solid #EF4444;">
      <h4 style="margin:0 0 6px 0; color: #DC2626;">🚨 Operational Bottleneck Diagnosis</h4>
      <p style="color: #1E293B; font-size: 0.95rem; margin: 0;">{imp['bottleneck_diagnosis']}</p>
    </div>
    """, unsafe_allow_html=True)

with col_rec:
    rec_items = "".join([f"<li>{r}</li>" for r in res.get("recommendations", [])])
    st.markdown(f"""
    <div class="om-card" style="border-left: 6px solid #10B981;">
      <h4 style="margin:0 0 6px 0; color: #059669;">💡 Recommended Mitigation Strategies</h4>
      <ul style="color: #1E293B; font-size: 0.92rem; margin: 0; padding-left: 18px;">
        {rec_items}
      </ul>
    </div>
    """, unsafe_allow_html=True)
