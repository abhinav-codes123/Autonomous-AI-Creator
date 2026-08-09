"""Post Validator for pre-publication quality checks."""

import re
from dataclasses import dataclass
from app.core.logging import logger


@dataclass
class ValidationResult:
    valid: bool
    reasons: list[str]


class PostValidator:
    """Validates generated posts before publication."""

    def validate(
        self,
        text: str,
        rationale: str,
        sources: list[str],
        topic_title: str,
        persona_domain: str,
    ) -> ValidationResult:
        reasons = []

        # 1. Post must not be empty or too short
        if not text or len(text.strip()) < 50:
            reasons.append("Post text is too short or empty")

        # 2. Rationale must not be empty
        if not rationale or len(rationale.strip()) < 20:
            reasons.append("Rationale is too short or empty")

        # 3. Sources must be valid URLs
        for source in sources:
            if not self._is_valid_url(source):
                reasons.append(f"Invalid source URL: {source}")

        # 4. Post should not contain error messages
        error_indicators = ["api connection error", "failed to generate", "error occurred", "analysis failed"]
        text_lower = text.lower()
        for indicator in error_indicators:
            if indicator in text_lower:
                reasons.append(f"Post contains error indicator: '{indicator}'")

        # 5. Post should not be entirely generic boilerplate
        boilerplate_phrases = [
            "demonstrates significant progress within",
            "a detailed examination of",
            "the underlying methodology introduces a refined",
        ]
        boilerplate_count = sum(1 for bp in boilerplate_phrases if bp in text_lower)
        if boilerplate_count >= 2:
            reasons.append("Post appears to be generic boilerplate")

        valid = len(reasons) == 0
        if not valid:
            logger.warning(f"Post validation FAILED for topic '{topic_title[:50]}': {reasons}")
        else:
            logger.info(f"Post validation PASSED for topic '{topic_title[:50]}'")

        return ValidationResult(valid=valid, reasons=reasons)

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Check if string is a valid URL."""
        return bool(re.match(r'^https?://[^\s]+$', url.strip()))

    @staticmethod
    def normalize_sources(sources: list[str]) -> list[str]:
        """Strip markdown formatting and normalize source URLs."""
        normalized = []
        for source in sources:
            # Strip markdown link formatting: [text](url) -> url
            md_match = re.search(r'\[.*?\]\((https?://[^\)]+)\)', source)
            if md_match:
                source = md_match.group(1)
            # Strip surrounding whitespace and quotes
            source = source.strip().strip('"').strip("'")
            # Only include valid URLs
            if re.match(r'^https?://[^\s]+$', source):
                normalized.append(source)
        return list(dict.fromkeys(normalized))  # deduplicate preserving order
