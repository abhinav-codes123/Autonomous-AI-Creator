import { formatTime } from '../utils/format';

function ActivityItem({ item }) {
  return (
    <div className={`activity-item activity-item--${item.status}`}>
      <div className="activity-item__track">
        <span className="activity-item__dot" aria-hidden="true" />
        <span className="activity-item__line" aria-hidden="true" />
      </div>
      <div className="activity-item__content">
        <div className="activity-item__header">
          <span className="activity-item__label">{item.label}</span>
          <time className="activity-item__time" dateTime={item.timestamp}>
            {formatTime(item.timestamp)}
          </time>
        </div>
        <p className="activity-item__description">{item.description}</p>
      </div>
    </div>
  );
}

function ActivityTimeline({ items }) {
  return (
    <section className="panel activity-panel" id="activity">
      <div className="panel__header">
        <h2 className="panel__title">Agent Activity</h2>
        <p className="panel__subtitle">Autonomous intelligence pipeline</p>
      </div>
      <div className="activity-timeline">
        {items.map((item) => (
          <ActivityItem key={item.id} item={item} />
        ))}
      </div>
    </section>
  );
}

export default ActivityTimeline;
