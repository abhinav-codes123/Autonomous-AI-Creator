import { useEffect, useRef } from 'react';
import { formatTime } from '../utils/format';

function CommandLog({ item }) {
  const getPrefixColor = () => {
    switch(item.status) {
      case 'active': return 'var(--accent-green)';
      case 'warning': return 'var(--accent-amber)';
      case 'complete': return 'var(--accent-purple)';
      default: return 'var(--text-dim)';
    }
  };

  return (
    <div className={`command-log command-log--${item.status}`}>
      <span className="command-log__time">[{formatTime(item.timestamp)}]</span>
      <span className="command-log__prefix" style={{ color: getPrefixColor() }}>{item.label}</span>
      <span className="command-log__text">{item.description}</span>
    </div>
  );
}

function ActivityTimeline({ items }) {
  const scrollRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [items]);

  return (
    <section className="panel command-center" id="command-center">
      <div className="panel__header command-center__header">
        <div>
          <h2 className="panel__title">Command Center</h2>
          <p className="panel__subtitle">Live Swarm Telemetry</p>
        </div>
        <div className="command-center__status">
          <span className="status-dot pulse"></span>
          <span className="status-text">SYS.ONLINE</span>
        </div>
      </div>
      <div className="command-center__console" ref={scrollRef}>
        {items.map((item) => (
          <CommandLog key={item.id} item={item} />
        ))}
        {items.length > 0 && items[0].status === 'active' && (
          <div className="command-log__cursor">_</div>
        )}
      </div>
    </section>
  );
}

export default ActivityTimeline;
