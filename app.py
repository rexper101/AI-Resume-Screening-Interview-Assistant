"""
app.py - AI Resume Screening & Interview Assistant
Main Streamlit application entry point.

Run with: streamlit run app.py
"""

import html
import streamlit as st
import time
import json
from pathlib import Path

# ── Page Configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeAI — Smart Resume Analysis",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/yourusername/ai-resume-screener",
        "About": "ResumeAI — AI Resume Screening & Interview Assistant v1.0"
    }
)

# ── Custom CSS Styling (light theme) ───────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Outfit:wght@400;500;600;700&display=swap');

    :root {
        --bg-deep: #F1F5F9;
        --bg-surface: #FFFFFF;
        --bg-card: #FFFFFF;
        --bg-muted: #F8FAFC;
        --border: rgba(13, 148, 136, 0.18);
        --border-hover: rgba(13, 148, 136, 0.45);
        --accent: #0D9488;
        --accent-2: #0891B2;
        --accent-soft: rgba(13, 148, 136, 0.1);
        --accent-text: #0F766E;
        --text: #0F172A;
        --text-muted: #475569;
        --text-dim: #64748B;
        --radius: 14px;
        --shadow: 0 4px 24px rgba(15, 23, 42, 0.06);
        --shadow-hover: 0 12px 40px rgba(13, 148, 136, 0.12);
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes glow {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 0.75; }
    }

    .stApp {
        background:
            radial-gradient(ellipse 80% 50% at 50% -15%, rgba(13, 148, 136, 0.08), transparent),
            radial-gradient(ellipse 50% 40% at 100% 0%, rgba(8, 145, 178, 0.05), transparent),
            linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
        border-right: 1px solid #E2E8F0;
        box-shadow: 2px 0 16px rgba(15, 23, 42, 0.04);
    }
    [data-testid="stSidebar"] .stMarkdown { color: var(--text-muted); }
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stButton > button[kind="secondary"],
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: none !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] .stButton > button:focus {
        background: #F0FDFA !important;
        border-color: #0D9488 !important;
        color: #0F766E !important;
        transform: none !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover *,
    [data-testid="stSidebar"] .stButton > button:focus * {
        color: #0F766E !important;
    }
    .sidebar-title { font-family: Outfit, sans-serif; font-size: 1.35rem; font-weight: 700; color: var(--text); }
    .sidebar-tagline { color: var(--text-dim); font-size: 0.7rem; letter-spacing: 0.14em; text-transform: uppercase; margin-top: 4px; }
    .nav-active {
        padding: 8px 12px; margin: 2px 0; border-radius: 10px;
        background: var(--accent-soft); border: 1px solid var(--border-hover);
        color: var(--accent-text); font-size: 0.88rem; font-weight: 600;
    }
    .stat-pill {
        background: var(--accent-soft); color: var(--accent-text);
        padding: 4px 10px; border-radius: 8px; font-size: 0.75rem; font-weight: 500;
    }
    .status-ready { color: #047857; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
    .info-panel {
        background: var(--bg-muted); border-radius: 12px; padding: 16px;
        border: 1px solid #E2E8F0; color: var(--text-muted); font-size: 0.9rem; line-height: 2;
    }
    .info-panel b { color: var(--text); }
    .highlight-card {
        background: linear-gradient(135deg, rgba(13,148,136,0.08), rgba(8,145,178,0.05));
        border: 1px solid var(--border); border-radius: 16px; padding: 20px;
    }

    .main .block-container {
        padding: 1.5rem 2rem 3rem;
        max-width: 1320px;
        animation: fadeInUp 0.35s ease both;
    }

    .glass-card {
        background: var(--bg-card);
        border: 1px solid #E2E8F0;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
    }

    .metric-card {
        background: var(--bg-card);
        border: 1px solid #E2E8F0;
        border-radius: var(--radius);
        padding: 22px 20px;
        text-align: center;
        box-shadow: var(--shadow);
        transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
        animation: fadeInUp 0.45s ease both;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-hover);
        box-shadow: var(--shadow-hover);
    }
    .metric-card .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.15;
    }
    .metric-card .metric-label {
        color: var(--text-dim);
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 8px;
    }
    .metric-card .metric-icon {
        font-size: 1.35rem;
        margin-bottom: 8px;
        line-height: 1;
    }

    .page-header {
        margin-bottom: 28px;
        animation: fadeInUp 0.4s ease both;
    }
    .page-header h1 {
        font-family: 'Outfit', sans-serif;
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 6px 0;
        letter-spacing: -0.02em;
    }
    .page-header p {
        color: var(--text-muted);
        font-size: 0.95rem;
        margin: 0;
        line-height: 1.5;
    }
    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.35rem;
        font-weight: 600;
        color: var(--text);
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 22px;
    }

    /* ── Skill Tags ─── */
    .skill-tag {
        display: inline-block;
        background: #CCFBF1;
        border: 1px solid #99F6E4;
        color: #0F766E;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 3px;
        transition: background .2s, transform .15s;
    }
    .skill-tag:hover { background: #99F6E4; transform: scale(1.03); }
    .skill-tag-missing {
        background: #FEE2E2; border-color: #FECACA; color: #B91C1C;
    }
    .skill-tag-present {
        background: #D1FAE5; border-color: #A7F3D0; color: #047857;
    }

    .tier-badge {
        display: inline-block; padding: 6px 16px; border-radius: 20px;
        font-size: 0.9rem; font-weight: 600; letter-spacing: 0.05em;
    }

    .job-card {
        background: var(--bg-card);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: var(--shadow);
        transition: border-color .25s, box-shadow .25s;
    }
    .job-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow-hover);
    }

    .custom-progress-container {
        background: #E2E8F0;
        border-radius: 8px;
        height: 8px;
        margin: 6px 0;
        overflow: hidden;
    }
    .custom-progress-fill {
        height: 100%; border-radius: 8px;
        transition: width .7s cubic-bezier(.4,0,.2,1);
    }

    .hero-section {
        text-align: center;
        padding: 56px 32px 48px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F0FDFA 50%, #ECFEFF 100%);
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow);
        animation: fadeInUp 0.5s ease both;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: 50%;
        transform: translateX(-50%);
        width: 120%;
        height: 100%;
        background: radial-gradient(ellipse, rgba(13, 148, 136, 0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        background: #CCFBF1;
        border: 1px solid #99F6E4;
        color: #0F766E;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 18px;
        position: relative;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: clamp(2rem, 4vw, 2.75rem);
        font-weight: 700;
        background: linear-gradient(135deg, #0F172A 0%, #0D9488 50%, #0891B2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.15;
        position: relative;
        letter-spacing: -0.03em;
    }
    .hero-subtitle {
        color: var(--text-muted);
        font-size: 1.05rem;
        margin-top: 14px;
        max-width: 560px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.65;
        position: relative;
    }
    .feature-card {
        background: var(--bg-card);
        border: 1px solid #E2E8F0;
        border-radius: var(--radius);
        padding: 20px 18px;
        height: 100%;
        box-shadow: var(--shadow);
        transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    }
    .feature-card:hover {
        border-color: var(--border-hover);
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }
    .feature-num {
        font-family: 'Outfit', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--accent);
        letter-spacing: 0.1em;
        margin-bottom: 10px;
    }
    .feature-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        color: var(--text);
        font-size: 1rem;
        margin-bottom: 6px;
    }
    .feature-desc {
        color: var(--text-dim);
        font-size: 0.82rem;
        line-height: 1.5;
    }
    .empty-state {
        text-align: center;
        padding: 64px 24px;
        background: var(--bg-muted);
        border: 1px dashed #CBD5E1;
        border-radius: 18px;
        color: var(--text-dim);
    }
    .empty-state-icon { font-size: 2.5rem; margin-bottom: 12px; opacity: 0.85; }
    .empty-state-title { font-size: 1.1rem; color: var(--text); font-weight: 500; }

    .feedback-positive { color: #047857; font-size: 0.9rem; padding: 4px 0; }
    .feedback-warning  { color: #B45309; font-size: 0.9rem; padding: 4px 0; }
    .feedback-negative { color: #B91C1C; font-size: 0.9rem; padding: 4px 0; }

    .stTabs [data-baseweb="tab"] {
        background: #F1F5F9;
        border-radius: 8px;
        color: var(--text-muted);
        font-weight: 500;
        border: 1px solid #E2E8F0;
    }
    .stTabs [aria-selected="true"] {
        background: #CCFBF1 !important;
        color: var(--accent-text) !important;
        border-color: #99F6E4 !important;
    }

    [data-testid="stFileUploader"] {
        border: 2px dashed #99F6E4;
        border-radius: 16px;
        padding: 10px;
        background: #F0FDFA;
        transition: border-color .3s;
    }
    [data-testid="stFileUploader"]:hover { border-color: var(--accent); background: #ECFEFF; }

    /* Primary buttons */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #0D9488, #0891B2) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(13, 148, 136, 0.25) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:focus,
    .stButton > button[data-testid="baseButton-primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:focus {
        background: linear-gradient(135deg, #0F766E, #0E7490) !important;
        color: #FFFFFF !important;
        border: none !important;
        opacity: 1 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(13, 148, 136, 0.35) !important;
    }
    .stButton > button[kind="primary"]:hover *,
    .stButton > button[kind="primary"]:focus *,
    .stButton > button[data-testid="baseButton-primary"]:hover *,
    .stButton > button[data-testid="baseButton-primary"]:focus * {
        color: #FFFFFF !important;
    }

    /* Secondary / default buttons */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        box-shadow: none !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button[kind="secondary"]:focus,
    .stButton > button[data-testid="baseButton-secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:focus {
        background: #F0FDFA !important;
        color: #0F766E !important;
        border-color: #0D9488 !important;
        opacity: 1 !important;
    }
    .stButton > button[kind="secondary"]:hover *,
    .stButton > button[kind="secondary"]:focus *,
    .stButton > button[data-testid="baseButton-secondary"]:hover *,
    .stButton > button[data-testid="baseButton-secondary"]:focus * {
        color: #0F766E !important;
    }

    /* Download button */
    .stDownloadButton > button,
    .stDownloadButton > button[kind="secondary"],
    .stDownloadButton > button[data-testid="baseButton-secondary"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }
    .stDownloadButton > button:hover,
    .stDownloadButton > button:focus {
        background: #F0FDFA !important;
        color: #0F766E !important;
        border-color: #0D9488 !important;
        opacity: 1 !important;
    }
    .stDownloadButton > button:hover *,
    .stDownloadButton > button:focus * {
        color: #0F766E !important;
    }

    .stSelectbox > div > div {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        color: var(--text);
    }

    .stSuccess { border-left: 4px solid #10B981; }
    .stError   { border-left: 4px solid #EF4444; }
    .stInfo    { border-left: 4px solid #06B6D4; }
    .stWarning { border-left: 4px solid #F59E0B; }

    hr { border-color: #E2E8F0; margin: 20px 0; }

    [data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        box-shadow: var(--shadow);
    }
    [data-testid="stExpander"]:hover { border-color: var(--border-hover); }

    .stTextArea textarea,
    [data-testid="stTextArea"] textarea {
        background: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.875rem;
        line-height: 1.55;
        caret-color: #0F172A;
    }
    .stTextArea textarea:disabled,
    [data-testid="stTextArea"] textarea:disabled {
        background: #F8FAFC !important;
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        opacity: 1 !important;
        cursor: default;
    }
    [data-testid="stTextArea"] label,
    [data-testid="stTextArea"] [data-baseweb="textarea"] {
        color: var(--text-muted);
    }

    .resume-preview {
        background: #F8FAFC;
        color: #0F172A;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 18px;
        max-height: 380px;
        overflow: auto;
        font-family: 'DM Sans', ui-monospace, monospace;
        font-size: 0.84rem;
        line-height: 1.55;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 0;
    }

    .nav-group-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--text-dim);
        margin: 18px 0 8px 4px;
    }
    .brand-logo {
        width: 44px; height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        display: flex; align-items: center; justify-content: center;
        font-size: 1.35rem;
        margin: 0 auto 12px;
        box-shadow: 0 4px 16px rgba(13, 148, 136, 0.2);
    }

    .question-box {
        background: #F8FAFC;
        border-left: 3px solid var(--accent);
        border: 1px solid #E2E8F0;
        border-left: 3px solid var(--accent);
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin: 8px 0;
        color: var(--text-muted);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .question-box:hover { background: #F0FDFA; border-left-color: var(--accent-2); }

    .cert-tag {
        background: #FEF3C7;
        border: 1px solid #FDE68A;
        color: #B45309;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.82rem;
        margin: 4px;
        display: inline-block;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-primary {
        background: #CCFBF1;
        color: #0F766E;
        border: 1px solid #99F6E4;
    }
    .badge-success {
        background: #D1FAE5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }

    .tier-message {
        background: #F8FAFC;
        border-radius: 8px;
        padding: 12px;
        color: var(--text-muted);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .prediction-hero {
        background: linear-gradient(135deg, #F0FDFA, #ECFEFF);
        border: 1px solid #99F6E4;
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        margin-bottom: 24px;
    }
    .prediction-hero .role-name { font-family: Outfit, sans-serif; font-size: 2.2rem; font-weight: 700; color: var(--text); }
    .prediction-hero .role-label { color: var(--text-dim); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; }
    .rank-card {
        margin-bottom: 16px;
        background: #FFFFFF;
        border-radius: 10px;
        padding: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: var(--shadow);
    }
    .rank-card.top { border-color: #99F6E4; background: #F0FDFA; }
    .feature-row { color: var(--text-muted); font-size: 0.88rem; padding: 6px 0; }
    .feature-row b, .feature-row strong { color: var(--accent-text); }

    h1, h2, h3, h4 { font-family: 'Outfit', sans-serif !important; color: var(--text) !important; }
    .stMarkdown, .stMarkdown p { color: var(--text-muted); }
    .stMarkdown h3 { color: var(--text) !important; }

    [data-testid="stMetricValue"] { color: var(--text) !important; }
    [data-testid="stHeader"] { background: rgba(255,255,255,0.9); backdrop-filter: blur(8px); border-bottom: 1px solid #E2E8F0; }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── UI Components ──────────────────────────────────────────────────────────────
PAGE_META = {
    "Home": ("Home", "Your AI-powered career intelligence hub"),
    "Upload & Analyze": ("Upload & Analyze", "Parse your resume and run the full pipeline"),
    "ATS Score": ("ATS Score", "Applicant tracking system compatibility"),
    "Job Matches": ("Job Matches", "Roles ranked by fit and skill overlap"),
    "Skill Analysis": ("Skill Analysis", "Extracted skills and categories"),
    "Skill Gap": ("Skill Gap", "What to learn for your target role"),
    "Role Predictor": ("Role Predictor", "ML-based career path prediction"),
    "Interview Prep": ("Interview Prep", "Personalized practice questions"),
    "Analytics Dashboard": ("Analytics", "All charts and metrics in one view"),
}

NAV_GROUPS = [
    ("Overview", ["Home"]),
    ("Analyze", ["Upload & Analyze", "ATS Score"]),
    ("Insights", ["Job Matches", "Skill Analysis", "Skill Gap", "Role Predictor"]),
    ("Prepare", ["Interview Prep", "Analytics Dashboard"]),
]

NAV_ICONS = {
    "Home": "🏠",
    "Upload & Analyze": "📄",
    "ATS Score": "📊",
    "Job Matches": "💼",
    "Skill Analysis": "🧠",
    "Skill Gap": "🎯",
    "Role Predictor": "🤖",
    "Interview Prep": "🎤",
    "Analytics Dashboard": "📈",
}


def render_page_header(page_key: str):
    title, subtitle = PAGE_META.get(page_key, (page_key, ""))
    st.markdown(f"""
    <div class='page-header'>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(icon: str, value, label: str, value_size: str = "2.25rem"):
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>{icon}</div>
        <div class='metric-value' style='font-size:{value_size};'>{value}</div>
        <div class='metric-label'>{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(icon: str, title: str, hint: str = ""):
    hint_html = f"<p style='margin-top:8px;font-size:0.88rem;'>{hint}</p>" if hint else ""
    st.markdown(f"""
    <div class='empty-state'>
        <div class='empty-state-icon'>{icon}</div>
        <div class='empty-state-title'>{title}</div>
        {hint_html}
    </div>
    """, unsafe_allow_html=True)


def require_analysis(page_name: str = "this section") -> bool:
    if not st.session_state.analysis_done:
        render_empty_state(
            "📋",
            f"No analysis yet",
            f"Upload a resume on Upload & Analyze, then open {page_name}."
        )
        if st.button("Go to Upload & Analyze", type="primary"):
            st.session_state.current_page = "Upload & Analyze"
            st.rerun()
        return False
    return True


# ── Session State Initialization ───────────────────────────────────────────────
def init_session_state():
    defaults = {
        "resume_text": None,
        "parsed_resume": None,
        "extracted_skills": None,
        "skill_data": None,
        "recommendations": None,
        "ats_result": None,
        "prediction_result": None,
        "interview_pack": None,
        "skill_gap": None,
        "current_page": "Home",
        "demo_mode": False,
        "analysis_done": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


# ── Import modules ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_modules():
    """Load and cache all backend modules."""
    from resume_parser import parse_resume, get_sample_resume_text
    from skill_extractor import extract_all
    from recommender import get_top_recommendations, compute_skill_gap, explain_recommendation
    from ats_calculator import calculate_ats_score, get_improvement_priority
    from interview_generator import generate_interview_pack, format_interview_pack_markdown
    from role_predictor import get_role_predictor
    from dashboard import (
        create_ats_gauge, create_skill_bar_chart, create_skill_category_donut,
        create_job_match_chart, create_ats_components_radar, create_role_prediction_chart,
        create_skill_gap_chart, create_ats_progress_bars_data
    )
    return {
        "parse_resume": parse_resume,
        "get_sample_resume_text": get_sample_resume_text,
        "extract_all": extract_all,
        "get_top_recommendations": get_top_recommendations,
        "compute_skill_gap": compute_skill_gap,
        "explain_recommendation": explain_recommendation,
        "calculate_ats_score": calculate_ats_score,
        "get_improvement_priority": get_improvement_priority,
        "generate_interview_pack": generate_interview_pack,
        "format_interview_pack_markdown": format_interview_pack_markdown,
        "get_role_predictor": get_role_predictor,
        "create_ats_gauge": create_ats_gauge,
        "create_skill_bar_chart": create_skill_bar_chart,
        "create_skill_category_donut": create_skill_category_donut,
        "create_job_match_chart": create_job_match_chart,
        "create_ats_components_radar": create_ats_components_radar,
        "create_role_prediction_chart": create_role_prediction_chart,
        "create_skill_gap_chart": create_skill_gap_chart,
        "create_ats_progress_bars_data": create_ats_progress_bars_data,
    }


mods = load_modules()


# ── Sidebar Navigation ─────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 8px 0 16px;'>
            <div class='brand-logo'>&#128203;</div>
            <div class='sidebar-title'>ResumeAI</div>
            <div class='sidebar-tagline'>Career Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

        current = st.session_state.get("current_page", "Home")
        for group_name, pages in NAV_GROUPS:
            st.markdown(f"<div class='nav-group-label'>{group_name}</div>", unsafe_allow_html=True)
            for page in pages:
                icon = NAV_ICONS.get(page, "\u2022")
                label = f"{icon}  {page}"
                if current == page:
                    st.markdown(
                        f"<div class='nav-active'>{label}</div>",
                        unsafe_allow_html=True,
                    )
                elif st.button(label, key=f"nav_{page}", use_container_width=True):
                    st.session_state.current_page = page
                    st.rerun()

        st.markdown("<hr style='border-color:rgba(20,184,166,0.12);margin:16px 0;'>", unsafe_allow_html=True)

        if st.session_state.analysis_done:
            skills_count = len(st.session_state.extracted_skills or [])
            ats_score = st.session_state.ats_result["total_score"] if st.session_state.ats_result else 0
            top_match = st.session_state.recommendations[0]["match_percentage"] if st.session_state.recommendations else 0
            st.markdown(f"""
            <div class='glass-card' style='padding:14px;'>
                <div class='status-ready'>Analysis ready</div>
                <div style='margin-top:10px;display:flex;gap:6px;flex-wrap:wrap;'>
                    <span class='stat-pill'>{skills_count} skills</span>
                    <span class='stat-pill'>ATS {ats_score}</span>
                    <span class='stat-pill'>{top_match}% match</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Start over", use_container_width=True):
                for key in ("resume_text", "parsed_resume", "extracted_skills", "skill_data",
                            "recommendations", "ats_result", "prediction_result",
                            "interview_pack", "skill_gap"):
                    st.session_state[key] = None
                st.session_state.analysis_done = False
                st.session_state.current_page = "Upload & Analyze"
                st.rerun()
        else:
            st.markdown("""
            <div class='glass-card' style='padding:14px;color:var(--text-muted);font-size:0.82rem;line-height:1.5;'>
                Upload a resume to unlock ATS scoring, job matches, and interview prep.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:24px;text-align:center;color:#475569;font-size:0.7rem;line-height:1.6;'>
            Python &middot; Streamlit &middot; scikit-learn<br>v1.0
        </div>
        """, unsafe_allow_html=True)



# ── Helper: Run Analysis ───────────────────────────────────────────────────────
def run_full_analysis(resume_text: str, parsed_resume: dict):
    """Run complete resume analysis pipeline."""

    progress = st.progress(0)
    status = st.empty()

    try:
        # Step 1: Skill Extraction
        status.markdown("**Extracting skills from resume...**")
        progress.progress(15)
        skill_data = mods["extract_all"](
            resume_text,
            parsed_resume.get("sections", {})
        )
        extracted_skills = skill_data["all_skills"]
        st.session_state.extracted_skills = extracted_skills
        st.session_state.skill_data = skill_data
        time.sleep(0.3)

        # Step 2: ATS Score
        status.markdown("**Calculating ATS compatibility score...**")
        progress.progress(30)
        ats_result = mods["calculate_ats_score"](
            resume_text,
            parsed_resume.get("sections", {}),
            extracted_skills,
            parsed_resume.get("contact_info", {}),
            skill_data.get("education_info", {})
        )
        st.session_state.ats_result = ats_result
        time.sleep(0.3)

        # Step 3: Job Recommendations
        status.markdown("**Generating job recommendations...**")
        progress.progress(50)
        recommendations = mods["get_top_recommendations"](resume_text, extracted_skills, top_n=8)
        st.session_state.recommendations = recommendations
        time.sleep(0.3)

        # Step 4: Role Prediction
        status.markdown("**Running ML role prediction model...**")
        progress.progress(65)
        predictor = mods["get_role_predictor"]("logistic_regression")
        prediction_result = predictor.predict(resume_text, extracted_skills)
        prediction_result["feature_importance"] = predictor.get_feature_importance(
            resume_text, extracted_skills
        )
        st.session_state.prediction_result = prediction_result
        time.sleep(0.3)

        # Step 5: Skill Gap for top role
        status.markdown("**Analyzing skill gaps...**")
        progress.progress(80)
        top_role = recommendations[0]["role"] if recommendations else "Data Scientist"
        skill_gap = mods["compute_skill_gap"](extracted_skills, top_role)
        st.session_state.skill_gap = skill_gap
        time.sleep(0.3)

        # Step 6: Interview Prep
        status.markdown("**Generating interview questions...**")
        progress.progress(92)
        experience_level = skill_data["experience_info"]["estimated_level"]
        interview_pack = mods["generate_interview_pack"](
            extracted_skills,
            experience_level=experience_level,
            target_role=top_role
        )
        st.session_state.interview_pack = interview_pack
        time.sleep(0.3)

        progress.progress(100)
        status.markdown("**Analysis complete!**")
        st.session_state.analysis_done = True
        time.sleep(0.8)
        progress.empty()
        status.empty()

        return True

    except Exception as e:
        progress.empty()
        status.empty()
        st.error(f"Analysis error: {str(e)}")
        return False


# ── Page: Home ─────────────────────────────────────────────────────────────────

def page_home():
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-badge'>AI-powered career toolkit</div>
        <div class='hero-title'>Screen smarter.<br>Interview better.</div>
        <div class='hero-subtitle'>
            One upload unlocks ATS scoring, job matches, skill gaps, ML role predictions,
            and a personalized interview prep pack.
        </div>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("01", "\U0001f4c4", "Resume Parser", "Extract structure, sections, and contact info from PDF"),
        ("02", "\U0001f4ca", "ATS Score", "7 weighted dimensions with actionable feedback"),
        ("03", "\U0001f4bc", "Job Matching", "TF-IDF + cosine similarity across 8 roles"),
        ("04", "\U0001f9e0", "Skill Extraction", "50+ skills across six technical categories"),
        ("05", "\U0001f3af", "Skill Gap", "See what to learn for your target role"),
        ("06", "\U0001f916", "ML Prediction", "Logistic regression, random forest, naive Bayes"),
        ("07", "\U0001f3a4", "Interview Prep", "Technical, behavioral, and scenario questions"),
        ("08", "\U0001f4c8", "Analytics", "Interactive Plotly dashboards in one view"),
    ]

    cols = st.columns(4)
    for i, (num, emoji, title, desc) in enumerate(features):
        with cols[i % 4]:
            st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-num'>{num}</div>
                <div style='font-size:1.25rem;margin-bottom:8px;'>{emoji}</div>
                <div class='feature-title'>{title}</div>
                <div class='feature-desc'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Quick start")
        for i, step in enumerate([
            "Open **Upload & Analyze** in the sidebar",
            "Upload a PDF or load the sample resume",
            "Click **Run Full AI Analysis**",
            "Explore ATS, matches, skills, and interview prep",
        ], 1):
            st.markdown(
                f"<div style='color:var(--text-muted);padding:6px 0;'>"
                f"<span style='color:#14B8A6;font-weight:700;margin-right:8px;'>{i}</span>{step}</div>",
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("### Built with")
        for item in ["Python 3.10+", "Streamlit", "scikit-learn", "Plotly", "PyPDF2"]:
            st.markdown(f"<span class='skill-tag'>{item}</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cta1, cta2, _ = st.columns([1, 1, 2])
    with cta1:
        if st.button("Upload resume", type="primary", use_container_width=True):
            st.session_state.current_page = "Upload & Analyze"
            st.rerun()
    with cta2:
        if st.session_state.analysis_done and st.button("View dashboard", use_container_width=True):
            st.session_state.current_page = "Analytics Dashboard"
            st.rerun()



# ── Page: Upload & Analyze ─────────────────────────────────────────────────────
def page_upload():
    render_page_header("Upload & Analyze")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### Upload your PDF Resume")
        uploaded_file = st.file_uploader(
            "Drag & drop or click to upload",
            type=["pdf"],
            help="Upload a PDF resume. Max 10MB.",
            label_visibility="collapsed"
        )

        st.markdown("#### Or use the Demo Resume")
        demo_col1, demo_col2 = st.columns(2)
        with demo_col1:
            if st.button("Load Sample Resume", use_container_width=True):
                sample_text = mods["get_sample_resume_text"]()
                st.session_state.resume_text = sample_text
                st.session_state.parsed_resume = {
                    "raw_text": sample_text,
                    "cleaned_text": sample_text,
                    "sections": {},
                    "contact_info": {
                        "email": "john.smith@email.com",
                        "phone": "+1-555-0123",
                        "linkedin": "linkedin.com/in/johnsmith",
                        "github": "github.com/johnsmith",
                    },
                    "stats": {
                        "word_count": len(sample_text.split()),
                        "estimated_pages": 1.5,
                    }
                }
                from resume_parser import detect_sections
                st.session_state.parsed_resume["sections"] = detect_sections(sample_text)
                st.session_state.demo_mode = True
                st.success("Sample resume loaded! Click 'Run Full Analysis' below.")

    with col2:
        st.markdown("#### Resume Tips")
        tips = [
            "Use a clean, single-column layout for better ATS parsing",
            "Include a dedicated Skills section with technical keywords",
            "Quantify your achievements with numbers and percentages",
            "Use standard section headers (Experience, Education, Skills)",
            "Add LinkedIn and GitHub profile URLs",
        ]
        for tip in tips:
            st.markdown(f"<div style='color:var(--text-muted); font-size:0.85rem; padding:4px 0;'>- {tip}</div>",
                        unsafe_allow_html=True)

    # Process uploaded file
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting text from PDF..."):
                parsed = mods["parse_resume"](uploaded_file)
                st.session_state.resume_text = parsed["cleaned_text"]
                st.session_state.parsed_resume = parsed
                st.session_state.demo_mode = False
            st.success(f"Resume uploaded successfully! ({parsed['stats']['word_count']} words detected)")
        except Exception as e:
            st.error(f"Failed to parse resume: {str(e)}")
            st.info("Try using the Sample Resume for a demo.")

    # Show resume content preview
    if st.session_state.resume_text:
        st.markdown("---")

        # Stats cards
        parsed = st.session_state.parsed_resume or {}
        stats = parsed.get("stats", {})
        contact = parsed.get("contact_info", {})

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>W</div>
                <div class='metric-value'>{stats.get('word_count', '?')}</div>
                <div class='metric-label'>Word Count</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>P</div>
                <div class='metric-value'>{stats.get('estimated_pages', '?')}</div>
                <div class='metric-label'>Est. Pages</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            has_email = "Yes" if contact.get("email") else "No"
            st.markdown(f"""<div class='metric-card' style='border: 1px solid rgba(20,184,166,0.15); border-radius: 12px; padding: 16px;'>
                <div class='metric-icon'>@</div>
                <div class='metric-value' style='font-size:1.5rem;'>{has_email}</div>
                <div class='metric-label'>Email Found</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            has_linkedin = "Yes" if contact.get("linkedin") else "No"
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>in</div>
                <div class='metric-value' style='font-size:1.5rem;'>{has_linkedin}</div>
                <div class='metric-label'>LinkedIn</div>
            </div>""", unsafe_allow_html=True)

        # Resume text preview
        st.markdown("#### Extracted Resume Content")
        with st.expander("View extracted text", expanded=False):
            preview = html.escape(st.session_state.resume_text or "")
            st.markdown(
                f'<pre class="resume-preview">{preview}</pre>',
                unsafe_allow_html=True,
            )

        # Analyze button
        st.markdown("---")
        if st.button("Run Full AI Analysis", use_container_width=True, type="primary"):
            success = run_full_analysis(st.session_state.resume_text, st.session_state.parsed_resume)
            if success:
                st.success("Analysis complete! Navigate to any section to see your results.")
                st.balloons()

    else:
        render_empty_state("\U0001f4c4", "No resume yet", "Upload a PDF or load the sample resume to get started.")


# ── Page: ATS Score ────────────────────────────────────────────────────────────
def page_ats_score():
    render_page_header("ATS Score")
    if not require_analysis("ATS Score"):
        return

    ats = st.session_state.ats_result

    # Main score display
    col1, col2 = st.columns([1, 2])

    with col1:
        fig_gauge = mods["create_ats_gauge"](ats["total_score"], ats["tier"])
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

        # Tier message
        tier_colors = {
            "Excellent": "#10B981", "Good": "#3B82F6",
            "Fair": "#F59E0B", "Poor": "#EF4444", "Critical": "#DC2626"
        }
        color = tier_colors.get(ats["tier"], "#6366F1")
        st.markdown(f"""
        <div style='background: var(--bg-muted); border: 1px solid {color}33;
                    border-left: 4px solid {color}; border-radius: 8px; padding: 12px;
                    color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;'>
            {ats['tier_message']}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Radar chart
        fig_radar = mods["create_ats_components_radar"](ats["component_scores"])
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    # Component breakdown
    st.markdown("#### Score Breakdown by Component")
    progress_data = mods["create_ats_progress_bars_data"](
        ats["component_scores"], ats["scoring_weights"]
    )

    col1, col2 = st.columns(2)
    for i, item in enumerate(progress_data):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            score = item["score"]
            st.markdown(f"""
            <div style='margin-bottom: 16px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                    <span style='color: var(--text-muted); font-size: 0.88rem; font-weight: 500;'>
                        {item['label']}
                    </span>
                    <span style='color: {item['color']}; font-size: 0.88rem; font-weight: 600;'>
                        {score}/100
                        <span style='color: #475569; font-size: 0.75rem;'>
                            (weight: {item['weight']}%)
                        </span>
                    </span>
                </div>
                <div class='custom-progress-container'>
                    <div class='custom-progress-fill' 
                         style='width: {score}%; background: linear-gradient(90deg, {item["color"]}88, {item["color"]});'>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Feedback
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### What's Working Well")
        for msg in ats["positive_feedback"][:10]:
            st.markdown(f"<div class='feedback-positive'>{msg}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("#### Improvements Needed")
        improvements = [m for m in ats["improvement_feedback"]][:5]
        warnings = [m for m in ats["improvement_feedback"] if m not in improvements][:5]
        for msg in improvements:
            st.markdown(f"<div class='feedback-negative'>{msg}</div>", unsafe_allow_html=True)
        for msg in warnings:
            st.markdown(f"<div class='feedback-warning'>{msg}</div>", unsafe_allow_html=True)


# ── Page: Job Matches ──────────────────────────────────────────────────────────
def page_job_matches():
    render_page_header("Job Matches")
    if not require_analysis("Job Matches"):
        return

    recs = st.session_state.recommendations

    # Chart
    fig = mods["create_job_match_chart"](recs)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")

    # Detailed cards for top matches
    st.markdown("#### Top Role Matches")

    for i, rec in enumerate(recs[:5]):
        score = rec["match_percentage"]
        score_color = (
            "#10B981" if score >= 75 else
            "#3B82F6" if score >= 55 else
            "#F59E0B" if score >= 35 else "#EF4444"
        )
        rank_label = ["#1", "#2", "#3", "#4", "#5"][i]

        with st.expander(f"{rank_label} {rec['role']} - {score}% Match | {rec['salary_range']}", expanded=i == 0):
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.markdown("**Matched Skills**")
                for skill in rec["matched_skills"]:
                    st.markdown(f"<span class='skill-tag skill-tag-present'>✓ {skill}</span>",
                                unsafe_allow_html=True)

            with col2:
                st.markdown("**Skills to Add**")
                for skill in rec["missing_skills"][:6]:
                    st.markdown(f"<span class='skill-tag skill-tag-missing'>+ {skill}</span>",
                                unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px;'>
                    <div style='font-size: 2rem; font-weight: 700; color: {score_color};'>{score}%</div>
                    <div style='color: #64748B; font-size: 0.75rem;'>Match Score</div>
                    <br>
                    <div style='color: var(--text-muted); font-size: 0.82rem;'>{rec['experience_years']}</div>
                    <div style='color: var(--text-muted); font-size: 0.82rem;'>{rec['salary_range']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Explanation
            explanation = mods["explain_recommendation"](rec, st.session_state.extracted_skills or [])
            st.markdown(explanation)


# ── Page: Skill Analysis ───────────────────────────────────────────────────────
def page_skill_analysis():
    render_page_header("Skill Analysis")
    if not require_analysis("Skill Analysis"):
        return

    skill_data = st.session_state.skill_data

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("", len(skill_data["all_skills"]), "Total Skills"),
        ("", len(skill_data["primary_skills"]), "Primary Skills"),
        ("", len(skill_data["categorized_skills"]), "Categories"),
        ("", skill_data["experience_info"]["estimated_level"], "Seniority Level"),
    ]
    for col, (icon, val, label) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>{icon}</div>
                <div class='metric-value' style='font-size: {'1.8rem' if isinstance(val, str) else '2.5rem'};'>
                    {val}
                </div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        fig_bar = mods["create_skill_bar_chart"](skill_data["skill_frequency"], top_n=15)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col2:
        fig_donut = mods["create_skill_category_donut"](skill_data["categorized_skills"])
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    # Skills by category
    st.markdown("---")
    st.markdown("#### Skills by Category")

    category_icons = {
        "programming_languages": "",
        "ml_ai": "",
        "frameworks_libraries": "",
        "databases": "",
        "cloud_devops": "",
        "tools": "",
        "other": ""
    }

    cats = skill_data["categorized_skills"]
    cols = st.columns(min(3, len(cats)))
    for i, (cat, skills) in enumerate(cats.items()):
        icon = category_icons.get(cat, "")
        label = cat.replace("_", " ").title()
        with cols[i % 3]:
            st.markdown(f"**{label}** ({len(skills)})")
            skill_html = " ".join([f"<span class='skill-tag'>{s}</span>" for s in skills])
            st.markdown(skill_html, unsafe_allow_html=True)
            st.markdown("")

    # Education & Experience info
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Education Info")
        edu = skill_data.get("education_info", {})
        st.markdown(f"""
        <div class='info-panel'>
                Degree: <b>{edu.get('degree', 'Not detected')}</b><br>
                Field: <b>{edu.get('field', 'Not detected')}</b><br>
                GPA: <b>{edu.get('gpa', 'Not detected')}</b><br>
                Year: <b>{edu.get('graduation_year', 'Not detected')}</b>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Experience Info")
        exp = skill_data.get("experience_info", {})
        st.markdown(f"""
        <div class='info-panel'>
                Level: <b>{exp.get('estimated_level', 'Unknown')}</b><br>
                Years: <b>{exp.get('total_years', 0)} years estimated</b><br>
                Positions: <b>{len(exp.get('year_ranges', []))} detected</b><br>
        </div>
        """, unsafe_allow_html=True)


# ── Page: Skill Gap ────────────────────────────────────────────────────────────
def page_skill_gap():
    render_page_header("Skill Gap")
    if not require_analysis("Skill Gap"):
        return

    from datasets.job_descriptions import JOB_ROLES
    all_roles = list(JOB_ROLES.keys())

    # Role selector
    default_role = st.session_state.recommendations[0]["role"] if st.session_state.recommendations else all_roles[0]
    default_idx = all_roles.index(default_role) if default_role in all_roles else 0

    selected_role = st.selectbox(
        "Select target job role for gap analysis:",
        options=all_roles,
        index=default_idx,
        help="Choose the role you're targeting to see your skill gaps"
    )

    if st.button("Analyze Skill Gap", use_container_width=False):
        skill_gap = mods["compute_skill_gap"](
            st.session_state.extracted_skills or [],
            selected_role
        )
        st.session_state.skill_gap = skill_gap

    # Display results
    if st.session_state.skill_gap:
        gap = st.session_state.skill_gap
        target = gap.get("target_role", selected_role)

        # Completion score
        completion = gap.get("completion_score", 0)
        score_color = "#10B981" if completion >= 75 else "#3B82F6" if completion >= 50 else "#F59E0B"

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #F0FDFA, #ECFEFF);
                    border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px;
                    margin: 16px 0; display: flex; align-items: center; gap: 20px;'>
            <div style='text-align: center; min-width: 100px;'>
                <div style='font-size: 2.5rem; font-weight: 700; color: {score_color};'>{completion}%</div>
                <div style='color: #64748B; font-size: 0.78rem;'>Requirements Met</div>
            </div>
            <div>
                <div style='font-family: Space Grotesk; font-size: 1.2rem; font-weight: 600; color: var(--text);'>
                    {target}
                </div>
                <div style='color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;'>
                    {gap.get('salary_range', 'N/A')} &nbsp;|&nbsp; {gap.get('experience_required', 'N/A')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Chart
        fig_gap = mods["create_skill_gap_chart"](gap)
        st.plotly_chart(fig_gap, use_container_width=True, config={"displayModeBar": False})

        # Skills breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Skills You Have")
            if gap["matched_required"]:
                for skill in gap["matched_required"]:
                    st.markdown(f"<span class='skill-tag skill-tag-present'>✓ {skill}</span>",
                                unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#64748B;'>None matched</span>", unsafe_allow_html=True)

        with col2:
            st.markdown("#### Skills to Learn")
            if gap["missing_required"]:
                for skill in gap["missing_required"]:
                    st.markdown(f"<span class='skill-tag skill-tag-missing'>+ {skill}</span>",
                                unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#10B981;'>All required skills covered!</span>",
                            unsafe_allow_html=True)

        # Certifications
        st.markdown("---")
        st.markdown("#### Recommended Certifications")
        certs = gap.get("recommended_certifications", [])
        if certs:
            for cert in certs:
                st.markdown(f"<span class='cert-tag'>{cert}</span>", unsafe_allow_html=True)
        else:
            st.info("No specific certifications found for this role.")


# ── Page: Role Predictor ───────────────────────────────────────────────────────
def page_role_predictor():
    render_page_header("Role Predictor")
    if not require_analysis("Role Predictor"):
        return

    pred = st.session_state.prediction_result

    # Prediction hero
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #F0FDFA, #ECFEFF);
                border: 1px solid #99F6E4; border-radius: 20px; padding: 28px;
                text-align: center; margin-bottom: 24px;'>
        <div style='color: var(--text-muted); font-size: 0.9rem; text-transform: uppercase; 
                    letter-spacing: 0.1em;'>ML Model Prediction</div>
        <div style='font-family: Space Grotesk; font-size: 2.2rem; font-weight: 700;
                    color: var(--text); margin: 12px 0;'>
            {pred['predicted_role']}
        </div>
        <div style='display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;'>
            <span class='badge badge-primary'>Confidence: {pred['confidence']:.1f}%</span>
            <span class='badge badge-primary'>Model: {pred['model_type'].replace('_', ' ').title()}</span>
            <span class='badge badge-success'>Accuracy: {pred['model_accuracy']:.0f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Probability chart
    col1, col2 = st.columns([3, 2])

    with col1:
        fig_pred = mods["create_role_prediction_chart"](pred)
        st.plotly_chart(fig_pred, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("#### Top 3 Predictions")
        for rank, (role, prob) in enumerate(pred["top_3_roles"]):
            rank_icon = ["#1", "#2", "#3"][rank]
            bar_width = int(prob * 2) if prob <= 50 else 100
            color = "#0D9488" if rank == 0 else "#0891B2" if rank == 1 else "#5EEAD4"
            st.markdown(f"""
            <div style='margin-bottom: 16px; background: var(--bg-muted);
                        border-radius: 10px; padding: 14px;
                        border: 1px solid {"#99F6E4" if rank == 0 else "#E2E8F0"};'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: var(--text); font-weight: 500;'>{rank_icon} {role}</span>
                    <span style='color: {color}; font-weight: 600;'>{prob:.1f}%</span>
                </div>
                <div class='custom-progress-container' style='margin-top: 8px;'>
                    <div class='custom-progress-fill' style='width: {prob:.0f}%; background: {color};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Feature importance (Explainable AI)
    st.markdown("---")
    st.markdown("#### Explainable AI - What Influenced the Prediction?")

    features = pred.get("feature_importance", [])
    if features:
        st.markdown("<p style='color:var(--text-muted); font-size:0.88rem;'>These keywords had the highest influence on the ML model's prediction:</p>",
                    unsafe_allow_html=True)

        cols = st.columns(2)
        for i, feat in enumerate(features[:8]):
            with cols[i % 2]:
                score_pct = min(100, feat["score"] * 1000)
                is_skill_badge = "skill" if feat["is_skill"] else "keyword"
                st.markdown(f"""
                <div style='background: #FFFFFF; border-radius: 8px; padding: 10px;
                            border: 1px solid #E2E8F0; margin-bottom: 8px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='color: var(--text); font-weight: 500; font-size: 0.9rem;'>
                            {feat['feature']}
                        </span>
                        <span style='color: var(--accent); font-size: 0.75rem;'>{is_skill_badge}</span>
                    </div>
                    <div class='custom-progress-container' style='margin-top: 6px;'>
                        <div class='custom-progress-fill' 
                             style='width: {score_pct:.0f}%; background: linear-gradient(90deg, #99F6E4, #0D9488);'>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Model selector
    st.markdown("---")
    st.markdown("#### Try Different ML Models")
    model_choice = st.selectbox(
        "Select model:",
        ["logistic_regression", "random_forest", "naive_bayes"],
        format_func=lambda x: x.replace("_", " ").title()
    )
    if st.button(f"Re-run with {model_choice.replace('_', ' ').title()}", use_container_width=False):
        with st.spinner("Training model and predicting..."):
            predictor = mods["get_role_predictor"](model_choice)
            new_pred = predictor.predict(
                st.session_state.resume_text or "",
                st.session_state.extracted_skills or []
            )
            new_pred["feature_importance"] = predictor.get_feature_importance(
                st.session_state.resume_text or "",
                st.session_state.extracted_skills or []
            )
            st.session_state.prediction_result = new_pred
            st.success(f"Re-run with {model_choice.replace('_', ' ').title()} complete!")
            st.rerun()


# ── Page: Interview Prep ───────────────────────────────────────────────────────
def page_interview_prep():
    render_page_header("Interview Prep")
    if not require_analysis("Interview Prep"):
        return

    pack = st.session_state.interview_pack

    # Header stats
    c1, c2, c3, c4 = st.columns(4)
    stats_data = [
        ("", pack["total_questions"], "Total Questions"),
        ("", len(pack["technical_questions"]), "Technical Topics"),
        ("", len(pack.get("role_specific_questions", [])), "Role-Specific"),
        ("", len(pack["behavioral_questions"]), "Behavioral"),
    ]
    for col, (icon, val, label) in zip([c1, c2, c3, c4], stats_data):
        with col:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>{icon}</div>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Interactive practice mode toggle
    practice_mode = st.toggle("Practice Mode — track your progress", value=False, key="practice_toggle")

    # Interview tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Technical", "Role-Specific", "Scenarios", "Behavioral"
    ])

    with tab1:
        for skill, questions in pack["technical_questions"].items():
            st.markdown(f"##### {skill}")
            for i, q in enumerate(questions, 1):
                qkey = f"tech_{skill}_{i}"
                col_q, col_check = st.columns([9, 1]) if practice_mode else (st.columns(1)[0], None)
                if practice_mode:
                    with col_q:
                        st.markdown(f"""
                        <div class='question-box'>
                            <span style='color: #14B8A6; font-weight: 600;'>Q{i}.</span> {q}
                        </div>
                        """, unsafe_allow_html=True)
                    with col_check:
                        st.checkbox("Done", key=qkey, label_visibility="collapsed")
                else:
                    with col_q:
                        st.markdown(f"""
                        <div class='question-box'>
                            <span style='color: #14B8A6; font-weight: 600;'>Q{i}.</span> {q}
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown("")

    with tab2:
        role_qs = pack.get("role_specific_questions", [])
        if role_qs:
            for i, q in enumerate(role_qs, 1):
                qkey = f"role_{i}"
                col_q, col_check = st.columns([9, 1]) if practice_mode else (st.columns(1)[0], None)
                if practice_mode:
                    with col_q:
                        st.markdown(f"""
                        <div class='question-box'>
                            <span style='color: #0891B2; font-weight: 600;'>Q{i}.</span> {q}
                        </div>
                        """, unsafe_allow_html=True)
                    with col_check:
                        st.checkbox("Done", key=qkey, label_visibility="collapsed")
                else:
                    with col_q:
                        st.markdown(f"""
                        <div class='question-box'>
                            <span style='color: #0891B2; font-weight: 600;'>Q{i}.</span> {q}
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No role-specific questions available.")

    with tab3:
        scenario_qs = pack.get("scenario_questions", [])
        if scenario_qs:
            for i, q in enumerate(scenario_qs, 1):
                st.markdown(f"""
                <div class='question-box' style='border-left-color: #EC4899;'>
                    <span style='color: #EC4899; font-weight: 600;'>Scenario {i}.</span> {q}
                </div>
                """, unsafe_allow_html=True)

    with tab4:
        for i, q in enumerate(pack["behavioral_questions"], 1):
            st.markdown(f"""
            <div class='question-box' style='border-left-color: #10B981;'>
                <span style='color: #10B981; font-weight: 600;'>Q{i}.</span> {q}
            </div>
            """, unsafe_allow_html=True)

    # Practice progress summary
    if practice_mode:
        total_practiced = sum(1 for k, v in st.session_state.items() if (k.startswith("tech_") or k.startswith("role_")) and v is True)
        st.markdown(f"""
        <div style='background: rgba(20,184,166,0.08); border: 1px solid rgba(20,184,166,0.20);
                    border-radius: 12px; padding: 14px 20px; margin-top: 12px;
                    color: var(--accent-text); font-size: 0.9rem; font-weight: 500;'>
            Questions practiced: <b>{total_practiced}</b>
        </div>
        """, unsafe_allow_html=True)

    # Download button
    st.markdown("---")
    md_content = mods["format_interview_pack_markdown"](pack)
    st.download_button(
        label="Download Interview Questions (Markdown)",
        data=md_content,
        file_name="interview_prep_guide.md",
        mime="text/markdown",
        use_container_width=False
    )


# ── Page: Analytics Dashboard ──────────────────────────────────────────────────
def page_analytics_dashboard():
    render_page_header("Analytics Dashboard")
    if not require_analysis("the analytics dashboard"):
        return

    ats = st.session_state.ats_result or {}
    skill_data = st.session_state.skill_data or {}
    recs = st.session_state.recommendations or []
    pred = st.session_state.prediction_result or {}

    # Summary metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    summary_metrics = [
        ("", f"{ats.get('total_score', 0)}/100", "ATS Score"),
        ("", len(skill_data.get("all_skills", [])), "Skills Detected"),
        ("", f"{recs[0]['match_percentage'] if recs else 0}%", "Best Match"),
        ("", pred.get("predicted_role", "N/A"), "Predicted Role"),
        ("", skill_data.get("experience_info", {}).get("estimated_level", "N/A"), "Seniority"),
    ]
    for col, (icon, val, label) in zip([c1, c2, c3, c4, c5], summary_metrics):
        with col:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>{icon}</div>
                <div class='metric-value' style='font-size: 1.5rem;'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        if ats.get("component_scores"):
            fig = mods["create_ats_components_radar"](ats["component_scores"])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        if recs:
            fig = mods["create_job_match_chart"](recs[:6])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Row 2
    col1, col2 = st.columns(2)
    with col1:
        if skill_data.get("skill_frequency"):
            fig = mods["create_skill_bar_chart"](skill_data["skill_frequency"], top_n=12)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        if pred:
            fig = mods["create_role_prediction_chart"](pred)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Row 3
    col1, col2 = st.columns(2)
    with col1:
        if skill_data.get("categorized_skills"):
            fig = mods["create_skill_category_donut"](skill_data["categorized_skills"])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        if st.session_state.skill_gap:
            fig = mods["create_skill_gap_chart"](st.session_state.skill_gap)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ATS gauge
    if ats:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            fig_gauge = mods["create_ats_gauge"](ats["total_score"], ats["tier"])
            st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})


# ── Main Router ────────────────────────────────────────────────────────────────
def main():
    render_sidebar()

    page = st.session_state.current_page

    if page == "Home":
        page_home()
    elif page == "Upload & Analyze":
        page_upload()
    elif page == "ATS Score":
        page_ats_score()
    elif page == "Job Matches":
        page_job_matches()
    elif page == "Skill Analysis":
        page_skill_analysis()
    elif page == "Skill Gap":
        page_skill_gap()
    elif page == "Role Predictor":
        page_role_predictor()
    elif page == "Interview Prep":
        page_interview_prep()
    elif page == "Analytics Dashboard":
        page_analytics_dashboard()


if __name__ == "__main__":
    main()
