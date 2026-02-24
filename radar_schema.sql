CREATE TABLE IF NOT EXISTS kv_store (
  k TEXT PRIMARY KEY,
  v TEXT NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS radar_candidates (
  candidate_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  source TEXT NOT NULL,
  title TEXT NOT NULL,
  summary TEXT,
  evidence_json TEXT NOT NULL,
  scores_json TEXT NOT NULL,
  total_score REAL NOT NULL,
  created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_radar_run_id ON radar_candidates(run_id);
CREATE INDEX IF NOT EXISTS idx_radar_total_score ON radar_candidates(total_score);
