"""
Knowledge-Base Semantic Retrieval Engine for OfficeMate 2.0
CSE472 Deep Learning for NLP - Project 20 Knowledge Retrieval
Performs passage chunking, TF-IDF / embedding vector representation,
cosine similarity ranking, source citation, and confidence thresholding.
"""

import re
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from db.database import get_knowledge_docs
from nlp.preprocessor import clean_text

class SemanticSearchEngine:
    def __init__(self, confidence_threshold: float = 0.15):
        self.confidence_threshold = confidence_threshold
        self.chunks = []
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.tfidf_matrix = None
        self._build_index()

    def _build_index(self):
        """Indexes knowledge base documents into semantic passages."""
        docs = get_knowledge_docs()
        self.chunks = []
        for doc in docs:
            # Chunk by sentences
            sentences = re.split(r"(?<=[.!?])\s+", doc["content"])
            # Pair every sentence or chunk
            for i, sent in enumerate(sentences):
                s = sent.strip()
                if not s or len(s) < 15:
                    continue
                self.chunks.append({
                    "doc_id": doc["id"],
                    "title": doc["title"],
                    "category": doc["category"],
                    "department_id": doc["department_id"],
                    "chunk_id": f"{doc['id']}_{i}",
                    "text": s,
                    "clean_text": clean_text(s)
                })

        if self.chunks:
            corpus = [c["clean_text"] for c in self.chunks]
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def reload(self):
        self._build_index()

    def search(self, query: str, category: Optional[str] = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """Searches indexed passages using TF-IDF cosine similarity."""
        if not self.chunks or self.tfidf_matrix is None:
            self._build_index()
            if not self.chunks:
                return []

        q_clean = clean_text(query)
        if not q_clean:
            return []

        q_vec = self.vectorizer.transform([q_clean])
        sims = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        ranked_indices = np.argsort(sims)[::-1]
        results = []

        for idx in ranked_indices:
            score = float(sims[idx])
            chunk = self.chunks[idx]

            if category and category != "All" and chunk["category"].upper() != category.upper():
                continue

            # Add phrase exact match bonus
            if q_clean in chunk["clean_text"]:
                score = min(1.0, score + 0.25)

            if score >= self.confidence_threshold:
                results.append({
                    "score": round(score, 4),
                    "title": chunk["title"],
                    "category": chunk["category"],
                    "department_id": chunk["department_id"],
                    "text": chunk["text"],
                    "chunk_id": chunk["chunk_id"]
                })

            if len(results) >= top_k:
                break

        return results

# Global engine instance
_engine = None

def get_engine() -> SemanticSearchEngine:
    global _engine
    if _engine is None:
        _engine = SemanticSearchEngine()
    return _engine

def search_knowledge_base(query: str, category: Optional[str] = None, top_k: int = 3) -> Dict[str, Any]:
    eng = get_engine()
    matches = eng.search(query, category=category, top_k=top_k)
    is_reliable = len(matches) > 0 and matches[0]["score"] >= 0.22
    return {
        "query": query,
        "reliable": is_reliable,
        "top_score": matches[0]["score"] if matches else 0.0,
        "results": matches
    }

if __name__ == "__main__":
    q = "What is the policy for sick leave and doctor note?"
    r = search_knowledge_base(q)
    print(f"Query: '{q}' -> Reliable: {r['reliable']} (Score: {r['top_score']})")
    for res in r["results"]:
        print(f" - [{res['title']}] ({res['score']:.2f}): {res['text']}")
