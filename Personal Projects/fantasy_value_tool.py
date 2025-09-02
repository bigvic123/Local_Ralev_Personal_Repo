
import argparse, sqlite3, pandas as pd, numpy as np, requests, io, re, pathlib, sys, time
DB_PATH = "fantasy_value.db"
HDR = {"User-Agent":"Mozilla/5.0"}
TEAM_MAP = {"JAX":"JAC","KCC":"KC","KAN":"KC","NOR":"NO","SFO":"SF","SFF":"SF","GNB":"GB","TAM":"TB","NWE":"NE","NEN":"NE","SDG":"LAC","LVR":"LV","OAK":"LV","STL":"LA","RAM":"LAR","LARM":"LAR","JAC":"JAC","WAS":"WAS","WFT":"WAS","ARI":"ARI","CRD":"ARI","HOU":"HOU","CLT":"IND","BAL":"BAL","CIN":"CIN","CLE":"CLE","DAL":"DAL","DEN":"DEN","DET":"DET","MIA":"MIA","MIN":"MIN","NE":"NE","NO":"NO","NYG":"NYG","NYJ":"NYJ","PHI":"PHI","PIT":"PIT","SEA":"SEA","LAC":"LAC","KC":"KC","BUF":"BUF","ATL":"ATL","CAR":"CAR","CHI":"CHI","TEN":"TEN","TB":"TB","GB":"GB","IND":"IND","LA":"LAR","LAR":"LAR","LV":"LV","SF":"SF","WAS Football Team":"WAS"}
POS_MAP = {"D/ST":"DST","DEF":"DST","DST":"DST","PK":"K","QB":"QB","RB":"RB","WR":"WR","TE":"TE","K":"K"}
def norm_name(n):
    if n is None:
        return None
    n = str(n)
    n = re.sub(r"\(.*?\)","",n)
    n = re.sub(r"[\*\u2020†]", "", n)
    n = re.sub(r"\b(Jr\.?|Sr\.?|III|II|IV)\b","",n, flags=re.I)
    n = re.sub(r"[^A-Za-z'\s\-]","",n)
    n = re.sub(r"\s+"," ",n).strip()
    return n
def name_key(n):
    n = norm_name(n).lower()
    n = n.replace("'", "").replace("-", "")
    return re.sub(r"\s+","",n)
def norm_team(t):
    if pd.isna(t):
        return None
    t = str(t).strip().upper()
    return TEAM_MAP.get(t, t)
def norm_pos(p):
    if p is None:
        return None
    p = str(p).strip().upper()
    return POS_MAP.get(p, p)
def ensure_db(conn):
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("CREATE TABLE IF NOT EXISTS sources (id INTEGER PRIMARY KEY, name TEXT UNIQUE, kind TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, name_key TEXT UNIQUE, position TEXT, team TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS adp (id INTEGER PRIMARY KEY, source_id INTEGER, player_id INTEGER, season INTEGER, format TEXT, adp REAL, rank REAL, sample INTEGER, updated_at INTEGER, UNIQUE(source_id, player_id, season, COALESCE(format,'')))")
    c.execute("CREATE TABLE IF NOT EXISTS projections (id INTEGER PRIMARY KEY, source_id INTEGER, player_id INTEGER, season INTEGER, scoring TEXT, points REAL, UNIQUE(source_id, player_id, season, COALESCE(scoring,'')))")
    c.execute("CREATE INDEX IF NOT EXISTS idx_adp_season ON adp(season)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_proj_season ON projections(season)")
    conn.commit()
def upsert_source(conn, name, kind):
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO sources(name,kind) VALUES(?,?)", (name, kind))
    cur.execute("SELECT id FROM sources WHERE name=?", (name,))
    return cur.fetchone()[0]
def upsert_player(conn, name, position=None, team=None):
    nk = name_key(name)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO players(name,name_key,position,team) VALUES(?,?,?,?)", (norm_name(name), nk, norm_pos(position), norm_team(team)))
    cur.execute("SELECT id,position,team FROM players WHERE name_key=?", (nk,))
    row = cur.fetchone()
    pid, ppos, pteam = row
    npos = norm_pos(position) if position else ppos
    nteam = norm_team(team) if team else pteam
    cur.execute("UPDATE players SET name=?, position=?, team=? WHERE id=?", (norm_name(name), npos, nteam, pid))
    return pid
def insert_adp_rows(conn, source_id, season, fmt, rows):
    ts = int(time.time())
    cur = conn.cursor()
    for r in rows:
        pid = upsert_player(conn, r["name"], r.get("pos"), r.get("team"))
        cur.execute("""INSERT OR REPLACE INTO adp(id,source_id,player_id,season,format,adp,rank,sample,updated_at)
                       VALUES(COALESCE((SELECT id FROM adp WHERE source_id=? AND player_id=? AND season=? AND COALESCE(format,'')=COALESCE(?,'')),NULL),
                              ?,?,?,?, ?,?,?,?)""",
                    (source_id,pid,season,fmt, source_id,pid,season,fmt, r.get("adp"), r.get("rank"), r.get("sample"), ts))
    conn.commit()
def insert_proj_rows(conn, source_id, season, scoring, rows):
    cur = conn.cursor()
    for r in rows:
        pid = upsert_player(conn, r["name"], r.get("pos"), r.get("team"))
        cur.execute("""INSERT OR REPLACE INTO projections(id,source_id,player_id,season,scoring,points)
                       VALUES(COALESCE((SELECT id FROM projections WHERE source_id=? AND player_id=? AND season=? AND COALESCE(scoring,'')=COALESCE(?,'')),NULL),
                              ?,?,?,?, ?)""",
                    (source_id,pid,season,scoring, source_id,pid,season,scoring, r.get("points")))
    conn.commit()
def read_html(url):
    r = requests.get(url, headers=HDR, timeout=45)
    r.raise_for_status()
    return r.text
def fp_adp(season, scoring):
    url = f"https://www.fantasypros.com/nfl/adp/overall.php?year={season}&scoring={scoring.lower()}"
    html = read_html(url)
    tables = pd.read_html(io.StringIO(html))
    df = None
    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        if any("player" in c for c in cols) and any("adp" in c for c in cols):
            df = t
            break
    if df is None:
        raise RuntimeError("ADP table not found")
    df.columns = [re.sub(r"\s+"," ",str(c)).strip() for c in df.columns]
    col_player = [c for c in df.columns if re.search(r"player", c, re.I)][0]
    col_team = [c for c in df.columns if re.search(r"team", c, re.I)]
    col_pos = [c for c in df.columns if re.search(r"pos", c, re.I)]
    col_adp = [c for c in df.columns if re.search(r"\bADP\b|Avg\.?\s*ADP|Average Draft Position", c, re.I)]
    col_rank = [c for c in df.columns if re.search(r"\brank\b|overall", c, re.I)]
    col_samp = [c for c in df.columns if re.search(r"drafts|sample|count", c, re.I)]
    out = []
    for _, row in df.iterrows():
        name = str(row[col_player])
        if name.lower().startswith("player") or not isinstance(name, str):
            continue
        out.append({
            "name": name,
            "team": row[col_team[0]] if col_team else None,
            "pos": row[col_pos[0]] if col_pos else None,
            "adp": pd.to_numeric(row[col_adp[0]], errors="coerce"),
            "rank": pd.to_numeric(row[col_rank[0]], errors="coerce") if col_rank else None,
            "sample": int(pd.to_numeric(row[col_samp[0]], errors="coerce")) if col_samp else None
        })
    out = [r for r in out if pd.notna(r["adp"])]
    return out
def fp_proj_for_pos(pos, scoring):
    url = f"https://www.fantasypros.com/nfl/projections/{pos.lower()}.php?week=draft&scoring={scoring.lower()}"
    html = read_html(url)
    tables = pd.read_html(io.StringIO(html))
    df = None
    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        if any("player" in c for c in cols) and any("fpts" in c or "points" in c for c in cols):
            df = t
            break
    if df is None:
        raise RuntimeError(f"Projection table not found for {pos}")
    df.columns = [re.sub(r"\s+"," ",str(c)).strip() for c in df.columns]
    col_player = [c for c in df.columns if re.search(r"player", c, re.I)][0]
    col_team = [c for c in df.columns if re.search(r"team", c, re.I)]
    col_points = [c for c in df.columns if re.search(r"fpts|fantasy points|points", c, re.I)][0]
    out = []
    for _, row in df.iterrows():
        name = str(row[col_player])
        if name.lower().startswith("player"):
            continue
        out.append({"name": name, "team": row[col_team[0]] if col_team else None, "pos": POS_MAP.get(pos.upper(), pos.upper()), "points": pd.to_numeric(row[col_points], errors="coerce")})
    out = [r for r in out if pd.notna(r["points"])]
    return out
def scrape_fantasypros(conn, season, scoring, include_adp, include_proj):
    sid_adp = upsert_source(conn, "FantasyPros ADP", "adp")
    sid_proj = upsert_source(conn, "FantasyPros Projections", "proj")
    if include_adp:
        rows = fp_adp(season, scoring)
        insert_adp_rows(conn, sid_adp, season, scoring.upper(), rows)
    if include_proj:
        rows = []
        for pos in ["qb","rb","wr","te","k","dst"]:
            try:
                rows += fp_proj_for_pos(pos, scoring)
            except Exception:
                continue
        insert_proj_rows(conn, sid_proj, season, scoring.upper(), rows)
def autodetect_csv(df):
    cols = list(df.columns)
    c_name = None
    for k in ["Player","PLAYER","Name","player","name"]:
        if k in cols:
            c_name = k; break
    c_team = None
    for k in ["Team","TEAM","Tm","team","NFL Team"]:
        if k in cols:
            c_team = k; break
    c_pos = None
    for k in ["Pos","POS","Position","position"]:
        if k in cols:
            c_pos = k; break
    c_adp = None
    for k in ["ADP","Avg ADP","Average Draft Position","Average ADP","Average_Draft_Position","Avg. ADP","AVG ADP","avg_adp","AvgPick"]:
        if k in cols:
            c_adp = k; break
    c_rank = None
    for k in ["Rank","Overall Rank","OVR","Overall"]:
        if k in cols:
            c_rank = k; break
    c_sample = None
    for k in ["Drafts","Sample","Count","NumDrafts"]:
        if k in cols:
            c_sample = k; break
    c_points = None
    for k in ["FPTS","Fantasy Points","Points","Proj Points","Projected Points","Fpts"]:
        if k in cols:
            c_points = k; break
    return {"name":c_name,"team":c_team,"pos":c_pos,"adp":c_adp,"rank":c_rank,"sample":c_sample,"points":c_points}
def import_csv(conn, kind, source, season, scoring_or_fmt, path):
    df = pd.read_csv(path)
    m = autodetect_csv(df)
    rows = []
    if kind=="adp":
        for _, r in df.iterrows():
            name = r.get(m["name"])
            if pd.isna(name): continue
            rows.append({"name":name,"team":r.get(m["team"]) if m["team"] else None,"pos":r.get(m["pos"]) if m["pos"] else None,"adp":pd.to_numeric(r.get(m["adp"]),errors="coerce") if m["adp"] else None,"rank":pd.to_numeric(r.get(m["rank"]),errors="coerce") if m["rank"] else None,"sample":int(pd.to_numeric(r.get(m["sample"]),errors="coerce")) if m["sample"] else None})
        rows = [x for x in rows if pd.notna(x["adp"])]
        sid = upsert_source(conn, source, "adp")
        insert_adp_rows(conn, sid, season, scoring_or_fmt.upper() if scoring_or_fmt else None, rows)
    else:
        for _, r in df.iterrows():
            name = r.get(m["name"])
            if pd.isna(name): continue
            rows.append({"name":name,"team":r.get(m["team"]) if m["team"] else None,"pos":r.get(m["pos"]) if m["pos"] else None,"points":pd.to_numeric(r.get(m["points"]),errors="coerce") if m["points"] else None})
        rows = [x for x in rows if pd.notna(x["points"])]
        sid = upsert_source(conn, source, "proj")
        insert_proj_rows(conn, sid, season, scoring_or_fmt.upper() if scoring_or_fmt else None, rows)
def adp_breakdown(conn, season):
    q = """SELECT p.id, p.name, s.name, a.adp FROM adp a JOIN players p ON p.id=a.player_id JOIN sources s ON s.id=a.source_id WHERE a.season=?"""
    df = pd.read_sql_query(q, conn, params=(season,))
    if df.empty:
        return pd.DataFrame(columns=["player_id","adp_sources"])
    df["row"] = df["name_y"] + ":" + df["adp"].round(2).astype(str)
    g = df.groupby("id").agg(adp_sources=("row", lambda x: "|".join(sorted(set(x))))).reset_index().rename(columns={"id":"player_id"})
    return g
def proj_breakdown(conn, season):
    q = """SELECT p.id, p.name, s.name, pr.points FROM projections pr JOIN players p ON p.id=pr.player_id JOIN sources s ON s.id=pr.source_id WHERE pr.season=?"""
    df = pd.read_sql_query(q, conn, params=(season,))
    if df.empty:
        return pd.DataFrame(columns=["player_id","proj_sources"])
    df["row"] = df["name_y"] + ":" + df["points"].round(1).astype(str)
    g = df.groupby("id").agg(proj_sources=("row", lambda x: "|".join(sorted(set(x))))).reset_index().rename(columns={"id":"player_id"})
    return g
def compute_values(conn, season, positions, min_adp_sources, min_proj_sources, scoring, top, require_both):
    qa = """SELECT p.id, p.name, p.position, p.team, AVG(a.adp) AS adp, COUNT(*) AS n_adp
            FROM adp a JOIN players p ON p.id=a.player_id
            WHERE a.season=?
            GROUP BY p.id"""
    qp = """SELECT p.id, AVG(pr.points) AS points, COUNT(*) AS n_proj
            FROM projections pr JOIN players p ON p.id=pr.player_id
            WHERE pr.season=? AND (? IS NULL OR pr.scoring=?)
            GROUP BY p.id"""
    da = pd.read_sql_query(qa, conn, params=(season,))
    dp = pd.read_sql_query(qp, conn, params=(season, scoring, scoring))
    if require_both:
        df = da.merge(dp, on="id", how="inner")
    else:
        df = da.merge(dp, on="id", how="outer")
    if positions:
        df = df[df["position"].isin([p.upper() for p in positions.split(",")])]
    df["n_adp"] = df["n_adp"].fillna(0).astype(int)
    df["n_proj"] = df["n_proj"].fillna(0).astype(int)
    df = df[(df["n_adp"]>=min_adp_sources) & (df["n_proj"]>=min_proj_sources)]
    df = df[pd.notna(df["adp"]) & pd.notna(df["points"])]
    if df.empty:
        return df
    df["proj_rank"] = df["points"].rank(ascending=False, method="min")
    df["adp_rank"] = df["adp"].rank(ascending=True, method="min")
    df["gap"] = df["adp_rank"] - df["proj_rank"]
    df["value_z"] = (df["points"]-df["points"].mean())/df["points"].std(ddof=0) - ((df["adp"]-df["adp"].mean())/df["adp"].std(ddof=0))
    bd_a = adp_breakdown(conn, season)
    bd_p = proj_breakdown(conn, season)
    df = df.merge(bd_a, left_on="id", right_on="player_id", how="left").drop(columns=["player_id"])
    df = df.merge(bd_p, left_on="id", right_on="player_id", how="left").drop(columns=["player_id"])
    df["team"] = df["team"].fillna("")
    df["position"] = df["position"].fillna("")
    df = df.sort_values(by=["gap","value_z","points"], ascending=[False, False, False]).head(top)
    cols = ["name","position","team","points","proj_rank","adp","adp_rank","gap","value_z","n_proj","n_adp","proj_sources","adp_sources"]
    return df[cols]
def show_table(conn, table, limit):
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT ?", conn, params=(limit,))
    print(df.to_csv(index=False))
def main():
    p = argparse.ArgumentParser(prog="fantasy_value_tool")
    sub = p.add_subparsers(dest="cmd", required=True)
    p_scrape = sub.add_parser("scrape")
    p_scrape.add_argument("--source", choices=["fantasypros"], required=True)
    p_scrape.add_argument("--season", type=int, required=True)
    p_scrape.add_argument("--scoring", choices=["PPR","HALF","STD"], default="PPR")
    p_scrape.add_argument("--adp", action="store_true")
    p_scrape.add_argument("--proj", action="store_true")
    p_import = sub.add_parser("import-csv")
    p_import.add_argument("--type", choices=["adp","proj"], required=True)
    p_import.add_argument("--source", required=True)
    p_import.add_argument("--season", type=int, required=True)
    p_import.add_argument("--scoring-or-format", default=None)
    p_import.add_argument("--path", required=True)
    p_value = sub.add_parser("value")
    p_value.add_argument("--season", type=int, required=True)
    p_value.add_argument("--positions", default=None)
    p_value.add_argument("--min-adp-sources", type=int, default=1)
    p_value.add_argument("--min-proj-sources", type=int, default=1)
    p_value.add_argument("--scoring", default=None)
    p_value.add_argument("--top", type=int, default=100)
    p_value.add_argument("--require-both", action="store_true")
    p_show = sub.add_parser("show")
    p_show.add_argument("--table", choices=["players","adp","projections","sources"], required=True)
    p_show.add_argument("--limit", type=int, default=20)
    args = p.parse_args()
    pathlib.Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)
    if args.cmd == "scrape":
        if args.source == "fantasypros":
            scrape_fantasypros(conn, args.season, args.scoring, args.adp or (not args.proj), args.proj or (not args.adp))
    elif args.cmd == "import-csv":
        import_csv(conn, args.type, args.source, args.season, args.scoring_or_format, args.path)
    elif args.cmd == "value":
        df = compute_values(conn, args.season, args.positions, args.min_adp_sources, args.min_proj_sources, args.scoring, args.top, args.require_both)
        if df.empty:
            print("")
        else:
            print(df.to_csv(index=False))
    elif args.cmd == "show":
        show_table(conn, args.table, args.limit)
    conn.close()
if __name__ == "__main__":
    main()
