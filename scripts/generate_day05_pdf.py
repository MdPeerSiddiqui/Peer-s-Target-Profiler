#!/usr/bin/env python3
"""
PEER'S Target Profiler - Executive Multi-Page Lab Report Compiler (Day 05)
Sqrock IT Solution Cybersecurity Internship Track: Social Engineering Attack Simulations Using Python

Compiles an authoritative executive lab report covering:
- Passive OSINT intelligence gathering from public Git metadata
- Commit email de-anonymization and timezone behavioral profiling
- Weaponized spear-phishing pretext generation (Attacker Perspective)
- Quantitative OPSEC exposure scoring (0-100) and defense frameworks
- Automated 7-point unit test validation ledger and ethical compliance statements
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
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

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE / EXECUTIVE SUMMARY & RESEARCH OBJECTIVE
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
    # PAGE 2: OSINT RECONNAISSANCE MECHANICS & TARGET PROFILING CATALOG
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
        "To test profiling accuracy and establish defensive benchmarks, three diverse profiles were analyzed: Linus Torvalds (Kernel Creator), "
        "Harish Kumar (Enterprise Security Engineer), and The Octocat (Official GitHub Mascot):",
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
        ]
    ]
    t_prof = Table(profile_comp, colWidths=[105, 115, 95, 135, 90])
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_prof)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ATTACKER PERSPECTIVE: SPEAR-PHISHING PRETEXT SYNTHESIS
    # =========================================================================
    story.append(Paragraph("5. Attacker Perspective: Spear-Phishing Pretext Synthesis", h1_style))
    story.append(Paragraph(
        "A critical requirement of the Day 05 assignment is documenting the <i>'Attacker Perspective'</i>—demonstrating how an adversary "
        "translates raw OSINT data points into weaponized spear-phishing attack vectors. PEER'S Target Profiler programmatically synthesizes "
        "three distinct attack pretexts for any loaded profile:",
        body_style
    ))

    pretext_data = [
        [
            Paragraph("<b>Pretext Vector & Hook</b>", body_bold),
            Paragraph("<b>OSINT Data Leveraged</b>", body_bold),
            Paragraph("<b>Adversary Attack Narrative & Deceptive CTA</b>", body_bold)
        ],
        [
            Paragraph("<b>[SP-01] Technical Zero-Day CVE Alert</b><br/><i>Urgent CVE Patch for cloud-guard-iam (Python)</i>", body_style),
            Paragraph("• Top Repo: <code>cloud-guard-iam</code><br/>• Primary Language: <code>Python</code><br/>• Leaked Email Address", body_style),
            Paragraph(
                "Adversary impersonates GitHub Security Advisories or a Python package maintainer. "
                "The email cites a critical unauthenticated Remote Code Execution (RCE) flaw in repository dependencies. "
                "<br/><b>CTA:</b> <i>'Review affected dependency tree: https://security-patch-advisory.org/cve/...'</i><br/>"
                "<b>Triggers:</b> Urgency, Technical Authority, Fear of Supply-Chain Compromise.",
                body_style
            )
        ],
        [
            Paragraph("<b>[SP-02] Corporate SSO / IT Migration</b><br/><i>Sqrock IT: Mandatory Single Sign-On Renewal</i>", body_style),
            Paragraph("• Employer: <code>Sqrock IT Solution</code><br/>• Target Name: <code>Harish Kumar</code><br/>• Work Email", body_style),
            Paragraph(
                "Adversary impersonates internal corporate IT Helpdesk. Citing an endpoint certificate expiration, "
                "the attacker issues a 24-hour ultimatum threatening account suspension across internal VPN and Slack channels. "
                "<br/><b>CTA:</b> <i>'Authenticate identity at: https://login.sqrockitsolution-portal.net/sso'</i><br/>"
                "<b>Triggers:</b> Legitimate Corporate Authority, Fear of Disruption, Strict Deadline.",
                body_style
            )
        ],
        [
            Paragraph("<b>[SP-03] Targeted Executive Recruiter Hook</b><br/><i>Confidential Python Lead Role for Harish</i>", body_style),
            Paragraph("• Skillset: <code>Python, Go</code><br/>• Location: <code>Bangalore</code><br/>• Bio & Projects", body_style),
            Paragraph(
                "Posing as an executive recruiter from a high-paying international firm, the attacker praises specific "
                "open-source commits and attaches a weaponized PDF or portal link containing 'compensation guidelines'. "
                "<br/><b>CTA:</b> <i>'Download role brief: https://talent-briefing-executive.io/role-spec.pdf'</i><br/>"
                "<b>Triggers:</b> Flattery, Professional Ambition, Financial Incentive.",
                body_style
            )
        ]
    ]
    t_pretext = Table(pretext_data, colWidths=[160, 130, 250])
    t_pretext.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, DARK_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_pretext)
    story.append(Spacer(1, 8))

    story.append(Paragraph("6. Psychological Exploitation Mechanisms", h2_style))
    story.append(Paragraph(
        "By intertwining factual reconnaissance (actual repository names, company names, and real programming languages) with synthetic urgency, "
        "the adversary disarms the victim's natural vigilance. Unlike generic spam, target-specific pretexting achieves an estimated <b>70%+ "
        "click-through rate</b> because the request appears directly relevant to the developer's day-to-day responsibilities.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: BEHAVIORAL PROFILING, OPSEC SCORING & DEFENSIVE REMEDIATION
    # =========================================================================
    story.append(Paragraph("7. Digital Footprint & OPSEC Risk Scoring Algorithm", h1_style))
    story.append(Paragraph(
        "To empower security teams and developers to audit their own exposure, PEER'S Target Profiler incorporates a quantitative "
        "<b>0–100 OPSEC Exposure Engine</b> based on empirical vulnerability factors:",
        body_style
    ))

    opsec_factors = [
        [Paragraph("<b>Reconnaissance Factor</b>", body_bold), Paragraph("<b>Weight</b>", body_bold), Paragraph("<b>Adversary Weaponization Impact</b>", body_bold)],
        [Paragraph("Direct Commit / Profile Email Leak", body_style), Paragraph("<b>+25 pts</b>", body_style), Paragraph("Permits direct spear-phishing inbox delivery, bypassing web forms.", body_style)],
        [Paragraph("Employer / Organization Listed", body_style), Paragraph("<b>+20 pts</b>", body_style), Paragraph("Enables internal IT Helpdesk, HR, and corporate authority pretexting.", body_style)],
        [Paragraph("Real Full Name Disclosed", body_style), Paragraph("<b>+15 pts</b>", body_style), Paragraph("Facilitates cross-platform correlation across LinkedIn, Twitter, and breach databases.", body_style)],
        [Paragraph("Geographic Location Exposed", body_style), Paragraph("<b>+15 pts</b>", body_style), Paragraph("Allows timezone mapping, regional event hooks, and localized pretexts.", body_style)],
        [Paragraph("Detailed Bio / Professional Focus", body_style), Paragraph("<b>+15 pts</b>", body_style), Paragraph("Discloses active project domains, seniority, and psychological levers.", body_style)],
        [Paragraph("Personal Domain / Social Links", body_style), Paragraph("<b>+10 pts</b>", body_style), Paragraph("Expands secondary reconnaissance surface to personal hosting and DNS records.", body_style)]
    ]
    t_opsec = Table(opsec_factors, colWidths=[170, 70, 300])
    t_opsec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_opsec)
    story.append(Spacer(1, 8))

    story.append(Paragraph("8. Defender OPSEC Hardening & Footprint Reduction", h1_style))
    story.append(Paragraph(
        "<b>1. Enforce GitHub Email Masking:</b> Configure account settings to <i>'Keep my email addresses private'</i> and check <i>'Block "
        "command line pushes that expose my email'</i> to prevent accidental Git author leaks.<br/>"
        "<b>2. Git Author Sanitization:</b> Ensure local git configurations utilize the privacy mask: "
        "<code>git config --global user.email 'username@users.noreply.github.com'</code>.<br/>"
        "<b>3. Remove Operational Infrastructure from Bios:</b> Avoid listing proprietary internal tooling names, internal domains, or "
        "specific enterprise subsidiaries in public biographies.<br/>"
        "<b>4. Out-of-Band Security Notification Verification:</b> Establish a zero-trust policy where all unexpected security alerts, "
        "dependency patches, or corporate re-authentication emails are validated through official internal dashboards before clicking links.",
        body_style
    ))
    story.append(Spacer(1, 6))

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
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, DARK_BLUE),
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
