"""Text similarity computation utilities for memory deduplication."""

import re
from difflib import SequenceMatcher

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "about", "above", "after", "again",
    "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both",
    "by", "can", "cannot", "could", "did", "do", "does", "doing", "down",
    "during", "each", "few", "for", "from", "further", "had", "has", "have",
    "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me",
    "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on",
    "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over",
    "own", "same", "she", "should", "so", "some", "such", "than", "that",
    "the", "their", "theirs", "them", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "we", "were", "what", "when", "where", "which", "while",
    "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself",
    "yourselves", "new", "shows", "releases", "released",
}

SYNONYMS_MAP = {
    "mcp": "model context protocol",
    "llm": "large language model",
    "llms": "large language models",
    "ai": "artificial intelligence",
    "vuln": "vulnerability",
    "vulns": "vulnerabilities",
    "pentest": "penetration test",
    "pentesting": "penetration testing",
    "rag": "retrieval augmented generation",
    "tool injection": "prompt injection",
    "tool-injection": "prompt injection",
    "study": "research",
    "risks": "risk",
    "ecosystems": "ecosystem",
}


def simple_stem(word: str) -> str:
    """Basic suffix stemming helper for common English plurals and endings."""
    if word.endswith("ing") and len(word) > 5:
        return word[:-3]
    if word.endswith("s") and len(word) > 3 and not word.endswith("ss"):
        return word[:-1]
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    return word


def expand_and_clean(text: str) -> list[str]:
    """Clean text, expand tech acronyms and phrase synonyms, and extract stemmed significant words."""
    lowered = text.lower()

    # Pre-process multi-word synonym phrases
    for phrase, replacement in SYNONYMS_MAP.items():
        if " " in phrase or "-" in phrase:
            lowered = lowered.replace(phrase, replacement)

    cleaned = re.sub(r"[^\w\s]", " ", lowered)
    words = cleaned.split()

    expanded = []
    for word in words:
        if word in SYNONYMS_MAP:
            expanded.extend(SYNONYMS_MAP[word].split())
        else:
            expanded.append(word)

    stemmed = [simple_stem(w) for w in expanded if w not in STOP_WORDS and len(w) > 1]
    return stemmed


def get_bigrams(words: list[str]) -> set[str]:
    """Generate set of word bigrams."""
    return {f"{words[i]}_{words[i+1]}" for i in range(len(words) - 1)}


def jaccard_similarity(text1: str, text2: str) -> float:
    """Calculate stop-word-filtered, synonym-expanded Jaccard similarity."""
    tokens1 = set(expand_and_clean(text1))
    tokens2 = set(expand_and_clean(text2))

    if not tokens1 or not tokens2:
        return 0.0

    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)

    return len(intersection) / len(union)


def bigram_jaccard_similarity(text1: str, text2: str) -> float:
    """Calculate bigram Jaccard similarity for phrase alignment."""
    words1 = expand_and_clean(text1)
    words2 = expand_and_clean(text2)

    bigrams1 = get_bigrams(words1)
    bigrams2 = get_bigrams(words2)

    if not bigrams1 or not bigrams2:
        return 0.0

    intersection = bigrams1.intersection(bigrams2)
    union = bigrams1.union(bigrams2)

    return len(intersection) / len(union)


def sequence_similarity(text1: str, text2: str) -> float:
    """Calculate string sequence matcher similarity ratio."""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def calculate_similarity(text1: str, text2: str) -> float:
    """Combine token Jaccard, bigram Jaccard, and Sequence similarity to detect semantic duplicates."""
    unigram_jaccard = jaccard_similarity(text1, text2)
    bigram_jaccard = bigram_jaccard_similarity(text1, text2)
    seq = sequence_similarity(text1, text2)

    # Weighted blend giving primary weight to token and phrase overlap
    weighted_score = (unigram_jaccard * 0.50) + (bigram_jaccard * 0.30) + (seq * 0.20)
    return max(weighted_score, unigram_jaccard, seq)
