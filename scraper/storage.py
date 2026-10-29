"""
SQLite database storage layer for candidate domains, metadata, and outreach contact details.
Handles domain-level deduplication, incremental updates, and export to CSV/Excel.
"""

import sqlite3
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import pandas as pd
from scraper.config import DB_PATH, EXPORTS_DIR

class Storage:
    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT UNIQUE NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT,
                    snippet TEXT,
                    keyword TEXT,
                    footprint TEXT,
                    engine TEXT,
                    status_code INTEGER,
                    contact_email TEXT,
                    contact_url TEXT,
                    social_links TEXT,
                    contact_checked INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT UNIQUE NOT NULL,
                    engine TEXT,
                    results_count INTEGER DEFAULT 0,
                    run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_targets_domain ON targets(domain)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_targets_checked ON targets(contact_checked)")
            conn.commit()

    def add_target(self, domain: str, url: str, title: str = "", snippet: str = "",
                   keyword: str = "", footprint: str = "", engine: str = "") -> bool:
        """
        Inserts a single target domain. Returns True if inserted, False if domain already exists.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO targets (domain, url, title, snippet, keyword, footprint, engine)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (domain, url, title, snippet, keyword, footprint, engine))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def batch_add_targets(self, items: List[Dict]) -> Tuple[int, int]:
        """
        Inserts a batch of scraped items.
        Returns (new_inserted_count, duplicate_count).
        """
        new_count = 0
        duplicate_count = 0
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for item in items:
                try:
                    cursor.execute("""
                        INSERT INTO targets (domain, url, title, snippet, keyword, footprint, engine)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        item.get("domain", "").strip().lower(),
                        item.get("url", "").strip(),
                        item.get("title", "").strip(),
                        item.get("snippet", "").strip(),
                        item.get("keyword", "").strip(),
                        item.get("footprint", "").strip(),
                        item.get("engine", "").strip(),
                    ))
                    new_count += 1
                except sqlite3.IntegrityError:
                    duplicate_count += 1
            conn.commit()
        return new_count, duplicate_count

    def log_query(self, query: str, engine: str, results_count: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO queries_log (query, engine, results_count, run_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (query, engine, results_count))
            conn.commit()

    def is_query_logged(self, query: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM queries_log WHERE query = ?", (query,))
            return cursor.fetchone() is not None

    def get_stats(self) -> Dict:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM targets")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM targets WHERE contact_checked = 1")
            checked = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM targets WHERE contact_email IS NOT NULL AND contact_email != ''")
            with_email = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM targets WHERE contact_url IS NOT NULL AND contact_url != ''")
            with_contact_page = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM queries_log")
            queries_run = cursor.fetchone()[0]

            cursor.execute("SELECT keyword, COUNT(*) as cnt FROM targets GROUP BY keyword ORDER BY cnt DESC LIMIT 5")
            top_keywords = [{"keyword": row["keyword"], "count": row["cnt"]} for row in cursor.fetchall()]

            cursor.execute("SELECT footprint, COUNT(*) as cnt FROM targets GROUP BY footprint ORDER BY cnt DESC LIMIT 5")
            top_footprints = [{"footprint": row["footprint"], "count": row["cnt"]} for row in cursor.fetchall()]

            return {
                "total_targets": total,
                "checked_for_contacts": checked,
                "with_email": with_email,
                "with_contact_page": with_contact_page,
                "queries_run": queries_run,
                "top_keywords": top_keywords,
                "top_footprints": top_footprints,
            }

    def get_uninspected_targets(self, limit: int = 50) -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, domain, url, title FROM targets
                WHERE contact_checked = 0
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def update_contact_info(self, target_id: int, email: Optional[str],
                            contact_url: Optional[str], social_links: Optional[str],
                            status_code: Optional[int]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE targets
                SET contact_email = ?,
                    contact_url = ?,
                    social_links = ?,
                    status_code = ?,
                    contact_checked = 1
                WHERE id = ?
            """, (email, contact_url, social_links, status_code, target_id))
            conn.commit()

    def get_all_targets_df(self) -> pd.DataFrame:
        with self._get_connection() as conn:
            query = """
                SELECT 
                    domain as "Domain",
                    url as "Target URL",
                    title as "Page Title",
                    contact_email as "Email",
                    contact_url as "Contact / About URL",
                    social_links as "Social Links",
                    keyword as "Keyword",
                    footprint as "Footprint Preset",
                    engine as "Search Engine",
                    snippet as "Snippet",
                    status_code as "HTTP Status",
                    created_at as "Discovered At"
                FROM targets
                ORDER BY id DESC
            """
            return pd.read_sql_query(query, conn)

    def export_to_csv(self, filename: Optional[str] = None) -> Tuple[int, str]:
        if not filename:
            filename = f"link_insertion_targets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        export_path = EXPORTS_DIR / filename
        df = self.get_all_targets_df()
        df.to_csv(export_path, index=False)
        return len(df), str(export_path)

    def export_to_excel(self, filename: Optional[str] = None) -> Tuple[int, str]:
        if not filename:
            filename = f"link_insertion_targets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        export_path = EXPORTS_DIR / filename
        df = self.get_all_targets_df()
        df.to_excel(export_path, index=False, engine="openpyxl")
        return len(df), str(export_path)
