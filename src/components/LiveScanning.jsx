import { useEffect, useState } from 'react';
import { secondsSince } from '../utils/format';

function LiveScanning({ domain, lastChecked, isPolling }) {
  const [scanSeconds, setScanSeconds] = useState(() => secondsSince(lastChecked));

  useEffect(() => {
    setScanSeconds(secondsSince(lastChecked));
    const intervalId = setInterval(() => {
      setScanSeconds(secondsSince(lastChecked));
    }, 1000);
    return () => clearInterval(intervalId);
  }, [lastChecked]);

  if (!isPolling) return null;

  const scanLabel = scanSeconds === null ? '—' : `${scanSeconds}s ago`;

  return (
    <div className="live-scanning">
      <div className="live-scanning__indicator">
        <span className="live-scanning__dot" aria-hidden="true" />
        <span className="live-scanning__label">SCANNING</span>
      </div>
      <span className="live-scanning__domain">{domain} sources</span>
      <span className="live-scanning__time">Last scan {scanLabel}</span>
    </div>
  );
}

export default LiveScanning;
