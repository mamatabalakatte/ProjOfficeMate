"""
Page 14: Organizational Knowledge Graph
Section 5 Requirement: Multi-relational network connecting
Departments, Policies, Workflows, Tickets, and Corporate Resources.
"""

import streamlit as st
import plotly.graph_objects as go
import math
from frontend.components.illustrations import render_banner_picture

st.set_page_config(page_title="Knowledge Graph | OfficeMate 2.0", page_icon="🕸️", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">🕸️ Organizational Knowledge Graph</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      Entity-relationship ontology linking Departments, Policies, Automated Workflows, Tickets, and Physical Resources.
    </p>
  </div>
  <div>
    <span class="om-badge badge-it" style="background: white; color: #4338CA;">Ontological Network</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Knowledge Graph Hero Banner
render_banner_picture("knowledge_graph.png", caption="🕸️ Enterprise Knowledge & Relationship Graph • Multi-Relational Ontology")
st.write("")

# Node entities definition
NODES = [
    # Center Departments
    {"id": "HR", "label": "HR Department", "type": "Dept", "color": "#EC4899", "size": 38, "x": 0.2, "y": 0.7},
    {"id": "IT", "label": "IT Department", "type": "Dept", "color": "#4F46E5", "size": 38, "x": 0.8, "y": 0.7},
    {"id": "ADMIN", "label": "Admin Dept", "type": "Dept", "color": "#F59E0B", "size": 38, "x": 0.5, "y": 0.2},
    
    # Policies
    {"id": "POL_LEAVE", "label": "Leave Policy 2026", "type": "Policy", "color": "#F472B6", "size": 24, "x": 0.05, "y": 0.9},
    {"id": "POL_BENEFIT", "label": "Health Insurance", "type": "Policy", "color": "#F472B6", "size": 24, "x": 0.25, "y": 0.95},
    {"id": "POL_VPN", "label": "VPN Security Guide", "type": "Policy", "color": "#818CF8", "size": 24, "x": 0.75, "y": 0.95},
    {"id": "POL_TOOL", "label": "Software Standards", "type": "Policy", "color": "#818CF8", "size": 24, "x": 0.95, "y": 0.9},
    {"id": "POL_TRAVEL", "label": "Travel Per Diem", "type": "Policy", "color": "#FBBF24", "size": 24, "x": 0.35, "y": 0.05},
    {"id": "POL_ERGO", "label": "Office Ergonomics", "type": "Policy", "color": "#FBBF24", "size": 24, "x": 0.65, "y": 0.05},

    # Workflows / Services
    {"id": "WF_TICKET", "label": "Auto-Ticket Triage", "type": "Workflow", "color": "#10B981", "size": 28, "x": 0.5, "y": 0.5},
    {"id": "WF_ROOM", "label": "Room Collision Guard", "type": "Workflow", "color": "#10B981", "size": 26, "x": 0.5, "y": 0.75},
    {"id": "WF_OCR", "label": "Screenshot Diagnostic", "type": "Workflow", "color": "#10B981", "size": 26, "x": 0.85, "y": 0.45},

    # Physical Resources
    {"id": "RES_BOARDROOM", "label": "Synergy Boardroom", "type": "Resource", "color": "#8B5CF6", "size": 22, "x": 0.35, "y": 0.6},
    {"id": "RES_VPN_GW", "label": "GlobalProtect GW", "type": "Resource", "color": "#8B5CF6", "size": 22, "x": 0.65, "y": 0.6}
]

EDGES = [
    ("HR", "POL_LEAVE"), ("HR", "POL_BENEFIT"), ("HR", "WF_TICKET"),
    ("IT", "POL_VPN"), ("IT", "POL_TOOL"), ("IT", "RES_VPN_GW"), ("IT", "WF_OCR"), ("IT", "WF_TICKET"),
    ("ADMIN", "POL_TRAVEL"), ("ADMIN", "POL_ERGO"), ("ADMIN", "WF_TICKET"),
    ("WF_ROOM", "RES_BOARDROOM"), ("WF_ROOM", "ADMIN"),
    ("WF_TICKET", "POL_LEAVE"), ("WF_TICKET", "POL_VPN")
]

# Build Plotly Network Graph
edge_x = []
edge_y = []
for src_id, dst_id in EDGES:
    src = [n for n in NODES if n["id"] == src_id][0]
    dst = [n for n in NODES if n["id"] == dst_id][0]
    edge_x.extend([src["x"], dst["x"], None])
    edge_y.extend([src["y"], dst["y"], None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=2, color='#CBD5E1'),
    hoverinfo='none',
    mode='lines'
)

node_x = [n["x"] for n in NODES]
node_y = [n["y"] for n in NODES]
node_text = [f"<b>{n['label']}</b><br>Type: {n['type']}" for n in NODES]
node_color = [n["color"] for n in NODES]
node_size = [n["size"] for n in NODES]

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=[n["label"] for n in NODES],
    textposition="bottom center",
    hovertext=node_text,
    hoverinfo='text',
    marker=dict(
        color=node_color,
        size=node_size,
        line=dict(width=2, color='#FFFFFF')
    )
)

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Enterprise Graph Topology (Departments, Workflows, Policies, Resources)',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=480
             ))

st.plotly_chart(fig, use_container_width=True)

st.subheader("🔍 Node Entity Inspector")
node_sel = st.selectbox("Select Node Entity to Inspect", [f"{n['label']} ({n['type']})" for n in NODES])
sel_label = node_sel.split(" (")[0]
selected = [n for n in NODES if n["label"] == sel_label][0]

connected = []
for s, d in EDGES:
    if s == selected["id"]:
        connected.append(d)
    elif d == selected["id"]:
        connected.append(s)

st.markdown(f"""
<div class="om-card" style="border-left: 6px solid {selected['color']};">
  <h3 style="margin:0 0 6px 0; color: #1E293B;">{selected['label']}</h3>
  <div style="font-size: 0.95rem; color: #475569;">
    • <strong>Entity Class:</strong> {selected['type']}<br>
    • <strong>Ontological ID:</strong> <code>{selected['id']}</code><br>
    • <strong>Connected Relationships:</strong> {', '.join(connected)}
  </div>
</div>
""", unsafe_allow_html=True)
