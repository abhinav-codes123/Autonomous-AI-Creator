import PostCard from './PostCard';

function Feed({ posts, loading, error, newPostIds, category }) {
  return (
    <section className="feed" id="intelligence">
      <div className="feed__header">
        <h2 className="feed__title">Live Intelligence</h2>
        <p className="feed__subtitle">Latest discoveries from your autonomous agent</p>
      </div>

      {loading && posts.length === 0 && (
        <div className="feed__state feed__state--loading">
          <div className="feed__spinner" aria-hidden="true" />
          <p className="feed__state-title">Synchronizing intelligence feed…</p>
          <p className="feed__state-subtitle">Connecting to autonomous agent</p>
        </div>
      )}

      {error && (
        <div className="feed__state feed__state--error" role="alert">
          <div className="feed__state-icon" aria-hidden="true">⚠</div>
          <p className="feed__state-title">Connection interrupted</p>
          <p className="feed__state-subtitle">
            Unable to reach the autonomous agent. Retrying automatically…
          </p>
        </div>
      )}

      {!loading && !error && posts.length === 0 && (
        <div className="feed__state feed__state--empty">
          <div className="feed__empty-radar" aria-hidden="true">
            <span className="feed__empty-ring feed__empty-ring--1" />
            <span className="feed__empty-ring feed__empty-ring--2" />
            <span className="feed__empty-ring feed__empty-ring--3" />
            <span className="feed__empty-core" />
          </div>
          <p className="feed__state-title">Your agent is watching.</p>
          <p className="feed__state-subtitle">
            Scanning the AI ecosystem for high-signal developments.
          </p>
        </div>
      )}

      {posts.length > 0 && (
        <div className="feed__posts">
          {posts.map((post, index) => (
            <PostCard
              key={post.id}
              post={post}
              isNew={newPostIds.has(post.id)}
              isFeatured={index === 0}
              category={category}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default Feed;
