#!/usr/bin/env python3
"""
███████╗██╗     ███████╗███████╗███╗   ██╗██████╗  █████╗ ██╗
██╔════╝██║     ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔══██╗██║
█████╗  ██║     █████╗  █████╗  ██╔██╗ ██║██████╔╝███████║██║
██╔══╝  ██║     ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══██╗██╔══██║██║
███████╗███████╗███████╗███████╗██║ ╚████║██║  ██║██║  ██║███████╗
╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

    OSINT Tool - Created by Youssef Elgenral
    GitHub: https://github.com/youssefelgenral
"""

import requests
import sys
import json
import os
import time
from datetime import datetime

# Colors for terminal
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

BANNER = f"""
{CYAN}{BOLD}
███████╗██╗     ███████╗███████╗███╗   ██╗██████╗  █████╗ ██╗
██╔════╝██║     ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔══██╗██║
█████╗  ██║     █████╗  █████╗  ██╔██╗ ██║██████╔╝███████║██║
██╔══╝  ██║     ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══██╗██╔══██║██║
███████╗███████╗███████╗███████╗██║ ╚████║██║  ██║██║  ██║███████╗
╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
{RESET}
{YELLOW}{BOLD}                  OSINT TOOL v1.0{RESET}
{GREEN}          Created by: Youssef Elgenral{RESET}
{CYAN}          GitHub: /youssefelgenral{RESET}
{WHITE}          {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}
"""

# Platforms to search
PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter/X": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}/",
    "Telegram": "https://t.me/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Facebook": "https://www.facebook.com/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Medium": "https://medium.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Linktree": "https://linktr.ee/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Keybase": "https://keybase.io/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "VK": "https://vk.com/{}",
    "Dev.to": "https://dev.to/{}",
    "Replit": "https://replit.com/@{}",
    "CodePen": "https://codepen.io/{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "Behance": "https://www.behance.net/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    "Discord": "https://discord.com/users/{}"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
}

def print_logo():
    """Clear screen and print the tool logo"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

def search_username(username):
    """Search for a username across all platforms"""
    results = {
        "found": [],
        "not_found": [],
        "errors": []
    }
    
    print(f"\n{CYAN}{BOLD}[*] Searching for username: {WHITE}{username}{RESET}")
    print(f"{CYAN}[*] Checking {len(PLATFORMS)} platforms...{RESET}\n")
    print(f"{WHITE}{'─'*60}{RESET}\n")
    
    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username)
        
        try:
            # Add delay to avoid rate limiting
            time.sleep(0.5)
            
            response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                results["found"].append({
                    "platform": platform,
                    "url": url,
                    "status_code": response.status_code
                })
                print(f"{GREEN}[✓] {platform:20} → {WHITE}{url}{RESET}")
            elif response.status_code == 403:
                results["not_found"].append({
                    "platform": platform,
                    "url": url,
                    "status_code": response.status_code
                })
                print(f"{YELLOW}[!] {platform:20} → {RED}Blocked (403){RESET}")
            elif response.status_code == 429:
                results["errors"].append({
                    "platform": platform,
                    "url": url,
                    "error": "Rate limited"
                })
                print(f"{YELLOW}[!] {platform:20} → {RED}Rate Limited (429){RESET}")
            else:
                results["not_found"].append({
                    "platform": platform,
                    "url": url,
                    "status_code": response.status_code
                })
                
        except requests.exceptions.ConnectionError:
            results["errors"].append({
                "platform": platform,
                "url": url,
                "error": "Connection error"
            })
            print(f"{RED}[✗] {platform:20} → {WHITE}Connection Error{RESET}")
        except requests.exceptions.Timeout:
            results["errors"].append({
                "platform": platform,
                "url": url,
                "error": "Timeout"
            })
            print(f"{RED}[✗] {platform:20} → {WHITE}Timeout{RESET}")
        except Exception as e:
            results["errors"].append({
                "platform": platform,
                "url": url,
                "error": str(e)[:50]
            })
            print(f"{RED}[✗] {platform:20} → {WHITE}Error: {str(e)[:30]}{RESET}")
    
    return results

def save_results(username, results):
    """Save results to a file"""
    filename = f"elgenral_osint_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write(f"ELGENRAL OSINT REPORT\n")
        f.write(f"Target Username: {username}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Created by: Youssef Elgenral\n")
        f.write(f"="*60 + "\n\n")
        
        f.write(f"PLATFORMS FOUND ({len(results['found'])}):\n")
        f.write("-"*40 + "\n")
        for item in results["found"]:
            f.write(f"[✓] {item['platform']}: {item['url']}\n")
        
        f.write(f"\nPLATFORMS NOT FOUND ({len(results['not_found'])}):\n")
        f.write("-"*40 + "\n")
        for item in results["not_found"]:
            f.write(f"[ ] {item['platform']}: {item['url']}\n")
        
        if results["errors"]:
            f.write(f"\nERRORS ({len(results['errors'])}):\n")
            f.write("-"*40 + "\n")
            for item in results["errors"]:
                f.write(f"[!] {item['platform']}: {item['error']}\n")
    
    return filename

def main():
    print_logo()
    
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print(f"{YELLOW}{BOLD}[?] Enter username to search: {RESET}", end="")
        username = input().strip()
    
    if not username:
        print(f"{RED}[!] No username provided. Exiting.{RESET}")
        sys.exit(1)
    
    # Check if user wants to search multiple usernames
    if "," in username:
        usernames = [u.strip() for u in username.split(",")]
        print(f"{CYAN}[*] Searching for {len(usernames)} usernames...{RESET}")
        for u in usernames:
            results = search_username(u)
            filename = save_results(u, results)
            
            print(f"\n{GREEN}{BOLD}[✓] Results saved to: {WHITE}{filename}{RESET}")
            print(f"{GREEN}[✓] Found on {len(results['found'])} platforms{RESET}")
            print(f"{RED}[-] Not found on {len(results['not_found'])} platforms{RESET}")
            if results["errors"]:
                print(f"{YELLOW}[!] Errors: {len(results['errors'])}{RESET}")
            print(f"\n{WHITE}{'─'*60}{RESET}")
    else:
        results = search_username(username)
        filename = save_results(username, results)
        
        print(f"\n{WHITE}{'─'*60}{RESET}")
        print(f"\n{GREEN}{BOLD}[✓] Scan Complete!{RESET}")
        print(f"{GREEN}[✓] Results saved to: {WHITE}{filename}{RESET}")
        print(f"{GREEN}[✓] Found on {len(results['found'])} platforms{RESET}")
        print(f"{RED}[-] Not found on {len(results['not_found'])} platforms{RESET}")
        if results["errors"]:
            print(f"{YELLOW}[!] Errors: {len(results['errors'])}{RESET}")
    
    print(f"\n{CYAN}{BOLD}─── Youssef Elgenral OSINT Tool ───{RESET}")
    print(f"{GREEN}Thank you for using the tool!{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Scan interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[!] Unexpected error: {e}{RESET}")
        sys.exit(1)