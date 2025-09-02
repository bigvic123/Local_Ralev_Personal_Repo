
import argparse, sqlite3, pandas as pd, requests, io, sys, pathlib, re
DB_PATH = "nba_stats.db"
def fetch_html(url):
    h = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=h, timeout=30)
    r.raise_for_status()
    return r.text
def read_advanced_table(html):
    tables = pd.read_html(io.StringIO(html))
    cand = None
    for t in tables:
        cols = [c.lower() for c in t.columns]
        if any("per" == c for c in cols) and any("ts%" in c for c in cols) and any("ws/48" in c for c in cols):
            cand = t
            break
    if cand is None:
        for t in tables:
            cols = [str(c).lower() for c in t.columns]
            if "per" in cols and "ts%" in cols:
                cand = t
                break
    if cand is None:
        raise RuntimeError("Advanced table not found")
    return cand
def clean_df(df):
    df = df.copy()
    if "Rk" in df.columns:
        df = df[df["Rk"].astype(str) != "Rk"]
    df.columns = [str(c) for c in df.columns]
    for c in df.columns:
        if isinstance(c, tuple):
            pass
    for c in ["PER","TS%","WS/48","BPM","VORP","MP"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if "Player" in df.columns:
        df["Player"] = df["Player"].astype(str).str.replace(r"[*†]", "", regex=True).str.strip()
    if "Tm" in df.columns:
        df["Tm"] = df["Tm"].astype(str)
    keep_cols = [c for c in ["Player","Tm","MP","PER","TS%","WS/48","BPM","VORP"] if c in df.columns]
    df = df[keep_cols]
    return df
def prefer_tot(df):
    if "Tm" not in df.columns:
        return df
    df = df.copy()
    df["_is_tot"] = (df["Tm"] == "TOT").astype(int)
    df["_mp_rank"] = df["MP"].fillna(0)
    df = df.sort_values(by=["Player","_is_tot","_mp_rank"], ascending=[True, False, False])
    df = df.groupby("Player", as_index=False).first()
    return df.drop(columns=["_is_tot","_mp_rank"])
def ensure_db(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL")
    cur.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    cur.execute("CREATE TABLE IF NOT EXISTS seasons (id INTEGER PRIMARY KEY, year INTEGER UNIQUE)")
    cur.execute("""CREATE TABLE IF NOT EXISTS stats_advanced (
        id INTEGER PRIMARY KEY,
        player_id INTEGER,
        season_id INTEGER,
        team TEXT,
        mp REAL,
        per REAL,
        ts REAL,
        ws48 REAL,
        bpm REAL,
        vorp REAL,
        UNIQUE(player_id, season_id),
        FOREIGN KEY(player_id) REFERENCES players(id),
        FOREIGN KEY(season_id) REFERENCES seasons(id)
    )""")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_stats_metric ON stats_advanced(season_id, per, ts, ws48, bpm, vorp)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_stats_player ON stats_advanced(player_id)")
    conn.commit()
def upsert(conn, table, key_col, key_val):
    cur = conn.cursor()
    cur.execute(f"INSERT OR IGNORE INTO {table}({key_col}) VALUES (?)", (key_val,))
    cur.execute(f"SELECT id FROM {table} WHERE {key_col}=?", (key_val,))
    return cur.fetchone()[0]
def insert_stats(conn, season_year, df, use_tot):
    conn.execute("BEGIN")
    try:
        sid = upsert(conn, "seasons", "year", int(season_year))
        if use_tot:
            df2 = prefer_tot(df)
        else:
            df2 = df.copy()
        for _, row in df2.iterrows():
            name = str(row.get("Player"))
            if not name or name == "nan":
                continue
            pid = upsert(conn, "players", "name", name)
            vals = {
                "team": str(row.get("Tm")) if "Tm" in row else None,
                "mp": float(row.get("MP")) if pd.notna(row.get("MP")) else None,
                "per": float(row.get("PER")) if pd.notna(row.get("PER")) else None,
                "ts": float(row.get("TS%")) if pd.notna(row.get("TS%")) else None,
                "ws48": float(row.get("WS/48")) if pd.notna(row.get("WS/48")) else None,
                "bpm": float(row.get("BPM")) if pd.notna(row.get("BPM")) else None,
                "vorp": float(row.get("VORP")) if pd.notna(row.get("VORP")) else None,
            }
            cur = conn.cursor()
            cur.execute("""INSERT OR REPLACE INTO stats_advanced
                (id, player_id, season_id, team, mp, per, ts, ws48, bpm, vorp)
                VALUES (
                    COALESCE((SELECT id FROM stats_advanced WHERE player_id=? AND season_id=?), NULL),
                    ?,?,?,?,?,?,?,?,?
                )
            """, (pid, sid, pid, sid, vals["team"], vals["mp"], vals["per"], vals["ts"], vals["ws48"], vals["bpm"], vals["vorp"]))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
def season_iter(spec):
    spec = str(spec).strip()
    if re.fullmatch(r"\d{4}", spec):
        yield int(spec)
        return
    if re.fullmatch(r"\d{4}\s*-\s*\d{4}", spec):
        a, b = re.split(r"\s*-\s*", spec)
        a, b = int(a), int(b)
        step = 1 if b >= a else -1
        for y in range(a, b + step, step):
            yield y
        return
    if "," in spec:
        for part in spec.split(","):
            part = part.strip()
            for y in season_iter(part):
                yield y
        return
    raise ValueError("Invalid season spec")
def fetch_season(season, use_tot):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_advanced.html"
    html = fetch_html(url)
    df = read_advanced_table(html)
    df = clean_df(df)
    return df
def fetch_command(args):
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)
    for season in season_iter(args.seasons):
        df = fetch_season(season, args.use_tot)
        insert_stats(conn, season, df, args.use_tot)
    conn.close()
def rank_command(args):
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)
    metric_map = {"per":"per","ts%":"ts","ts":"ts","ws/48":"ws48","ws48":"ws48","bpm":"bpm","vorp":"vorp"}
    mcol = metric_map.get(args.metric.lower())
    if not mcol:
        raise SystemExit("Unknown metric")
    seasons = list(season_iter(args.seasons))
    placeholders = ",".join(["?"]*len(seasons))
    per_season_cut = max(args.min_mp, 0)
    if args.agg == "weighted":
        q = f"""
        WITH filt AS (
            SELECT sa.player_id, sa.season_id, sa.mp, sa.{mcol} AS val
            FROM stats_advanced sa JOIN seasons s ON s.id=sa.season_id
            WHERE s.year IN ({placeholders}) AND sa.mp >= ?
        )
        SELECT p.name, SUM(f.mp) AS mp, ROUND(SUM(f.val*f.mp)/NULLIF(SUM(f.mp),0), 4) AS value,
               GROUP_CONCAT(s.year, ',') AS seasons
        FROM filt f
        JOIN players p ON p.id=f.player_id
        JOIN seasons s ON s.id=f.season_id
        GROUP BY p.id
        HAVING mp >= ?
        ORDER BY value DESC, mp DESC
        LIMIT ?
        """
        params = seasons + [per_season_cut, args.min_total_mp, args.top]
    elif args.agg == "mean":
        q = f"""
        WITH filt AS (
            SELECT sa.player_id, sa.season_id, sa.mp, sa.{mcol} AS val
            FROM stats_advanced sa JOIN seasons s ON s.id=sa.season_id
            WHERE s.year IN ({placeholders}) AND sa.mp >= ?
        )
        SELECT p.name, SUM(f.mp) AS mp, ROUND(AVG(f.val),4) AS value, GROUP_CONCAT(s.year, ',') AS seasons
        FROM filt f JOIN players p ON p.id=f.player_id JOIN seasons s ON s.id=f.season_id
        GROUP BY p.id
        HAVING mp >= ?
        ORDER BY value DESC, mp DESC
        LIMIT ?
        """
        params = seasons + [per_season_cut, args.min_total_mp, args.top]
    else:
        q = f"""
        WITH filt AS (
            SELECT sa.player_id, sa.season_id, sa.mp, sa.{mcol} AS val
            FROM stats_advanced sa JOIN seasons s ON s.id=sa.season_id
            WHERE s.year IN ({placeholders}) AND sa.mp >= ?
        )
        SELECT p.name, SUM(f.mp) AS mp, ROUND(MAX(f.val),4) AS value, GROUP_CONCAT(s.year, ',') AS seasons
        FROM filt f JOIN players p ON p.id=f.player_id JOIN seasons s ON s.id=f.season_id
        GROUP BY p.id
        HAVING mp >= ?
        ORDER BY value DESC, mp DESC
        LIMIT ?
        """
        params = seasons + [per_season_cut, args.min_total_mp, args.top]
    cur = conn.cursor()
    cur.execute(q, params)
    rows = cur.fetchall()
    cols = ["player","total_mp","value","seasons"]
    df = pd.DataFrame(rows, columns=cols)
    print(df.to_csv(index=False))
    conn.close()
def table_command(args):
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)
    cur = conn.cursor()
    cur.execute("""SELECT p.name, s.year, sa.team, sa.mp, sa.per, sa.ts, sa.ws48, sa.bpm, sa.vorp
                   FROM stats_advanced sa
                   JOIN players p ON p.id=sa.player_id
                   JOIN seasons s ON s.id=sa.season_id
                   ORDER BY s.year DESC, sa.per DESC, sa.mp DESC
                   LIMIT ?""", (args.limit,))
    rows = cur.fetchall()
    cols = ["player","season","team","mp","per","ts","ws48","bpm","vorp"]
    df = pd.DataFrame(rows, columns=cols)
    print(df.to_csv(index=False))
    conn.close()
def main():
    parser = argparse.ArgumentParser(prog="basketball_ranker")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_fetch = sub.add_parser("fetch")
    p_fetch.add_argument("--seasons", type=str, required=True)
    p_fetch.add_argument("--use-tot", action="store_true")
    p_fetch.set_defaults(func=fetch_command)
    p_rank = sub.add_parser("rank")
    p_rank.add_argument("--metric", type=str, required=True)
    p_rank.add_argument("--seasons", type=str, required=True)
    p_rank.add_argument("--min-mp", type=int, default=250)
    p_rank.add_argument("--min-total-mp", type=int, default=1000)
    p_rank.add_argument("--agg", type=str, choices=["weighted","mean","max"], default="weighted")
    p_rank.add_argument("--top", type=int, default=25)
    p_rank.set_defaults(func=rank_command)
    p_table = sub.add_parser("show")
    p_table.add_argument("--limit", type=int, default=50)
    p_table.set_defaults(func=table_command)
    args = parser.parse_args()
    main_dir = pathlib.Path(DB_PATH).parent
    main_dir.mkdir(parents=True, exist_ok=True)
    args.func(args)
if __name__ == "__main__":
    main()
