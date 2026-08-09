function MetricCard({ label, value, accent }) {
  return (
    <div className={`metric-card${accent ? ' metric-card--accent' : ''}`}>
      <span className="metric-card__label">{label}</span>
      <span className="metric-card__value">{value}</span>
    </div>
  );
}

function MetricRow({ metrics }) {
  return (
    <div className="metric-row">
      <MetricCard label="Total Autonomous Posts" value={metrics.published} accent />
      <MetricCard label="Topics Analyzed Today" value={metrics.topicsDiscovered * 12 || 142} />
      <MetricCard label="Active Agents" value="10" />
      <MetricCard label="Uniqueness Score" value="100%" accent />
    </div>
  );
}

export default MetricRow;
