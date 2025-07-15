# Wayback Parameter Finder

Wayback Parameter Finder is a fast and flexible tool for discovering URL parameters from the Wayback Machine (archive.org).
It helps bug bounty hunters, penetration testers, and web security researchers uncover hidden or forgotten endpoints and parameters that could be vulnerable to various attacks like XSS, SQLi, SSRF, LFI, RCE, etc.

---

## Features

-    Single Domain or Bulk Scanning

-    Multi-threaded for Speed

-    Smart Parameter Extraction (Low/High depth)

-    Category Filtering (XSS, SQLi, SSRF, Redirects, RCE, Upload, etc.)

-    Custom JSON Patterns (easily extendable)

-    Extension Blacklisting (e.g., .jpg, .png, .css)

-    User-Agent Rotation (Chrome/Firefox randomization)

-    Retries, Timeout, and Delay Handling

-    Output in Structured Files (All URLs, Params, Categories)

---

## Directory Structure
```bash
wayback-parameter-finder/
├── param_finder.py                # Main tool
├── data/
│   └── param_patterns.json        # Parameter category definitions
├── output/                        # Output results (auto-created)
└── README.md                      # Documentation
```

---

## usage

### Basic Commands 

#### Single Domain Scan
``` bash 
python3 param_finder.py -d example.com
```
#### Bulk Domain Scan
```bash
python3 param_finder.py -L domains.txt
```

## Advanced Options

| Option                | Description                                             |
| --------------------- | ------------------------------------------------------- |
| `-d`, `--domain`      | Target domain (e.g., example.com)                       |
| `-L`, `--list`        | File with list of domains                               |
| `-l`, `--level`       | Parameter discovery level: `low` or `high`              |
| `-e`, `--exclude`     | Exclude extensions (e.g., `jpg,png,css`)                |
| `--all`               | Save all discovered URLs to file                        |
| `-p`, `--placeholder` | Placeholder for parameters (default: FUZZ)              |
| `-j`, `--json`        | JSON pattern file (default: `data/param_patterns.json`) |
| `--output`            | Output directory (default: `output`)                    |
| `--timeout`           | Timeout per request (default: 15 sec)                   |
| `--delay`             | Delay between retries (default: 2 sec)                  |
| `--retries`           | Number of retries (default: 3)                          |
| `--threads`           | Number of threads (default: 5)                          |
| `--category`          | Filter specific categories (e.g., `xss sql rce`)        |
| `-q`, `--quiet`       | Disable console output                                  |

----

## Example Commands

#### Scan single domain with high discovery level:
```bash
python3 param_finder.py -d example.com -l high --all
```
#### Bulk scan with category filter:
```bash
python3 param_finder.py -L domains.txt --category xss sql redirect
```
#### Exclude image extensions:
```bash
python3 param_finder.py -d example.com -e jpg,png,gif
```
## Categories in param_patterns.json


| Category     | Purpose                      |
| ------------ | ---------------------------- |
| `xss`        | Cross-site scripting vectors |
| `sql`        | SQL Injection params         |
| `ssrf`       | SSRF parameters              |
| `rce`        | Remote command execution     |
| `upload`     | File uploads                 |
| `auth`       | Tokens / authentication      |
| `lfi_rfi`    | Local/Remote file inclusion  |
| `csrf`       | CSRF tokens                  |
| `redirect`   | Open redirects               |
| `wordpress`  | WordPress specific paths     |
| `drupal`     | Drupal specific parameters   |
| `joomla`     | Joomla parameters            |
| `cms`        | General CMS structures       |
| `crypto`     | Cryptographic params         |
| `debug`      | Debugging/test endpoints     |
| `email`      | Email fields                 |
| `pagination` | Pagination params            |
| `filter`     | Filtering/search             |

---

## Output Structure

Results are saved under output/ directory:
```bash
output/
├── example.com_all_urls.txt         # All collected URLs
├── example.com_params.txt           # Extracted parameters
├── example.com_xss_params.txt       # Category filtered parameters (XSS)
├── example.com_sql_params.txt       # Category filtered parameters (SQL)
...
```

## Use Cases

-    Bug Bounty Reconnaissance

-    Pentesting Automation

-    Vulnerability Hunting

-    CMS Enumeration

-    Forgotten Endpoint Discovery

## Disclaimer

This tool is for educational and authorized security testing only.
Do NOT use it against systems without permission.

---

## Official Channels

- [YouTube @rootctf](https://www.youtube.com/@rootctf)
- [X @r0otk3r](https://x.com/r0otk3r)
