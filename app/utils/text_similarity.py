"""Text similarity computation utilities for memory deduplication."""

import re
from difflib import SequenceMatcher


def tokenize(text: str) -> set[str]:
    """Clean and tokenize text into lowercase word tokens."""
    cleaned = re.sub(r"[^\w\s]", "", text.lower())
    return set(cleaned.split())


def jaccard_similarity(text1: str, text2: str) -> float:
    """Calculate Jaccard similarity between two text strings."""
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)

    if not tokens1 or not tokens2:
        return 0.0

    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)

    return len(intersection) / len(union)


def sequence_similarity(text1: str, text2: str) -> float:
    """Calculate string sequence matcher similarity ratio."""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def calculate_similarity(text1: str, text2: str) -> float:
    """Combine Jaccard and Sequence similarity to produce a robust text similarity score (0.0 to 1.0)."""
    jaccard = jaccard_similarity(text1, text2)
    seq = sequence_similarity(text1, text2)
    return max(jaccard, seq)
