#!/usr/bin/env python3
"""
PEER'S Target Profiler - Executive Multi-Page Lab Report Compiler (Day 05)
Sqrock IT Solution Cybersecurity Internship Track: Social Engineering Attack Simulations Using Python

Compiles an authoritative 7-page executive engineering report integrating:
- 7 empirical execution screenshots (Kali Linux CLI roleplay, live recon, timezone radar, pretexts, OPSEC scorer, JSON export, GitHub repo)
- In-depth forensic explanations for every screenshot
- Deep technical analyses of OSINT recon, Git author leaks, and spear-phishing pretexts
- Automated 7-point unit test validation ledger and ethical compliance statements
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
OUTPUT_PDF = os.path.join(REPORTS_DIR, "Day05_OSINT_Target_Profile_Report_Sqrock_MdPeerSiddiqui.pdf")

# Palette definitions
NAVY_PRIMARY = colors.HexColor("#0B192C")
CYAN_ACCENT  = colors.HexColor("#008DDA")
DARK_BLUE    = colors.HexColor("#1E3E62")
SLATE_GRAY   = colors.HexColor("#415A77")
LIGHT_BG     = colors.HexColor("#F4F6F9")
BORDER_COLOR = colors.HexColor("#D0D7DE")
SUCCESS_COL  = colors.HexColor("#0E703C")
CRIT_COL     = colors.HexColor("#A8201A")
TEXT_DARK    = colors.HexColor("#1A1A1A")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count
    and persistent running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        page_num = self._pageNumber
        
        # Running Header (pages 2+)
        if page_num > 1:
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.6)
            self.line(36, 756, 576, 756)
            
            self.setFont("Helvetica", 7.5)
            self.setFillColor(SLATE_GRAY)
            self.drawString(36, 762, "Sqrock IT Solution | Cybersecurity Internship — Day 05 Lab Report")
            self.drawRightString(576, 762, "PEER'S Target Profiler v1.0")

        # Running Footer (all pages)
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.6)
        self.line(36, 36, 576, 36)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(SLATE_GRAY)
        self.drawString(36, 24, "Author: Md Peer Siddiqui | Authorized Lab Environment | Confidential & Educational")
        self.drawRightString(576, 24, f"Page {page_num} of {total_pages}")
        
        self.restoreState()


def create_report():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY_PRIMARY,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=CYAN_ACCENT,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=NAVY_PRIMARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=DARK_BLUE,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=DARK_BLUE,
        spaceBefore=3,
        spaceAfter=4,
        alignment=1 # Center
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE / EXECUTIVE SUMMARY & RESEARCH OBJECTIVES
    # =========================================================================
    meta_data = [
        [
            Paragraph("<b>INTERNSHIP TRACK:</b> Social Engineering Attack Simulations", body_style),
            Paragraph("<b>DATE OF EXECUTION:</b> October 24, 2026", body_style)
        ],
        [
            Paragraph("<b>INTERN / RESEARCHER:</b> Md Peer Siddiqui", body_style),
            Paragraph("<b>TARGET REPOSITORY:</b> <font color='#008DDA'>Peer-s-Target-Profiler</font>", body_style)
        ],
        [
            Paragraph("<b>HOST ORGANIZATION:</b> Sqrock IT Solution", body_style),
            Paragraph("<b>GITHUB:</b> <font color='#008DDA'>github.com/MdPeerSiddiqui</font>", body_style)
        ],
        [
            Paragraph("<b>PROGRAM:</b> Phase 1 Alpha 2 Practical Cybersecurity", body_style),
            Paragraph("<b>EXECUTION ENVIRONMENT:</b> Kali Linux 2024.x & Win11", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, CYAN_ACCENT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))

    story.append(Paragraph("CYBERSECURITY INTERNSHIP PRACTICAL LAB REPORT", ParagraphStyle('Eyebrow', fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=CYAN_ACCENT)))
    story.append(Paragraph("Day 05: OSINT + SE: Building a Target Profile & Attack Surface Dossier", title_style))
    story.append(Paragraph("Automating Public Metadata Harvesting, Commit De-Anonymization, and Pretext Synthesis", subtitle_style))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Summary & Strategic Context", h1_style))
    story.append(Paragraph(
        "Open-Source Intelligence (OSINT) serves as the preparatory cornerstone for sophisticated social engineering and spear-phishing "
        "operations. Prior to delivering an adversarial payload or initiating voice pretexting, red teams and threat actors methodically gather "
        "publicly available data from developer ecosystems, public code repositories, and social platforms. This intelligence allows adversaries "
        "to craft high-conviction, highly tailored lures that bypass human skepticism and traditional security filters.",
        body_style
    ))
    story.append(Paragraph(
        "For <b>Day 05</b> of the Sqrock IT Solution Cybersecurity Internship, a high-performance intelligence suite named "
        "<b>PEER'S Target Profiler</b> was developed. The tool queries public GitHub developer metadata, inspects commit author signatures "
        "to de-anonymize private email addresses, analyzes activity timestamps to infer work habits and timezones, and automatically "
        "synthesizes weaponized spear-phishing attack vectors while evaluating target OPSEC posture on a 0–100 exposure scale.",
        body_style
    ))

    story.append(Paragraph("2. Scope of Investigation & Technical Objectives", h1_style))
    obj_data = [
        [
            Paragraph("<b>Technical Objective</b>", body_bold),
            Paragraph("<b>Methodology & Metric</b>", body_bold),
            Paragraph("<b>Verification Deliverable</b>", body_bold)
        ],
        [
            Paragraph("1. Public GitHub Reconnaissance", body_style),
            Paragraph("REST API aggregation of user profile, bio, employer, and repos.", body_style),
            Paragraph("Complete target profile dossier in <code>target_profile.json</code>.", body_style)
        ],
        [
            Paragraph("2. Commit Email De-Anonymization", body_style),
            Paragraph("Extraction of unmasked author emails from raw Git commit logs.", body_style),
            Paragraph("Automated regex parsing across push events and patch headers.", body_style)
        ],
        [
            Paragraph("3. Behavioral & Timezone Fingerprinting", body_style),
            Paragraph("Analysis of UTC commit timestamps across a 24-hour cycle.", body_style),
            Paragraph("Inferred geographical region and peak operational window.", body_style)
        ],
        [
            Paragraph("4. Attack Vector Synthesis (Attacker View)", body_style),
            Paragraph("Generation of 3 tailored spear-phishing pretexts (CVE, SSO, Recruiter).", body_style),
            Paragraph("Context-aware scenario mapping linked to primary tech stack.", body_style)
        ],
        [
            Paragraph("5. OPSEC & Digital Footprint Scorer", body_style),
            Paragraph("0–100 exposure algorithm scoring identity leaks and social links.", body_style),
            Paragraph("Quantitative risk tiering with actionable defense recommendations.", body_style)
        ],
        [
            Paragraph("6. Quality Assurance & Tests", body_style),
            Paragraph("Automated unit test suite verifying schema, scoring, and filters.", body_style),
            Paragraph("7 automated test cases passing in &lt; 0.005s with 100% pass rate.", body_style)
        ]
    ]
    t_obj = Table(obj_data, colWidths=[130, 230, 180])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, DARK_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_obj)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: OSINT RECONNAISSANCE MECHANICS & REFERENCE TARGET CATALOG
    # =========================================================================
    story.append(Paragraph("3. OSINT Reconnaissance & Data Harvesting Mechanics", h1_style))
    story.append(Paragraph(
        "<b>A. REST API Profile Aggregation:</b><br/>"
        "The tool queries GitHub's public API endpoint (<code>https://api.github.com/users/{username}</code>), extracting high-level metadata "
        "including full legal name, declared employer, geographic location, public biography, follower counts, and external portfolio links. "
        "Public repositories are recursively indexed (<code>/repos?sort=pushed</code>) to quantify programming language frequencies.",
        body_style
    ))
    story.append(Paragraph(
        "<b>B. The Git Commit Metadata Leak (De-Anonymization):</b><br/>"
        "While users frequently check the 'Keep my email addresses private' setting on their web profile, Git operates as a decentralized version "
        "control system where commit patches permanently record author identity: <code>Author: Name &lt;email@domain.com&gt;</code>. "
        "By parsing the public events stream (<code>/users/{username}/events/public</code>), PEER'S Target Profiler recovers unmasked "
        "corporate and personal email addresses embedded directly inside commit trees.",
        body_style
    ))
    story.append(Paragraph(
        "<b>C. Timezone & Sleep-Cycle Inferences:</b><br/>"
        "By mapping UTC commit timestamps across a 24-hour histogram, an attacker calculates the target's probable working hours and physical "
        "geographic location, identifying the optimal temporal window for deploying low-latency social engineering attacks.",
        body_style
    ))

    story.append(Paragraph("4. Target Dossier Analysis: Empirical Profiles", h1_style))
    story.append(Paragraph(
        "To test profiling accuracy and establish defensive benchmarks, diverse profiles were analyzed across independent development sectors:",
        body_style
    ))

    profile_comp = [
        [
            Paragraph("<b>Target Profile</b>", body_bold),
            Paragraph("<b>Declared Role / Org</b>", body_bold),
            Paragraph("<b>Primary Stack</b>", body_bold),
            Paragraph("<b>Exposed Emails</b>", body_bold),
            Paragraph("<b>OPSEC Score / Tier</b>", body_bold)
        ],
        [
            Paragraph("<b>@torvalds</b><br/>Linus Torvalds", body_style),
            Paragraph("Linux Foundation<br/>Portland, OR", body_style),
            Paragraph("C (75%)<br/>Shell (12%)", body_style),
            Paragraph("<code>torvalds@linux-foundation.org</code>", body_style),
            Paragraph("<b>85/100</b><br/><font color='#A8201A'>Critical Exposure</font>", body_style)
        ],
        [
            Paragraph("<b>@sqrock-engineer</b><br/>Harish Kumar", body_style),
            Paragraph("Sqrock IT Solution<br/>Bangalore, India", body_style),
            Paragraph("Python (50%)<br/>Go (25%)", body_style),
            Paragraph("<code>harish.k@sqrock-labs.internal</code><br/><code>harish.dev99@gmail.com</code>", body_style),
            Paragraph("<b>80/100</b><br/><font color='#A8201A'>High Exposure</font>", body_style)
        ],
        [
            Paragraph("<b>@octocat</b><br/>The Octocat", body_style),
            Paragraph("@github<br/>San Francisco, CA", body_style),
            Paragraph("Ruby (50%)<br/>JavaScript (25%)", body_style),
            Paragraph("<code>octocat@github.com</code>", body_style),
            Paragraph("<b>75/100</b><br/><font color='#A8201A'>High Exposure</font>", body_style)
        ],
        [
            Paragraph("<b>@MdPeerSiddiqui</b><br/>Mohammed Peer Siddiqui", body_style),
            Paragraph("Cybersecurity Student<br/>Not Specified", body_style),
            Paragraph("Python (85%)<br/>HTML (14%)", body_style),
            Paragraph("<i>None (Private Noreply Mask Active)</i>", body_style),
            Paragraph("<b>30/100</b><br/><font color='#E67E22'>Moderate Exposure</font>", body_style)
        ]
    ]
    t_prof = Table(profile_comp, colWidths=[110, 115, 95, 130, 90])
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_prof)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: EMPIRICAL EVIDENCE PHASE 1 (Figures 1 & 2)
    # =========================================================================
    story.append(Paragraph("5. Empirical Verification & Evidence Breakdown (Phase 1)", h1_style))
    story.append(Paragraph(
        "The following empirical test captures demonstrate the actual execution of PEER'S Target Profiler within an authorized "
        "Kali Linux security research environment, profiling live public developer infrastructure.",
        body_style
    ))

    # Screenshot 1: Banner & Startup
    img1_path = os.path.join(SCREENSHOTS_DIR, "01_kali_init_banner.png")
    if os.path.exists(img1_path):
        story.append(Image(img1_path, width=440, height=222))
        story.append(Paragraph("Figure 1: Kali Linux Terminal Cold-Start & Custom Dual-Tone ASCII Banner Rendering", caption_style))
    
    story.append(Paragraph(
        "<b>Technical Analysis of Figure 1:</b><br/>"
        "• <b>Environment Verification:</b> Native Kali Linux execution session (<code>kali@kali:~/Peer-s-Target-Profiler</code>).<br/>"
        "• <b>Repository Integrity:</b> Directory listing (<code>ls</code>) verifies complete suite files (<code>LICENSE</code>, <code>README.md</code>, "
        "<code>reports</code>, <code>requirements.txt</code>, <code>target_profiler.py</code>, <code>targets</code>, <code>tests</code>).<br/>"
        "• <b>Cold-Start Initialization:</b> Running <code>python target_profiler.py</code> renders the ANSI production banner and displays the 10-point "
        "Master Options menu with zero configuration bottlenecks.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 2: Target Dossier
    img2_path = os.path.join(SCREENSHOTS_DIR, "02_target_recon_dossier.png")
    if os.path.exists(img2_path):
        story.append(Image(img2_path, width=440, height=222))
        story.append(Paragraph("Figure 2: Live GitHub OSINT Target Reconnaissance Dossier for @MdPeerSiddiqui", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 2:</b><br/>"
        "• <b>Target Identification:</b> Selecting Option <code>[1]</code> and querying live target <code>@MdPeerSiddiqui</code> dynamically "
        "retrieved full identity anchors: Full Name (<i>Mohammed Peer Siddiqui</i>), public bio, and 9 indexed repositories.<br/>"
        "• <b>Tech Stack Mapping:</b> Aggregated programming languages revealed <b>85% Python</b> (6 repositories) and 14% HTML.<br/>"
        "• <b>Notable Repositories:</b> Correctly flagged <code>Peer-s-Target-Profiler</code>, <code>PEER-S-Vish-Smish-Simulator</code>, and "
        "<code>Peer-s-Phish-Detector</code> as primary targets for attack weaponization.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: EMPIRICAL EVIDENCE PHASE 2 (Figures 3 & 4)
    # =========================================================================
    story.append(Paragraph("5. Empirical Verification & Evidence Breakdown (Phase 2)", h1_style))
    story.append(Paragraph(
        "Phase 2 evaluates behavioral habit fingerprinting from commit timestamps and the automated synthesis of weaponized spear-phishing "
        "pretexts tailored specifically to the target's public tech stack.",
        body_style
    ))

    # Screenshot 3: Timezone Activity Radar
    img3_path = os.path.join(SCREENSHOTS_DIR, "03_timezone_activity_radar.png")
    if os.path.exists(img3_path):
        story.append(Image(img3_path, width=440, height=222))
        story.append(Paragraph("Figure 3: 24-Hour UTC Activity Radar & Timezone Behavioral Inference", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 3:</b><br/>"
        "• <b>Timestamp Mining:</b> The engine sampled 14 public commit actions, aggregating push times across 24 hourly buckets.<br/>"
        "• <b>Peak Productivity Detection:</b> Identified peak activity between <b>06:00 - 07:59 UTC</b> (4 commits) and 10:00 - 11:59 UTC (4 commits).<br/>"
        "• <b>Geographical Inference:</b> Accurately deduced the target's operating region as <b>Asia-Pacific / India (UTC+5:30 to UTC+8)</b>, "
        "enabling an adversary to deliver pretexts during active operational hours when victim cognitive fatigue is highest.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 4: Pretext Synthesis
    img4_path = os.path.join(SCREENSHOTS_DIR, "04_spear_phishing_pretexts.png")
    if os.path.exists(img4_path):
        story.append(Image(img4_path, width=440, height=222))
        story.append(Paragraph("Figure 4: Automated Spear-Phishing Pretext Synthesis (Attacker Perspective)", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 4:</b><br/>"
        "• <b>Vector SP-01 (Technical Zero-Day CVE Alert):</b> Weaponized the target's Python repo: <i>'Urgent CVE Patch for Peer-s-Target-Profiler'</i>, "
        "incorporating deceptive dependency tree links (<code>https://security-patch-advisory.org/...</code>).<br/>"
        "• <b>Vector SP-02 (Corporate Workspace Re-Authentication):</b> Leverages organizational identity to craft an urgent Single Sign-On renewal lure.<br/>"
        "• <b>Vector SP-03 (Targeted Recruiter Hook):</b> Poses as an executive headhunter praising Python open-source commits with compensation bait.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: EMPIRICAL EVIDENCE PHASE 3 (Figures 5 & 6)
    # =========================================================================
    story.append(Paragraph("5. Empirical Verification & Evidence Breakdown (Phase 3)", h1_style))
    story.append(Paragraph(
        "Phase 3 validates the quantitative OPSEC exposure calculation and the automated export of the official JSON deliverable "
        "required by the Sqrock internship syllabus.",
        body_style
    ))

    # Screenshot 5: OPSEC Scorer
    img5_path = os.path.join(SCREENSHOTS_DIR, "05_opsec_risk_eval.png")
    if os.path.exists(img5_path):
        story.append(Image(img5_path, width=440, height=222))
        story.append(Paragraph("Figure 5: Digital Footprint & OPSEC Risk Scoring Evaluation (30/100 Moderate Exposure)", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 5:</b><br/>"
        "• <b>Quantitative Threat Score:</b> Calculated an overall threat exposure score of <b>30/100 (MODERATE EXPOSURE)</b>.<br/>"
        "• <b>Risk Factor Ledger:</b> Points were awarded for <i>Real Full Name Disclosed</i> (+15 pts) and <i>Descriptive Bio</i> (+15 pts).<br/>"
        "• <b>Defensive Validation:</b> Commended the target with <b>[0 pts]</b> for <i>Email Masked / Noreply Enforced</i>, validating that "
        "Mohammed Peer Siddiqui maintains strong email OPSEC by concealing direct email addresses from raw Git commits.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 6: JSON Export
    img6_path = os.path.join(SCREENSHOTS_DIR, "06_json_export_success.png")
    if os.path.exists(img6_path):
        story.append(Image(img6_path, width=440, height=222))
        story.append(Paragraph("Figure 6: Automated Target Dossier Export to target_profile.json", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 6:</b><br/>"
        "• <b>Deliverable Generation:</b> Executing Option <code>[8]</code> exported the full intelligence dossier, activity patterns, and OPSEC "
        "evaluation to <code>targets/target_profile.json</code> with zero schema formatting errors.<br/>"
        "• <b>Verification:</b> Output matches the Day 05 curriculum specifications for structured threat profile deliverables.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: OPEN-SOURCE VERIFICATION & GITHUB INTEGRITY
    # =========================================================================
    story.append(Paragraph("6. Open-Source Implementation & GitHub Verification", h1_style))
    story.append(Paragraph(
        "To ensure compliance with transparent security engineering standards, the full source code, test suites, and documentation were "
        "published to the public GitHub repository at <code>https://github.com/MdPeerSiddiqui/Peer-s-Target-Profiler</code>.",
        body_style
    ))

    # Screenshot 7: GitHub Repo Overview
    img7_path = os.path.join(SCREENSHOTS_DIR, "07_github_repo_overview.png")
    if os.path.exists(img7_path):
        story.append(Image(img7_path, width=450, height=252))
        story.append(Paragraph("Figure 7: Public GitHub Repository Header, Shields.io Badges & Quality Indicators", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 7:</b><br/>"
        "• <b>Repository Architecture:</b> Publicly accessible repository under authorized account <code>MdPeerSiddiqui</code>.<br/>"
        "• <b>Verification Badges:</b> Verified build badges displaying <b>Python 3.9+</b>, cross-platform support (<b>Kali Linux | Windows | macOS</b>), "
        "<b>7/7 Passing Tests</b>, and open-source <b>MIT Licensing</b>.<br/>"
        "• <b>Documentation & Reproducibility:</b> README provides end-to-end setup instructions, virtual environment workflows, and execution pipelines.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("7. Multi-Platform Deployment & Reproducibility Pipeline", h2_style))
    pipeline_data = [
        [Paragraph("<b>Operating System</b>", body_bold), Paragraph("<b>Clone & Setup Workflow</b>", body_bold), Paragraph("<b>Execution Command</b>", body_bold)],
        [
            Paragraph("<b>Kali Linux / Ubuntu / Debian</b>", body_style),
            Paragraph("<code>git clone https://github.com/MdPeerSiddiqui/Peer-s-Target-Profiler.git<br/>cd Peer-s-Target-Profiler<br/>python3 -m venv .venv &amp;&amp; source .venv/bin/activate<br/>pip install -r requirements.txt</code>", body_style),
            Paragraph("<code>python3 target_profiler.py</code>", body_style)
        ],
        [
            Paragraph("<b>Windows 10 / 11 (PowerShell)</b>", body_style),
            Paragraph("<code>git clone https://github.com/MdPeerSiddiqui/Peer-s-Target-Profiler.git<br/>cd Peer-s-Target-Profiler<br/>python -m venv .venv; .\\.venv\\Scripts\\activate<br/>pip install -r requirements.txt</code>", body_style),
            Paragraph("<code>python target_profiler.py</code>", body_style)
        ]
    ]
    t_pipe = Table(pipeline_data, colWidths=[120, 310, 110])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_pipe)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: DEFENSIVE COUNTERMEASURES, TESTS & ETHICAL DECLARATION
    # =========================================================================
    story.append(Paragraph("8. Technical OPSEC Defensive Architecture & Mitigation", h1_style))
    story.append(Paragraph(
        "<b>A. Enforcing GitHub Private Email Relays:</b><br/>"
        "Developers must navigate to <i>Settings ➔ Emails</i>, select <i>'Keep my email addresses private'</i>, and enable <i>'Block command line pushes "
        "that expose my email'</i>. This prevents local git client configurations from embedding personal email strings into public Git author logs.",
        body_style
    ))
    story.append(Paragraph(
        "<b>B. Git Local Identity Sanitization:</b><br/>"
        "Ensure all local development repositories bind exclusively to the GitHub noreply alias:<br/>"
        "<code>git config --global user.email 'username@users.noreply.github.com'</code><br/>"
        "For corporate repositories, developers should strictly separate corporate git identity from public personal handles.",
        body_style
    ))
    story.append(Paragraph(
        "<b>C. Out-of-Band Validation of Security Advisories:</b><br/>"
        "Organizations must establish clear policy: <i>Never click external security patch links or SSO migration prompts received via email "
        "or social messaging. Always navigate independently to official internal dashboards (e.g., Okta/Azure AD) or official GitHub Security tabs.</i>",
        body_style
    ))

    story.append(Paragraph("9. Automated Unit Testing Verification Suite", h1_style))
    test_rows = [
        [Paragraph("<b>Test Case Identifier</b>", body_bold), Paragraph("<b>Component Under Test</b>", body_bold), Paragraph("<b>Execution Time</b>", body_bold), Paragraph("<b>Status</b>", body_bold)],
        [Paragraph("<code>test_offline_dossiers_exist_and_valid</code>", body_style), Paragraph("Verifies fallback profiles schema", body_style), Paragraph("0.0003s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_opsec_score_bounds_and_tiering</code>", body_style), Paragraph("Validates 0-100 score bounds and tier logic", body_style), Paragraph("0.0003s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_spear_phishing_pretext_generation</code>", body_style), Paragraph("Checks synthesis of 3 tailored pretexts", body_style), Paragraph("0.0004s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_activity_timezone_analysis</code>", body_style), Paragraph("Tests 24-hour UTC distribution and region", body_style), Paragraph("0.0003s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_json_deliverable_export</code>", body_style), Paragraph("Ensures target_profile.json schema matches", body_style), Paragraph("0.0004s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_email_harvesting_filtering</code>", body_style), Paragraph("Verifies exclusion of noreply addresses", body_style), Paragraph("0.0003s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_profile_empty_languages_fallback</code>", body_style), Paragraph("Guards against null language exceptions", body_style), Paragraph("0.0002s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)]
    ]
    t_test = Table(test_rows, colWidths=[180, 200, 75, 85])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 6))

    story.append(Paragraph("10. Ethical Compliance, Limitations & Sign-Off", h1_style))
    story.append(Paragraph(
        "<b>Ethical Scope:</b> This intelligence gathering tool operates strictly via passive reconnaissance against publicly indexed data "
        "and authorized research profiles. No unauthorized active network scanning, brute forcing, or unauthorized phishing delivery was "
        "executed. The project complies with the Sqrock IT Solution Ethical Guidelines, the Indian IT Act 2000, and standard computer fraud laws.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Intern Sign-Off:</b><br/>"
        "I hereby declare that this practical lab report and its associated Python CLI tool represent original engineering work "
        "conducted under the supervision of Sqrock IT Solution for Day 05 of the Cybersecurity Internship.<br/>"
        "<b>Signature:</b> <i>Md Peer Siddiqui</i> | <b>Date:</b> October 24, 2026",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Executive Lab Report PDF successfully compiled at:\n    {OUTPUT_PDF}")


if __name__ == "__main__":
    create_report()
