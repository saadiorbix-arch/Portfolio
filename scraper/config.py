"""
Configuration settings, footprints, and domain filtering rules.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "links.db"
EXPORTS_DIR = DATA_DIR / "exports"

DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# User-Agent rotation pool
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/125.0.0.0",
]

# Domains to ignore (Social networks, search engines, app stores, file hosts, big aggregators)
EXCLUDED_DOMAINS = {
    # Search engines & big tech
    "google.com", "google.co.uk", "google.ca", "google.com.au", "bing.com",
    "yahoo.com", "duckduckgo.com", "baidu.com", "yandex.com", "ask.com",
    "microsoft.com", "apple.com", "amazon.com", "aws.amazon.com",
    
    # Social media & community platforms
    "facebook.com", "twitter.com", "x.com", "linkedin.com", "instagram.com",
    "pinterest.com", "tiktok.com", "reddit.com", "quora.com", "youtube.com",
    "vimeo.com", "tumblr.com", "discord.com", "slack.com", "telegram.org",
    
    # Code & open source repositories
    "github.com", "gitlab.com", "bitbucket.org", "sourceforge.net", "npm.im",
    "npmjs.com", "pypi.org", "stackoverflow.com", "stackexchange.com",
    
    # Generic platforms, wikis & directories
    "wikipedia.org", "wikimedia.org", "w3.org", "archive.org",
    "medium.com", "substack.com", "wordpress.com", "blogspot.com", "wix.com",
    "weebly.com", "squarespace.com", "github.io",
    
    # Ad networks / CDNs / analytics
    "cloudflare.com", "doubleclick.net", "googletagmanager.com",
}

# Request settings
REQUEST_TIMEOUT = 12.0
DEFAULT_DELAY = 1.5  # Seconds between search engine requests
CONCURRENT_CONTACT_CRAWLS = 10
