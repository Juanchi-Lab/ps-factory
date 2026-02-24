PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY,
  topic TEXT NOT NULL,
  bitcoin_anchor TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',         -- draft|approved|rejected|posted
  draft_chat_id INTEGER,
  draft_message_id INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS post_versions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id TEXT NOT NULL,
  version INTEGER NOT NULL,
  model TEXT,
  content_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
  UNIQUE(post_id, version)
);

CREATE TABLE IF NOT EXISTS post_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id TEXT NOT NULL,
  event_type TEXT NOT NULL,                     -- GEN|REGEN|APPROVE|REJECT|EDIT
  meta_json TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS posts_updated_at
AFTER UPDATE ON posts
FOR EACH ROW
BEGIN
  UPDATE posts SET updated_at=datetime('now') WHERE id=OLD.id;
END;
