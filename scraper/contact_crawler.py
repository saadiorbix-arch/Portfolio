"""
Deep Contact & Editorial Crawler.
Inspects candidate websites to uncover outreach emails, contact pages,
editorial guideline links, and social channels.
"""

import asyncio
import re
import urllib.parse
from typing import Dict, Optional, Set, Tuple
import httpx
from bs4 import BeautifulSoup

from scraper.config import USER_AGENTS, REQUEST_TIMEOUT, CONCURRENT_CONTACT_CRAWLS

# Email regex pattern
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
)

# Common junk emails / false positives
IGNORED_EMAIL_DOMAINS = {
    "example.com", "domain.com", "yourdomain.com", "mysite.com", "wixpress.com",
    "sentry.io", "gravatar.com", "bootstrap.com", "fontawesome.com", "schema.org"
}

IGNORED_EMAIL_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".css", ".js", ".woff", ".woff2")

CONTACT_SLUGS = [
    "contact", "contact-us", "about", "about-us", "write-for-us",
    "guest-post", "contribute", "editorial-guidelines", "submissions", "pitch-us"
]

class ContactCrawler:
    def __init__(self, concurrency: int = CONCURRENT_CONTACT_CRAWLS):
        self.semaphore = asyncio.Semaphore(concurrency)

    def _clean_email(self, email: str) -> Optional[str]:
        email = email.strip().lower().rstrip(".,;:'\"")
        if any(email.endswith(ext) for ext in IGNORED_EMAIL_EXTENSIONS):
            return None
        parts = email.split("@")
        if len(parts) != 2:
            return None
        domain = parts[1]
        if domain in IGNORED_EMAIL_DOMAINS:
            return None
        if len(parts[0]) > 40 or len(domain) < 4:
            return None
        return email

    def extract_emails(self, text: str, soup: BeautifulSoup) -> Set[str]:
        found = set()
        # 1. Mailto links
        for a in soup.select('a[href^="mailto:"]'):
            href = a.get("href", "")
            raw_email = href.replace("mailto:", "").split("?")[0]
            clean = self._clean_email(raw_email)
            if clean:
                found.add(clean)

        # 2. Text regex
        matches = EMAIL_REGEX.findall(text)
        for m in matches:
            clean = self._clean_email(m)
            if clean:
                found.add(clean)

        return found

    def find_contact_urls(self, base_url: str, soup: BeautifulSoup) -> Optional[str]:
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            full_url = urllib.parse.urljoin(base_url, href)
            path_lower = urllib.parse.urlparse(full_url).path.lower()
            text_lower = a.get_text(strip=True).lower()

            for slug in CONTACT_SLUGS:
                if slug in path_lower or slug.replace("-", " ") in text_lower:
                    # Make sure it's the same domain
                    if urllib.parse.urlparse(full_url).netloc == urllib.parse.urlparse(base_url).netloc:
                        return full_url
        return None

    def find_socials(self, soup: BeautifulSoup) -> Dict[str, str]:
        socials = {}
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if "twitter.com/" in href or "x.com/" in href:
                if "/status/" not in href and "intent/tweet" not in href:
                    socials["twitter"] = href
            elif "linkedin.com/company/" in href or "linkedin.com/in/" in href:
                socials["linkedin"] = href
        return socials

    async def inspect_page(self, client: httpx.AsyncClient, url: str) -> Tuple[Optional[int], Set[str], Optional[str], Dict[str, str]]:
        headers = {"User-Agent": USER_AGENTS[0], "Accept": "text/html"}
        try:
            resp = await client.get(url, headers=headers, timeout=REQUEST_TIMEOUT, follow_redirects=True)
            status_code = resp.status_code
            if status_code != 200:
                return status_code, set(), None, {}

            soup = BeautifulSoup(resp.text, "html.parser")
            emails = self.extract_emails(resp.text, soup)
            contact_url = self.find_contact_urls(url, soup)
            socials = self.find_socials(soup)
            return status_code, emails, contact_url, socials
        except Exception:
            return None, set(), None, {}

    async def crawl_target(self, client: httpx.AsyncClient, target: Dict) -> Dict:
        target_id = target["id"]
        url = target["url"]

        async with self.semaphore:
            status_code, emails, contact_url, socials = await self.inspect_page(client, url)

            # If no email found on target page and a contact page exists, inspect contact page
            if not emails and contact_url:
                _, c_emails, _, c_socials = await self.inspect_page(client, contact_url)
                emails.update(c_emails)
                socials.update(c_socials)

            # Format primary email
            primary_email = next(iter(emails)) if emails else None
            social_str = ", ".join([f"{k}: {v}" for k, v in socials.items()]) if socials else None

            return {
                "id": target_id,
                "status_code": status_code,
                "email": primary_email,
                "contact_url": contact_url,
                "social_links": social_str,
            }

    async def enrich_batch(self, targets: list) -> list:
        async with httpx.AsyncClient() as client:
            tasks = [self.crawl_target(client, t) for t in targets]
            return await asyncio.gather(*tasks)
