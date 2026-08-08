"""Editorial Engine for topic scoring and filtering."""

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from app.services.discovery.base import TopicData
from app.services.persona.persona_engine import PersonaProfile


@dataclass
class EditorialScore:
    importance: float
    novelty: float
    credibility: float
    persona_fit: float
    recency: float
    repeated_penalty: float
    final_score: float
    is_accepted: bool
    rejection_reason: str | None = None


class EditorialEngine:
    """Evaluates topics based on importance, novelty, credibility, persona fit, recency, and duplicate penalties."""

    PROMOTIONAL_PATTERNS = [
        r"\bbuy now\b", r"\bdiscount\b", r"\bsale\b", r"\blimited offer\b",
        r"\bsponsored\b", r"\bpromo\b", r"\baffiliate\b", r"\bearn money\b",
        r"\bbest price\b", r"\b\d+% off\b",
    ]

    CLICKBAIT_PATTERNS = [
        r"you won'?t believe",
        r"shocking reason",
        r"blow your mind",
        r"secret method",
        r"number \d+ will surprise you",
        r"\b\d+ ways to\b",
    ]

    HIGH_CREDIBILITY_SOURCES = {
        "arXiv", "Hacker News", "OpenAI Blog", "Anthropic Research",
        "Google DeepMind", "GitHub Trending", "MIT Tech Review AI",
    }

    def __init__(self, min_score_threshold: float = 15.0) -> None:
        self.min_score_threshold = min_score_threshold

    def evaluate_topic(
        self,
        topic: TopicData,
        persona: PersonaProfile,
        is_duplicate: bool = False,
        similarity_score: float = 0.0,
    ) -> EditorialScore:
        text = f"{topic.title} {topic.summary}".lower()

        # 1. Quick Rejection Checks
        # Clickbait Check
        for pattern in self.CLICKBAIT_PATTERNS:
            if re.search(pattern, text):
                return EditorialScore(
                    importance=2.0, novelty=2.0, credibility=1.0,
                    persona_fit=2.0, recency=5.0, repeated_penalty=0.0,
                    final_score=12.0, is_accepted=False,
                    rejection_reason="Clickbait title detected",
                )

        # Promotional Check (Word Boundary)
        for pattern in self.PROMOTIONAL_PATTERNS:
            if re.search(pattern, text):
                return EditorialScore(
                    importance=1.0, novelty=2.0, credibility=1.0,
                    persona_fit=1.0, recency=5.0, repeated_penalty=0.0,
                    final_score=10.0, is_accepted=False,
                    rejection_reason="Too promotional",
                )

        # 2. Score Components (0-10 each)
        # Persona Fit: Token overlap + keyword bonus
        domain_tokens = set(re.sub(r"[^\w\s]", "", persona.domain.lower()).split())
        text_tokens = set(re.sub(r"[^\w\s]", "", text).split())
        matched_keywords = sum(1 for kw in persona.keywords if kw.lower() in text)

        if matched_keywords > 0:
            persona_fit = min(10.0, 6.0 + (matched_keywords * 2.0))
        elif domain_tokens.intersection(text_tokens):
            persona_fit = 7.0
        else:
            # Base persona fit for general technology/AI topics
            persona_fit = 5.0

        # Credibility
        credibility = 9.0 if topic.source_name in self.HIGH_CREDIBILITY_SOURCES else 6.0

        # Recency (hours since publication)
        now = datetime.now(timezone.utc)
        pub_time = topic.published_time
        if pub_time.tzinfo is None:
            pub_time = pub_time.replace(tzinfo=timezone.utc)
        hours_old = max(0.0, (now - pub_time).total_seconds() / 3600.0)

        if hours_old <= 12:
            recency = 10.0
        elif hours_old <= 24:
            recency = 8.0
        elif hours_old <= 48:
            recency = 6.0
        else:
            recency = 5.0

        # Importance & Novelty estimation
        importance = min(10.0, 5.0 + (matched_keywords * 1.5))
        novelty = min(10.0, 6.0 + (recency * 0.3))

        # Repeated / Duplicate Penalty
        repeated_penalty = 0.0
        if is_duplicate:
            repeated_penalty = -10.0 if similarity_score > 0.8 else -5.0

        # Calculate Final Score
        final_score = importance + novelty + credibility + persona_fit + recency + repeated_penalty

        # Check rejection threshold and specific failure reasons
        rejection_reason = None
        is_accepted = True

        if is_duplicate:
            is_accepted = False
            rejection_reason = "Already discussed"
        elif persona_fit < 3.0:
            is_accepted = False
            rejection_reason = "Low relevance"
        elif recency < 3.0:
            is_accepted = False
            rejection_reason = "Old news"
        elif final_score < self.min_score_threshold:
            is_accepted = False
            rejection_reason = f"Score ({final_score:.1f}) below threshold ({self.min_score_threshold})"

        return EditorialScore(
            importance=importance,
            novelty=novelty,
            credibility=credibility,
            persona_fit=persona_fit,
            recency=recency,
            repeated_penalty=repeated_penalty,
            final_score=final_score,
            is_accepted=is_accepted,
            rejection_reason=rejection_reason,
        )
