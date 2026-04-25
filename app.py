"""
Caseware Cloud Migration Readiness Assessor
============================================
A discovery-stage tool for Professional Services consultants to assess
an accounting firm's readiness to migrate from Caseware Working Papers
(desktop) to Caseware Cloud.

Built by Hammad Mirza | Portfolio Project for Caseware PS Consultant Role
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG & STYLING
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Caseware Cloud Migration Readiness Assessor",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');

    .main { background-color: #f8f9fc; }

    .header-banner {
        background: linear-gradient(135deg, #1a3c5e 0%, #2d6a9f 50%, #1a3c5e 100%);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .header-banner h1 {
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 0.3rem;
        color: white;
    }
    .header-banner p {
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 300;
        font-size: 1.05rem;
        opacity: 0.9;
        margin: 0;
    }

    .section-header {
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        color: #1a3c5e;
        border-bottom: 3px solid #2d6a9f;
        padding-bottom: 0.4rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #2d6a9f;
        margin-bottom: 1rem;
    }

    .risk-flag {
        background: #fff3f0;
        border-left: 4px solid #e74c3c;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    .risk-flag-medium {
        background: #fffbf0;
        border-left: 4px solid #f39c12;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    .strength-flag {
        background: #f0faf4;
        border-left: 4px solid #27ae60;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }

    .recommendation-box {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%);
        border: 1px solid #c5d5ea;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .footer-note {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
    }

    div[data-testid="stExpander"] {
        background: white;
        border-radius: 10px;
        border: 1px solid #e8ecf1;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <h1>☁️ Caseware Cloud Migration Readiness Assessor</h1>
    <p>Professional Services Discovery Tool — Desktop Working Papers → Caseware Cloud</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
> **Purpose:** This tool supports the discovery phase of a Caseware Cloud implementation 
> engagement. It helps PS consultants assess a firm's current environment, identify migration 
> risks early, and recommend a structured adoption approach — before the first SOW is drafted.
""")

# ─────────────────────────────────────────────────────────────
# SIDEBAR — FIRM PROFILE (CONTEXT, NOT SCORED)
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏢 Firm Profile")
    st.caption("Context for the assessment — helps tailor recommendations.")

    firm_name = st.text_input("Firm Name", placeholder="e.g., Baker & Associates LLP")
    
    firm_size = st.selectbox(
        "Firm Size (Professional Staff)",
        ["Select...", "Solo practitioner (1)", "Small (2–10)", "Mid-size (11–50)", 
         "Large (51–200)", "Enterprise (200+)"]
    )
    
    primary_services = st.multiselect(
        "Primary Service Lines",
        ["Audit & Assurance", "Review & Compilation", "Tax Compliance", 
         "Tax Planning & Advisory", "Bookkeeping / Accounting Services",
         "Corporate Finance / Advisory", "Forensic Accounting",
         "Estate & Trust", "Not-for-Profit / Public Sector"]
    )
    
    client_count = st.selectbox(
        "Approximate Client Engagements / Year",
        ["Select...", "Under 50", "50–150", "150–500", "500–1,000", "1,000+"]
    )

    regulated_clients = st.radio(
        "Do you serve publicly listed or regulated entities?",
        ["No", "Some (< 25%)", "Significant portion (25%+)"]
    )

    st.markdown("---")
    st.caption("Built by **Hammad Mirza**")
    st.caption("Portfolio Project · April 2026")


# ─────────────────────────────────────────────────────────────
# ASSESSMENT SECTIONS
# ─────────────────────────────────────────────────────────────

scores = {}  # category -> (score, max_score)
risk_flags = []
strengths = []

# ═══════════════════════════════════════════════════════════
# SECTION 1: CURRENT TECHNOLOGY ENVIRONMENT
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="section-header">1. Current Technology Environment</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    current_software = st.selectbox(
        "Current engagement management software",
        ["Select...", "Caseware Working Papers (Desktop)", 
         "Caseware Working Papers + IDEA",
         "CCH Engagement / ProSystem fx", 
         "Thomson Reuters Practice CS",
         "Manual / Excel-based workflows",
         "Other / Mixed"]
    )
    
    wp_version = st.selectbox(
        "If using Working Papers, approximate version",
        ["N/A", "Current (within last 2 years)", 
         "1–3 versions behind", "3+ versions behind", "Unsure"]
    )

with col2:
    cloud_adoption = st.selectbox(
        "Current cloud tool usage (any business tools)",
        ["Select...", "Fully cloud-native (M365, cloud accounting, etc.)",
         "Hybrid — some cloud, some desktop",
         "Primarily desktop / on-premise",
         "Minimal technology adoption overall"]
    )
    
    it_support = st.selectbox(
        "IT support model",
        ["Select...", "In-house IT team", "Managed IT provider (MSP)", 
         "Partner/staff handles IT informally", "No dedicated IT support"]
    )

# Score Section 1
s1_score, s1_max = 0, 20

if current_software == "Caseware Working Papers (Desktop)":
    s1_score += 5
    strengths.append("Already on Caseware Working Papers — migration path via CloudBridge is well-defined.")
elif current_software == "Caseware Working Papers + IDEA":
    s1_score += 5
    strengths.append("Using both Working Papers and IDEA — strong Caseware ecosystem familiarity.")
elif current_software == "Manual / Excel-based workflows":
    s1_score += 1
    risk_flags.append(("High", "Manual/Excel workflows require significant process re-engineering before cloud migration."))
elif current_software == "CCH Engagement / ProSystem fx":
    s1_score += 3
    risk_flags.append(("Medium", "Migrating from a competitor platform requires data conversion planning and staff retraining."))
elif current_software != "Select...":
    s1_score += 2

if wp_version == "Current (within last 2 years)":
    s1_score += 5
    strengths.append("Working Papers version is current — CloudBridge compatibility is maximized.")
elif wp_version == "1–3 versions behind":
    s1_score += 3
    risk_flags.append(("Medium", "Working Papers version may need upgrading before CloudBridge migration is supported."))
elif wp_version == "3+ versions behind":
    s1_score += 1
    risk_flags.append(("High", "Significantly outdated Working Papers version — upgrade required before cloud migration."))

if cloud_adoption == "Fully cloud-native (M365, cloud accounting, etc.)":
    s1_score += 5
    strengths.append("Firm is already cloud-native — adoption friction will be low.")
elif cloud_adoption == "Hybrid — some cloud, some desktop":
    s1_score += 4
elif cloud_adoption == "Primarily desktop / on-premise":
    s1_score += 2
    risk_flags.append(("Medium", "Desktop-first culture may require additional change management during migration."))
elif cloud_adoption == "Minimal technology adoption overall":
    s1_score += 1
    risk_flags.append(("High", "Low overall technology adoption — foundational IT readiness work needed before cloud migration."))

if it_support == "In-house IT team":
    s1_score += 5
elif it_support == "Managed IT provider (MSP)":
    s1_score += 4
elif it_support == "Partner/staff handles IT informally":
    s1_score += 2
    risk_flags.append(("Medium", "No formal IT support — migration may strain partner bandwidth. Consider MSP engagement."))
elif it_support == "No dedicated IT support":
    s1_score += 1
    risk_flags.append(("High", "No IT support structure — cloud migration will require external implementation support."))

scores["Technology Environment"] = (s1_score, s1_max)


# ═══════════════════════════════════════════════════════════
# SECTION 2: WORKFLOW & PROCESS STANDARDIZATION
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="section-header">2. Workflow & Process Standardization</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    template_usage = st.selectbox(
        "Engagement template standardization",
        ["Select...", "Fully standardized templates across all engagements",
         "Mostly standardized with some partner-specific variations",
         "Significant variation — each partner/manager has their own approach",
         "No standardized templates"]
    )
    
    methodology = st.selectbox(
        "Audit methodology alignment",
        ["Select...", "CAS / CSAE (Canadian standards)",
         "ISA (International Standards on Auditing)",
         "AICPA (US standards)", 
         "Multiple standards depending on engagement",
         "No formal methodology framework"]
    )

with col2:
    tb_import = st.selectbox(
        "Trial balance import process",
        ["Select...", "Automated import from accounting software (API/connector)",
         "Semi-automated (export CSV, import to WP)",
         "Manual entry / Excel copy-paste",
         "Varies by client"]
    )
    
    rollforward = st.selectbox(
        "Year-end rollforward process",
        ["Select...", "Automated rollforward in current software",
         "Semi-manual (rollforward + manual cleanup)",
         "Fully manual rebuild each year",
         "N/A"]
    )

# Score Section 2
s2_score, s2_max = 0, 20

if template_usage == "Fully standardized templates across all engagements":
    s2_score += 5
    strengths.append("Standardized templates — cloud template migration will be efficient.")
elif template_usage == "Mostly standardized with some partner-specific variations":
    s2_score += 4
elif template_usage == "Significant variation — each partner/manager has their own approach":
    s2_score += 2
    risk_flags.append(("Medium", "Template fragmentation — consolidation recommended before migration to avoid carrying tech debt to cloud."))
elif template_usage == "No standardized templates":
    s2_score += 1
    risk_flags.append(("High", "No standardized templates — cloud migration is an opportunity to establish firm-wide standards, but adds project scope."))

if methodology == "CAS / CSAE (Canadian standards)":
    s2_score += 5
    strengths.append("CAS-aligned methodology — Caseware Cloud's PEG-based Canadian content is a direct fit.")
elif methodology == "ISA (International Standards on Auditing)":
    s2_score += 5
elif methodology == "Multiple standards depending on engagement":
    s2_score += 3
    risk_flags.append(("Medium", "Multi-standard environment — template configuration will need to support multiple methodologies."))
elif methodology == "No formal methodology framework":
    s2_score += 1
    risk_flags.append(("High", "No formal methodology — this must be established before or during implementation."))
elif methodology != "Select...":
    s2_score += 4

if tb_import == "Automated import from accounting software (API/connector)":
    s2_score += 5
    strengths.append("Automated TB import — transition to Caseware Cloud connectors will be smooth.")
elif tb_import == "Semi-automated (export CSV, import to WP)":
    s2_score += 4
elif tb_import == "Manual entry / Excel copy-paste":
    s2_score += 2
    risk_flags.append(("Medium", "Manual TB process — Caseware Cloud's automated import will be a significant efficiency gain, but requires mapping setup."))
elif tb_import == "Varies by client":
    s2_score += 3

if rollforward == "Automated rollforward in current software":
    s2_score += 5
elif rollforward == "Semi-manual (rollforward + manual cleanup)":
    s2_score += 3
elif rollforward == "Fully manual rebuild each year":
    s2_score += 1
    risk_flags.append(("Medium", "Manual annual rebuild — Caseware Cloud's rollforward will save significant time, but initial year setup is heavier."))
elif rollforward != "N/A" and rollforward != "Select...":
    s2_score += 2

scores["Workflow Standardization"] = (s2_score, s2_max)


# ═══════════════════════════════════════════════════════════
# SECTION 3: TEAM READINESS & CHANGE MANAGEMENT
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="section-header">3. Team Readiness & Change Management</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    partner_buy_in = st.selectbox(
        "Partner/leadership support for cloud migration",
        ["Select...", "Strong — partners are driving the initiative",
         "Moderate — open to it but not championing",
         "Mixed — some partners supportive, others resistant",
         "Low — primarily an IT/operations initiative"]
    )
    
    tech_comfort = st.selectbox(
        "Staff comfort with new technology",
        ["Select...", "High — team adapts quickly, minimal resistance expected",
         "Moderate — will need structured training but generally open",
         "Low — significant resistance to workflow changes expected",
         "Varies widely across team"]
    )

with col2:
    training_capacity = st.selectbox(
        "Capacity for training during implementation",
        ["Select...", "Dedicated training time can be allocated (off-season)",
         "Limited — training must fit around client work",
         "Very limited — peak season, no slack in schedule",
         "Unsure"]
    )
    
    change_champion = st.selectbox(
        "Is there an internal change champion identified?",
        ["Select...", "Yes — senior manager/partner + tech-savvy staff member",
         "Yes — one person (partner or staff)",
         "Not yet — but willing to assign",
         "No — and unlikely to assign"]
    )

# Score Section 3
s3_score, s3_max = 0, 20

if partner_buy_in == "Strong — partners are driving the initiative":
    s3_score += 5
    strengths.append("Strong partner buy-in — #1 predictor of successful cloud migration.")
elif partner_buy_in == "Moderate — open to it but not championing":
    s3_score += 3
    risk_flags.append(("Medium", "Partner buy-in is moderate — recommend executive alignment session early in engagement."))
elif partner_buy_in == "Mixed — some partners supportive, others resistant":
    s3_score += 2
    risk_flags.append(("High", "Mixed partner support — resistant partners can block adoption. Address through ROI demonstration and peer advocacy."))
elif partner_buy_in == "Low — primarily an IT/operations initiative":
    s3_score += 1
    risk_flags.append(("High", "Partner disengagement is the #1 risk factor. Migration should not proceed without executive sponsorship."))

if tech_comfort == "High — team adapts quickly, minimal resistance expected":
    s3_score += 5
elif tech_comfort == "Moderate — will need structured training but generally open":
    s3_score += 4
elif tech_comfort == "Low — significant resistance to workflow changes expected":
    s3_score += 1
    risk_flags.append(("High", "Expected staff resistance — invest in hands-on training labs and early-win pilot engagements."))
elif tech_comfort == "Varies widely across team":
    s3_score += 3
    risk_flags.append(("Medium", "Mixed tech comfort — consider tiered rollout: cloud-ready teams first, then others with peer mentoring."))

if training_capacity == "Dedicated training time can be allocated (off-season)":
    s3_score += 5
    strengths.append("Training time available — align implementation timeline with off-season for maximum absorption.")
elif training_capacity == "Limited — training must fit around client work":
    s3_score += 3
elif training_capacity == "Very limited — peak season, no slack in schedule":
    s3_score += 1
    risk_flags.append(("High", "No training capacity — do NOT launch during busy season. Target post-April or post-September window."))
elif training_capacity == "Unsure":
    s3_score += 2

if change_champion == "Yes — senior manager/partner + tech-savvy staff member":
    s3_score += 5
    strengths.append("Change champion pair identified (senior + technical) — ideal for driving adoption.")
elif change_champion == "Yes — one person (partner or staff)":
    s3_score += 4
elif change_champion == "Not yet — but willing to assign":
    s3_score += 2
elif change_champion == "No — and unlikely to assign":
    s3_score += 1
    risk_flags.append(("High", "No change champion — every successful implementation needs an internal advocate. Non-negotiable."))

scores["Team Readiness"] = (s3_score, s3_max)


# ═══════════════════════════════════════════════════════════
# SECTION 4: DATA, SECURITY & COMPLIANCE
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="section-header">4. Data, Security & Compliance</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    data_sovereignty = st.selectbox(
        "Data residency requirements",
        ["Select...", "Canadian data residency required",
         "No specific residency requirements",
         "Multi-jurisdictional requirements",
         "Unsure — needs legal review"]
    )
    
    data_volume = st.selectbox(
        "Volume of historical engagement data to migrate",
        ["Select...", "Current year + 1 prior year only",
         "3–5 years of engagement history",
         "5+ years (regulatory retention requirements)",
         "Unsure"]
    )

with col2:
    security_reqs = st.selectbox(
        "Firm's security/compliance posture",
        ["Select...", "Formal security policies + vendor assessment process",
         "Basic security policies in place",
         "Informal / ad-hoc security practices",
         "No documented security policies"]
    )
    
    client_restrictions = st.selectbox(
        "Any clients with cloud restrictions (e.g., 'no cloud' clauses)?",
        ["Select...", "No — all clients cloud-compatible",
         "A few clients (< 10%) with restrictions",
         "Significant number (10-30%) with restrictions",
         "Many (30%+) or unsure"]
    )

# Score Section 4
s4_score, s4_max = 0, 20

if data_sovereignty == "Canadian data residency required":
    s4_score += 5
    strengths.append("Canadian data residency aligns with Caseware Cloud's Canadian-hosted infrastructure (PIPEDA compliant).")
elif data_sovereignty == "No specific residency requirements":
    s4_score += 5
elif data_sovereignty == "Multi-jurisdictional requirements":
    s4_score += 3
    risk_flags.append(("Medium", "Multi-jurisdictional data requirements — verify Caseware Cloud hosting regions meet all applicable regulations."))
elif data_sovereignty == "Unsure — needs legal review":
    s4_score += 2
    risk_flags.append(("Medium", "Data residency requirements unclear — legal review should precede migration planning."))

if data_volume == "Current year + 1 prior year only":
    s4_score += 5
    strengths.append("Minimal data migration scope — reduces migration complexity and timeline.")
elif data_volume == "3–5 years of engagement history":
    s4_score += 3
elif data_volume == "5+ years (regulatory retention requirements)":
    s4_score += 2
    risk_flags.append(("Medium", "Large historical data volume — consider phased migration: current year to cloud, archive older years on desktop."))
elif data_volume == "Unsure":
    s4_score += 2

if security_reqs == "Formal security policies + vendor assessment process":
    s4_score += 5
    strengths.append("Mature security posture — Caseware's SOC 2 Type II and ISO 27001 certifications will satisfy vendor assessment.")
elif security_reqs == "Basic security policies in place":
    s4_score += 4
elif security_reqs == "Informal / ad-hoc security practices":
    s4_score += 2
elif security_reqs == "No documented security policies":
    s4_score += 1
    risk_flags.append(("Medium", "No formal security policies — cloud migration is an opportunity to establish baseline security standards."))

if client_restrictions == "No — all clients cloud-compatible":
    s4_score += 5
elif client_restrictions == "A few clients (< 10%) with restrictions":
    s4_score += 4
    risk_flags.append(("Medium", "Some clients have cloud restrictions — hybrid approach may be needed (cloud for most, desktop for restricted clients)."))
elif client_restrictions == "Significant number (10-30%) with restrictions":
    s4_score += 2
    risk_flags.append(("High", "Significant client-side cloud restrictions — must determine if hybrid desktop/cloud operation is feasible long-term."))
elif client_restrictions == "Many (30%+) or unsure":
    s4_score += 1
    risk_flags.append(("High", "Major client restriction concern — migration feasibility depends on resolving these constraints first."))

scores["Data & Security"] = (s4_score, s4_max)


# ═══════════════════════════════════════════════════════════
# SECTION 5: BUSINESS DRIVERS & TIMELINE
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="section-header">5. Business Drivers & Timeline</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    primary_driver = st.selectbox(
        "Primary driver for considering cloud migration",
        ["Select...", "Remote/hybrid work enablement",
         "Operational efficiency & automation",
         "Real-time collaboration (multi-location teams)",
         "Scalability — growing firm, current tools limiting",
         "Security & compliance improvement",
         "Vendor/platform end-of-life or support concerns",
         "Competitive pressure — clients expecting modern tools"]
    )
    
    timeline = st.selectbox(
        "Desired migration timeline",
        ["Select...", "ASAP — urgent (within 3 months)",
         "Near-term — next 3–6 months",
         "Planned — 6–12 months",
         "Exploratory — no firm deadline"]
    )

with col2:
    budget_awareness = st.selectbox(
        "Budget allocated for migration?",
        ["Select...", "Yes — approved budget in place",
         "Preliminary — ballpark discussed, not approved",
         "No budget allocated yet",
         "Unknown"]
    )
    
    success_criteria = st.multiselect(
        "How will the firm measure migration success? (select all)",
        ["Reduced engagement cycle time", "Improved staff satisfaction",
         "Real-time reviewer access", "Lower IT overhead / maintenance",
         "Better client collaboration", "Regulatory compliance confidence",
         "Faster onboarding of new staff", "Cost savings"]
    )

# Score Section 5
s5_score, s5_max = 0, 20

if primary_driver != "Select...":
    s5_score += 4  # Having a clear driver is positive regardless
    strengths.append(f"Clear migration driver identified: {primary_driver}")

if timeline == "ASAP — urgent (within 3 months)":
    s5_score += 3
    risk_flags.append(("High", "3-month timeline is aggressive — may require parallel run rather than full cutover. Manage expectations early."))
elif timeline == "Near-term — next 3–6 months":
    s5_score += 5
    strengths.append("3–6 month timeline is ideal — enough runway for proper planning, training, and pilot phase.")
elif timeline == "Planned — 6–12 months":
    s5_score += 5
elif timeline == "Exploratory — no firm deadline":
    s5_score += 2

if budget_awareness == "Yes — approved budget in place":
    s5_score += 5
    strengths.append("Approved budget — removes a major implementation blocker.")
elif budget_awareness == "Preliminary — ballpark discussed, not approved":
    s5_score += 3
elif budget_awareness == "No budget allocated yet":
    s5_score += 1
    risk_flags.append(("Medium", "No budget allocated — SOW and business case needed before engagement can proceed."))
elif budget_awareness == "Unknown":
    s5_score += 1

if len(success_criteria) >= 3:
    s5_score += 6
    strengths.append(f"{len(success_criteria)} success criteria defined — clear vision for measuring ROI.")
elif len(success_criteria) >= 1:
    s5_score += 3
else:
    s5_score += 0

scores["Business Drivers"] = (s5_score, s5_max)


# ─────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────
st.markdown("---")

# Check if enough data was entered
answered = sum(1 for v in [current_software, cloud_adoption, it_support, 
                           template_usage, methodology, tb_import,
                           partner_buy_in, tech_comfort, training_capacity,
                           change_champion, data_sovereignty, security_reqs,
                           primary_driver, timeline, budget_awareness] 
               if v != "Select...")

if answered < 8:
    st.info("📋 **Complete at least 8 assessment questions above to generate your readiness report.**")
    st.stop()


# Calculate overall score
total_score = sum(s for s, _ in scores.values())
total_max = sum(m for _, m in scores.values())
pct = round((total_score / total_max) * 100) if total_max > 0 else 0

# Determine readiness tier
if pct >= 80:
    tier = "High Readiness"
    tier_color = "#27ae60"
    tier_emoji = "🟢"
    tier_desc = "This firm is well-positioned for a structured cloud migration. Recommend proceeding with a standard implementation engagement."
elif pct >= 60:
    tier = "Moderate Readiness"
    tier_color = "#2d6a9f"
    tier_emoji = "🔵"
    tier_desc = "Firm shows solid foundations with some areas requiring attention. Recommend a phased approach with a pilot engagement group."
elif pct >= 40:
    tier = "Conditional Readiness"
    tier_color = "#f39c12"
    tier_emoji = "🟡"
    tier_desc = "Several readiness gaps identified. Recommend a pre-implementation readiness phase to address foundational issues before migration."
else:
    tier = "Not Yet Ready"
    tier_color = "#e74c3c"
    tier_emoji = "🔴"
    tier_desc = "Significant readiness gaps across multiple areas. Recommend foundational enablement engagement before cloud migration planning."

st.markdown('<div class="section-header">📊 Migration Readiness Assessment Results</div>', unsafe_allow_html=True)

# ── Overall Score Display ──
col_gauge, col_summary = st.columns([1, 1.2])

with col_gauge:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={"suffix": "%", "font": {"size": 48, "color": tier_color}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#ccc"},
            "bar": {"color": tier_color},
            "bgcolor": "#f0f0f0",
            "steps": [
                {"range": [0, 40], "color": "#fde8e8"},
                {"range": [40, 60], "color": "#fff8e8"},
                {"range": [60, 80], "color": "#e8f0fe"},
                {"range": [80, 100], "color": "#e8f8ed"},
            ],
            "threshold": {
                "line": {"color": tier_color, "width": 3},
                "thickness": 0.8,
                "value": pct,
            },
        },
        title={"text": f"{tier_emoji} {tier}", "font": {"size": 18, "color": tier_color}},
    ))
    fig.update_layout(
        height=280, margin=dict(l=30, r=30, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)", font={"family": "Source Sans Pro"}
    )
    st.plotly_chart(fig, use_container_width=True)

with col_summary:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: {tier_color}; margin-top: 0;">{tier_emoji} {tier}</h3>
        <p style="font-size: 1rem; line-height: 1.6;">{tier_desc}</p>
        <p style="font-size: 0.85rem; color: #888; margin-bottom: 0;">
            Score: {total_score} / {total_max} across 5 assessment categories
            {"<br>Firm: <strong>" + firm_name + "</strong>" if firm_name else ""}
            <br>Assessment Date: {datetime.now().strftime("%B %d, %Y")}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── Category Breakdown ──
st.markdown("#### Category Scores")

categories = list(scores.keys())
cat_pcts = [round((s / m) * 100) if m > 0 else 0 for s, m in scores.values()]
cat_colors = []
for p in cat_pcts:
    if p >= 80:
        cat_colors.append("#27ae60")
    elif p >= 60:
        cat_colors.append("#2d6a9f")
    elif p >= 40:
        cat_colors.append("#f39c12")
    else:
        cat_colors.append("#e74c3c")

fig2 = go.Figure(go.Bar(
    x=cat_pcts,
    y=categories,
    orientation="h",
    marker_color=cat_colors,
    text=[f"{p}%" for p in cat_pcts],
    textposition="auto",
    textfont=dict(size=14, color="white"),
))
fig2.update_layout(
    height=280,
    margin=dict(l=10, r=30, t=10, b=10),
    xaxis=dict(range=[0, 100], title="Readiness %", showgrid=True, gridcolor="#eee"),
    yaxis=dict(autorange="reversed"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Source Sans Pro", size=13),
)
st.plotly_chart(fig2, use_container_width=True)


# ── Risk Flags ──
high_risks = [(sev, msg) for sev, msg in risk_flags if sev == "High"]
med_risks = [(sev, msg) for sev, msg in risk_flags if sev == "Medium"]

if high_risks or med_risks:
    st.markdown("#### ⚠️ Risk Flags")
    for sev, msg in high_risks:
        st.markdown(f'<div class="risk-flag">🔴 <strong>HIGH:</strong> {msg}</div>', unsafe_allow_html=True)
    for sev, msg in med_risks:
        st.markdown(f'<div class="risk-flag-medium">🟡 <strong>MEDIUM:</strong> {msg}</div>', unsafe_allow_html=True)

# ── Strengths ──
if strengths:
    st.markdown("#### ✅ Strengths & Accelerators")
    for s in strengths:
        st.markdown(f'<div class="strength-flag">🟢 {s}</div>', unsafe_allow_html=True)


# ── Recommended Approach ──
st.markdown("#### 🗺️ Recommended Migration Approach")

if pct >= 80:
    approach = "Standard Implementation"
    phases = [
        ("Phase 1 — Kickoff & Planning", "2 weeks", "SOW sign-off, project plan, stakeholder alignment, environment setup."),
        ("Phase 2 — Configuration & Templates", "3–4 weeks", "Migrate/configure templates, map chart of accounts, set up user roles and permissions."),
        ("Phase 3 — Data Migration (CloudBridge)", "2–3 weeks", "Pilot migration of 3–5 engagements, validate data integrity, refine mapping."),
        ("Phase 4 — Training & Parallel Run", "2–3 weeks", "Role-based training sessions, parallel processing of live engagements in cloud."),
        ("Phase 5 — Go-Live & Hypercare", "2 weeks", "Full cutover, dedicated support channel, post-go-live health checks."),
    ]
elif pct >= 60:
    approach = "Phased Rollout with Pilot Group"
    phases = [
        ("Phase 1 — Discovery & Readiness", "2–3 weeks", "Deep-dive requirements, resolve medium-risk items, establish change champion team."),
        ("Phase 2 — Pilot Configuration", "3–4 weeks", "Configure for 1–2 service lines, standardize templates, pilot group selection."),
        ("Phase 3 — Pilot Migration & Validation", "4–6 weeks", "Migrate pilot group (5–10 engagements), parallel run, collect feedback."),
        ("Phase 4 — Broader Training & Rollout", "4–6 weeks", "Train remaining staff, phase 2 migration cohort, iterate on lessons learned."),
        ("Phase 5 — Full Go-Live & Optimization", "2–4 weeks", "Complete migration, decommission desktop for migrated groups, optimization sprints."),
    ]
elif pct >= 40:
    approach = "Readiness-First Engagement"
    phases = [
        ("Phase 0 — Pre-Implementation Readiness", "4–6 weeks", "Address high-risk items: template standardization, IT infrastructure, partner alignment workshops, change management plan."),
        ("Phase 1 — Foundation & Configuration", "4–6 weeks", "Environment setup, methodology alignment, template design in cloud."),
        ("Phase 2 — Small-Scale Pilot", "6–8 weeks", "3–5 engagements migrated with intensive support, learning documentation."),
        ("Phase 3 — Evaluate & Expand", "4–6 weeks", "Assess pilot results, train next cohort, expand migration scope."),
        ("Phase 4 — Graduated Go-Live", "Ongoing", "Incremental migration over 2–3 engagement cycles with continuous support."),
    ]
else:
    approach = "Foundational Enablement (Pre-Migration)"
    phases = [
        ("Phase 0 — Assessment & Business Case", "4–6 weeks", "Build executive business case, IT infrastructure assessment, data readiness audit."),
        ("Phase 1 — Foundational Readiness", "8–12 weeks", "Establish templates, standardize workflows, IT modernization, security policy development."),
        ("Phase 2 — Cloud Familiarization", "4–6 weeks", "Sandbox environment, staff exposure to Caseware Cloud, identify early adopters."),
        ("Phase 3 — Migration Readiness Re-Assessment", "2 weeks", "Re-score readiness, proceed to standard implementation if thresholds met."),
    ]

st.markdown(f"""
<div class="recommendation-box">
    <h4 style="margin-top: 0; color: #1a3c5e;">Recommended Approach: {approach}</h4>
    <p>Based on the firm's readiness profile, the following phased approach is recommended:</p>
</div>
""", unsafe_allow_html=True)

for phase_name, duration, description in phases:
    with st.expander(f"📌 {phase_name} — _{duration}_"):
        st.write(description)


# ── Engagement Sizing Estimate ──
st.markdown("#### 📐 Engagement Sizing Estimate")

# Estimate based on firm size and readiness
size_multiplier = {
    "Solo practitioner (1)": 0.5,
    "Small (2–10)": 1.0,
    "Mid-size (11–50)": 1.8,
    "Large (51–200)": 3.0,
    "Enterprise (200+)": 5.0,
}.get(firm_size, 1.0)

readiness_multiplier = 1.0
if pct >= 80:
    readiness_multiplier = 0.8
elif pct >= 60:
    readiness_multiplier = 1.0
elif pct >= 40:
    readiness_multiplier = 1.4
else:
    readiness_multiplier = 1.8

base_weeks = 10
est_weeks = round(base_weeks * size_multiplier * readiness_multiplier)
est_weeks_low = max(4, est_weeks - 3)
est_weeks_high = est_weeks + 4

col_e1, col_e2, col_e3 = st.columns(3)
with col_e1:
    st.metric("Estimated Duration", f"{est_weeks_low}–{est_weeks_high} weeks")
with col_e2:
    consultant_days = round(est_weeks * 2.5)  # ~2.5 days/week
    st.metric("Est. Consultant Days", f"{consultant_days - 10}–{consultant_days + 10} days")
with col_e3:
    st.metric("Recommended Team", 
              "1 Lead + 1 Associate" if size_multiplier <= 1.8 else "1 Lead + 2 Associates")


# ── Next Steps ──
st.markdown("#### 📋 Recommended Next Steps")

next_steps = []
if high_risks:
    next_steps.append("**1. Address High-Risk Items** — Schedule working sessions to resolve critical blockers before scoping the SOW.")
if not firm_name:
    next_steps.append("**Document firm profile details** — Complete the sidebar context for a comprehensive assessment record.")

next_steps.extend([
    f"**{'2' if high_risks else '1'}. Share this assessment** with the engagement partner and internal champion for alignment.",
    f"**{'3' if high_risks else '2'}. Schedule a solution demo** — Walk the team through Caseware Cloud with their own sample engagement data.",
    f"**{'4' if high_risks else '3'}. Scope the SOW** — Use this assessment to define implementation scope, timeline, and pricing.",
    f"**{'5' if high_risks else '4'}. Set a target go-live date** — Align with the firm's engagement calendar (avoid Jan–April busy season for Canadian firms).",
])

for step in next_steps:
    st.markdown(f"- {step}")



# ── Footer ──
st.markdown(f"""
<div class="footer-note">
    <strong>Caseware Cloud Migration Readiness Assessor</strong> · v1.0<br>
    Built by Hammad Mirza · Professional Services Portfolio Project · April 2026<br>
    <em>This tool is designed to support structured discovery conversations during pre-implementation engagements.
    It is not affiliated with or endorsed by Caseware International Inc.</em>
</div>
""", unsafe_allow_html=True)
