"""
Unit Tests for Knowledge-Base Semantic Retrieval
"""

import pytest
from nlp.semantic_search import search_knowledge_base

def test_semantic_search_retrieval_success():
    res = search_knowledge_base("What is the policy for sick leave and doctor certificate?")
    assert len(res["results"]) > 0
    top = res["results"][0]
    assert "Annual & Sick Leave Policy" in top["title"]
    assert top["score"] > 0.15

def test_semantic_search_unreliable_unknown_query():
    res = search_knowledge_base("Can I keep a pet komodo dragon inside my desk cubicle?")
    assert res["reliable"] is False
    assert res["top_score"] < 0.22

def test_category_filtering():
    res_hr = search_knowledge_base("How to book hotel for business travel?", category="HR")
    res_admin = search_knowledge_base("How to book hotel for business travel?", category="ADMIN")
    assert any("Travel" in r["title"] for r in res_admin["results"])
