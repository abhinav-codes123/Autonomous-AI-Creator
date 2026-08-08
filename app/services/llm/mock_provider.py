"""Mock LLM Provider for offline testing and fallback environments."""

import re
from app.services.llm.base import LLMGeneratedContent, LLMProvider


class MockLLMProvider(LLMProvider):
    """Generates realistic, domain-tailored technical posts without external API calls."""

    async def generate(self, prompt: str) -> LLMGeneratedContent:
        # Extract title, URL, name, and domain from prompt
        title_match = re.search(r"Title:\s*(.+)", prompt)
        url_match = re.search(r"Source:\s*.+\((https?://[^\)]+)\)", prompt)
        domain_match = re.search(r"Domain:\s*(.+)", prompt)
        name_match = re.search(r"Name:\s*(.+)", prompt)

        title = title_match.group(1).strip() if title_match else "Recent Technology Breakthrough"
        url = url_match.group(1).strip() if url_match else "https://news.ycombinator.com"
        domain = domain_match.group(1).strip() if domain_match else "AI & Technology"
        name = name_match.group(1).strip() if name_match else "Sentinel"

        domain_lower = domain.lower()

        if "security" in domain_lower or "cyber" in domain_lower or "sentinel" in name.lower():
            text = (
                f"Threat Analysis & Security Brief: '{title}'\n\n"
                f"This recent development in {domain} highlights an evolving attack surface in production AI systems. "
                f"The core vulnerability lies in unverified context boundaries, where malicious input payloads bypass "
                f"standard output guardrails if deterministic input sanitization is not enforced.\n\n"
                f"Engineering Directive: Security teams deploying models in this domain must move beyond passive prompt filters. "
                f"Recommended mitigations include strict XML input boundary isolation, continuous automated red-teaming, "
                f"and cryptographic attestation of pipeline dependencies to neutralize exploit vectors."
            )
            rationale = (
                f"Why Selected: '{title}' addresses high-priority vulnerabilities in {domain} production environments.\n"
                f"Why Relevant Now: Emerging exploit techniques make input sanitization an immediate operational priority.\n"
                f"Why Chosen Over Alternatives: Provides actionable defensive countermeasures over generic industry reporting."
            )
        elif "infra" in domain_lower or "hardware" in domain_lower or "cloud" in domain_lower or "stack" in name.lower():
            text = (
                f"System Architecture Analysis: '{title}'\n\n"
                f"Evaluating '{title}' from an {domain} perspective reveals critical trade-offs between compute efficiency "
                f"and system throughput. As model parameter scales expand, hardware interconnect bandwidth and memory access "
                f"latencies represent the primary engineering bottlenecks for multi-node deployments.\n\n"
                f"Infrastructure Takeaway: Production clusters must prioritize kernel-level memory optimization and distributed "
                f"sharding strategies. Teams optimizing for low p99 latencies should evaluate custom memory allocators "
                f"to maximize GPU utilization and reduce operational overhead."
            )
            rationale = (
                f"Why Selected: Directly targets core infrastructure bottlenecks in scaling {domain} workloads.\n"
                f"Why Relevant Now: High compute costs demand rigorous architectural optimization for production clusters.\n"
                f"Why Chosen Over Alternatives: Demonstrates tangible performance gains and resource utilization improvements."
            )
        elif "open source" in domain_lower or "model" in domain_lower or "forge" in name.lower():
            text = (
                f"Open Source Deep-Dive: '{title}'\n\n"
                f"The release of '{title}' marks a notable step forward for open-weights development in {domain}. "
                f"By providing open model checkpoints and reproducible training scripts, the community gains a transparent "
                f"foundation for parameter-efficient fine-tuning (PEFT) and local inference benchmarking.\n\n"
                f"Developer Perspective: Permissive licensing combined with modular codebases accelerates decentralized innovation. "
                f"We recommend open-source practitioners benchmark model quantization performance on edge devices to evaluate "
                f"real-world utility across constrained computing environments."
            )
            rationale = (
                f"Why Selected: Represents a key open-source milestone in {domain} model accessibility.\n"
                f"Why Relevant Now: Community-driven research is rapidly closing the gap with proprietary frontier models.\n"
                f"Why Chosen Over Alternatives: Offers open artifacts, code repositories, and verifiable empirical benchmarks."
            )
        else:
            text = (
                f"Technical Commentary: '{title}'\n\n"
                f"A detailed examination of '{title}' demonstrates significant progress within {domain}. "
                f"The underlying methodology introduces a refined algorithmic approach that balances computational complexity "
                f"with practical deployment feasibility.\n\n"
                f"Strategic Insight: Organizations operating in {domain} should track these methodological innovations closely. "
                f"Integrating these architectural principles early provides a clear competitive edge in shipping resilient AI features."
            )
            rationale = (
                f"Why Selected: High technical significance and alignment with {domain} strategic objectives.\n"
                f"Why Relevant Now: Timely discovery with immediate relevance to modern AI engineering workflows.\n"
                f"Why Chosen Over Alternatives: Strongest empirical evidence and highest domain relevance among candidate topics."
            )

        return LLMGeneratedContent(
            text=text,
            rationale=rationale,
            sources=[url],
        )
