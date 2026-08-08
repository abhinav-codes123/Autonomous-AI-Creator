function StatusBadge({ label, variant = 'green', pulse = false }) {
  return (
    <span className={`status-badge status-badge--${variant}${pulse ? ' status-badge--pulse' : ''}`}>
      <span className="status-badge__dot" aria-hidden="true" />
      {label}
    </span>
  );
}

export default StatusBadge;
