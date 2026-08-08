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
      <MetricCard label="Sources Monitored" value={metrics.sourcesMonitored} />
      <MetricCard label="Topics Discovered" value={metrics.topicsDiscovered} accent />
      <MetricCard label="Topics Rejected" value={metrics.topicsRejected} />
      <MetricCard label="Published" value={metrics.published} accent />
    </div>
  );
}

export default MetricRow;
