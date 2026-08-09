"""Persona Relevance Service for domain-specific topic filtering."""

import re
from dataclasses import dataclass
from app.services.discovery.base import TopicData
from app.services.persona.persona_engine import PersonaProfile
from app.core.logging import logger


@dataclass
class RelevanceResult:
    relevant: bool
    score: int  # 0-100
    reason: str


class PersonaRelevanceService:
    """Evaluates whether a topic has substantive relevance to a persona's domain."""

    # Technology/AI meta-keywords that are broadly relevant
    TECH_META_KEYWORDS = [
        "ai", "artificial intelligence", "machine learning", "deep learning",
        "neural network", "llm", "large language model", "gpt", "transformer",
        "automation", "algorithm", "data", "software", "engineering",
        "robotics", "computing", "cloud", "api", "open source",
        "benchmark", "optimization", "simulation", "model", "deployment",
    ]

    # Irrelevant topic indicators
    IRRELEVANT_INDICATORS = [
        "celebrity", "gossip", "sports score", "weather forecast",
        "horoscope", "recipe", "fashion trend", "movie review",
        "reality tv", "tabloid",
    ]

    def __init__(self, min_relevance_score: int = 30) -> None:
        self.min_relevance_score = min_relevance_score

    def evaluate_relevance(
        self,
        topic: TopicData,
        persona: PersonaProfile,
    ) -> RelevanceResult:
        """Evaluate whether a topic is substantively relevant to the persona's domain."""
        text = f"{topic.title} {topic.summary}".lower()
        domain_lower = persona.domain.lower()

        # Quick rejection: obviously irrelevant
        for indicator in self.IRRELEVANT_INDICATORS:
            if indicator in text:
                return RelevanceResult(
                    relevant=False,
                    score=0,
                    reason=f"Topic contains irrelevant indicator: '{indicator}'",
                )

        score = 0
        reasons = []

        # 1. Direct domain keyword match (strongest signal)
        domain_tokens = set(re.sub(r"[^\w\s]", "", domain_lower).split())
        text_tokens = set(re.sub(r"[^\w\s]", "", text).split())
        domain_overlap = domain_tokens.intersection(text_tokens)
        if domain_overlap:
            score += 35
            reasons.append(f"Direct domain term match: {domain_overlap}")

        # 2. Core interests match (strong signal)
        interests_matched = []
        for interest in persona.core_interests:
            interest_lower = interest.lower()
            # Check if the multi-word interest phrase appears in text
            if interest_lower in text:
                interests_matched.append(interest)
            else:
                # Check individual words of the interest (at least 2 must match)
                interest_words = set(interest_lower.split())
                if len(interest_words) >= 2 and len(interest_words.intersection(text_tokens)) >= 2:
                    interests_matched.append(interest)

        if interests_matched:
            interest_score = min(40, len(interests_matched) * 15)
            score += interest_score
            reasons.append(f"Core interest match: {interests_matched[:3]}")

        # 3. Persona keywords match (moderate signal)
        keyword_matches = [kw for kw in persona.keywords if kw.lower() in text]
        if keyword_matches:
            kw_score = min(25, len(keyword_matches) * 8)
            score += kw_score
            reasons.append(f"Keyword match: {keyword_matches[:3]}")

        # 4. Technology/AI meta-relevance (weak but positive signal)
        tech_matches = [t for t in self.TECH_META_KEYWORDS if t in text]
        if tech_matches:
            tech_score = min(15, len(tech_matches) * 3)
            score += tech_score
            reasons.append(f"Tech/AI relevance: {tech_matches[:3]}")

        # Cap at 100
        score = min(100, score)

        # Decision
        if score >= self.min_relevance_score:
            reason_str = "; ".join(reasons) if reasons else "General technology relevance"
            logger.info(f"RELEVANT (score={score}): '{topic.title[:60]}' — {reason_str}")
            return RelevanceResult(relevant=True, score=score, reason=reason_str)
        else:
            reason_str = f"No substantive connection to {persona.domain}. " + ("; ".join(reasons) if reasons else "No matching signals found.")
            logger.info(f"IRRELEVANT (score={score}): '{topic.title[:60]}' — {reason_str}")
            return RelevanceResult(relevant=False, score=score, reason=reason_str)
