#!/usr/bin/env python3
"""
Link Insertion Discovery & Scraper Tool
Built for Content Strategy Portfolio Outreach (sadiulalam.com)
"""

import sys
import os
import argparse
import asyncio
import warnings

warnings.filterwarnings("ignore")
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm, IntPrompt

from scraper.config import DB_PATH, EXPORTS_DIR
from scraper.storage import Storage
from scraper.footprints import FOOTPRINT_PRESETS, DEFAULT_KEYWORDS
from scraper.serp_scraper import SerpScraper
from scraper.contact_crawler import ContactCrawler

console = Console()
storage = Storage()
serp_scraper = SerpScraper()
contact_crawler = ContactCrawler()

TARGET_MILESTONE = 10000

def display_header():
    stats = storage.get_stats()
    total = stats["total_targets"]
    pct = min(100.0, (total / TARGET_MILESTONE) * 100.0)

    header_text = f"""[bold cyan]Link Insertion Discovery Tool[/bold cyan] | [dim]sadiulalam.com[/dim]
[green]Target Milestone:[/] [bold white]{total:,}[/] / [bold white]{TARGET_MILESTONE:,}[/] websites ([bold yellow]{pct:.1f}%[/])
[green]With Outreach Email:[/] [bold white]{stats['with_email']:,}[/] | [green]With Contact Page:[/] [bold white]{stats['with_contact_page']:,}[/] | [green]Searches Executed:[/] [bold white]{stats['queries_run']:,}[/]"""
    console.print(Panel(header_text, border_style="cyan", expand=False))

async def run_scrape_footprint(keyword: str, preset_key: str, engine: str = "all", max_results_per_query: int = 25):
    preset = FOOTPRINT_PRESETS.get(preset_key)
    if not preset:
        console.print(f"[bold red]Unknown footprint preset:[/] {preset_key}")
        return

    footprints = preset["footprints"]
    console.print(f"\n[cyan]Starting campaign for keyword:[/] '[bold white]{keyword}[/]' using '[bold green]{preset['name']}[/]'")
    console.print(f"[dim]Running {len(footprints)} footprint variations across search engine(s)...[/dim]\n")

    total_added = 0
    total_duplicates = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Scraping footprints...", total=len(footprints))

        for fp in footprints:
            query = fp.format(keyword=keyword)
            progress.update(task, description=f"[cyan]Searching:[/] [dim]{query[:45]}...[/dim]")

            # Perform async SERP search
            results = await serp_scraper.search(query, engine=engine, max_results=max_results_per_query)

            # Associate metadata with items
            for item in results:
                item["keyword"] = keyword
                item["footprint"] = preset_key

            added, dupes = storage.batch_add_targets(results)
            storage.log_query(query, engine, len(results))

            total_added += added
            total_duplicates += dupes
            progress.advance(task)

    console.print(f"\n[bold green]✓ Footprint Search Complete![/]")
    console.print(f"  • [bold white]+{total_added}[/] newly discovered unique website domains added.")
    console.print(f"  • [dim]{total_duplicates} duplicate / already seen domains filtered out.[/dim]")
    
    current_total = storage.get_stats()["total_targets"]
    console.print(f"  • Current Database Total: [bold cyan]{current_total:,}[/] / [bold white]{TARGET_MILESTONE:,}[/] websites\n")

async def run_batch_campaign(keywords: List[str], preset_keys: List[str], engine: str = "all", max_results: int = 20):
    console.print(f"\n[bold magenta]🚀 Launching Multi-Keyword Batch Campaign[/]")
    console.print(f"Total Keywords: [bold white]{len(keywords)}[/] | Footprint Sets: [bold white]{len(preset_keys)}[/]\n")

    grand_added = 0
    grand_dupes = 0

    for i, kw in enumerate(keywords, 1):
        console.print(f"[bold yellow]Keyword [{i}/{len(keywords)}]:[/] [bold white]{kw}[/]")
        for pk in preset_keys:
            preset = FOOTPRINT_PRESETS.get(pk)
            if not preset:
                continue
            for fp in preset["footprints"]:
                query = fp.format(keyword=kw)
                results = await serp_scraper.search(query, engine=engine, max_results=max_results)
                for item in results:
                    item["keyword"] = kw
                    item["footprint"] = pk
                added, dupes = storage.batch_add_targets(results)
                storage.log_query(query, engine, len(results))
                grand_added += added
                grand_dupes += dupes

        stats = storage.get_stats()
        console.print(f"  → Added so far: [green]+{grand_added}[/] new unique domains (Total: {stats['total_targets']:,}/{TARGET_MILESTONE:,})")

    console.print(f"\n[bold green]✓ Batch Campaign Finished![/]")
    console.print(f"Total new websites saved: [bold cyan]{grand_added:,}[/]")

async def run_contact_enrichment(limit: int = 50):
    uninspected = storage.get_uninspected_targets(limit=limit)
    if not uninspected:
        console.print("[yellow]All discovered websites have already been inspected for contact information![/]")
        return

    console.print(f"\n[cyan]Inspecting [bold white]{len(uninspected)}[/] websites for editorial emails and contact forms...[/dim]")

    found_emails = 0
    found_contacts = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Crawling websites...", total=len(uninspected))

        # Enrich in batches of 10
        chunk_size = 10
        for i in range(0, len(uninspected), chunk_size):
            chunk = uninspected[i:i + chunk_size]
            results = await contact_crawler.enrich_batch(chunk)

            for r in results:
                storage.update_contact_info(
                    target_id=r["id"],
                    email=r["email"],
                    contact_url=r["contact_url"],
                    social_links=r["social_links"],
                    status_code=r["status_code"]
                )
                if r["email"]:
                    found_emails += 1
                if r["contact_url"]:
                    found_contacts += 1
                progress.advance(task)

    console.print(f"\n[bold green]✓ Enrichment Complete![/]")
    console.print(f"  • Contact Emails Uncovered: [bold green]+{found_emails}[/]")
    console.print(f"  • Contact/About Pages Identified: [bold green]+{found_contacts}[/]\n")

def show_detailed_stats():
    stats = storage.get_stats()
    total = stats["total_targets"]
    pct = min(100.0, (total / TARGET_MILESTONE) * 100.0)

    table = Table(title="Database & Campaign Insights", border_style="cyan")
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", style="bold white")

    table.add_row("Total Discovered Domains", f"{total:,} ({pct:.1f}% of {TARGET_MILESTONE:,} goal)")
    table.add_row("Websites Inspected for Contacts", f"{stats['checked_for_contacts']:,}")
    table.add_row("With Valid Outreach Email", f"{stats['with_email']:,}")
    table.add_row("With Contact / Guidelines URL", f"{stats['with_contact_page']:,}")
    table.add_row("Total SERP Footprints Logged", f"{stats['queries_run']:,}")

    console.print(table)

    if stats["top_keywords"]:
        kw_table = Table(title="Top Keywords Discovered", border_style="yellow")
        kw_table.add_column("Keyword", style="yellow")
        kw_table.add_column("Domains Count", style="bold white")
        for row in stats["top_keywords"]:
            kw_table.add_row(row["keyword"], str(row["count"]))
        console.print(kw_table)

    if stats["top_footprints"]:
        fp_table = Table(title="Top Footprint Strategies", border_style="green")
        fp_table.add_column("Footprint", style="green")
        fp_table.add_column("Domains Count", style="bold white")
        for row in stats["top_footprints"]:
            preset_name = FOOTPRINT_PRESETS.get(row["footprint"], {}).get("name", row["footprint"])
            fp_table.add_row(preset_name, str(row["count"]))
        console.print(fp_table)

def export_data():
    console.print("\n[bold cyan]Export Candidate Outreach List[/]")
    format_choice = Prompt.ask("Choose format", choices=["csv", "excel", "both"], default="both")

    if format_choice in ("csv", "both"):
        count, path = storage.export_to_csv()
        console.print(f"[bold green]✓ CSV Exported:[/] [white]{path}[/] ([bold white]{count:,}[/] rows)")

    if format_choice in ("excel", "both"):
        count, path = storage.export_to_excel()
        console.print(f"[bold green]✓ Excel (.xlsx) Exported:[/] [white]{path}[/] ([bold white]{count:,}[/] rows)")
    console.print("")

async def interactive_menu():
    while True:
        console.clear()
        display_header()
        console.print("\n[bold]Select an action:[/bold]")
        console.print("  [bold cyan]1[/] 🎯 Scrape Search Footprints (Single Keyword / Custom Preset)")
        console.print("  [bold cyan]2[/] ⚡ Run Multi-Keyword Batch Campaign (Scale toward 10k)")
        console.print("  [bold cyan]3[/] 📧 Deep Contact & Editorial Email Finder")
        console.print("  [bold cyan]4[/] 📊 View Target Database Stats & Insights")
        console.print("  [bold cyan]5[/] 📁 Export Outreach List (CSV / Excel)")
        console.print("  [bold cyan]6[/] ❌ Exit")

        choice = Prompt.ask("\nEnter choice", choices=["1", "2", "3", "4", "5", "6"], default="1")

        if choice == "1":
            kw = Prompt.ask("\nEnter target keyword (e.g. 'content strategy', 'SEO', 'B2B SaaS')", default="content strategy")
            console.print("\nSelect footprint preset:")
            presets = list(FOOTPRINT_PRESETS.keys())
            for idx, pkey in enumerate(presets, 1):
                pdata = FOOTPRINT_PRESETS[pkey]
                console.print(f"  [cyan]{idx}[/] [bold]{pdata['name']}[/] - [dim]{pdata['description']}[/dim]")
            preset_idx = IntPrompt.ask("Choose preset", default=1)
            selected_preset = presets[max(0, min(len(presets)-1, preset_idx - 1))]

            engine = Prompt.ask("Search Engine", choices=["duckduckgo", "bing", "all"], default="all")
            max_results = IntPrompt.ask("Max results per query", default=25)

            await run_scrape_footprint(kw, selected_preset, engine=engine, max_results_per_query=max_results)
            Prompt.ask("\nPress [bold]Enter[/bold] to return to menu...")

        elif choice == "2":
            console.print("\n[bold yellow]Default keywords available:[/] " + ", ".join(DEFAULT_KEYWORDS[:5]) + "...")
            kw_mode = Prompt.ask("Use default content strategy keywords or enter custom?", choices=["default", "custom"], default="default")
            if kw_mode == "default":
                kws = DEFAULT_KEYWORDS
            else:
                raw_kws = Prompt.ask("Enter comma-separated keywords")
                kws = [k.strip() for k in raw_kws.split(",") if k.strip()]

            engine = Prompt.ask("Search Engine", choices=["duckduckgo", "bing", "all"], default="all")
            await run_batch_campaign(kws, list(FOOTPRINT_PRESETS.keys()), engine=engine)
            Prompt.ask("\nPress [bold]Enter[/bold] to return to menu...")

        elif choice == "3":
            uninspected_count = len(storage.get_uninspected_targets(limit=1000))
            if uninspected_count == 0:
                console.print("\n[yellow]No uninspected domains found. Run scraping first![/]")
            else:
                limit = IntPrompt.ask(f"\nHow many websites to inspect? (Available: {uninspected_count})", default=min(50, uninspected_count))
                await run_contact_enrichment(limit=limit)
            Prompt.ask("\nPress [bold]Enter[/bold] to return to menu...")

        elif choice == "4":
            console.print("")
            show_detailed_stats()
            Prompt.ask("\nPress [bold]Enter[/bold] to return to menu...")

        elif choice == "5":
            export_data()
            Prompt.ask("\nPress [bold]Enter[/bold] to return to menu...")

        elif choice == "6":
            console.print("[green]Goodbye! Happy outreach for sadiulalam.com![/]\n")
            break

def main():
    parser = argparse.ArgumentParser(description="Link Insertion Scraper Tool for sadiulalam.com")
    subparsers = parser.add_subparsers(dest="command")

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape links for a specific keyword and footprint")
    scrape_parser.add_argument("--keyword", "-k", type=str, required=True, help="Target keyword")
    scrape_parser.add_argument("--preset", "-p", type=str, default="link_insertion_resources", choices=list(FOOTPRINT_PRESETS.keys()), help="Footprint preset")
    scrape_parser.add_argument("--engine", "-e", type=str, default="all", choices=["duckduckgo", "bing", "all"], help="Search engine")
    scrape_parser.add_argument("--max-results", "-m", type=int, default=25, help="Max results per footprint query")

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Run batch campaign over keywords")
    batch_parser.add_argument("--keywords", "-k", type=str, help="Comma-separated list of keywords")
    batch_parser.add_argument("--file", "-f", type=str, help="Path to text file containing keywords (one per line)")
    batch_parser.add_argument("--engine", "-e", type=str, default="all", choices=["duckduckgo", "bing", "all"])

    # Enrich command
    enrich_parser = subparsers.add_parser("enrich", help="Enrich discovered websites with contact emails and links")
    enrich_parser.add_argument("--limit", "-l", type=int, default=50, help="Number of sites to inspect")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export targets to CSV or Excel")
    export_parser.add_argument("--format", type=str, default="both", choices=["csv", "excel", "both"])

    # Stats command
    subparsers.add_parser("stats", help="View current progress and database statistics")

    args = parser.parse_args()

    if not args.command:
        # Interactive mode by default
        try:
            asyncio.run(interactive_menu())
        except KeyboardInterrupt:
            console.print("\n[yellow]Session interrupted. Progress saved in database.[/]")
    elif args.command == "scrape":
        asyncio.run(run_scrape_footprint(args.keyword, args.preset, engine=args.engine, max_results_per_query=args.max_results))
    elif args.command == "batch":
        kws = []
        if args.file and os.path.exists(args.file):
            with open(args.file, "r") as f:
                kws = [line.strip() for line in f if line.strip()]
        elif args.keywords:
            kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        else:
            kws = DEFAULT_KEYWORDS
        asyncio.run(run_batch_campaign(kws, list(FOOTPRINT_PRESETS.keys()), engine=args.engine))
    elif args.command == "enrich":
        asyncio.run(run_contact_enrichment(limit=args.limit))
    elif args.command == "export":
        if args.format in ("csv", "both"):
            count, path = storage.export_to_csv()
            console.print(f"[bold green]✓ CSV Exported:[/] [white]{path}[/] ([bold white]{count:,}[/] rows)")
        if args.format in ("excel", "both"):
            count, path = storage.export_to_excel()
            console.print(f"[bold green]✓ Excel (.xlsx) Exported:[/] [white]{path}[/] ([bold white]{count:,}[/] rows)")
    elif args.command == "stats":
        show_detailed_stats()

if __name__ == "__main__":
    main()
