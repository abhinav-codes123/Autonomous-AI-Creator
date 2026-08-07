"""Mock LLM Provider for offline testing and fallback environments."""

import re
from app.services.llm.base import LLMGeneratedContent, LLMProvider


class MockLLMProvider(LLMProvider):
    """Generates realistic, persona-aligned technical posts without external API calls."""

    async def generate(self, prompt: str) -> LLMGeneratedContent:
        # Extract title and URL from prompt if present
        title_match = re.search(r"Title:\s*(.+)", prompt)
        url_match = re.search(r"Source:\s*.+\((https?://[^\)]+)\)", prompt)
        domain_match = re.search(r"Domain:\s*(.+)", prompt)

        title = title_match.group(1).strip() if title_match else "Recent AI Security Advancement"
        url = url_match.group(1).strip() if url_match else "https://arxiv.org/abs/2401.00001"
        domain = domain_match.group(1).strip() if domain_match else "AI Security"

        text = (
            f"Technical Analysis of '{title}':\n\n"
            f"Recent developments in {domain} highlight critical shifts in threat models and system robustness. "
            f"The primary attack vector discussed in this research demonstrates how adversarial inputs can bypass "
            f"standard alignment guardrails if context boundaries are not strictly enforced.\n\n"
            f"From an engineering perspective, reliance on soft prompt boundaries remains inadequate for high-assurance systems. "
            f"Production implementations must incorporate hard deterministic input parsing, robust output schema validation, "
            f"and continuous red-teaming benchmarks to mitigate zero-day exploit vulnerabilities."
        )

        rationale = (
            f"Selection Rationale:\n"
            f"1. Why selected: '{title}' directly targets core vulnerabilities in {domain} systems.\n"
            f"2. Why relevant now: Emerging deployment patterns make these attack vectors an immediate priority for production engineers.\n"
            f"3. Why chosen over alternatives: Offers concrete empirical findings and actionable defensive insights rather than speculative commentary."
        )

        return LLMGeneratedContent(
            text=text,
            rationale=rationale,
            sources=[url],
        )
