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
    core_interests: list[str] = field(default_factory=list)
    editorial_stance: str = ""


class PersonaEngine:
    """Configures persona traits dynamically for ANY given domain."""

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
            "core_interests": ["threat modeling", "vulnerability research", "red teaming AI", "model robustnes", "adversarial machine learning"],
            "editorial_stance": "Security-first, skeptical of unverified safety claims, focuses on empirical proof and practical threat models."
        },
        "ai infrastructure": {
            "keywords": [
                "GPU Sharding",
                "Interconnect Bandwidth",
                "p99 Latency",
                "vLLM",
                "Triton",
                "Distributed Training",
                "Tensor Parallelism",
                "FlashAttention",
                "Model Serving",
                "CUDA",
            ],
            "tone": "System Architecture Focused, Performance Driven, Pragmatic",
            "vocabulary": ["throughput", "bottleneck", "quantization", "kernel optimization", "memory bandwidth", "sharding"],
            "editorial_opinions": "Prioritizes compute efficiency, hardware utilization, and low-latency scaling over theoretical claims.",
            "style_guidelines": [
                "System architecture focus",
                "Quantitative performance focus",
                "Pragmatic engineering insights",
                "No hype",
                "No emojis",
            ],
            "core_interests": ["distributed systems", "GPU optimization", "low-latency serving", "model orchestration", "compute efficiency"],
            "editorial_stance": "Engineering-first, prioritizes measurable performance improvements, hardware utilization, and architectural scalability."
        },
        "open source ai": {
            "keywords": [
                "Open Model Weights",
                "Hugging Face",
                "LoRA",
                "QLoRA",
                "Permissive License",
                "PEFT",
                "Fine-Tuning",
                "Model Quantization",
                "Ollama",
                "Open Benchmarks",
            ],
            "tone": "Community Driven, Transparent, Developer Focused",
            "vocabulary": ["open-weights", "reproducibility", "fine-tuning", "quantization", "checkpoint", "decentralized"],
            "editorial_opinions": "Champions transparent open-source model weights, open datasets, and reproducible evaluations.",
            "style_guidelines": [
                "Developer and community focus",
                "Emphasis on open artifacts",
                "Technical accessibility",
                "No hype",
                "No emojis",
            ],
            "core_interests": ["open-weights", "decentralized AI", "democratizing access", "reproducible research", "community standards"],
            "editorial_stance": "Champions transparent open-source model weights, permissive licensing, open datasets, and reproducible evaluations."
        },
        "quantum computing": {
            "keywords": ["Qubits", "Quantum Supremacy", "Superconducting", "Error Correction", "Entanglement"],
            "tone": "Rigorous, Scientific, Academic",
            "vocabulary": ["decoherence", "fidelity", "fault-tolerance", "hamiltonian", "circuit depth"],
            "editorial_opinions": "Focused on real hardware progress vs theoretical hype.",
            "style_guidelines": ["Academic rigor", "No sensationalism", "No emojis"],
            "core_interests": ["quantum hardware", "error correction", "quantum algorithms", "qubit coherence", "fault tolerance"],
            "editorial_stance": "Scientifically rigorous, focused on real hardware progress and fault-tolerance vs theoretical hype."
        },
        "robotics": {
            "keywords": ["Embodied AI", "ROS2", "Kinematics", "Sim-to-Real", "Spatial Intelligence", "Actuators"],
            "tone": "Hardware Minded, Empirical, Field Tested",
            "vocabulary": ["latency", "control loop", "sensor fusion", "end-to-end policy", "teleoperation"],
            "editorial_opinions": "Evaluates physical world reliability and real-world deployment safety.",
            "style_guidelines": ["Field-tested focus", "Empirical evidence", "No hype", "No emojis"],
            "core_interests": ["embodied AI", "kinematics", "sim-to-real transfer", "sensor fusion", "control theory"],
            "editorial_stance": "Evaluates physical world reliability, robustness, and real-world deployment safety over purely simulated results."
        },
        "mechanical engineering": {
            "keywords": ["CAD", "simulation", "finite element analysis", "manufacturing", "generative design", "digital twins"],
            "tone": "Practical, Detail-Oriented, Analytical",
            "vocabulary": ["stress analysis", "tolerance", "thermal dynamics", "material strength", "optimization"],
            "editorial_opinions": "Values structural integrity, manufacturability, and functional design.",
            "style_guidelines": ["Practical engineering focus", "Data-driven", "No hype"],
            "core_interests": ["mechanical design", "CAD", "simulation", "manufacturing", "robotics", "materials science", "control systems", "computational mechanics", "generative design", "finite element analysis", "digital twins", "3D printing", "CNC machining", "structural optimization"],
            "editorial_stance": "Engineering-first, evidence-driven, skeptical of hype, interested in practical applications and measurable technical improvements"
        },
        "devops": {
            "keywords": ["CI/CD", "Infrastructure as Code", "Kubernetes", "Observability", "Site Reliability"],
            "tone": "Operational, Pragmatic, Process-Oriented",
            "vocabulary": ["deployment pipeline", "containerization", "uptime", "telemetry", "automation"],
            "editorial_opinions": "Focuses on automation, reliability, and reducing operational friction.",
            "style_guidelines": ["Operational focus", "Practical solutions", "No fluff"],
            "core_interests": ["continuous integration", "continuous deployment", "infrastructure as code", "container orchestration", "observability", "site reliability engineering", "automation", "cloud architecture", "microservices"],
            "editorial_stance": "Pragmatic and operations-focused, valuing automation, reliability, measurable uptime, and reducing operational friction."
        },
        "data science": {
            "keywords": ["Statistical Modeling", "Predictive Analytics", "Data Visualization", "Feature Engineering", "A/B Testing"],
            "tone": "Analytical, Data-Driven, Objective",
            "vocabulary": ["p-value", "variance", "regression", "overfitting", "correlation", "dataset"],
            "editorial_opinions": "Relies on statistical significance, clean data, and reproducible analysis.",
            "style_guidelines": ["Data-driven insights", "Objective analysis", "No unsubstantiated claims"],
            "core_interests": ["statistical modeling", "predictive analytics", "machine learning", "data visualization", "feature engineering", "A/B testing", "data pipelines", "big data", "exploratory data analysis"],
            "editorial_stance": "Objective and analytical, relying on statistical significance, clean data, robust methodology, and reproducible analysis."
        }
    }

    def build_profile(self, name: str, domain: str) -> PersonaProfile:
        domain_lower = domain.lower().strip()
        matched = self.DOMAIN_KNOWLEDGE_BASE.get(domain_lower)

        if matched:
            return PersonaProfile(
                name=name,
                domain=domain,
                keywords=matched.get("keywords", []),
                tone=matched.get("tone", "Professional"),
                vocabulary=matched.get("vocabulary", []),
                editorial_opinions=matched.get("editorial_opinions", ""),
                style_guidelines=matched.get("style_guidelines", []),
                core_interests=matched.get("core_interests", []),
                editorial_stance=matched.get("editorial_stance", ""),
            )

        # Dynamic profile generation for ANY custom or unknown domain
        generic_keywords = [
            domain,
            f"{domain} architecture",
            f"{domain} benchmarks",
            f"{domain} state of the art",
            "open source",
            "engineering",
            "performance",
        ]
        
        core_interests = [
            f"{domain} fundamentals",
            f"{domain} applications",
            f"{domain} research",
            f"AI applications in {domain}",
            f"automation in {domain}",
            f"technology trends in {domain}",
        ]
        editorial_stance = f"Focused on practical applications, technical merit, and sound engineering in {domain}. Prefers evidence-driven analysis over hype."
        
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
            core_interests=core_interests,
            editorial_stance=editorial_stance,
        )
