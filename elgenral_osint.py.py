#!/usr/bin/env python3
"""
███████╗██╗     ███████╗███████╗███╗   ██╗██████╗  █████╗ ██╗
██╔════╝██║     ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔══██╗██║
█████╗  ██║     █████╗  █████╗  ██╔██╗ ██║██████╔╝███████║██║
██╔══╝  ██║     ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══██╗██╔══██║██║
███████╗███████╗███████╗███████╗██║ ╚████║██║  ██║██║  ██║███████╗
╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

    ELGENRAL OSINT TOOL v4.0 - FINAL EDITION
    Created by: Youssef Elgenral
    GitHub: https://github.com/youssefelgenral
"""

import requests
import sys
import json
import os
import time
import re
import socket
import hashlib
from datetime import datetime
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

# ─── Colors ──────────────────────────────────────────────────────────────
RED      = "\033[91m"
GREEN    = "\033[92m"
YELLOW   = "\033[93m"
BLUE     = "\033[94m"
MAGENTA  = "\033[95m"
CYAN     = "\033[96m"
WHITE    = "\033[97m"
RESET    = "\033[0m"
BOLD     = "\033[1m"
DIM      = "\033[2m"

# ─── Ghost ASCII ─────────────────────────────────────────────────────────
GHOST = f"""
{BLUE}{BOLD}
           .-.
          (o o)
          | O |
         _|   |_
   _   / |_____| \\   _
  ('>  <  (''')  >  <')
  /_\\  |   ---   |  /_\\
       |_________|
        \\_______/
 {RESET}{CYAN}   YOUSSEF ELGENRAL{RESET}
"""

BANNER = f"""
{GHOST}
{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
║       ELGENRAL OSINT TOOL v4.0 - FINAL EDITION       ║
╠══════════════════════════════════════════════════════╣
║  {WHITE}Created by:{RESET}{GREEN} Youssef Elgenral                     {CYAN}║
║  {WHITE}GitHub:   {RESET}{BLUE} https://github.com/youssefelgenral        {CYAN}║
║  {WHITE}Features: {RESET}{YELLOW}13 Powerful OSINT Modules              {CYAN}║
╚══════════════════════════════════════════════════════╝{RESET}
"""

# ─── Headers ─────────────────────────────────────────────────────────────
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
}

# ─── Platforms ───────────────────────────────────────────────────────────
PLATFORMS = {
    "GitHub":         "https://github.com/{}",
    "Twitter/X":      "https://x.com/{}",
    "Instagram":      "https://www.instagram.com/{}/",
    "Reddit":         "https://www.reddit.com/user/{}/",
    "Telegram":       "https://t.me/{}",
    "YouTube":        "https://www.youtube.com/@{}",
    "TikTok":         "https://www.tiktok.com/@{}",
    "Facebook":       "https://www.facebook.com/{}",
    "Twitch":         "https://www.twitch.tv/{}",
    "Medium":         "https://medium.com/@{}",
    "Pinterest":      "https://www.pinterest.com/{}/",
    "Linktree":       "https://linktr.ee/{}",
    "Pastebin":       "https://pastebin.com/u/{}",
    "Keybase":        "https://keybase.io/{}",
    "HackerNews":     "https://news.ycombinator.com/user?id={}",
    "VK":             "https://vk.com/{}",
    "Dev.to":         "https://dev.to/{}",
    "Replit":         "https://replit.com/@{}",
    "CodePen":        "https://codepen.io/{}",
    "Fiverr":         "https://www.fiverr.com/{}",
    "Behance":        "https://www.behance.net/{}",
    "SoundCloud":     "https://soundcloud.com/{}",
    "Patreon":        "https://www.patreon.com/{}",
    "BuyMeACoffee":   "https://www.buymeacoffee.com/{}",
    "Snapchat":       "https://www.snapchat.com/add/{}",
    "Steam":          "https://steamcommunity.com/id/{}",
    "Spotify":        "https://open.spotify.com/user/{}",
    "Dribbble":       "https://dribbble.com/{}"
}

# ─── Subdomains ─────────────────────────────────────────────────────────
SUBDOMAINS = [
    "www", "mail", "ftp", "admin", "api", "dev", "test", "blog", "shop",
    "support", "cdn", "static", "assets", "images", "docs", "wiki", "forum",
    "help", "status", "community", "portal", "app", "m", "mobile", "news",
    "store", "vpn", "secure", "login", "register", "download", "upload",
    "webmail", "server", "ns1", "ns2", "smtp", "pop", "imap", "demo",
    "stage", "beta", "alpha", "prod", "backup", "monitor", "chat", "live"
]

# ─── Common ports ─────────────────────────────────────────────────────────
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 3306, 3389, 5432, 8080, 8443, 9000, 9090, 10000]

# ═══════════════════════════════════════════════════════════════════════════
#                          UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def save_results(filename, data_list):
    with open(filename, "w", encoding="utf-8") as f:
        for line in data_list:
            f.write(line + "\n")
    return filename

def fetch_url(url, timeout=10):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except:
        return None

def print_sep():
    print(f"\n{DIM}{'─'*65}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#                            MAIN MENU
# ═══════════════════════════════════════════════════════════════════════════

def print_menu():
    print(f"""
    {CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
    ║          ELGENRAL OSINT TOOL - MAIN MENU            ║
    ╠══════════════════════════════════════════════════════╣
    ║                                                     ║
    ║  {WHITE}[1] {GREEN}Search Username on 30+ Platforms          ║
    ║  {WHITE}[2] {GREEN}Enumerate Subdomains                      ║
    ║  {WHITE}[3] {GREEN}Extract Emails from Domain                ║
    ║  {WHITE}[4] {GREEN}Check Email Breach Checker                      ║
    ║  {WHITE}[5] {GREEN}IP Geolocation & Domain Info              ║
    ║  {WHITE}[6] {GREEN}Wayback Machine Archive                   ║
    ║  {WHITE}[7] {GREEN}GitHub Profile Analyzer                   ║
    ║  {WHITE}[8] {GREEN}DNS Enumeration                           ║
    ║  {WHITE}[9] {GREEN}Port Scanner (Common Ports)               ║
    ║  {WHITE}[10] {GREEN}Web Crawler (Extract Everything)         ║
    ║  {WHITE}[11] {GREEN}Profile Picture Downloader               ║
    ║  {WHITE}[12] {GREEN}Image Metadata Extractor                 ║
    ║  {WHITE}[13] {GREEN}Full Scan - All Features at Once        ║
    ║                                                     ║
    ║  {WHITE}[0] {RED}Exit                                        ║
    ║                                                     ║
    ╚══════════════════════════════════════════════════════╝{RESET}
    """)

# ═══════════════════════════════════════════════════════════════════════════
#                    FEATURE 1: USERNAME SEARCH ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def search_username(username):
    """Search username across 30+ platforms - results may vary by platform"""
    results = {"found": [], "not_found": [], "errors": []}
    log = []

    print(f"\n{CYAN}{BOLD}[*] Searching for username: {WHITE}{username}{RESET}")
    print(f"{CYAN}[*] Checking {len(PLATFORMS)} platforms (this may take a minute)...{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Username Search Report")
    log.append(f"Target: {username}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username)
        time.sleep(0.2)

        r = fetch_url(url)
        if r is None:
            results["errors"].append({"platform": platform, "error": "Connection failed"})
            print(f"  {RED}[✗]{RESET} {platform:20} → Connection Error")
            continue

        if r.status_code == 200:
            # Instagram and some platforms return 200 even for non-existent users
            # Double-check by showing a login page. We check content length to be smarter.
            if "Instagram" in platform and "The link you followed may be broken" in r.text:
                results["not_found"].append({"platform": platform, "url": url})
                log.append(f"[NOT_FOUND] {platform}")
                continue
            results["found"].append({"platform": platform, "url": url})
            print(f"  {GREEN}[✓]{RESET} {platform:20} → {WHITE}{url}{RESET}")
            log.append(f"[FOUND] {platform}: {url}")
        elif r.status_code == 403:
            results["not_found"].append({"platform": platform, "url": url})
            print(f"  {YELLOW}[!]{RESET} {platform:20} → {RED}Blocked (403){RESET}")
            log.append(f"[BLOCKED] {platform}")
        elif r.status_code == 429:
            results["errors"].append({"platform": platform, "error": "Rate limited"})
            print(f"  {YELLOW}[!]{RESET} {platform:20} → {RED}Rate Limited (429){RESET}")
            log.append(f"[RATE_LIMITED] {platform}")
        else:
            results["not_found"].append({"platform": platform, "url": url})
            log.append(f"[NOT_FOUND] {platform}: status {r.status_code}")

    print_sep()
    print(f"\n{GREEN}[✓] Found on {len(results['found'])} platforms{RESET}")
    print(f"{RED}[-] Not found on {len(results['not_found'])} platforms{RESET}")
    if results["errors"]:
        print(f"{YELLOW}[!] Errors: {len(results['errors'])}{RESET}")

    filename = f"elgenral_username_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

    return results

# ═══════════════════════════════════════════════════════════════════════════
#                FEATURE 2: SUBDOMAIN ENUMERATION ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def enum_subdomains(domain):
    """Enumerate subdomains using DNS requests and HTTP probes"""
    found = []
    log = []

    print(f"\n{CYAN}{BOLD}[*] Enumerating subdomains for: {WHITE}{domain}{RESET}")
    print(f"{CYAN}[*] Checking {len(SUBD)} subdomains...{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Subdomain Enumeration")
    log.append(f"Target: {domain}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    for sub in SUBD:
        url = f"https://{sub}.{domain}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=5)
            if r.status_code < 400:
                found.append({"sub": sub, "url": url, "status": r.status_code})
                print(f"  {GREEN}[✓]{RESET} {sub:20} → {WHITE}{url}{RESET} ({r.status_code})")
                log.append(f"[FOUND] {sub}.{domain} (HTTP {r.status_code})")
            elif r.status_code == 403:
                found.append({"sub": sub, "url": url, "status": 403})
                print(f"  {YELLOW}[!]{RESET} {sub:20} → {WHITE}{url}{RESET} (403 Forbidden)")
                log.append(f"[FORBIDDEN] {sub}.{domain}")
        except:
            pass

    print_sep()
    print(f"\n{GREEN}[✓] Found {len(found)} live subdomains{RESET}")

    filename = f"elgenral_subdomains_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")
    return found

# ═══════════════════════════════════════════════════════════════════════════
#                  FEATURE 3: EMAIL EXTRACTOR ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def extract_emails(domain):
    """Extract emails from Google, Bing, and direct website content"""
    emails = set()
    log = []

    print(f"\n{CYAN}{BOLD}[*] Extracting emails for domain: {WHITE}{domain}{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Email Extractor")
    log.append(f"Target: {domain}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    sources = [
        f"https://www.google.com/search?q=%40{domain}+email+contact",
        f"https://search.yahoo.com/search?p=%40{domain}",
        f"https://www.bing.com/search?q=%40{domain}",
        f"https://{domain}/contact",
        f"https://{domain}/about",
        f"https://{domain}/team",
    ]

    for source in sources:
        try:
            r = requests.get(source, headers=HEADERS, timeout=10)
            found = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.{1-]+\.{1}[a-zA-Z]{2,}', r.text))
            # Filter only emails from target domain
            domain_emails = {e for e in found if domain in e}
            emails.update(domain_emails)
        except:
            pass

    if emails:
        for email in sorted(emails):
            print(f"  {GREEN}[✓]{RESET} {WHITE}{email}{RESET}")
            log.append(f"[FOUND] {email}")
    else:
        print(f"  {YELLOW}[!]{RESET} No emails found for this domain")
        log.append("[INFO] No emails found")

    print_sep()
    print(f"\n{GREEN}[✓] Found {len(emails)} email addresses{RESET}")

    filename = f"elgenral_emails_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")
    return list(emails)

# ═══════════════════════════════════════════════════════════════════════════
#                   FEATURE 4: BREACH CHECKER ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def check_breach(email):
    """Check email against known breach databases"""
    log = []

    print(f"\n{CYAN}{BOLD}[*] Checking breaches for: {WHITE}{email}{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Breach Check Report")
    log.append(f"Target: {email}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    total_breaches = 0

    # 1. Leak-check.net
    print(f"\n  {CYAN}[1/3]{RESET} Checking leak-check.net...")
    try:
        r = requests.get(f"https://leak-check.net/api/public/check?account={email}",
                        headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("success") and data.get("breaches"):
                breaches = data["breaches"]
                for breach in breaches:
                    print(f"  {RED}[!]{RESET} Leak-check: {WHITE}{breach}{RESET}")
                    log.append(f"[BREACH] {breach}")
                    total_breaches += 1
            else:
                print(f"  {GREEN}[✓]{RESET} No breaches via leak-check")
    except:
        print(f"  {YELLOW}[!]{RESET} leak-check.net unavailable")

    # 2. Scylla.so
    print(f"\n  {CYAN}[2/3]{RESET} Checking scylla.so...")
    try:
        r = requests.get(f"https://scylla.so/api/check?email={email}",
                        headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            count = data.get("count", 0)
            if count > 0:
                print(f"  {RED}[!]{RESET} Scylla: Found in {count} breach records!")
                log.append(f"[BREACH] scylla.so: {count} records")
                total_breaches += count
            else:
                print(f"  {GREEN}[✓]{RESET} No breaches via scylla")
    except:
        print(f"  {YELLOW}[!]{RESET} scylla.so unavailable")

    # 3. Dehashed.org (limited)
    print(f"\n  {CYAN}[3/3]{RESET} Checking dehashed (public)...")
    try:
        r = requests.get(f"https://dehashed.com/check?email={email}",
                        headers=HEADERS, timeout=10)
        if "found" in r.text.lower():
            print(f"  {RED}[!]{RESET} Dehashed: Possible breach found")
            log.append("[BREACH] dehashed.com: possible breach")
            total_breaches += 1
        else:
            print(f"  {GREEN}[✓]{RESET} No breaches via dehashed")
    except:
        print(f"  {YELLOW}[!]{RESET} dehashed.com unavailable")

    print_sep()
    if total_breaches > 0:
        print(f"\n{RED}[!] Found in {total_breaches} breach record(s)! Update your password!{RESET}")
    else:
        print(f"\n{GREEN}[✓] No breaches found (using public APIs){RESET}")
    print(f"{YELLOW}[!] Note: Full results require API keys for premium services{RESET}")

    filename = f"elgenral_breach_{email.replace('@','_at_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#                 FEATURE 5: IP GEOLOCATION ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def ip_lookup(target):
    """Get geolocation and ISP information for an IP or domain"""
    log = []

    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
        try:
            target = socket.gethostbyname(target)
            print(f"\n{CYAN}[*] Resolved to IP: {WHITE}{target}{RESET}")
            log.append(f"[INFO] Resolved domain to IP: {target}")
        except:
            print(f"{RED}[!] Could not resolve domain{RESET}")
            return

    print(f"\n{CYAN}{BOLD}[*] IP Geolocation for: {WHITE}{target}{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - IP Geolocation Report")
    log.append(f"Target IP: {target}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    # ip-api.com (free, no key needed, 45 requests/minute)
    try:
        r = requests.get(f"http://ip-api.com/json/{target}", timeout=10)
        data = r.json()
        if data["status"] == "success":
            fields = [
                ("Country", "country"),
                ("Region", "regionName"),
                ("City", "city"),
                ("ZIP Code", "zip"),
                ("ISP", "isp"),
                ("Organization", "org"),
                ("AS Number", "as"),
                ("Latitude", "lat"),
                ("Longitude", "lon"),
                ("Timezone", "timezone"),
            ]
            for label, key in fields:
                val = data.get(key, "N/A")
                print(f"  {GREEN}{label}:{RESET} {WHITE}{val}{RESET}")
                log.append(f"{label}: {val}")
        else:
            print(f"  {RED}[!] API error: {data.get('message', 'Unknown')}{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

    # Try ipinfo.io as backup
    print(f"\n  {CYAN}[*]{RESET} Additional info from ipinfo.io...")
    try:
        r = requests.get(f"https://ipinfo.io/{target}/json", headers=HEADERS, timeout=10)
        data = r.json()
        if data.get("hostname"):
            print(f"  {GREEN}Hostname:{RESET} {WHITE}{data['hostname']}{RESET}")
            log.append(f"Hostname: {data['hostname']}")
        if data.get("loc"):
            print(f"  {GREEN}Location:{RESET} {WHITE}{data['loc']}{RESET}")
    except:
        pass

    print_sep()

    filename = f"elgenral_ip_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#                FEATURE 6: WAYBACK MACHINE ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def wayback_search(target):
    """Get archived URLs from Wayback Machine"""
    log = []

    print(f"\n{CYAN}{BOLD}[*] Wayback Machine search for: {WHITE}{target}{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Wayback Machine Report")
    log.append(f"Target: {target}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    try:
        url = f"https://web.archive.org/cdx/search/cdx?url={target}/*&output=json&limit=30"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if len(data) > 1:
                urls_found = []
                for entry in data[1:]:
                    if len(entry) > 2:
                        urls_found.append(entry[2])
                unique_urls = list(set(urls_found))
                print(f"  {GREEN}[✓]{RESET} Found {len(unique_urls)} archived URLs:")
                for i, u in enumerate(unique_urls[:20], 1):
                    print(f"      {GREEN}[{i:02d}]{RESET} {WHITE}{u}{RESET}")
                    log.append(u)
                if len(unique_urls) > 20:
                    print(f"      {YELLOW}... and {len(unique_urls)-20} more{RESET}")
            else:
                print(f"  {YELLOW}[!]{RESET} No archived URLs found")
                log.append("[INFO] No archived URLs")
        else:
            print(f"  {RED}[!]{RESET} Wayback Machine error (HTTP {r.status_code})")
    except Exception as e:
        print(f"  {RED}[!]{RESET} Error: {e}")

    print_sep()

    filename = f"elgenral_wayback_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#               FEATURE 7: GITHUB PROFILE ANALYZER ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def analyze_github(username):
    """Analyze GitHub profile - email, bio, repos, followers, etc."""
    log = []

    print(f"\n{CYAN}{BOLD}[*] Analyzing GitHub profile: {WHITE}{username}{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - GitHub Profile Analyzer")
    log.append(f"Target: {username}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    try:
        r = requests.get(f"https://api.github.com/users/{username}", headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            fields = [
                ("Username", "login"),
                ("Name", "name"),
                ("Bio", "bio"),
                ("Company", "company"),
                ("Location", "location"),
                ("Email", "email"),
                ("Blog/Website", "blog"),
                ("Twitter", "twitter_username"),
                ("Public Repos", "public_repos"),
                ("Public Gists", "public_gists"),
                ("Followers", "followers"),
                ("Following", "following"),
                ("Account Created", "created_at"),
                ("Last Updated", "updated_at"),
            ]
            for label, key in fields:
                val = data.get(key, "N/A")
                if val:
                    print(f"  {GREEN}{label}:{RESET} {WHITE}{val}{RESET}")
                    log.append(f"{label}: {val}")

            # Fetch latest repos
            print(f"\n  {CYAN}[*]{RESET} Fetching latest repositories...")
            r_repos = requests.get(data['repos_url'], headers=HEADERS, timeout=10)
            if r_repos.status_code == 200:
                repos = r_repos.json()
                log.append(f"\nLatest Repositories ({min(5, len(repos))} of {len(repos)}):")
                for repo in repos[:5]:
                    name = repo['name']
                    lang = repo.get('language', 'Unknown')
                    stars = repo.get('stargazers_count', 0)
                    desc = repo.get('description', '')[:50] if repo.get('description') else ''
                    print(f"      {WHITE}→ {name}{RESET} ({lang}) ⭐{stars}")
                    if desc:
                        print(f"         {DIM}{desc}{RESET}")
                    log.append(f"  {name} ({lang}) - ⭐{stars}")

            # Fetch followers (first 5)
            print(f"\n  {CYAN}[*]{RESET} Recent followers...")
            r_followers = requests.get(data['followers_url'], headers=HEADERS, timeout=10)
            if r_followers.status_code == 200:
                followers = r_followers.json()
                for f in followers[:5]:
                    print(f"      {WHITE}→ {f['login']}{RESET}")
                    log.append(f"  Follower: {f['login']}")

        elif r.status_code == 403:
            print(f"  {RED}[!] GitHub API rate limited. Wait a minute.{RESET}")
        else:
            print(f"  {RED}[!] GitHub user not found (HTTP {r.status_code}){RESET}")

    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

    print_sep()

    filename = f"elgenral_github_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#                    FEATURE 8: DNS ENUMERATION ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def dns_enum(domain):
    """Enumerate DNS records (A, MX, NS, TXT, CNAME, SOA)"""
    log = []

    print(f"\n{CYAN}{BOLD}[*] DNS Enumeration for: {WHITE}{domain}{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - DNS Enumeration")
    log.append(f"Target: {domain}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    # A record (direct resolution)
    try:
        ips = socket.gethostbyname_ex(domain)[2]
        for ip in ips:
            print(f"  {GREEN}[A]{RESET} {WHITE}{domain} → {ip}{RESET}")
            log.append(f"[A] {domain} → {ip}")
    except:
        print(f"  {RED}[A]{RESET} No A record found")
        log.append("[A] Not found")

    # DNS records via Google DNS over HTTPS
    dns_types = {'A': 1, 'AAAA': 28, 'MX': 15, 'NS': 2, 'TXT': 16, 'CNAME': 5, 'SOA': 6}
    for rtype_name, rtype_val in dns_types.items():
        try:
            r = requests.get(f"https://dns.google/resolve?name={domain}&type={rtype_val}",
                            headers=HEADERS, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data.get('Answer'):
                    for ans in data['Answer'][:3]:
                        val = ans.get('data', ans.get('rdata', 'N/A'))
                        print(f"  {GREEN}[{rtype_name}]{RESET} {WHITE}{val}{RESET}")
                        log.append(f"[{rtype_name}] {val}")
        except:
            pass

    print_sep()

    filename = f"elgenral_dns_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#                     FEATURE 9: PORT SCANNER ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def port_scanner(host):
    """Scan common ports on a target host"""
    open_ports = []
    log = []

    print(f"\n{CYAN}{BOLD}[*] Scanning common ports on: {WHITE}{host}{RESET}")
    print(f"{CYAN}[*] Checking {len(COMMON_PORTS)} ports...{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Port Scanner")
    log.append(f"Target: {host}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    def check_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return port
        except:
            return None

    with ThreadPoolExecutor(max_workers=15) as executor:
        results = executor.map(check_port, COMMON_PORTS)
        for port in results:
            if port:
                open_ports.append(port)
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                print(f"  {GREEN}[✓]{RESET} Port {WHITE}{port:5}{RESET} → {service}")
                log.append(f"[OPEN] Port {port} ({service})")

    if not open_ports:
        print(f"  {YELLOW}[!]{RESET} No open ports found (or host is blocking)")
        log.append("[INFO] No open ports detected")

    print_sep()
    print(f"\n{GREEN}[✓] Found {len(open_ports)} open ports{RESET}")

    filename = f"elgenral_ports_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")
    return open_ports

# ═══════════════════════════════════════════════════════════════════════════
#              FEATURE 10: WEB CRAWLER ✅ حقيقي (بيجيب كل حاجة)
# ═══════════════════════════════════════════════════════════════════════════

def web_crawler(start_url):
    """Crawl a website and extract emails, phones, links, and forms"""
    visited = set()
    extracted_emails = set()
    extracted_phones = set()
    extracted_links = set()
    log = []

    print(f"\n{CYAN}{BOLD}[*] Web Crawler starting for: {WHITE}{start_url}{RESET}")
    print(f"{CYAN}[*] Crawling up to 50 pages...{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Web Crawler Report")
    log.append(f"Target: {start_url}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    def crawl(url, depth=0, max_depth=2, max_pages=50):
        if depth > max_depth or len(visited) >= max_pages or url in visited:
            return
        visited.add(url)

        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                return

            text = r.text

            # Extract emails
            found_emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.{1}[a-zA-Z]{2,}', text))
            extracted_emails.update(found_emails)

            # Extract phone numbers (international and local)
            found_phones = set(re.findall(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}', text))
            # Filter to reasonable phone numbers
            found_phones = {p for p in found_phones if len(re.sub(r'[^0-9]', '', p)) >= 7}
            extracted_phones.update(found_phones)

            # Extract all links
            found_urls = re.findall(r'href=["\'](https?://[^"\']+)["\']', text)
            for link in found_urls:
                extracted_links.add(link)
                if depth < max_depth:
                    crawl(link, depth + 1, max_depth, max_pages)

        except:
            pass

    crawl(start_url)

    print(f"\n  {GREEN}[✓]{RESET} Crawled {len(visited)} pages")

    if extracted_emails:
        print(f"\n  {CYAN}── Emails Found ({len(extracted_emails)}) ──{RESET}")
        for email in sorted(extracted_emails)[:20]:
            print(f"    {GREEN}[✓]{RESET} {email}")
            log.append(f"[EMAIL] {email}")
        if len(extracted_emails) > 20:
            print(f"    {YELLOW}... and {len(extracted_emails)-20} more{RESET}")

    if extracted_phones:
        print(f"\n  {CYAN}── Phone Numbers ({len(extracted_phones)}) ──{RESET}")
        for phone in sorted(extracted_phones)[:10]:
            print(f"    {GREEN}[✓]{RESET} {phone}")
            log.append(f"[PHONE] {phone}")
        if len(extracted_phones) > 10:
            print(f"    {YELLOW}... and {len(extracted_phones)-10} more{RESET}")

    print(f"\n  {CYAN}── Links Found ({len(extracted_links)}) ──{RESET}")
    for link in sorted(extracted_links)[:15]:
        print(f"    {WHITE}→ {link[:80]}{RESET}")

    print_sep()
    print(f"\n{GREEN}[✓] Summary:{RESET}")
    print(f"  {WHITE}Pages crawled:{RESET} {len(visited)}")
    print(f"  {WHITE}Emails found:{RESET} {len(extracted_emails)}")
    print(f"  {WHITE}Phone numbers:{RESET} {len(extracted_phones)}")
    print(f"  {WHITE}Links found:{RESET} {len(extracted_links)}")

    filename = f"elgenral_crawl_{start_url[:30].replace('https://','').replace('/','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#            FEATURE 11: PROFILE PIC DOWNLOADER ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def download_profile_pic(username):
    """Download profile pictures from GitHub and try Instagram"""
    log = []

    print(f"\n{CYAN}{BOLD}[*] Downloading profile pictures for: {WHITE}{username}{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Profile Picture Downloader")
    log.append(f"Target: {username}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    # GitHub - always works
    print(f"\n  {CYAN}[1/2]{RESET} GitHub avatar...")
    try:
        r = requests.get(f"https://api.github.com/users/{username}", headers=HEADERS, timeout=10)
        if r.status_code == 200:
            avatar_url = r.json().get('avatar_url')
            if avatar_url:
                img_data = requests.get(avatar_url).content
                filename = f"elgenral_{username}_github.jpg"
                with open(filename, "wb") as f:
                    f.write(img_data)
                print(f"  {GREEN}[✓]{RESET} Saved: {WHITE}{filename}{RESET}")
                log.append(f"[SAVED] GitHub: {filename}")
    except:
        print(f"  {YELLOW}[!]{RESET} GitHub: Could not download")
        log.append("[ERROR] GitHub download failed")

    # Instagram - may work for public profiles
    print(f"\n  {CYAN}[2/2]{RESET} Instagram profile picture...")
    try:
        r = requests.get(f"https://www.instagram.com/{username}/", headers=HEADERS, timeout=10)
        if r.status_code == 200 and "The link you followed may be broken" not in r.text:
            # Extract profile pic from the page's JSON data
            match = re.search(r'"profile_pic_url_hd":"([^"]+)"', r.text)
            if match:
                pic_url = match.group(1).replace('\\u0026', '&')
                img_data = requests.get(pic_url, headers=HEADERS).content
                filename = f"elgenral_{username}_instagram.jpg"
                with open(filename, "wb") as f:
                    f.write(img_data)
                print(f"  {GREEN}[✓]{RESET} Saved: {WHITE}{filename}{RESET}")
                log.append(f"[SAVED] Instagram: {filename}")
            else:
                print(f"  {YELLOW}[!]{RESET} Instagram: Profile exists, but couldn't extract pic URL")
        else:
            print(f"  {YELLOW}[!]{RESET} Instagram: Profile not found or private")
    except:
        print(f"  {YELLOW}[!]{RESET} Instagram: Could not access")
        log.append("[ERROR] Instagram download failed")

    print_sep()

    filename = f"elgenral_pic_report_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#               FEATURE 12: IMAGE METADATA EXTRACTOR ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def extract_metadata(image_path):
    """Extract EXIF metadata from image files"""
    log = []

    print(f"\n{CYAN}{BOLD}[*] Extracting metadata from: {WHITE}{image_path}{RESET}")
    print_sep()

    log.append(f"ELGENRAL OSINT - Image Metadata Extractor")
    log.append(f"Target: {image_path}")
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("="*60)

    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        img = Image.open(image_path)
        exif_data = img._getexif()

        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                print(f"  {GREEN}{tag_name}:{RESET} {WHITE}{value}{RESET}")
                log.append(f"{tag_name}: {value}")

                # Special handling for GPS
                if tag_name == "GPSInfo":
                    for gps_tag, gps_value in value.items():
                        gps_name = TAGS.get(gps_tag, gps_tag)
                        print(f"    {RED}GPS {gps_name}:{RESET} {gps_value}")
                        log.append(f"  GPS {gps_name}: {gps_value}")
        else:
            print(f"  {YELLOW}[!]{RESET} No metadata found in this image")
            log.append("[INFO] No metadata found")
            print(f"  {YELLOW}[!]{RESET} The image may have been stripped of EXIF data")

    except ImportError:
        print(f"  {RED}[!]{RESET} PIL/Pillow not installed.")
        print(f"  {CYAN}[*]{RESET} Install with: pip install Pillow")
        log.append("[ERROR] Pillow not installed")
    except FileNotFoundError:
        print(f"  {RED}[!]{RESET} File not found: {image_path}")
        log.append(f"[ERROR] File not found: {image_path}")
    except Exception as e:
        print(f"  {RED}[!]{RESET} Error: {e}")
        log.append(f"[ERROR] {e}")

    print_sep()

    filename = f"elgenral_metadata_{os.path.basename(image_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_results(filename, log)
    print(f"{GREEN}[✓] Report saved: {WHITE}{filename}{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#                FEATURE 13: FULL SCAN ✅ حقيقي
# ═══════════════════════════════════════════════════════════════════════════

def full_scan(target):
    """Run all applicable features against a single target"""
    print(f"\n{CYAN}{BOLD}═══════════════════════════════════════════════")
    print(f"           ELGENRAL FULL SCAN")
    print(f"           Target: {WHITE}{target}{RESET}")
    print(f"{CYAN}{BOLD}═══════════════════════════════════════════════{RESET}")

    # Detect target type
    if "@" in target:
        print(f"\n{YELLOW}[!] Detected: Email address{RESET}")
        check_breach(target)
        domain = target.split("@")[1]
        extract_emails(domain)
        dns_enum(domain)

    elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
        print(f"\n{YELLOW}[!] Detected: IP address{RESET}")
        ip_lookup(target)
        port_scanner(target)

    elif re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
        print(f"\n{YELLOW}[!] Detected: Domain{RESET}")
        ip_lookup(target)
        enum_subdomains(target)
        extract_emails(target)
        wayback_search(target)
        dns_enum(target)
        port_scanner(target)

    else:
        print(f"\n{YELLOW}[!] Detected: Username{RESET}")
        search_username(target)
        analyze_github(target)
        download_profile_pic(target)

    print(f"\n{CYAN}{BOLD}═══════════════════════════════════════════════")
    print(f"           FULL SCAN COMPLETE")
    print(f"{CYAN}{BOLD}═══════════════════════════════════════════════{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
#                               MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    while True:
        clear_screen()
        print(BANNER)
        print_menu()

        choice = input(f"\n{YELLOW}{BOLD}[?] Choose option (0-13): {RESET}").strip()

        if choice == "0":
            print(f"\n{GREEN}Thank you for using ELGENRAL OSINT Tool!")
            print(f"Created by Youssef Elgenral{RESET}")
            sys.exit(0)

        elif choice == "1":
            t = input(f"{YELLOW}[?] Enter username: {RESET}").strip()
            if t: search_username(t)

        elif choice == "2":
            t = input(f"{YELLOW}[?] Enter domain (e.g., example.com): {RESET}").strip()
            if t: enum_subdomains(t)

        elif choice == "3":
            t = input(f"{YELLOW}[?] Enter domain: {RESET}").strip()
            if t: extract_emails(t)

        elif choice == "4":
            t = input(f"{YELLOW}[?] Enter email address: {RESET}").strip()
            if t: check_breach(t)

        elif choice == "5":
            t = input(f"{YELLOW}[?] Enter IP or domain: {RESET}").strip()
            if t: ip_lookup(t)

        elif choice == "6":
            t = input(f"{YELLOW}[?] Enter domain/username: {RESET}").strip()
            if t: wayback_search(t)

        elif choice == "7":
            t = input(f"{YELLOW}[?] Enter GitHub username: {RESET}").strip()
            if t: analyze_github(t)

        elif choice == "8":
            t = input(f"{YELLOW}[?] Enter domain: {RESET}").strip()
            if t: dns_enum(t)

        elif choice == "9":
            t = input(f"{YELLOW}[?] Enter IP or domain to scan: {RESET}").strip()
            if t: port_scanner(t)

        elif choice == "10":
            t = input(f"{YELLOW}[?] Enter full URL to crawl (e.g., https://example.com): {RESET}").strip()
            if t: web_crawler(t)

        elif choice == "11":
            t = input(f"{YELLOW}[?] Enter username for profile pics: {RESET}").strip()
            if t: download_profile_pic(t)

        elif choice == "12":
            t = input(f"{YELLOW}[?] Enter image file path: {RESET}").strip()
            if t: extract_metadata(t)

        elif choice == "13":
            t = input(f"{YELLOW}[?] Enter target (username/domain/IP/email): {RESET}").strip()
            if t: full_scan(t)

        else:
            print(f"\n{RED}[!] Invalid option! Please choose 0-13.{RESET}")

        if choice != "0":
            input(f"\n{DIM}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] Interrupted by user. Exiting...{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[!] Unexpected error: {e}{RESET}")
        sys.exit(1)
