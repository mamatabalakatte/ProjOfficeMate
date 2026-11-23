"""
Text Preprocessing Module for OfficeMate 2.0
Implements text cleaning, tokenization, stopword removal, and normalization.
"""

import re
import string
from typing import List

# Common English stopwords commonly filtered in enterprise NLP
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", 
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", 
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", 
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she", 
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", 
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", 
    "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", 
    "why", "will", "with", "would", "you", "your", "yours", "yourself", "yourselves"
}

CONTRACTIONS = {
    "can't": "cannot", "won't": "will not", "n't": " not", "'re": " are",
    "'s": " is", "'d": " would", "'ll": " will", "'t": " not", "'ve": " have", "'m": " am"
}

def expand_contractions(text: str) -> str:
    """Expands contractions in input string."""
    for cont, expanded in CONTRACTIONS.items():
        text = text.replace(cont, expanded)
    return text

def clean_text(text: str) -> str:
    """Cleans text: lowercase, expands contractions, removes URLs & non-alphanumeric chars."""
    if not text:
        return ""
    text = text.lower()
    text = expand_contractions(text)
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Remove HTML tags if any
    text = re.sub(r"<.*?>", " ", text)
    # Remove punctuation & symbols except internal hyphens
    text = re.sub(r"[^a-zA-Z0-9\s-]", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str) -> List[str]:
    """Tokenizes string into a list of words."""
    cleaned = clean_text(text)
    if not cleaned:
        return []
    return cleaned.split()

def remove_stopwords(tokens: List[str]) -> List[str]:
    """Filters out stopwords from a token list."""
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

def normalize(text: str, filter_stops: bool = True) -> str:
    """Full normalization pipeline: clean -> tokenize -> optional stopword filter -> rejoin."""
    tokens = tokenize(text)
    if filter_stops:
        tokens = remove_stopwords(tokens)
    return " ".join(tokens)
