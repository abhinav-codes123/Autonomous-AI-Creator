import { useState } from 'react';
import { formatTimestamp, getSourceDisplayName } from '../utils/format';

function ExternalLinkIcon() {
  return (
    <svg
      className="post-card__external-icon"
      width="12"
      height="12"
      viewBox="0 0 12 12"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M4.5 2H2.5C2.22 2 2 2.22 2 2.5V9.5C2 9.78 2.22 10 2.5 10H9.5C9.78 10 10 9.78 10 9.5V7.5"
        stroke="currentColor"
        strokeWidth="1.2"
        strokeLinecap="round"
      />
      <path
        d="M7 2H10V5M10 2L5.5 6.5"
        stroke="currentColor"
        strokeWidth="1.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function PostCard({ post, isNew, isFeatured, category }) {
  const [showRationale, setShowRationale] = useState(false);

  return (
    <article
      className={`post-card${isFeatured ? ' post-card--featured' : ''}${isNew ? ' post-card--new' : ''}`}
    >
      <div className="post-card__top">
        <span className="post-card__publication-label">Autonomous Publication</span>
        <div className="post-card__badges">
          {isNew && <span className="post-card__new">NEW</span>}
          <span className="post-card__category">{category}</span>
        </div>
      </div>

      <div className="post-card__header">
        <span className="post-card__id">{post.id}</span>
        <time className="post-card__time" dateTime={post.createdAt}>
          {formatTimestamp(post.createdAt)}
        </time>
      </div>

      <p className="post-card__text">{post.text}</p>

      {post.sources && post.sources.length > 0 && (
        <div className="post-card__section">
          <ul className="post-card__sources">
            {post.sources.map((source) => (
              <li key={source}>
                <a
                  href={source}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="post-card__source-link"
                >
                  <span>{getSourceDisplayName(source)}</span>
                  <ExternalLinkIcon />
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="post-card__actions">
        <button 
          className="btn-rationale" 
          onClick={() => setShowRationale(!showRationale)}
        >
          <span className="btn-rationale__icon">🧠</span>
          {showRationale ? 'Hide AI Rationale' : 'View AI Rationale'}
        </button>
      </div>

      {showRationale && (
        <div className="post-card__rationale-panel slide-down">
          <h3 className="rationale-panel__title">AI Thought Process</h3>
          <p className="rationale-panel__text">{post.rationale}</p>
        </div>
      )}
    </article>
  );
}

export default PostCard;
