export function formatTimestamp(isoString) {
  try {
    const date = new Date(isoString);
    if (Number.isNaN(date.getTime())) {
      return 'Unknown date';
    }

    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    }).format(date);
  } catch {
    return 'Unknown date';
  }
}

export function formatTime(isoString) {
  try {
    const date = new Date(isoString);
    if (Number.isNaN(date.getTime())) {
      return '—';
    }

    return new Intl.DateTimeFormat('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    }).format(date);
  } catch {
    return '—';
  }
}

export function secondsSince(date) {
  if (!date || !(date instanceof Date) || Number.isNaN(date.getTime())) {
    return null;
  }
  return Math.max(0, Math.floor((Date.now() - date.getTime()) / 1000));
}

export function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return 'GOOD MORNING';
  if (hour < 17) return 'GOOD AFTERNOON';
  return 'GOOD EVENING';
}

export function getSourceDisplayName(url) {
  try {
    const parsed = new URL(url);
    const hostname = parsed.hostname.replace(/^www\./, '');

    if (hostname.includes('arxiv.org')) return 'arXiv Research';
    if (hostname.includes('owasp.org')) return 'OWASP';
    if (hostname.includes('nist.gov')) return 'NIST NVD';
    if (hostname.includes('github.com')) return 'GitHub';
    if (hostname.includes('openai.com')) return 'OpenAI';

    const parts = hostname.split('.');
    const name = parts.length > 1 ? parts[parts.length - 2] : parts[0];
    return name.charAt(0).toUpperCase() + name.slice(1);
  } catch {
    return 'External Source';
  }
}
