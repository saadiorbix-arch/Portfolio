# Link Insertion Scraper & Discovery Tool
**Built for sadiulalam.com (Content Strategy Outreach)**

A high-performance, asynchronous search engine footprint scraper and deep contact finder engineered to find and curate a pipeline of **10,000+ candidate websites** for **link insertions**, **resource page inclusions**, and **guest contributor outreach**.

---

## 🌟 Key Features

1. **Link Insertion & Outreach Footprint Presets**:
   - **Resource Pages**: `inurl:resources "{keyword}"`, `"useful resources"`, `"suggest a resource"`, etc.
   - **Guest Posts & Contributor**: `"write for us"`, `"guest post guidelines"`, `inurl:write-for-us`, etc.
   - **Roundups & Curations**: `"weekly roundup"`, `"best articles of the week"`, etc.
   - **Niche Editorial Blogs**: `inurl:blog "{keyword}" guide`, etc.

2. **Domain Deduplication & Noise Filtering**:
   - Extracts registered root domains (`example.com`) to prevent duplicate URLs from the same host.
   - Automatically excludes non-target domains (Google, YouTube, Twitter/X, LinkedIn, Facebook, Wikipedia, GitHub, Reddit, Medium, etc.).

3. **Multi-Engine SERP Scraper**:
   - DuckDuckGo & Bing search engines with user-agent rotation and anti-block request delays.
   - Decodes redirect wrappers and cleans tracking parameters (`utm_*`, `fbclid`).

4. **Deep Contact & Editorial Intelligence**:
   - Discovers author / editorial contact email addresses.
   - Detects `/contact`, `/about`, and `/write-for-us` page links.
   - Extracts Twitter/X and LinkedIn profile links.

5. **SQLite Persistence & Dual Export**:
   - Incremental progress stored in `data/links.db`. Never lose work if paused or restarted.
   - Real-time progress bar tracking against the **10,000 website milestone**.
   - One-click export to **CSV** and **Excel (.xlsx)** ready for Pitchbox, BuzzStream, Lemlist, Hunter, or Google Sheets.

---

## 🚀 Quick Start

### 1. Run the Interactive CLI Menu
```bash
.venv/bin/python main.py
```
This opens an interactive dashboard where you can:
- Scrape footprints interactively
- Launch batch campaigns
- Enrich websites with emails & contact forms
- View real-time database stats
- Export your lists to CSV or Excel

### 2. Command Line (Headless / Scripting)

#### Scrape a specific keyword:
```bash
.venv/bin/python main.py scrape --keyword "content strategy" --preset link_insertion_resources --max-results 30
```

#### Run a multi-keyword batch campaign:
```bash
.venv/bin/python main.py batch --keywords "content strategy,SEO audit,copywriting,B2B marketing"
```

#### Enrich discovered websites with emails & contact links:
```bash
.venv/bin/python main.py enrich --limit 100
```

#### View database statistics & progress towards 10,000 websites:
```bash
.venv/bin/python main.py stats
```

#### Export your gathered targets:
```bash
.venv/bin/python main.py export --format both
```
Files will be saved in `data/exports/`.

---

## 📁 Project Structure

```
.
├── main.py                    # Main interactive and CLI entry point
├── scraper/
│   ├── __init__.py
│   ├── config.py              # Configuration, user agents, domain filters
│   ├── footprints.py          # Footprint search presets and keyword lists
│   ├── serp_scraper.py        # Asynchronous multi-engine SERP parser
│   ├── contact_crawler.py     # Deep email, contact page & social scraper
│   └── storage.py             # SQLite database and CSV/Excel export layer
├── data/
│   ├── links.db               # SQLite persistent database
│   └── exports/               # Exported CSV / Excel files
├── requirements.txt           # Python dependencies
└── README.md
```
