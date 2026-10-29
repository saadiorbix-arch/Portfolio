"""
Search Engine Results Page (SERP) Scraper.
Supports DuckDuckGo (HTML / Lite) and Bing with rate-limiting, user-agent rotation,
clean URL extraction, and domain filtering.
"""

import asyncio
import random
import re
import warnings
import urllib.parse
from typing import List, Dict, Optional
import httpx
from bs4 import BeautifulSoup
import tldextract

warnings.filterwarnings("ignore")

from scraper.config import USER_AGENTS, EXCLUDED_DOMAINS, REQUEST_TIMEOUT, DEFAULT_DELAY

class SerpScraper:
    def __init__(self, delay_between_requests: float = DEFAULT_DELAY):
        self.delay = delay_between_requests
        self.tld_extractor = tldextract.TLDExtract()

    def _get_random_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
        }

    def extract_registered_domain(self, url: str) -> Optional[str]:
        """
        Extracts clean root domain (e.g. 'sub.example.co.uk' -> 'example.co.uk').
        """
        try:
            extracted = self.tld_extractor(url)
            if not extracted.domain or not extracted.suffix:
                return None
            return f"{extracted.domain}.{extracted.suffix}".lower()
        except Exception:
            return None

    def clean_target_url(self, raw_url: str) -> Optional[str]:
        """
        Cleans redirect wrappers (such as DuckDuckGo /l/?uddg=... or Bing redirection).
        """
        if not raw_url:
            return None
        
        # DuckDuckGo redirect decode
        if "duckduckgo.com/l/?" in raw_url or "/l/?uddg=" in raw_url:
            parsed = urllib.parse.urlparse(raw_url)
            query_params = urllib.parse.parse_qs(parsed.query)
            if "uddg" in query_params and query_params["uddg"]:
                raw_url = urllib.parse.unquote(query_params["uddg"][0])

        # Bing redirect decode if necessary
        if "bing.com/ck/a?" in raw_url:
            # Skip internal bing tracking links if not decoded
            return None

        # Clean tracking params (utm_*, ref, etc.)
        try:
            parsed = urllib.parse.urlparse(raw_url)
            if not parsed.scheme or not parsed.netloc:
                return None
            if parsed.scheme not in ("http", "https"):
                return None

            clean_query = urllib.parse.parse_qsl(parsed.query)
            clean_query = [(k, v) for k, v in clean_query if not k.lower().startswith("utm_") and k.lower() not in ("ref", "fbclid")]
            new_query = urllib.parse.urlencode(clean_query)
            cleaned = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, ""))
            return cleaned.rstrip("/")
        except Exception:
            return None

    def is_allowed_domain(self, domain: str) -> bool:
        if not domain:
            return False
        domain_lower = domain.lower()
        return domain_lower not in EXCLUDED_DOMAINS

    async def scrape_duckduckgo(self, client: httpx.AsyncClient, query: str, max_results: int = 30) -> List[Dict]:
        """
        Scrapes DuckDuckGo HTML endpoint.
        """
        results = []
        url = "https://html.duckduckgo.com/html/"
        headers = self._get_random_headers()
        headers["Referer"] = "https://html.duckduckgo.com/"
        data = {"q": query, "b": ""}

        try:
            resp = await client.post(url, data=data, headers=headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                # Fallback to Lite version if HTML blocks
                return await self.scrape_duckduckgo_lite(client, query, max_results)

            soup = BeautifulSoup(resp.text, "html.parser")
            result_elements = soup.select(".result")

            for el in result_elements:
                title_el = el.select_one(".result__title .result__a")
                snippet_el = el.select_one(".result__snippet")

                if not title_el or not title_el.get("href"):
                    continue

                raw_href = title_el["href"]
                clean_url = self.clean_target_url(raw_href)
                if not clean_url:
                    continue

                domain = self.extract_registered_domain(clean_url)
                if not domain or not self.is_allowed_domain(domain):
                    continue

                title = title_el.get_text(strip=True)
                snippet = snippet_el.get_text(strip=True) if snippet_el else ""

                results.append({
                    "domain": domain,
                    "url": clean_url,
                    "title": title,
                    "snippet": snippet,
                    "engine": "duckduckgo",
                })
                if len(results) >= max_results:
                    break

        except Exception as e:
            # Fallback to Lite on connection issues
            return await self.scrape_duckduckgo_lite(client, query, max_results)

        return results

    async def scrape_duckduckgo_lite(self, client: httpx.AsyncClient, query: str, max_results: int = 30) -> List[Dict]:
        """
        Scrapes DuckDuckGo Lite endpoint (clean HTML, very lightweight).
        """
        results = []
        url = "https://lite.duckduckgo.com/lite/"
        headers = self._get_random_headers()
        data = {"q": query}

        try:
            resp = await client.post(url, data=data, headers=headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                return results

            soup = BeautifulSoup(resp.text, "html.parser")
            rows = soup.select("table tbody tr")

            for i, row in enumerate(rows):
                link_el = row.select_one("a.result-link")
                if link_el and link_el.get("href"):
                    raw_href = link_el["href"]
                    clean_url = self.clean_target_url(raw_href)
                    if not clean_url:
                        continue

                    domain = self.extract_registered_domain(clean_url)
                    if not domain or not self.is_allowed_domain(domain):
                        continue

                    title = link_el.get_text(strip=True)
                    # Snippet is often in the next table row
                    snippet = ""
                    if i + 1 < len(rows):
                        snippet_el = rows[i + 1].select_one(".result-snippet")
                        if snippet_el:
                            snippet = snippet_el.get_text(strip=True)

                    results.append({
                        "domain": domain,
                        "url": clean_url,
                        "title": title,
                        "snippet": snippet,
                        "engine": "duckduckgo_lite",
                    })
                    if len(results) >= max_results:
                        break

        except Exception:
            pass

        return results

    async def scrape_bing(self, client: httpx.AsyncClient, query: str, max_results: int = 30) -> List[Dict]:
        """
        Scrapes Bing Search HTML endpoint across multiple result pages.
        """
        results = []
        headers = self._get_random_headers()
        pages_to_crawl = (max_results // 10) + 1

        for page in range(min(pages_to_crawl, 3)):
            first = (page * 10) + 1
            url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&first={first}"

            try:
                resp = await client.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                if resp.status_code != 200:
                    break

                soup = BeautifulSoup(resp.text, "html.parser")
                items = soup.select("li.b_algo")

                if not items:
                    break

                for item in items:
                    link_el = item.select_one("h2 a")
                    if not link_el or not link_el.get("href"):
                        continue

                    raw_href = link_el["href"]
                    clean_url = self.clean_target_url(raw_href)
                    if not clean_url:
                        continue

                    domain = self.extract_registered_domain(clean_url)
                    if not domain or not self.is_allowed_domain(domain):
                        continue

                    title = link_el.get_text(strip=True)
                    snippet_el = item.select_one(".b_caption p")
                    snippet = snippet_el.get_text(strip=True) if snippet_el else ""

                    results.append({
                        "domain": domain,
                        "url": clean_url,
                        "title": title,
                        "snippet": snippet,
                        "engine": "bing",
                    })

                    if len(results) >= max_results:
                        return results

                await asyncio.sleep(self.delay)

            except Exception:
                break

        return results

    async def search(self, query: str, engine: str = "all", max_results: int = 30) -> List[Dict]:
        """
        Executes search using requested search engine(s).
        """
        results = []
        async with httpx.AsyncClient(follow_redirects=True) as client:
            if engine in ("duckduckgo", "all"):
                ddg_results = await self.scrape_duckduckgo(client, query, max_results)
                results.extend(ddg_results)
                await asyncio.sleep(self.delay)

            if engine in ("bing", "all") and len(results) < max_results:
                bing_results = await self.scrape_bing(client, query, max_results - len(results))
                results.extend(bing_results)

        # In-memory domain deduplication for this query batch
        seen_domains = set()
        deduped = []
        for r in results:
            if r["domain"] not in seen_domains:
                seen_domains.add(r["domain"])
                deduped.append(r)

        return deduped
