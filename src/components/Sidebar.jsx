import StatusBadge from './StatusBadge';

const NAV_ITEMS = [
  { id: 'overview', label: 'Overview' },
  { id: 'intelligence', label: 'Live Intelligence' },
  { id: 'editorial', label: 'Editorial Decisions' },
  { id: 'activity', label: 'Activity' },
];

function Sidebar({ persona, isDemo }) {
  function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <div className="sidebar__logo" aria-hidden="true">
          <span className="sidebar__logo-inner" />
        </div>
        <div>
          <p className="sidebar__product">AUTONOMOUS AI CREATOR</p>
          <p className="sidebar__network">Intelligence Network</p>
        </div>
      </div>

      <div className="sidebar__agent persona-card">
        <div className="persona-card__avatar">
          {persona.name.charAt(0).toUpperCase()}
        </div>
        <div className="persona-card__info">
          <p className="sidebar__agent-label">Agent Identity</p>
          <p className="sidebar__agent-name">{persona.name.toUpperCase()}</p>
          <p className="sidebar__agent-domain">{persona.domain.toUpperCase()}</p>
        </div>
        <div className="persona-card__status">
          <StatusBadge label="ONLINE" variant="green" pulse />
          {isDemo && (
            <span className="sidebar__demo-tag">DEMO MODE</span>
          )}
        </div>
      </div>

      <nav className="sidebar__nav" aria-label="Dashboard navigation">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            type="button"
            className="sidebar__nav-item"
            onClick={() => scrollToSection(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar__footer">
        <span className="sidebar__system-dot" aria-hidden="true" />
        <span className="sidebar__system-text">SYSTEM OPERATIONAL</span>
      </div>
    </aside>
  );
}

export default Sidebar;
