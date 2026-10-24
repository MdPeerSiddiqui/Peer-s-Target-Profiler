# PEER'S Target Profiler 🕵️‍♂️⚡

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Windows%20%7C%20macOS-0078D4?style=for-the-badge&logo=linux&logoColor=white)](https://kali.org)
[![Security](https://img.shields.io/badge/Security-OSINT%20%26%20Reconnaissance-red?style=for-the-badge&logo=shield)](https://sqrock.com)
[![Tests](https://img.shields.io/badge/Tests-7%2F7%20Passing-brightgreen?style=for-the-badge&logo=checkmarx)](https://github.com/MdPeerSiddiqui/Peer-s-Target-Profiler)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> **OSINT Target Dossier & Social Engineering Attack Surface Analyzer**  
> Developed by **Md Peer Siddiqui** for the **Sqrock IT Solution Cybersecurity Internship (Day 05: OSINT + SE: Build a Target Profile)**.

---

## 🎯 Executive Overview

Open-Source Intelligence (OSINT) is the critical reconnaissance phase preceding high-impact social engineering and spear-phishing operations. Before threat actors draft a deceptive email or initiate voice pretexting, they passively harvest public developer metadata, repository histories, and organizational affiliations to maximize attack credibility.

**PEER'S Target Profiler** is a production-grade, zero-crash Python CLI intelligence suite designed to:
1. Harvest and aggregate public developer profiles from public code repositories.
2. Uncover hidden email addresses leaked directly inside raw Git commit headers.
3. Fingerprint developer activity hours and infer geographical timezones.
4. Synthesize tailored spear-phishing pretexts from the **Attacker Perspective**.
5. Quantify digital footprint exposure using an empirical **0–100 OPSEC Risk Scorer**.

---

## 🚀 Key Features

* **🕵️ Target Dossier Aggregator:** Queries public GitHub developer metadata (name, organization, location, bio, follower graph, and repositories) with graceful offline fallback caching to prevent rate-limit crashes.
* **📧 Deep Commit Email Harvester:** Inspects public push event commits to recover unmasked personal and corporate email addresses that are masked on the target's web profile.
* **⏰ Activity & Timezone Fingerprinting:** Analyzes commit timestamps over a 24-hour UTC histogram to identify work/sleep cycles and deduce the target's probable geographic timezone.
* **📊 Tech Stack Quantification:** Recursively indexes repositories to compute programming language distribution percentages.
* **🎣 Spear-Phishing Pretext Generator (Attacker Perspective):** Automatically synthesizes 3 weaponized, context-aware social engineering attack angles based on real gathered OSINT:
  * **[SP-01] Technical Zero-Day CVE Alert:** Masquerading as an urgent patch for the target's active repository ecosystem.
  * **[SP-02] Corporate SSO / IT Migration:** Leveraging the target's employer for an urgent credential re-authentication lure.
  * **[SP-03] Executive Recruiter Hook:** Tailored to the developer's top programming languages with compensation bait.
* **🛡️ OPSEC & Digital Footprint Scorer (0–100):** Evaluates exposure across 6 risk vectors (Name, Employer, Location, Leaked Emails, Social Links, Bio) and provides actionable remediation guidance.
* **📁 Standardized JSON Export:** Produces the required `targets/target_profile.json` deliverable.
* **📄 Executive PDF Report Generator:** Compiles an authoritative multi-page lab report with ReportLab.

---

## 📦 Installation & Setup

### For Kali Linux / Debian / Ubuntu:
```bash
# 1. Clone the repository
git clone https://github.com/MdPeerSiddiqui/Peer-s-Target-Profiler.git
cd Peer-s-Target-Profiler

# 2. Set up a Python virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the profiler
python3 target_profiler.py
```

### For Windows (PowerShell / Command Prompt):
```powershell
# 1. Clone the repository
git clone https://github.com/MdPeerSiddiqui/Peer-s-Target-Profiler.git
cd Peer-s-Target-Profiler

# 2. Set up virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the profiler
python target_profiler.py
```

---

## 🎮 CLI Master Control Menu

```text
========================================================================
 ⚡ OSINT TARGET DOSSIER & SOCIAL ENGINEERING ATTACK SURFACE ANALYZER ⚡
 Developed by: Md Peer Siddiqui | Sqrock IT Solution Internship (Day 05)
========================================================================

 Master Options:
  [1] Profile Target by GitHub Username (Live API or Cache)
  [2] Inspect Target Dossier & Tech Stack Breakdown
  [3] Deep Commit Email & Identity Leak Harvester
  [4] Activity Hours & Timezone Behavioral Analysis
  [5] Generate Tailored Spear-Phishing Pretexts (Attacker View)
  [6] OPSEC Risk & Digital Footprint Exposure Scorer
  [7] Run Benchmark Audit Across 3 Reference Profiles
  [8] Export Target Dossier to JSON (target_profile.json)
  [9] Compile Executive PDF Threat Report (Day 05)
  [0] Exit Profiler
```

---

## 🧪 Automated Testing

The suite includes 7 automated unit tests verifying schema adherence, OPSEC scoring bounds, spear-phishing pretext generation, timezone analysis, and JSON exports.

Run tests via:
```bash
python -m unittest tests/test_profiler.py -v
```

**Test Output:**
```
test_activity_timezone_analysis (tests.test_profiler.TestTargetProfiler) ... ok
test_email_harvesting_filtering (tests.test_profiler.TestTargetProfiler) ... ok
test_json_deliverable_export (tests.test_profiler.TestTargetProfiler) ... ok
test_offline_dossiers_exist_and_valid (tests.test_profiler.TestTargetProfiler) ... ok
test_opsec_score_bounds_and_tiering (tests.test_profiler.TestTargetProfiler) ... ok
test_profile_empty_languages_fallback (tests.test_profiler.TestTargetProfiler) ... ok
test_spear_phishing_pretext_generation (tests.test_profiler.TestTargetProfiler) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```

---

## 📁 Repository Structure

```
Peer-s-Target-Profiler/
├── target_profiler.py       # Core interactive CLI intelligence suite
├── requirements.txt         # Dependencies (requests, colorama, reportlab)
├── LICENSE                  # MIT License
├── README.md                # Comprehensive documentation
├── .gitignore               # Python and environment exclusions
├── targets/
│   └── target_profile.json  # Exported target profile deliverable
├── tests/
│   └── test_profiler.py     # 7-point automated unit test suite
├── scripts/
│   └── generate_day05_pdf.py# Executive ReportLab PDF compiler
└── reports/
    └── Day05_OSINT_Target_Profile_Report_Sqrock_MdPeerSiddiqui.pdf
```

---

## 🛡️ Ethical Compliance & Disclaimer

> **NOTICE:** This tool and its simulation models are developed strictly for **authorized educational, awareness training, and academic research purposes** under the **Sqrock IT Solution Cybersecurity Internship Program**.  
> The intelligence techniques demonstrate passive open-source reconnaissance to help developers identify public exposure and harden operational security (OPSEC). Unauthorized profiling, stalking, or spear-phishing targeting individuals or organizations without explicit prior consent is strictly prohibited under the **Information Technology Act 2000 (India)** and international cybersecurity regulations.

---

## 👤 Author

* **Md Peer Siddiqui**
* **Cybersecurity Intern at Sqrock IT Solution**
* **GitHub:** [@MdPeerSiddiqui](https://github.com/MdPeerSiddiqui)
* **LinkedIn:** [Md Peer Siddiqui](https://linkedin.com)
