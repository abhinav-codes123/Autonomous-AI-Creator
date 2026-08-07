"""Persona Engine for managing dynamic persona behavior, tone, style, and domain keywords."""

from dataclasses import dataclass, field


@dataclass
class PersonaProfile:
    name: str
    domain: str
    keywords: list[str] = field(default_factory=list)
    tone: str = "Professional, Analytical, Evidence-Driven"
    vocabulary: list[str] = field(default_factory=list)
    editorial_opinions: str = ""
    style_guidelines: list[str] = field(default_factory=list)


class PersonaEngine:
    """Configures persona traits dynamically for any given domain."""

    DOMAIN_KNOWLEDGE_BASE = {
        "ai security": {
            "keywords": [
                "Prompt Injection",
                "Red Teaming",
                "Model Jailbreaks",
                "CVEs",
                "LLM Security",
                "Supply Chain Attacks",
                "AI Malware",
                "Adversarial Attacks",
                "Data Poisoning",
                "Model Extraction",
            ],
            "tone": "Professional, Technical, Evidence Driven, Skeptical",
            "vocabulary": ["attack vector", "mitigation", "vulnerability", "threat model", "zero-day", "exfiltration"],
            "editorial_opinions": "Skeptical of unverified security claims; values reproducible benchmarks and empirical proof.",
            "style_guidelines": [
                "Professional and authoritative",
                "Technical precision",
                "Evidence driven",
                "Skeptical tone",
                "No hype or marketing buzzwords",
                "No emojis under any circumstances",
            ],
        },
        "quantum computing": {
            "keywords": ["Qubits", "Quantum Supremacy", "Superconducting", "Error Correction", "Entanglement"],
            "tone": "Rigorous, Scientific, Academic",
            "vocabulary": ["decoherence", "fidelity", "fault-tolerance", "hamiltonian", "circuit depth"],
            "editorial_opinions": "Focused on real hardware progress vs theoretical hype.",
            "style_guidelines": ["Academic rigor", "No sensationalism", "No emojis"],
        },
    }

    def build_profile(self, name: str, domain: str) -> PersonaProfile:
        domain_lower = domain.lower().strip()
        matched = self.DOMAIN_KNOWLEDGE_BASE.get(domain_lower)

        if matched:
            return PersonaProfile(
                name=name,
                domain=domain,
                keywords=matched["keywords"],
                tone=matched["tone"],
                vocabulary=matched["vocabulary"],
                editorial_opinions=matched["editorial_opinions"],
                style_guidelines=matched["style_guidelines"],
            )

        # Dynamic fallback for arbitrary tech domain
        generic_keywords = [
            domain,
            f"{domain} architecture",
            f"{domain} benchmarks",
            f"{domain} state of the art",
            "open source",
            "engineering",
        ]
        return PersonaProfile(
            name=name,
            domain=domain,
            keywords=generic_keywords,
            tone="Professional, Analytical, Objective",
            vocabulary=["system design", "benchmark", "performance", "scalability", "architecture"],
            editorial_opinions=f"Focuses on practical applications, technical merit, and sound engineering in {domain}.",
            style_guidelines=[
                "Professional and concise",
                "Technical clarity",
                "Evidence driven",
                "No hype",
                "No emojis",
            ],
        )
