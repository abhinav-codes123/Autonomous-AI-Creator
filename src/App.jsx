import { useCallback, useEffect, useMemo, useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MetricRow from './components/MetricRow';
import LiveScanning from './components/LiveScanning';
import ActivityTimeline from './components/ActivityTimeline';
import EditorialPanel from './components/EditorialPanel';
import Feed from './components/Feed';
import {
  buildLiveActivity,
  buildLiveEditorial,
  buildLiveMetrics,
  clearAgentSession,
  fetchFeed,
  fetchStats,
  getDemoFeed,
  getDemoMetrics,
  DEMO_ACTIVITY,
  DEMO_EDITORIAL,
  getStoredAgentId,
  getStoredPersona,
  getUrlParams,
  initializeAgent,
  saveAgentSession,
} from './services/api';
import './App.css';

const DEFAULT_PERSONA = { name: 'Ada', domain: 'AI Security' };
const POLL_INTERVAL_MS = 10000;

function sortPostsNewestFirst(posts) {
  return [...posts].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
  );
}

function mergePosts(existingPosts, incomingPosts) {
  const existingIds = new Set(existingPosts.map((post) => post.id));
  const newIds = incomingPosts
    .filter((post) => !existingIds.has(post.id))
    .map((post) => post.id);

  const mergedMap = new Map();
  for (const post of [...incomingPosts, ...existingPosts]) {
    if (!mergedMap.has(post.id)) {
      mergedMap.set(post.id, post);
    }
  }

  return {
    posts: sortPostsNewestFirst(Array.from(mergedMap.values())),
    newIds,
  };
}

function readInitialState() {
  const params = getUrlParams();
  const isDemo = params.demo;
  const storedId = getStoredAgentId();
  const connected = isDemo || Boolean(params.agentId || storedId);

  return {
    isDemo,
    urlAgentId: params.agentId,
    agentId: isDemo ? 'demo' : params.agentId || storedId || null,
    connected,
    persona: getStoredPersona() || DEFAULT_PERSONA,
    posts: isDemo ? sortPostsNewestFirst(getDemoFeed().posts) : [],
    loading: connected && !isDemo,
    isPolling: connected,
    lastChecked: isDemo && connected ? new Date() : null,
  };
}

function App() {
  const [initial] = useState(readInitialState);
  const { isDemo, urlAgentId } = initial;

  const [agentId, setAgentId] = useState(initial.agentId);
  const [persona, setPersona] = useState(initial.persona);
  const [connected, setConnected] = useState(initial.connected);
  const [posts, setPosts] = useState(initial.posts);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(initial.loading);
  const [error, setError] = useState(false);
  const [isPolling, setIsPolling] = useState(initial.isPolling);
  const [lastChecked, setLastChecked] = useState(initial.lastChecked);
  const [newPostIds, setNewPostIds] = useState(() => new Set());

  const [personaName, setPersonaName] = useState(DEFAULT_PERSONA.name);
  const [personaDomain, setPersonaDomain] = useState(DEFAULT_PERSONA.domain);
  const [initLoading, setInitLoading] = useState(false);
  const [initError, setInitError] = useState(null);

  useEffect(() => {
    if (urlAgentId && !isDemo) {
      saveAgentSession(urlAgentId, getStoredPersona() || DEFAULT_PERSONA);
    }
  }, [urlAgentId, isDemo]);

  const markNewPosts = useCallback((ids) => {
    if (ids.length === 0) return;

    setNewPostIds((prev) => {
      const next = new Set(prev);
      ids.forEach((id) => next.add(id));
      return next;
    });
  }, []);

  useEffect(() => {
    if (!connected || isDemo || !agentId) {
      return undefined;
    }

    let cancelled = false;

    async function loadFeed() {
      try {
        const [feedData, statsData] = await Promise.all([
          fetchFeed(agentId),
          fetchStats(agentId),
        ]);

        if (cancelled) return;

        const incoming = feedData.posts || [];
        setPosts((prev) => {
          const { posts: merged, newIds } = mergePosts(prev, incoming);
          markNewPosts(newIds);
          return merged;
        });

        if (statsData) {
          setStats(statsData);
        }

        setLastChecked(new Date());
        setError(false);
      } catch {
        if (!cancelled) {
          setError(true);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadFeed();

    const intervalId = setInterval(loadFeed, POLL_INTERVAL_MS);

    return () => {
      cancelled = true;
      clearInterval(intervalId);
      setIsPolling(false);
    };
  }, [connected, agentId, isDemo, markNewPosts]);

  useEffect(() => {
    if (connected && isDemo) {
      setLastChecked(new Date());
    }
  }, [connected, isDemo]);

  async function handleInitialize(event) {
    event.preventDefault();
    setInitLoading(true);
    setInitError(null);

    const personaData = { name: personaName.trim(), domain: personaDomain.trim() };

    try {
      const result = await initializeAgent(personaData);
      saveAgentSession(result.agentId, personaData);
      setAgentId(result.agentId);
      setPersona(personaData);
      setConnected(true);
      setPosts([]);
      setNewPostIds(new Set());
      setError(false);
      setLoading(true);
      setIsPolling(true);
    } catch {
      setInitError('Unable to initialize agent. Please check your connection and try again.');
    } finally {
      setInitLoading(false);
    }
  }

  function handleDisconnect() {
    clearAgentSession();
    setConnected(false);
    setAgentId(null);
    setPosts([]);
    setStats(null);
    setIsPolling(false);
  }

  const metrics = useMemo(() => {
    if (isDemo) return getDemoMetrics(posts.length);
    return buildLiveMetrics(stats, posts.length);
  }, [isDemo, stats, posts.length]);

  const editorialStats = useMemo(() => {
    if (isDemo) return DEMO_EDITORIAL;
    return buildLiveEditorial(stats, posts.length);
  }, [isDemo, stats, posts.length]);

  const activityItems = useMemo(() => {
    if (isDemo) return DEMO_ACTIVITY;
    return buildLiveActivity({ lastChecked, postCount: posts.length, isPolling, loading, error });
  }, [isDemo, lastChecked, posts.length, isPolling, loading, error]);

  if (!connected) {
    return (
      <div className="app app--connect">
        <div className="connect-layout">
          <div className="connect-layout__brand">
            <div className="sidebar__logo sidebar__logo--large" aria-hidden="true">
              <span className="sidebar__logo-inner" />
            </div>
            <p className="connect-layout__product">AUTONOMOUS AI CREATOR</p>
            <p className="connect-layout__network">Intelligence Network</p>
          </div>

          <section className="panel connect-agent">
            <h2 className="panel__title">Initialize System</h2>
            <p className="connect-agent__description">
              {isDemo 
                ? 'Demo mode active. Initialize the simulated agent swarm to view the dashboard.' 
                : 'Initialize your autonomous AI agent to begin monitoring the ecosystem and publishing intelligence.'}
            </p>

            {isDemo ? (
              <div className="demo-init-container">
                <button
                  type="button"
                  className="connect-agent__button demo-swarm-btn"
                  onClick={() => {
                    setConnected(true);
                    setAgentId('demo');
                    setIsPolling(true);
                  }}
                >
                  <span className="demo-swarm-btn__icon">🚀</span>
                  Initialize Demo Swarm
                </button>
              </div>
            ) : (
              <form className="connect-agent__form" onSubmit={handleInitialize}>
                <div className="connect-agent__field">
                  <label htmlFor="persona-name">Persona Name</label>
                  <input
                    id="persona-name"
                    type="text"
                    value={personaName}
                    onChange={(e) => setPersonaName(e.target.value)}
                    placeholder="Ada"
                    required
                  />
                </div>

                <div className="connect-agent__field">
                  <label htmlFor="persona-domain">Domain</label>
                  <input
                    id="persona-domain"
                    type="text"
                    value={personaDomain}
                    onChange={(e) => setPersonaDomain(e.target.value)}
                    placeholder="AI Security"
                    required
                  />
                </div>

                {initError && (
                  <p className="connect-agent__error" role="alert">
                    {initError}
                  </p>
                )}

                <button
                  type="submit"
                  className="connect-agent__button"
                  disabled={initLoading}
                >
                  {initLoading ? 'Initializing…' : 'Initialize Agent'}
                </button>
              </form>
            )}

            {!isDemo && (
              <p className="connect-agent__hint">
                For demo mode without a backend, add{' '}
                <code>?demo=true</code> to the URL.
              </p>
            )}
          </section>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <Sidebar persona={persona} isDemo={isDemo} />

      <div className="app-main">
        <Header
          persona={persona}
          showLive={isPolling}
          lastChecked={lastChecked}
          onDisconnect={handleDisconnect}
        />

        <div className="dashboard">
          <section className="dashboard__section" id="overview">
            <MetricRow metrics={metrics} />
            <LiveScanning
              domain={persona.domain}
              lastChecked={lastChecked}
              isPolling={isPolling}
            />
          </section>

          <div className="dashboard__grid">
            <ActivityTimeline items={activityItems} />
            <EditorialPanel stats={editorialStats} />
          </div>

          <Feed
            posts={posts}
            loading={loading}
            error={error}
            newPostIds={newPostIds}
            category={persona.domain}
          />
        </div>

        <footer className="footer">
          <p className="footer__title">Autonomous AI Creator</p>
          <p className="footer__tagline">Continuously discovering. Evaluating. Publishing.</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
