import { useEffect, useState } from 'react';
import StatusBadge from './StatusBadge';
import { getGreeting, secondsSince } from '../utils/format';

function Header({ persona, showLive, lastChecked, onDisconnect }) {
  const [syncSeconds, setSyncSeconds] = useState(() => secondsSince(lastChecked));

  useEffect(() => {
    setSyncSeconds(secondsSince(lastChecked));
    const intervalId = setInterval(() => {
      setSyncSeconds(secondsSince(lastChecked));
    }, 1000);
    return () => clearInterval(intervalId);
  }, [lastChecked]);

  const syncLabel =
    syncSeconds === null ? 'Awaiting sync' : `Last sync: ${syncSeconds}s ago`;

  return (
    <header className="dashboard-header">
      <div className="dashboard-header__intro">
        <h1 className="dashboard-header__greeting">
          {getGreeting()}, {persona.name.toUpperCase()}
        </h1>
        <p className="dashboard-header__subtitle">
          Your autonomous intelligence system is monitoring the AI ecosystem.
        </p>
      </div>

      <div className="dashboard-header__status">
        <StatusBadge label="AUTONOMOUS" variant="green" pulse />
        {showLive && <StatusBadge label="LIVE" variant="live" pulse />}
        <span className="dashboard-header__sync">{syncLabel}</span>
        {onDisconnect && (
          <button
            type="button"
            className="connect-agent__button"
            style={{ padding: '0.4rem 0.8rem', fontSize: '0.75rem', marginLeft: '0.5rem' }}
            onClick={onDisconnect}
          >
            + New Agent
          </button>
        )}
      </div>
    </header>
  );
}

export default Header;
