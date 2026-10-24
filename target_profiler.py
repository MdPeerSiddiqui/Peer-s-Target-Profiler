#!/usr/bin/env python3
"""
PEER'S TARGET PROFILER v1.0
OSINT & Social Engineering Target Dossier Generator
Author: Md Peer Siddiqui
Internship Track: Social Engineering Attack Simulations Using Python (Day 05)
Host Organization: Sqrock IT Solution
"""

import os
import sys
import json
import re
import datetime
from collections import Counter
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("[!] Error: 'requests' library is required. Install via: pip install requests")
    sys.exit(1)

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
except ImportError:
    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = DummyColor()
    Style = DummyColor()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGETS_DIR = os.path.join(BASE_DIR, "targets")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DEFAULT_OUTPUT_JSON = os.path.join(TARGETS_DIR, "target_profile.json")

# Built-in offline fallback target profiles (guards against GitHub API rate-limits)
OFFLINE_DOSSIERS = {
    "torvalds": {
        "login": "torvalds",
        "name": "Linus Torvalds",
        "company": "Linux Foundation",
        "location": "Portland, OR",
        "email": "torvalds@linux-foundation.org",
        "bio": "Creator of Linux and Git.",
        "blog": "https://kernel.org",
        "twitter_username": None,
        "public_repos": 7,
        "public_gists": 0,
        "followers": 235000,
        "following": 0,
        "created_at": "2011-09-03T15:26:22Z",
        "updated_at": "2026-10-15T10:00:00Z",
        "languages": {"C": 6, "Shell": 1, "Perl": 1},
        "top_repositories": [
            {"name": "linux", "stars": 182000, "forks": 54000, "lang": "C", "desc": "Linux kernel source tree"},
            {"name": "uemacs", "stars": 1200, "forks": 290, "lang": "C", "desc": "MicroEMACS editor"}
        ],
        "leaked_emails": ["torvalds@linux-foundation.org"],
        "activity_hours_utc": [14, 15, 16, 17, 18, 19, 20, 21, 22]
    },
    "sqrock-engineer": {
        "login": "sqrock-engineer",
        "name": "Harish Kumar",
        "company": "Sqrock IT Solution",
        "location": "Bangalore, India",
        "email": "harish.k@sqrock-labs.internal",
        "bio": "Senior Cloud Security Engineer & Backend Dev. Building resilient identity pipelines.",
        "blog": "https://sqrock.com/engineering",
        "twitter_username": "harish_sec",
        "public_repos": 14,
        "public_gists": 3,
        "followers": 142,
        "following": 88,
        "created_at": "2021-04-12T08:14:00Z",
        "updated_at": "2026-10-22T14:30:00Z",
        "languages": {"Python": 8, "Go": 4, "TypeScript": 2, "Dockerfile": 2},
        "top_repositories": [
            {"name": "cloud-guard-iam", "stars": 45, "forks": 12, "lang": "Python", "desc": "Zero-trust IAM policy auditor"},
            {"name": "telecom-sip-monitor", "stars": 32, "forks": 8, "lang": "Go", "desc": "Real-time VoIP SIP telemetry scanner"}
        ],
        "leaked_emails": ["harish.k@sqrock-labs.internal", "harish.dev99@gmail.com"],
        "activity_hours_utc": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    },
    "octocat": {
        "login": "octocat",
        "name": "The Octocat",
        "company": "@github",
        "location": "San Francisco, CA",
        "email": "octocat@github.com",
        "bio": "GitHub's official mascot and demo identity.",
        "blog": "https://github.blog",
        "twitter_username": "github",
        "public_repos": 8,
        "public_gists": 8,
        "followers": 18900,
        "following": 9,
        "created_at": "2011-01-25T18:44:36Z",
        "updated_at": "2026-10-01T12:00:00Z",
        "languages": {"Ruby": 4, "JavaScript": 2, "HTML": 2},
        "top_repositories": [
            {"name": "Hello-World", "stars": 2900, "forks": 2400, "lang": "Ruby", "desc": "My first repository on GitHub!"},
            {"name": "Spoon-Knife", "stars": 14000, "forks": 148000, "lang": "HTML", "desc": "Repo for testing forks"}
        ],
        "leaked_emails": ["octocat@github.com"],
        "activity_hours_utc": [17, 18, 19, 20, 21, 22, 23, 0]
    }
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    banner = rf"""{Fore.CYAN}{Style.BRIGHT}
  ____  _____ _____ ____  _ ____    _____ _    ____   ____ _____ _____ 
 |  _ \| ____| ____|  _ \/ ___|  |_   _/ \  |  _ \ / ___| ____|_   _|
 | |_) |  _| |  _| | |_) \___ \    | |/ _ \ | |_) | |  _|  _|   | |  
 |  __/| |___| |___|  _ < ___) |   | / ___ \|  _ <| |_| | |___  | |  
 |_|   |_____|_____|_| \_\____/    |_/_/   \_\_| \_\\____|_____| |_|  
                                                                       
  ____  ____   ___  _____ ___ _     _____ ____                         
 |  _ \|  _ \ / _ \|  ___|_ _| |   | ____|  _ \                        
 | |_) | |_) | | | | |_   | || |   |  _| | |_) |                       
 |  __/|  _ <| |_| |  _|  | || |___| |___|  _ <                        
 |_|   |_| \_\\___/|_|   |___|_____|_____|_| \_\                       
{Fore.YELLOW}{Style.BRIGHT} ⚡ OSINT TARGET DOSSIER & SOCIAL ENGINEERING ATTACK SURFACE ANALYZER ⚡
{Fore.WHITE} Developed by: Md Peer Siddiqui | Sqrock IT Solution Internship (Day 05)
{Fore.CYAN}========================================================================{Style.RESET_ALL}
"""
    print(banner)


def fetch_github_profile(username, token=None):
    """
    Fetches public GitHub profile data, repositories, and commit event metadata.
    Falls back gracefully to offline dossiers if rate limits (HTTP 403) are encountered.
    """
    clean_user = username.strip().lower()
    headers = {
        "User-Agent": "PEER-Target-Profiler-Sqrock/1.0",
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"

    base_url = "https://api.github.com"
    try:
        # 1. Fetch user base profile
        res_u = requests.get(f"{base_url}/users/{clean_user}", headers=headers, timeout=6)
        
        if res_u.status_code == 404:
            return {"status": "error", "message": f"Target username '{clean_user}' not found on GitHub."}
        
        if res_u.status_code in (403, 429):
            # Rate limited
            if clean_user in OFFLINE_DOSSIERS:
                data = dict(OFFLINE_DOSSIERS[clean_user])
                data["_source"] = "offline_cache_ratelimit"
                return {"status": "success", "profile": data}
            else:
                return {
                    "status": "rate_limited",
                    "message": "GitHub API unauthenticated rate limit reached (60 req/hr).",
                    "suggestion": "Using cached sample profile for demonstration."
                }

        u = res_u.json()

        # 2. Fetch public repositories
        res_repos = requests.get(f"{base_url}/users/{clean_user}/repos?per_page=30&sort=pushed", headers=headers, timeout=6)
        repos = res_repos.json() if res_repos.status_code == 200 else []

        # Aggregate languages
        langs = {}
        top_repos = []
        for r in repos:
            if isinstance(r, dict):
                lang = r.get("language")
                if lang:
                    langs[lang] = langs.get(lang, 0) + 1
                if len(top_repos) < 5:
                    top_repos.append({
                        "name": r.get("name"),
                        "stars": r.get("stargazers_count", 0),
                        "forks": r.get("forks_count", 0),
                        "lang": lang or "None",
                        "desc": (r.get("description") or "No description provided")[:80]
                    })

        # 3. Fetch public events for commit email leaks & active hours
        res_events = requests.get(f"{base_url}/users/{clean_user}/events/public?per_page=30", headers=headers, timeout=6)
        events = res_events.json() if res_events.status_code == 200 else []

        leaked_emails = set()
        activity_hours = []

        if isinstance(events, list):
            for ev in events:
                # Capture hour
                created_at = ev.get("created_at")
                if created_at:
                    try:
                        dt = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        activity_hours.append(dt.hour)
                    except Exception:
                        pass

                # Capture commit emails from PushEvent
                if ev.get("type") == "PushEvent":
                    payload = ev.get("payload", {})
                    commits = payload.get("commits", [])
                    for c in commits:
                        author = c.get("author", {})
                        email = author.get("email", "")
                        if email and "@" in email and "noreply" not in email.lower():
                            leaked_emails.add(email)

        # Base email from profile if provided
        if u.get("email"):
            leaked_emails.add(u.get("email"))

        profile_data = {
            "login": u.get("login"),
            "name": u.get("name"),
            "company": u.get("company"),
            "location": u.get("location"),
            "email": u.get("email"),
            "bio": u.get("bio"),
            "blog": u.get("blog"),
            "twitter_username": u.get("twitter_username"),
            "public_repos": u.get("public_repos", 0),
            "public_gists": u.get("public_gists", 0),
            "followers": u.get("followers", 0),
            "following": u.get("following", 0),
            "created_at": u.get("created_at"),
            "updated_at": u.get("updated_at"),
            "languages": langs,
            "top_repositories": top_repos,
            "leaked_emails": list(leaked_emails),
            "activity_hours_utc": activity_hours,
            "_source": "live_github_api"
        }

        return {"status": "success", "profile": profile_data}

    except requests.exceptions.RequestException as e:
        # Network down / offline
        if clean_user in OFFLINE_DOSSIERS:
            data = dict(OFFLINE_DOSSIERS[clean_user])
            data["_source"] = "offline_cache_network_err"
            return {"status": "success", "profile": data}
        return {"status": "error", "message": f"Network error querying GitHub API: {e}"}


def calculate_opsec_score(profile):
    """
    Calculates an OPSEC & Digital Footprint Exposure Score (0-100).
    Higher score = Greater public exposure and higher spear-phishing vulnerability.
    """
    score = 0
    factors = []

    # 1. Real Name Disclosure
    if profile.get("name") and len(profile.get("name").strip()) > 2:
        score += 15
        factors.append({"factor": "Real Full Name Disclosed", "points": 15, "risk": "Enables cross-platform social graph pivoting"})
    else:
        factors.append({"factor": "Anonymous/Pseudonymous Handle", "points": 0, "risk": "Hardens against personal identity correlation"})

    # 2. Company / Employer Exposure
    if profile.get("company"):
        score += 20
        factors.append({"factor": "Employer/Organization Listed", "points": 20, "risk": "Enables corporate authority & IT helpdesk pretexting"})
    
    # 3. Physical Location
    if profile.get("location"):
        score += 15
        factors.append({"factor": "Geographic Location Exposed", "points": 15, "risk": "Permits targeted timezone and regional event pretexting"})

    # 4. Leaked Direct Emails
    leaked = profile.get("leaked_emails", [])
    if leaked:
        score += 25
        factors.append({"factor": f"Raw Commit/Profile Email Leaked ({len(leaked)} found)", "points": 25, "risk": "Bypasses web contact forms; direct spear-phishing inbox vector"})
    elif profile.get("email"):
        score += 20
        factors.append({"factor": "Public Email Listed in Profile", "points": 20, "risk": "Direct communication vector available"})
    else:
        factors.append({"factor": "Email Masked / Noreply Enforced", "points": 0, "risk": "Good OPSEC: Uses GitHub privacy mask"})

    # 5. External Website / Twitter / Social Anchors
    if profile.get("blog") or profile.get("twitter_username"):
        score += 10
        factors.append({"factor": "Personal Domain / Twitter Linked", "points": 10, "risk": "Provides secondary attack surfaces and credential harvesting avenues"})

    # 6. Detailed Bio / Habit Information
    if profile.get("bio") and len(profile.get("bio")) > 15:
        score += 15
        factors.append({"factor": "Descriptive Bio & Professional Focus", "points": 15, "risk": "Reveals current active projects and psychological triggers"})

    final_score = min(score, 100)
    
    if final_score <= 25:
        tier = "LOW EXPOSURE"
        color = Fore.GREEN
        summary = "Target maintains rigorous OPSEC. Digital footprint is minimal; difficult to craft high-conviction spear-phishing."
    elif final_score <= 55:
        tier = "MODERATE EXPOSURE"
        color = Fore.YELLOW
        summary = "Standard technical footprint. Sufficient data exists for generic recruiter or language-based lures."
    elif final_score <= 80:
        tier = "HIGH EXPOSURE"
        color = Fore.RED
        summary = "Extensive reconnaissance surface. Organization, location, and technical skillset provide strong pretext hooks."
    else:
        tier = "CRITICAL EXPOSURE"
        color = Fore.RED + Style.BRIGHT
        summary = "Severe identity exposure. Direct personal email, employer, and activity patterns enable multi-stage targeted whaling/vishing."

    return {
        "score": final_score,
        "tier": tier,
        "color": color,
        "summary": summary,
        "factors": factors
    }


def analyze_activity_timezones(activity_hours):
    """
    Infers working habits and probable timezone based on UTC commit hours.
    """
    if not activity_hours:
        return {
            "has_data": False,
            "message": "No recent public commit events found to analyze activity patterns."
        }

    counts = Counter(activity_hours)
    # Peak hour in UTC
    peak_utc_hour = counts.most_common(1)[0][0]
    
    # Inferred region
    if 0 <= peak_utc_hour <= 7:
        region = "Asia-Pacific / India (UTC+5:30 to UTC+8)"
    elif 8 <= peak_utc_hour <= 15:
        region = "Europe / Middle East / Africa (UTC+0 to UTC+3)"
    else:
        region = "Americas (UTC-8 to UTC-4)"

    return {
        "has_data": True,
        "total_events_sampled": len(activity_hours),
        "peak_utc_hour": peak_utc_hour,
        "inferred_region": region,
        "hour_distribution": {h: counts.get(h, 0) for h in range(24)}
    }


def generate_spear_phishing_pretexts(profile):
    """
    Synthesizes gathered OSINT into 3 weaponized social engineering pretext scenarios.
    """
    name = profile.get("name") or profile.get("login") or "Target"
    company = profile.get("company") or "the organization"
    location = profile.get("location") or "their regional office"
    
    # Identify top language
    langs = profile.get("languages", {})
    top_lang = max(langs.keys(), key=lambda k: langs[k]) if langs else "Python"
    
    # Identify top repo
    repos = profile.get("top_repositories", [])
    top_repo_name = repos[0]["name"] if repos else "internal-tools"

    scenarios = [
        {
            "id": "SP-01",
            "title": f"Technical Zero-Day CVE Alert ({top_lang} Ecosystem)",
            "vector": "Email / GitHub Issue Injection",
            "pretext": (
                f"Adversary impersonates GitHub Security Advisories or the {top_lang} core security team. "
                f"They send an urgent notification citing an unauthenticated Remote Code Execution (RCE) "
                f"vulnerability in dependency trees matching repository '{top_repo_name}'."
            ),
            "hook": f"Urgent CVE Patch for {top_repo_name} ({top_lang})",
            "call_to_action": f"Click link to review affected dependency tree: https://security-patch-advisory.org/cve/{top_repo_name}",
            "psychological_triggers": ["Urgency", "Technical Authority", "Fear of Compromise"]
        },
        {
            "id": "SP-02",
            "title": f"Corporate Workspace Re-Authentication ({company})",
            "vector": "Spear-Phishing Email / Internal Slack Impersonation",
            "pretext": (
                f"Leveraging the public exposure of employer '{company}' and location '{location}', "
                f"attacker impersonates {company} IT Operations. They notify {name} that their corporate VPN/SSO "
                f"certificate is pending mandatory migration before the end of the business day."
            ),
            "hook": f"{company} IT Notice: Mandatory Single Sign-On Endpoint Renewal",
            "call_to_action": f"Authenticate your identity via the corporate portal: https://login.{company.lower().replace(' ', '')}-portal.net/sso",
            "psychological_triggers": ["Authority", "Compliance", "Urgency"]
        },
        {
            "id": "SP-03",
            "title": f"Targeted Executive / Recruiter Headhunting Hook ({top_lang} Specialist)",
            "vector": "LinkedIn InMail / Direct Email Spear-Phish",
            "pretext": (
                f"Attacker poses as an executive talent scout from a high-profile technology firm, praising "
                f"{name}'s open-source contributions in {top_lang}. They attach a weaponized PDF or link "
                f"purporting to be a confidential compensation structure and technical architecture brief."
            ),
            "hook": f"Confidential Senior {top_lang} Architecture Lead Opportunity for {name}",
            "call_to_action": f"Download the candidate briefing packet: https://talent-briefing-executive.io/role-spec.pdf",
            "psychological_triggers": ["Flattery / Liking", "Greed / Ambition", "Curiosity"]
        }
    ]

    return scenarios


def display_target_dossier(profile):
    """
    Renders the aggregated OSINT profile cleanly in the terminal.
    """
    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" 🕵️ TARGET INTELLIGENCE DOSSIER: @{profile.get('login', 'UNKNOWN')}")
    print(f"========================================================================{Style.RESET_ALL}")
    
    print(f" {Fore.YELLOW}Full Name        :{Style.RESET_ALL} {profile.get('name') or 'Not Specified'}")
    print(f" {Fore.YELLOW}Company / Org    :{Style.RESET_ALL} {profile.get('company') or 'Not Specified'}")
    print(f" {Fore.YELLOW}Location         :{Style.RESET_ALL} {profile.get('location') or 'Not Specified'}")
    print(f" {Fore.YELLOW}Public Bio       :{Style.RESET_ALL} {profile.get('bio') or 'No Bio'}")
    print(f" {Fore.YELLOW}Personal Website :{Style.RESET_ALL} {profile.get('blog') or 'None'}")
    print(f" {Fore.YELLOW}Twitter/X Handle :{Style.RESET_ALL} @{profile.get('twitter_username') or 'None'}")
    print(f" {Fore.YELLOW}Public Repos     :{Style.RESET_ALL} {profile.get('public_repos', 0)} repositories")
    print(f" {Fore.YELLOW}Followers / Following:{Style.RESET_ALL} {profile.get('followers', 0)} / {profile.get('following', 0)}")
    print(f" {Fore.YELLOW}Account Created  :{Style.RESET_ALL} {profile.get('created_at') or 'Unknown'}")
    
    # Leaked emails
    emails = profile.get("leaked_emails", [])
    if emails:
        print(f"\n {Fore.RED}{Style.BRIGHT}[!] RECOVERED / LEAKED EMAIL IDENTIFIERS:{Style.RESET_ALL}")
        for em in emails:
            print(f"   {Fore.RED}└──► {em}{Style.RESET_ALL}")
    else:
        print(f"\n {Fore.GREEN}[✓] No direct raw commit emails leaked in public events.{Style.RESET_ALL}")

    # Top languages
    langs = profile.get("languages", {})
    if langs:
        print(f"\n {Fore.CYAN}{Style.BRIGHT}[*] PRIMARY PROGRAMMING LANGUAGES & TECH STACK:{Style.RESET_ALL}")
        total = sum(langs.values())
        for lang, count in sorted(langs.items(), key=lambda x: x[1], reverse=True)[:6]:
            pct = int((count / max(total, 1)) * 100)
            bar = "█" * (pct // 5)
            print(f"   {lang:<14} : {bar:<20} {pct:>2}% ({count} repos)")

    # Top repos
    top_repos = profile.get("top_repositories", [])
    if top_repos:
        print(f"\n {Fore.CYAN}{Style.BRIGHT}[*] NOTABLE REPOSITORIES FOR WEAPONIZATION:{Style.RESET_ALL}")
        for r in top_repos[:3]:
            print(f"   • {Fore.WHITE}{Style.BRIGHT}{r['name']}{Style.RESET_ALL} ({r['lang']}) - ⭐ {r['stars']} | 🍴 {r['forks']}")
            print(f"     └─ {Fore.LIGHTBLACK_EX}{r['desc']}{Style.RESET_ALL}")


def display_opsec_evaluation(profile):
    """
    Prints the OPSEC exposure scoring in terminal.
    """
    opsec = calculate_opsec_score(profile)
    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" 🛡️ DIGITAL FOOTPRINT & OPSEC RISK EVALUATION: @{profile.get('login')}")
    print(f"========================================================================{Style.RESET_ALL}")
    
    print(f" Overall Threat Exposure Score : {opsec['color']}{opsec['score']}/100 [{opsec['tier']}]{Style.RESET_ALL}")
    print(f" Adversary Assessment          : {opsec['summary']}\n")
    
    print(f" {Fore.WHITE}{Style.BRIGHT}Risk Factor Breakdown:{Style.RESET_ALL}")
    for item in opsec["factors"]:
        pts = f"+{item['points']} pts" if item['points'] > 0 else "0 pts"
        pt_color = Fore.RED if item['points'] >= 20 else (Fore.YELLOW if item['points'] > 0 else Fore.GREEN)
        print(f"   [{pt_color}{pts:<7}{Style.RESET_ALL}] {Fore.WHITE}{item['factor']}{Style.RESET_ALL}")
        print(f"             └─ {Fore.LIGHTBLACK_EX}Adversary Impact: {item['risk']}{Style.RESET_ALL}")

    print(f"\n {Fore.GREEN}{Style.BRIGHT}Defender OPSEC Hardening Checklist:{Style.RESET_ALL}")
    print("   1. Enable GitHub Email Privacy: Select 'Keep my email addresses private' in settings.")
    print("   2. Sanitize Git Commits: Ensure local git config does not embed corporate email into public repos.")
    print("   3. Scrub Employer Tags: Avoid naming specific operational infrastructure or internal divisions.")
    print("   4. Beware Inbound PRs & Urgent CVE Links: Validate all security notifications via official channels.")


def display_activity_hours(profile):
    """
    Displays the commit activity histogram and inferred timezone.
    """
    activity = analyze_activity_timezones(profile.get("activity_hours_utc", []))
    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" ⏰ ACTIVITY TIMESTAMPS & WORKING HOURS ANALYSIS: @{profile.get('login')}")
    print(f"========================================================================{Style.RESET_ALL}")
    
    if not activity["has_data"]:
        print(f" {Fore.YELLOW}{activity['message']}{Style.RESET_ALL}")
        return

    print(f" Sampled Events          : {activity['total_events_sampled']} commit actions")
    print(f" Peak Activity (UTC)     : {activity['peak_utc_hour']:02d}:00 UTC")
    print(f" Inferred Target Region  : {Fore.YELLOW}{activity['inferred_region']}{Style.RESET_ALL}")
    print(f"\n {Fore.WHITE}{Style.BRIGHT}24-Hour UTC Activity Radar:{Style.RESET_ALL}")

    dist = activity["hour_distribution"]
    max_c = max(dist.values()) or 1
    for h in range(0, 24, 2):
        c1 = dist.get(h, 0)
        c2 = dist.get(h+1, 0)
        c = c1 + c2
        bar_len = int((c / max_c) * 20)
        bar = "█" * bar_len
        marker = f" {Fore.RED}◄ PEAK WORK WINDOW{Style.RESET_ALL}" if (h <= activity['peak_utc_hour'] <= h+1) else ""
        print(f"   {h:02d}:00 - {h+1:02d}:59 UTC : {Fore.CYAN}{bar:<20}{Style.RESET_ALL} ({c} commits){marker}")


def display_spear_phishing_pretexts(profile):
    """
    Displays the 3 synthesized spear-phishing attack vectors.
    """
    scenarios = generate_spear_phishing_pretexts(profile)
    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" 🎣 TAILORED SPEAR-PHISHING PRETEXTS (ATTACKER PERSPECTIVE)")
    print(f" Target: @{profile.get('login')} ({profile.get('name') or 'Engineer'})")
    print(f"========================================================================{Style.RESET_ALL}")

    for s in scenarios:
        print(f"\n {Fore.RED}{Style.BRIGHT}[{s['id']}] {s['title']}{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}Primary Vector    :{Style.RESET_ALL} {s['vector']}")
        print(f"   {Fore.YELLOW}Pretext Narrative :{Style.RESET_ALL} {s['pretext']}")
        print(f"   {Fore.YELLOW}Weaponized Hook   :{Style.RESET_ALL} \"{s['hook']}\"")
        print(f"   {Fore.YELLOW}Deceptive CTA     :{Style.RESET_ALL} {s['call_to_action']}")
        print(f"   {Fore.YELLOW}Triggers Weaponized:{Style.RESET_ALL} {', '.join(s['psychological_triggers'])}")


def export_target_profile_json(profile, filepath=DEFAULT_OUTPUT_JSON):
    """
    Exports the complete target profile into JSON format as required by the internship deliverable.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    opsec = calculate_opsec_score(profile)
    pretexts = generate_spear_phishing_pretexts(profile)
    activity = analyze_activity_timezones(profile.get("activity_hours_utc", []))

    deliverable = {
        "metadata": {
            "tool": "PEER'S Target Profiler v1.0",
            "intern_name": "Md Peer Siddiqui",
            "organization": "Sqrock IT Solution",
            "track": "Social Engineering Attack Simulations Using Python (Day 05)",
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        "target_profile": {
            "login": profile.get("login"),
            "name": profile.get("name"),
            "company": profile.get("company"),
            "location": profile.get("location"),
            "bio": profile.get("bio"),
            "blog": profile.get("blog"),
            "twitter_username": profile.get("twitter_username"),
            "public_repos_count": profile.get("public_repos", 0),
            "followers": profile.get("followers", 0),
            "following": profile.get("following", 0),
            "top_languages": profile.get("languages", {}),
            "top_repositories": profile.get("top_repositories", []),
            "recovered_commit_emails": profile.get("leaked_emails", [])
        },
        "adversary_intelligence": {
            "activity_analysis": activity,
            "spear_phishing_pretexts": pretexts
        },
        "defensive_opsec_evaluation": {
            "exposure_score": opsec["score"],
            "exposure_tier": opsec["tier"],
            "exposure_summary": opsec["summary"],
            "risk_factors": opsec["factors"]
        }
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(deliverable, f, indent=2)

    return filepath


def run_benchmark_audit():
    """
    Audits and profiles preset reference identities (Linus Torvalds, Harish/Sqrock, Octocat).
    """
    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" [*] EXECUTING SAMPLE TARGET PROFILING BENCHMARK AUDIT...")
    print(f"========================================================================{Style.RESET_ALL}")
    print(f" {'#':<3} | {'Username':<18} | {'Identified Name':<20} | {'Org/Company':<18} | {'Score':<8} | {'Risk Tier'}")
    print(f" {Fore.CYAN}{'-'*85}{Style.RESET_ALL}")

    idx = 1
    for key, dossier in OFFLINE_DOSSIERS.items():
        opsec = calculate_opsec_score(dossier)
        name = dossier.get("name") or "Unknown"
        comp = dossier.get("company") or "None"
        tier_str = f"{opsec['color']}{opsec['tier']}{Style.RESET_ALL}"
        print(f" {idx:<3} | @{key:<17} | {name:<20} | {comp:<18} | {opsec['score']:>3}/100 | {tier_str}")
        idx += 1

    print(f" {Fore.CYAN}{'-'*85}{Style.RESET_ALL}")
    print(f" {Fore.GREEN}[✓] Benchmark Complete: All sample target profiles analyzed successfully.{Style.RESET_ALL}")


def interactive_menu():
    """
    Master interactive console loop.
    """
    current_profile = OFFLINE_DOSSIERS["sqrock-engineer"]

    while True:
        try:
            print_banner()
            target_disp = f"@{current_profile.get('login')} ({current_profile.get('name') or 'No Name'})"
            print(f" Active Loaded Target: {Fore.GREEN}{Style.BRIGHT}{target_disp}{Style.RESET_ALL}\n")
            print(" Master Options:")
            print(f"  {Fore.CYAN}[1]{Style.RESET_ALL} Profile Target by GitHub Username (Live API or Cache)")
            print(f"  {Fore.CYAN}[2]{Style.RESET_ALL} Inspect Target Dossier & Tech Stack Breakdown")
            print(f"  {Fore.CYAN}[3]{Style.RESET_ALL} Deep Commit Email & Identity Leak Harvester")
            print(f"  {Fore.CYAN}[4]{Style.RESET_ALL} Activity Hours & Timezone Behavioral Analysis")
            print(f"  {Fore.CYAN}[5]{Style.RESET_ALL} Generate Tailored Spear-Phishing Pretexts (Attacker View)")
            print(f"  {Fore.CYAN}[6]{Style.RESET_ALL} OPSEC Risk & Digital Footprint Exposure Scorer")
            print(f"  {Fore.CYAN}[7]{Style.RESET_ALL} Run Benchmark Audit Across 3 Reference Profiles")
            print(f"  {Fore.CYAN}[8]{Style.RESET_ALL} Export Target Dossier to JSON ({Fore.YELLOW}target_profile.json{Style.RESET_ALL})")
            print(f"  {Fore.CYAN}[9]{Style.RESET_ALL} Compile Executive PDF Threat Report (Day 05)")
            print(f"  {Fore.CYAN}[0]{Style.RESET_ALL} Exit Profiler")

            choice = input(f"\n{Fore.GREEN}PROFILER > {Style.RESET_ALL}").strip()

            if choice == "1":
                uname = input(f"\n{Fore.YELLOW}Enter target GitHub username (e.g. torvalds, octocat, or custom) > {Style.RESET_ALL}").strip()
                if not uname:
                    print(f"{Fore.RED}[!] Username cannot be empty.{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.CYAN}[*] Fetching public OSINT reconnaissance for @{uname}...{Style.RESET_ALL}")
                    res = fetch_github_profile(uname)
                    if res["status"] == "success":
                        current_profile = res["profile"]
                        print(f"{Fore.GREEN}[✓] Successfully loaded profile for @{current_profile['login']}!{Style.RESET_ALL}")
                        display_target_dossier(current_profile)
                    elif res["status"] == "rate_limited":
                        print(f"{Fore.YELLOW}[!] {res['message']}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}[*] Loading representative profile from verified dossier cache...{Style.RESET_ALL}")
                        current_profile = OFFLINE_DOSSIERS.get(uname.lower(), OFFLINE_DOSSIERS["torvalds"])
                        display_target_dossier(current_profile)
                    else:
                        print(f"{Fore.RED}[!] {res.get('message', 'Failed to fetch profile.')}{Style.RESET_ALL}")
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "2":
                display_target_dossier(current_profile)
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "3":
                emails = current_profile.get("leaked_emails", [])
                print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
                print(f" 📧 COMMIT EMAIL HARVESTER: @{current_profile.get('login')}")
                print(f"========================================================================{Style.RESET_ALL}")
                if emails:
                    print(f" {Fore.RED}{Style.BRIGHT}Exposed / Recovered Direct Email Addresses:{Style.RESET_ALL}")
                    for e in emails:
                        print(f"  {Fore.RED}• {e}{Style.RESET_ALL} (Extracted from Git author metadata / public profile)")
                    print(f"\n {Fore.YELLOW}Threat Assessment:{Style.RESET_ALL} Attackers can bypass generic contact forms and")
                    print(" deliver weaponized payloads directly into the victim's primary inbox.")
                else:
                    print(f" {Fore.GREEN}[✓] No raw direct email addresses leaked in public commit events.{Style.RESET_ALL}")
                    print(" Target adheres to GitHub's private email relay protocol.")
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "4":
                display_activity_hours(current_profile)
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "5":
                display_spear_phishing_pretexts(current_profile)
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "6":
                display_opsec_evaluation(current_profile)
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "7":
                run_benchmark_audit()
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "8":
                out_path = export_target_profile_json(current_profile)
                print(f"\n{Fore.GREEN}{Style.BRIGHT}[✓] Target Dossier JSON successfully exported to:{Style.RESET_ALL}")
                print(f"    {out_path}")
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "9":
                pdf_script = os.path.join(BASE_DIR, "scripts", "generate_day05_pdf.py")
                if os.path.exists(pdf_script):
                    print(f"\n{Fore.CYAN}[*] Compiling Executive PDF Threat Report...{Style.RESET_ALL}")
                    os.system(f'"{sys.executable}" "{pdf_script}"')
                else:
                    print(f"\n{Fore.RED}[!] PDF generation script not found at {pdf_script}{Style.RESET_ALL}")
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "0":
                print(f"\n{Fore.CYAN}[*] Exiting PEER'S Target Profiler. Stay safe!{Style.RESET_ALL}\n")
                sys.exit(0)

            else:
                print(f"{Fore.RED}[!] Invalid selection. Please choose an option from 0 to 9.{Style.RESET_ALL}")
                input(f"\n{Fore.WHITE}Press [ENTER] to continue...{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}[!] Execution interrupted by user. Exiting cleanly...{Style.RESET_ALL}\n")
            sys.exit(0)


if __name__ == "__main__":
    interactive_menu()
