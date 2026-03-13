# ⚡ High-Speed HTTP Proxy Scraper & Checker

A lightweight, multi-threaded Python tool designed to scrape public HTTP proxies from reliable sources and validate them in real-time.

## 🚀 Features
* **Multi-threaded Validation:** Uses Python's `threading` and `Queue` for high-concurrency testing.
* **Auto-Deduplication:** Automatically removes duplicate proxies from various sources.
* **Real-time Output:** Beautiful CLI interface powered by the `Rich` library.
* **Instant Saving:** Valid proxies are saved immediately to `proxies.txt` with thread-safe file handling.
* **Performance Focused:** Configured with a fast timeout to filter for the most responsive proxies.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/proxy-scraper.git](https://github.com/yourusername/proxy-scraper.git)
   cd proxy-scraper
