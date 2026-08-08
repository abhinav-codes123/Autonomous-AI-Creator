function EditorialPanel({ stats }) {
  const base = stats.discovered || 1;
  const stages = [
    { label: 'Discovered', value: stats.discovered, width: 100 },
    { label: 'Rejected', value: stats.rejected, width: (stats.rejected / base) * 100 },
    { label: 'Shortlisted', value: stats.shortlisted, width: (stats.shortlisted / base) * 100 },
    { label: 'Selected', value: stats.selected, width: (stats.selected / base) * 100 },
  ];

  return (
    <section className="panel editorial-panel" id="editorial">
      <div className="panel__header">
        <h2 className="panel__title">Editorial Decision</h2>
        <p className="panel__subtitle">Autonomous topic evaluation pipeline</p>
      </div>

      <div className="editorial-stats">
        <div className="editorial-stat">
          <span className="editorial-stat__value">{stats.discovered}</span>
          <span className="editorial-stat__label">topics discovered</span>
        </div>
        <div className="editorial-stat editorial-stat--muted">
          <span className="editorial-stat__value">{stats.rejected}</span>
          <span className="editorial-stat__label">rejected</span>
        </div>
        <div className="editorial-stat editorial-stat--accent">
          <span className="editorial-stat__value">{stats.shortlisted}</span>
          <span className="editorial-stat__label">shortlisted</span>
        </div>
        <div className="editorial-stat editorial-stat--highlight">
          <span className="editorial-stat__value">{stats.selected}</span>
          <span className="editorial-stat__label">selected</span>
        </div>
      </div>

      <div className="editorial-funnel" aria-hidden="true">
        {stages.map((stage) => (
          <div key={stage.label} className="editorial-funnel__stage">
            <div
              className="editorial-funnel__bar"
              style={{ width: `${Math.max(stage.width, 8)}%` }}
            />
            <span className="editorial-funnel__label">{stage.label}</span>
          </div>
        ))}
      </div>

      <p className="editorial-panel__note">
        Not every discovery becomes a publication.
      </p>
    </section>
  );
}

export default EditorialPanel;
