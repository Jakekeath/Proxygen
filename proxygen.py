import requests
import threading
import time
from queue import Queue
from rich.console import Console
from rich.panel import Panel

# --- Configuration ---
SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/Thordata/awesome-free-proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/Munachukwuw/Best-Free-Proxies/main/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt"
]

OUTPUT_FILE = "proxies.txt"
THREADS = 75     # High concurrency for public lists
TIMEOUT = 5      # FAST MODE: Ignores anything slower than 2 seconds
TEST_URL = "http://httpbin.org/ip"

console = Console()
file_lock = threading.Lock()
stats = {"found": 0, "scanned": 0}
stats_lock = threading.Lock()

def test_worker(q):
    while not q.empty():
        proxy = q.get()
        try:
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            start_time = time.time()
            r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
            latency = round((time.time() - start_time) * 1000)
            
            if r.status_code == 200:
                # 1. Output to CLI immediately
                console.print(f"[bold green][ALIVE][/bold green] {proxy:<22} | [cyan]{latency}ms[/cyan]")
                
                # 2. Instant Save + Flush
                with file_lock:
                    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                        f.write(f"{proxy}\n")
                        f.flush()
                
                with stats_lock:
                    stats["found"] += 1
        except:
            pass
        
        with stats_lock:
            stats["scanned"] += 1
        q.task_done()

def main():
    # Clear file
    with open(OUTPUT_FILE, "w") as f: f.write("")

    console.print(Panel("[bold cyan]HTTPS Proxy Scraper[/bold cyan]", expand=False))
    console.print(f"[*] Timeout: [bold yellow]{TIMEOUT}s[/bold yellow] | Threads: [bold yellow]{THREADS}[/bold yellow]")
    
    # 1. Scraping Sources
    raw_list = set()
    with console.status("[bold white]Fetching proxy lists..."):
        for url in SOURCES:
            try:
                res = requests.get(url, timeout=10)
                extracted = [p.strip() for p in res.text.splitlines() if ":" in p]
                raw_list.update(extracted)
            except:
                continue

    # 2. Setup Queue
    proxy_queue = Queue()
    for p in raw_list:
        proxy_queue.put(p)

    console.print(f"[*] Deduplicated [bold cyan]{len(raw_list)}[/bold cyan] total proxies.\n")

    # 3. Execution
    start_run = time.time()
    for _ in range(THREADS):
        t = threading.Thread(target=test_worker, args=(proxy_queue,), daemon=True)
        t.start()
    
    # Block until finished
    proxy_queue.join()
    
    duration = round(time.time() - start_run, 2)
    console.print("\n" + "━" * 45)
    console.print(f"[bold green]COMPLETE[/bold green]")
    console.print(f"• Found: [bold white]{stats['found']}[/bold white]")
    console.print(f"• Scanned: {stats['scanned']}")
    console.print(f"• Time: {duration}s")
    console.print(f"• Saved to: [bold underline]{OUTPUT_FILE}[/bold underline]")
    console.print("━" * 45)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Session Aborted.[/red]")