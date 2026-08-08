import StatusBadge from './StatusBadge';

function formatLastChecked(date) {
  if (!date || !(date instanceof Date) || Number.isNaN(date.getTime())) {
    return '—';
  }

  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  }).format(date);
}

function AgentOverview({ persona, postCount, lastChecked, isDemo }) {
  return (
    <section className="card agent-overview">
      <div className="agent-overview__header">
        <h2 className="card__title">Agent Overview</h2>
        <div className="agent-overview__badges">
          <StatusBadge label="ACTIVE" variant="green" />
          <StatusBadge label="AUTONOMOUS" variant="purple" />
          {isDemo && <StatusBadge label="DEMO" variant="blue" />}
        </div>
      </div>

      <div className="agent-overview__grid">
        <div className="agent-overview__item">
          <span className="agent-overview__label">Persona</span>
          <span className="agent-overview__value">{persona.name}</span>
        </div>
        <div className="agent-overview__item">
          <span className="agent-overview__label">Domain</span>
          <span className="agent-overview__value">{persona.domain}</span>
        </div>
        <div className="agent-overview__item">
          <span className="agent-overview__label">Publications</span>
          <span className="agent-overview__value agent-overview__value--accent">
            {postCount}
          </span>
        </div>
        <div className="agent-overview__item">
          <span className="agent-overview__label">Last Checked</span>
          <span className="agent-overview__value">{formatLastChecked(lastChecked)}</span>
        </div>
      </div>

      <p className="agent-overview__monitoring">
        <span className="agent-overview__monitoring-dot" aria-hidden="true" />
        Monitoring live sources
      </p>
    </section>
  );
}

export default AgentOverview;
