#!/usr/bin/env python3
#By r0otk3r

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

import requests
import random
import argparse
import os
import sys
import time
import json
import threading
from urllib.parse import unquote
from queue import Queue

def load_patterns(json_file):
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load {json_file}: {e}")
        sys.exit(1)

def get_user_agent():
    chrome_versions = [str(v) for v in range(90, 125)]
    firefox_versions = [str(v) for v in range(80, 120)]

    chrome = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)}.0.0.0 Safari/537.36"
    firefox = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{random.choice(firefox_versions)}.0) Gecko/20100101 Firefox/{random.choice(firefox_versions)}.0"

    return random.choice([chrome, firefox])

def connector(url, timeout, retries, delay):
    headers = {'User-Agent': get_user_agent()}

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[!] {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(delay)
    return None

def extract_params(urls, level, blacklist, placeholder):
    found = set()

    for url in urls:
        if '?' not in url or '=' not in url:
            continue

        if any(ext in url for ext in blacklist):
            continue

        param_pairs = url.split('?')[1].split('&')
        for param in param_pairs:
            if '=' in param:
                key = param.split('=')[0]
                base = url.split('?')[0]
                found.add(f"{base}?{key}={placeholder}")
                if level == 'high':
                    found.add(f"{base}?{key}={placeholder}&FUZZ={placeholder}")

    return list(found)

def filter_by_category(params, patterns):
    matched = []
    for param in params:
        for p in patterns:
            if p in param:
                matched.append(param)
                break
    return matched

def save_output(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(line + '\n')

def scan_domain(domain, args, param_patterns):
    print(f"[+] Scanning {domain}")

    url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey"

    response = connector(url, args.timeout, args.retries, args.delay)
    if not response:
        print(f"[!] Failed to retrieve data for {domain}")
        return

    urls = list(set(unquote(response).splitlines()))

    blacklist = []
    if args.exclude:
        blacklist = [f".{ext.strip()}" for ext in args.exclude.split(",")]

    params = extract_params(urls, args.level, blacklist, args.placeholder)

    output_dir = args.output or "output"
    base_filename = f"{output_dir}/{domain}"

    if args.all:
        save_output(urls, f"{base_filename}_all_urls.txt")

    if not params:
        print(f"[!] No parameters found for {domain}")
        return

    save_output(params, f"{base_filename}_params.txt")

    for category, data in param_patterns.items():
        if args.category and category not in args.category:
            continue

        cat_patterns = data.get('patterns', [])
        cat_params = filter_by_category(params, cat_patterns)
        if cat_params:
            save_output(cat_params, f"{base_filename}_{category}_params.txt")
            if not args.quiet:
                print(f"[+] {category.title()} params saved to {base_filename}_{category}_params.txt")

    if not args.quiet:
        print(f"[+] {domain} - Params found: {len(params)}")

def worker(queue, args, param_patterns):
    while not queue.empty():
        domain = queue.get()
        try:
            scan_domain(domain, args, param_patterns)
        except Exception as e:
            print(f"[!] Error scanning {domain}: {e}")
        queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="Wayback Parameter Finder")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domain", help="Single target domain (e.g., example.com)")
    group.add_argument("-L", "--list", help="File with list of domains (one per line)")

    parser.add_argument("-l", "--level", choices=["low", "high"], default="low", help="Parameter discovery depth")
    parser.add_argument("-e", "--exclude", help="Extensions to exclude (comma-separated)")
    parser.add_argument("--all", action="store_true", help="Save all found URLs to file")
    parser.add_argument("-p", "--placeholder", default="FUZZ", help="Placeholder for parameter values")
    parser.add_argument("-q", "--quiet", action="store_true", help="Do not print results on screen")
    parser.add_argument("-j", "--json", default="data/param_patterns.json", help="JSON pattern file")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--timeout", type=int, default=15, help="Request timeout (default: 15)")
    parser.add_argument("--delay", type=int, default=2, help="Delay between retries (default: 2)")
    parser.add_argument("--retries", type=int, default=3, help="Retry attempts (default: 3)")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads (default: 5)")
    parser.add_argument("--category", nargs='*', help="Specific category to filter (e.g., xss sql wordpress)")

    args = parser.parse_args()
    start = time.time()

    param_patterns = load_patterns(args.json)

    domains = []
    if args.domain:
        domains.append(args.domain)
    elif args.list:
        with open(args.list, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]

    queue = Queue()
    for domain in domains:
        queue.put(domain)

    threads = []
    for _ in range(min(args.threads, len(domains))):
        t = threading.Thread(target=worker, args=(queue, args, param_patterns))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"[!] Total execution time: {round(time.time() - start, 2)} seconds")

if __name__ == "__main__":
    main()
