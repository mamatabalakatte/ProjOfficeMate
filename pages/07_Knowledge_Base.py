"""
Page 7: Knowledge Base & Semantic Search
CSE472 Knowledge Retrieval Requirement
Full policy document library, semantic passage search, and document management.
"""

import streamlit as st
from db.database import get_knowledge_docs, execute_insert
from nlp.semantic_search import search_knowledge_base, get_engine
from frontend.components.illustrations import render_banner_picture

st.set_page_config(page_title="Knowledge Base | OfficeMate 2.0", page_icon="📚", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">📚 Corporate Knowledge Base</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      Authoritative repository for company policies, IT guides, and administrative protocols with AI semantic search.
    </p>
  </div>
  <div>
    <span class="om-badge badge-it">Hybrid Cosine Semantic Retrieval</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Knowledge Archive Hero Banner
render_banner_picture("knowledge_base.png", caption="📚 Organizational Knowledge Repository • Semantic Search & RAG")
st.write("")

tab_search, tab_browse, tab_add = st.tabs(["🔍 Semantic Search", "📖 Browse All Documents", "➕ Publish New Document"])

with tab_search:
    st.markdown("#### Natural Language Semantic Document Search")
    col_q, col_cat = st.columns([3, 1])
    with col_q:
        search_query = st.text_input("Enter natural language question or keywords", placeholder="e.g. Can I carry over unused vacation days to next year?")
    with col_cat:
        search_cat = st.selectbox("Filter Department", ["All", "HR", "IT", "ADMIN"])

    if search_query:
        with st.spinner("Executing semantic retrieval over document chunks..."):
            res = search_knowledge_base(search_query, category=search_cat, top_k=4)

        if not res["results"]:
            st.warning("No matching policy clauses found. Consider submitting a support ticket!")
        else:
            rel_badge = '<span class="om-badge badge-success">High Confidence</span>' if res["reliable"] else '<span class="om-badge badge-high">Moderate Match</span>'
            st.markdown(f"**Top Match Score:** `{res['top_score']:.1%}` • {rel_badge}", unsafe_allow_html=True)
            st.write("")

            for r in res["results"]:
                cat_badge = {"HR": "badge-hr", "IT": "badge-it", "ADMIN": "badge-admin"}.get(r["category"], "badge-open")
                st.markdown(f"""
                <div class="om-card">
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                    <strong style="color: #4F46E5;">{r['title']}</strong>
                    <div>
                      <span class="om-badge {cat_badge}">{r['category']}</span>
                      <span class="om-badge badge-it">Relevance: {r['score']:.1%}</span>
                    </div>
                  </div>
                  <p style="font-size: 0.95rem; color: #1E293B; background: #F8FAFC; padding: 12px; border-radius: 8px; border-left: 4px solid #6366F1;">
                    "{r['text']}"
                  </p>
                </div>
                """, unsafe_allow_html=True)

with tab_browse:
    st.markdown("#### Organizational Policy Library")
    cat_filter = st.radio("Category Filter", ["All", "HR", "IT", "ADMIN"], horizontal=True)
    docs = get_knowledge_docs(category=cat_filter)
    
    for doc in docs:
        c_badge = {"HR": "badge-hr", "IT": "badge-it", "ADMIN": "badge-admin"}.get(doc["category"], "badge-open")
        with st.expander(f"{doc['title']} (v{doc['version']})", expanded=False):
            st.markdown(f"<span class='om-badge {c_badge}'>{doc['category']}</span>", unsafe_allow_html=True)
            st.write(doc["content"])
            st.caption(f"Index ID: {doc['id']} • Tags: {doc['tags']} • Updated: {doc['updated_at']}")

with tab_add:
    st.markdown("#### Add New Policy or Documentation")
    with st.form("add_doc_form"):
        title = st.text_input("Document Title", placeholder="e.g. Remote Work Hardware Ergonomics 2026")
        cat = st.selectbox("Department Category", ["HR", "IT", "ADMIN", "General"])
        dept_id = {"HR": 1, "IT": 2, "ADMIN": 3}.get(cat, 1)
        tags = st.text_input("Tags (comma separated)", placeholder="remote, hardware, allowance, monitor")
        content = st.text_area("Full Document Content / Policy Clauses", height=150)
        
        save_btn = st.form_submit_button("💾 Index & Publish Document", use_container_width=True)
        if save_btn:
            if not title or not content:
                st.error("Title and content are required.")
            else:
                doc_id = execute_insert(
                    """INSERT INTO knowledge_docs (title, category, department_id, content, tags, version)
                       VALUES (?, ?, ?, ?, ?, '1.0')""",
                    (title, cat, dept_id, content, tags)
                )
                get_engine().reload()
                st.success(f"✅ Document '{title}' published (ID #{doc_id}) and re-indexed into semantic search!")
