"""
Supervisor Agent for OfficeMate 2.0
Orchestrates multi-agent triage:
1. Intent & Department Classification (Bi-LSTM / TF-IDF)
2. Knowledge Retrieval (RAG via SemanticSearchEngine)
3. Universal Assistant Brain & Ticket Routing
4. Generative LLM Fallback (OpenAI GPT-4 when enabled)
"""

import os
from typing import Dict, Any, Optional

from nlp.semantic_search import SemanticSearchEngine
from nlp.bilstm_model import BiLSTMPipeline
from nlp.tfidf_baseline import TfidfBaselineClassifier
from agents.universal_brain import UniversalBrain
from agents.ticket_agent import auto_create_ticket_from_query
from db.database import query_one

# Optional LLM fallback import
if os.getenv("USE_LLM") == "1":
    try:
        from nlp.generative_fallback import get_answer as llm_get_answer
    except Exception:
        llm_get_answer = None
else:
    llm_get_answer = None


class SupervisorAgent:
    """Orchestrates request handling: classification, knowledge search, ticket routing, and optional LLM fallback."""

    def __init__(self, use_deep_learning: bool = True):
        self.use_deep_learning = use_deep_learning
        if self.use_deep_learning:
            self.classifier = BiLSTMPipeline()
        else:
            self.classifier = TfidfBaselineClassifier()
        self.search_engine = SemanticSearchEngine()
        self.universal_brain = UniversalBrain()

    def process_query(
        self,
        query: str,
        user_id: int = 1,
        conversation_id: Optional[str] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """Main entry point.
        Returns a dict containing response, department, intent, confidence, sources, and ticket.
        """
        # Fetch active user name if available
        user_row = query_one("SELECT full_name FROM users WHERE id = ?", (user_id,))
        user_name = user_row["full_name"] if user_row else "Alex Chen"

        # 1. Classification (department & intent)
        classification = self.classifier.predict(query)
        department = classification.get("department", "IT")
        intent = classification.get("intent", "general_inquiry")
        confidence = float(classification.get("confidence", 0.0))

        # 2. Knowledge-base search
        kb_results = self.search_engine.search(query, category=department, top_k=3)
        top_score = kb_results[0]["score"] if kb_results else 0.0

        # If no department match or score is below threshold, search across all categories
        broad_results = self.search_engine.search(query, category=None, top_k=3)
        if broad_results:
            if not kb_results or broad_results[0]["score"] > top_score:
                kb_results = broad_results
                top_score = broad_results[0]["score"]
                # Align department with authoritative document category
                if top_score >= self.search_engine.confidence_threshold:
                    department = broad_results[0].get("category", department)

        reliable_kb = (top_score >= self.search_engine.confidence_threshold) if kb_results else False

        # 3. Universal Brain processing
        ans_text, citations, should_create_ticket = self.universal_brain.answer_query(
            query=query,
            detected_dept=department,
            detected_intent=intent,
            confidence=confidence,
            kb_matches=kb_results,
            reliable_kb=reliable_kb,
            user_name=user_name
        )

        # 4. Optional Generative LLM fallback if enabled and KB was not high-confidence
        if llm_get_answer and not reliable_kb and not citations:
            try:
                context_snippet = kb_results[0].get("clean_text") if kb_results else None
                llm_response = llm_get_answer(query, department, context_snippet)
                if llm_response and len(llm_response.strip()) > 10:
                    ans_text = llm_response
            except Exception:
                pass

        # 5. Automatic ticket generation if flagged
        ticket = None
        if should_create_ticket:
            ticket = auto_create_ticket_from_query(
                query=query,
                department_code=department,
                intent=intent,
                user_id=user_id
            )

        return {
            "response": ans_text,
            "department": department,
            "intent": intent,
            "confidence": confidence,
            "sources": citations,
            "ticket": ticket,
            "ticket_created": bool(ticket)
        }


def handle_chat_message(
    message: str,
    user_id: int = 1,
    conversation_id: Optional[str] = None,
    language: str = "en",
    use_deep_learning: bool = True
) -> Dict[str, Any]:
    """Unified wrapper used by the Flask API, Streamlit front-end, and audit scripts."""
    agent = SupervisorAgent(use_deep_learning=use_deep_learning)
    return agent.process_query(
        query=message,
        user_id=user_id,
        conversation_id=conversation_id,
        language=language
    )
