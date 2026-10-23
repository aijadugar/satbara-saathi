"""SQLite-backed anonymous counters. No names, no survey numbers, no images."""
import csv
import io
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "impact.db"


class ImpactDB:
    def __init__(self, db_path: Path = DB_PATH):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init()

    def _init(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT, partner TEXT,
                documents INTEGER DEFAULT 0,
                lang_mr INTEGER DEFAULT 0, lang_hi INTEGER DEFAULT 0, lang_en INTEGER DEFAULT 0,
                feedback_yes INTEGER DEFAULT 0, feedback_no INTEGER DEFAULT 0,
                fields_corrected INTEGER DEFAULT 0,
                flags_serious INTEGER DEFAULT 0, flags_check INTEGER DEFAULT 0, flags_info INTEGER DEFAULT 0,
                UNIQUE(date, partner)
            );
        """)
        self.conn.commit()

    def _today(self):
        return datetime.utcnow().strftime("%Y-%m-%d")

    def _upsert(self, partner, col, inc=1):
        d = self._today()
        self.conn.execute(
            "INSERT INTO daily_stats(date,partner) VALUES(?,?) ON CONFLICT(date,partner) DO NOTHING",
            (d, partner),
        )
        self.conn.execute(
            f"UPDATE daily_stats SET {col}={col}+? WHERE date=? AND (partner=? OR (partner IS NULL AND ? IS NULL))",
            (inc, d, partner, partner),
        )
        self.conn.commit()

    def log_document(self, partner=None, language=None):
        self._upsert(partner, "documents")
        if language in ("mr", "hi", "en"):
            self._upsert(partner, f"lang_{language}")

    def log_flags(self, flags, partner=None):
        for f in flags:
            sev = f.get("severity", "info")
            col = {"serious": "flags_serious", "check": "flags_check", "info": "flags_info"}.get(sev)
            if col:
                self._upsert(partner, col)

    def log_feedback(self, positive, partner=None):
        self._upsert(partner, "feedback_yes" if positive else "feedback_no")

    def log_corrections(self, count, partner=None):
        self._upsert(partner, "fields_corrected", count)

    def get_stats(self, days=30, partner=None):
        start = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
        q = "SELECT SUM(documents) d, SUM(lang_mr) mr, SUM(lang_hi) hi, SUM(lang_en) en, SUM(feedback_yes) fy, SUM(feedback_no) fn FROM daily_stats WHERE date>=?"
        p = [start]
        if partner:
            q += " AND partner=?"
            p.append(partner)
        row = self.conn.execute(q, p).fetchone()
        return {
            "documents": row["d"] or 0,
            "languages": {"mr": row["mr"] or 0, "hi": row["hi"] or 0, "en": row["en"] or 0},
            "feedback": {"yes": row["fy"] or 0, "no": row["fn"] or 0},
        }

    def export_csv(self, days=30):
        start = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
        rows = self.conn.execute("SELECT * FROM daily_stats WHERE date>=? ORDER BY date", (start,)).fetchall()
        buf = io.StringIO()
        w = csv.writer(buf)
        if rows:
            w.writerow(rows[0].keys())
            for r in rows:
                w.writerow(list(r))
        return buf.getvalue()
