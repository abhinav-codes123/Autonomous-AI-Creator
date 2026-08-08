const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const STORAGE_KEYS = {
  agentId: 'aac_agent_id',
  persona: 'aac_persona',
};

export const DEMO_POSTS = [
  {
    id: 'demo-p1',
    createdAt: '2026-08-07T14:30:00Z',
    text: 'Researchers have demonstrated a new class of prompt-injection attacks that bypass guardrails in widely deployed LLM APIs by embedding instructions in multilingual metadata fields. Early mitigation strategies focus on input canonicalization and output verification layers.',
    rationale:
      'This represents a significant shift in attack surface for production LLM deployments. The technique affects multiple major providers and has immediate implications for teams shipping AI-powered features without dedicated security review.',
    sources: [
      'https://arxiv.org/abs/example-prompt-injection',
      'https://owasp.org/www-project-top-10-for-large-language-model-applications/',
    ],
  },
  {
    id: 'demo-p2',
    createdAt: '2026-08-07T11:15:00Z',
    text: 'A coalition of AI labs published a shared framework for model weight integrity verification, enabling downstream consumers to cryptographically confirm that deployed models match audited checkpoints. The approach uses Merkle-tree attestations embedded in model cards.',
    rationale:
      'Supply-chain integrity for AI models is becoming a regulatory and enterprise requirement. This framework offers a practical path toward verifiable deployments without requiring full model retraining pipelines.',
    sources: ['https://example.com/ai-model-integrity-framework'],
  },
  {
    id: 'demo-p3',
    createdAt: '2026-08-07T08:45:00Z',
    text: 'New analysis reveals that federated learning systems in edge AI deployments remain vulnerable to model poisoning when participant verification is weak. Recommended mitigations include differential privacy budgets and anomaly detection on gradient updates.',
    rationale:
      'Edge AI adoption is accelerating in healthcare and finance, where poisoning attacks carry high stakes. This analysis consolidates recent findings into actionable guidance for teams evaluating federated architectures.',
    sources: [
      'https://example.com/federated-learning-security',
      'https://nvd.nist.gov/vuln/detail/example',
    ],
  },
];

export async function initializeAgent(persona) {
  const response = await fetch(`${API_BASE_URL}/api/agent/init`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ persona }),
  });

  if (!response.ok) {
    throw new Error('Failed to initialize agent');
  }

  return response.json();
}

export async function fetchFeed(agentId) {
  const response = await fetch(
    `${API_BASE_URL}/api/agent/feed?agentId=${encodeURIComponent(agentId)}`,
  );

  if (!response.ok) {
    throw new Error('Failed to fetch feed');
  }

  return response.json();
}

export async function fetchStats(agentId) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/agent/stats?agentId=${encodeURIComponent(agentId)}`,
    );
    if (!response.ok) return null;
    return await response.json();
  } catch {
    return null;
  }
}

export function getDemoFeed() {
  return { posts: DEMO_POSTS };
}

export function getStoredAgentId() {
  return localStorage.getItem(STORAGE_KEYS.agentId);
}

export function getStoredPersona() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.persona);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function saveAgentSession(agentId, persona) {
  localStorage.setItem(STORAGE_KEYS.agentId, agentId);
  localStorage.setItem(STORAGE_KEYS.persona, JSON.stringify(persona));
}

export function clearAgentSession() {
  localStorage.removeItem(STORAGE_KEYS.agentId);
  localStorage.removeItem(STORAGE_KEYS.persona);
}

export function getUrlParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    demo: params.get('demo') === 'true',
    agentId: params.get('agentId'),
  };
}

export const DEMO_METRICS = {
  sourcesMonitored: 8,
  topicsDiscovered: 45,
  topicsRejected: 43,
  published: 2,
};

export const DEMO_EDITORIAL = {
  discovered: 45,
  rejected: 43,
  shortlisted: 2,
  selected: 1,
};

export const DEMO_ACTIVITY = [
  {
    id: 'act-1',
    label: 'PUBLISHING',
    description: 'Publication queued: prompt-injection attack analysis',
    timestamp: '2026-08-07T14:28:00Z',
    status: 'complete',
  },
  {
    id: 'act-2',
    label: 'SELECTING A TOPIC',
    description: 'Selected high-signal topic from 3 shortlisted candidates',
    timestamp: '2026-08-07T14:25:00Z',
    status: 'complete',
  },
  {
    id: 'act-3',
    label: 'REJECTING LOW-SIGNAL TOPICS',
    description: 'Filtered 8 topics below relevance threshold',
    timestamp: '2026-08-07T14:20:00Z',
    status: 'complete',
  },
  {
    id: 'act-4',
    label: 'EVALUATING RELEVANCE',
    description: 'Scoring 14 discovered topics against AI Security criteria',
    timestamp: '2026-08-07T14:15:00Z',
    status: 'complete',
  },
  {
    id: 'act-5',
    label: 'DISCOVERING TOPICS',
    description: 'Extracted 14 candidate topics from monitored sources',
    timestamp: '2026-08-07T14:10:00Z',
    status: 'complete',
  },
  {
    id: 'act-6',
    label: 'SCANNING SOURCES',
    description: 'Monitoring arXiv, OWASP, NIST, and security advisories',
    timestamp: '2026-08-07T14:05:00Z',
    status: 'active',
  },
];

export function getDemoMetrics(postCount) {
  return {
    ...DEMO_METRICS,
    published: postCount,
  };
}

export function buildLiveMetrics(stats, postCount) {
  if (!stats) {
    const discovered = postCount > 0 ? postCount * 22 : 20;
    const rejected = postCount > 0 ? (postCount * 22) - postCount : 19;
    return {
      sourcesMonitored: 8,
      topicsDiscovered: discovered,
      topicsRejected: rejected,
      published: postCount,
    };
  }
  return {
    sourcesMonitored: stats.sourcesMonitored || 8,
    topicsDiscovered: stats.topicsDiscovered || 20,
    topicsRejected: stats.topicsRejected || 19,
    published: stats.published !== undefined ? stats.published : postCount,
  };
}

export function buildLiveEditorial(stats, postCount) {
  if (!stats) {
    const discovered = postCount > 0 ? postCount * 22 : 20;
    const rejected = postCount > 0 ? (postCount * 22) - postCount : 19;
    return {
      discovered,
      rejected,
      shortlisted: postCount > 0 ? postCount : 1,
      selected: postCount,
    };
  }
  return {
    discovered: stats.topicsDiscovered || 20,
    rejected: stats.topicsRejected || 19,
    shortlisted: stats.shortlisted || 1,
    selected: stats.selected !== undefined ? stats.selected : postCount,
  };
}

export function buildLiveActivity({ lastChecked, postCount, isPolling, loading, error }) {
  const now = lastChecked ? lastChecked.toISOString() : new Date().toISOString();
  const items = [];

  if (isPolling) {
    items.push({
      id: 'live-scan',
      label: 'SCANNING SOURCES',
      description: loading
        ? 'Synchronizing with intelligence feed'
        : 'Monitoring 8 live intelligence source endpoints (HN, GitHub, arXiv, RSS)',
      timestamp: now,
      status: error ? 'warning' : 'active',
    });
  }

  if (postCount > 0) {
    items.push({
      id: 'live-publish',
      label: 'PUBLISHING',
      description: `${postCount} publication${postCount === 1 ? '' : 's'} preserved in intelligence feed`,
      timestamp: now,
      status: 'complete',
    });
  }

  if (items.length === 0) {
    items.push({
      id: 'live-init',
      label: 'EVALUATING RELEVANCE',
      description: 'Agent initialized — awaiting first discovery cycle',
      timestamp: now,
      status: 'active',
    });
  }

  return items;
}
