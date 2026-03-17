# CENTCOM Press Release Crawler

A web crawler built with [Crawlee](https://crawlee.dev/python/) that scrapes all press releases from the [U.S. Central Command (CENTCOM)](https://www.centcom.mil/MEDIA/PRESS-RELEASES/) public website.

For each press release, it extracts:
- Pagination page number
- Publication date
- URL
- Full article body text

## How it works

The crawler uses two handlers:

1. **Listing handler** — visits each paginated press release listing page, extracts the date and URL of each release, and enqueues them for detail crawling. Also enqueues the next pagination pages.
2. **Detail handler** — visits each individual press release page and extracts the full article body text.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Setup

**Clone the repo:**
```bash
git clone <repo-url>
cd test-crawlee
```

**Install dependencies using uv:**
```bash
uv sync
```

**Install Playwright browser binaries:**
```bash
uv run playwright install chromium
```

> Note: If you are on a non-standard Linux distro (e.g. Oracle Linux, CentOS), system browser dependencies may need to be installed manually. Run `uv run playwright install-deps` or install the equivalent packages via your package manager.

## Running

```bash
uv run main.py
```

Output is logged to the terminal in the format:
```
Page {n} | {date} | {url} | {content}
```

## Configuration

In `main.py`, you can adjust the following in the `PlaywrightCrawler` constructor:

| Option | Description |
|---|---|
| `max_requests_per_crawl` | Limit total requests (comment out for full crawl of all 256 pages) |
| `headless` | Set to `False` to watch the browser in action |
| `request_handler_timeout` | Timeout per page request |
| `concurrency_settings` | Use `ConcurrencySettings(min_concurrency=1, max_concurrency=1)` to slow down crawling and avoid 403 rate limiting |

## Notes

- The CENTCOM site has ~256 pages of press releases (2,500+ releases)
- The site may return 403 errors if crawled too aggressively — use `ConcurrencySettings` to limit concurrency
- Crawlee stores the request queue and crawl stats in `./storage/` by default (gitignored)
