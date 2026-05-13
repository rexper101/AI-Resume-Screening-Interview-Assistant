"""
dashboard.py - Interactive analytics dashboard visualizations using Plotly.
Creates all charts and graphs for the resume analysis results.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional


# ── Color Palette ─────────────────────────────────────────────────────────────
COLORS = {
    "primary": "#8B5CF6",      # Violet
    "secondary": "#6366F1",    # Indigo
    "accent": "#EC4899",       # Pink
    "success": "#10B981",      # Emerald
    "warning": "#F59E0B",      # Amber
    "danger": "#EF4444",       # Red
    "info": "#3B82F6",         # Blue
    "bg_dark": "#09090B",
    "card_bg": "#18181B",
    "text": "#F8FAFC",
}

CHART_COLORS = [
    "#8B5CF6", "#6366F1", "#EC4899", "#10B981", "#F59E0B",
    "#3B82F6", "#A78BFA", "#F97316", "#84CC16", "#06B6D4"
]

CHART_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#F8FAFC", "family": "Inter, sans-serif"},
        "xaxis": {"gridcolor": "rgba(255,255,255,0.1)", "linecolor": "rgba(255,255,255,0.2)"},
        "yaxis": {"gridcolor": "rgba(255,255,255,0.1)", "linecolor": "rgba(255,255,255,0.2)"},
    }
}


def apply_dark_theme(fig: go.Figure) -> go.Figure:
    """Apply consistent dark theme to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="Inter, sans-serif", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)")
    return fig


def create_ats_gauge(score: int, tier: str) -> go.Figure:
    """
    Create an ATS score gauge chart.

    Args:
        score: ATS score (0-100)
        tier: Score tier (Excellent, Good, Fair, Poor)

    Returns:
        Plotly figure
    """
    tier_colors = {
        "Excellent": "#10B981",
        "Good": "#3B82F6",
        "Fair": "#F59E0B",
        "Poor": "#EF4444",
        "Critical": "#DC2626"
    }
    color = tier_colors.get(tier, "#6366F1")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        number={
            "suffix": "/100",
            "font": {"size": 36, "color": color, "family": "Outfit, sans-serif"},
        },
        delta={"reference": 70, "increasing": {"color": "#10B981"}, "decreasing": {"color": "#EF4444"}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(255,255,255,0.3)",
                "tickfont": {"color": "#94A3B8"},
            },
            "bar": {"color": color, "thickness": 0.7},
            "bgcolor": "rgba(255,255,255,0.05)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(239,68,68,0.15)"},
                {"range": [40, 60], "color": "rgba(245,158,11,0.15)"},
                {"range": [60, 80], "color": "rgba(59,130,246,0.15)"},
                {"range": [80, 100], "color": "rgba(16,185,129,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#FFFFFF", "width": 2},
                "thickness": 0.85,
                "value": score,
            },
        },
        title={
            "text": f"ATS Score<br><span style='font-size:14px;color:{color}'>{tier}</span>",
            "font": {"size": 18, "color": "#F8FAFC", "family": "Outfit, sans-serif"}
        }
    ))


    fig = go.Figure()

    # Filled area
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill='toself',
        fillcolor="rgba(139,92,246,0.2)",
        line=dict(color="#8B5CF6", width=2),
        name="Your Resume",
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.0f}/100<extra></extra>'
    ))

    # Target line (80 for all)
    target = [80] * len(labels) + [80]
    fig.add_trace(go.Scatterpolar(
        r=target,
        theta=labels_closed,
        fill='toself',
        fillcolor="rgba(16,185,129,0.05)",
        line=dict(color="#10B981", width=1, dash="dot"),
        name="Target (80)",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#A1A1AA", size=10),
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.15)"
            ),
            angularaxis=dict(
                tickfont=dict(color="#F8FAFC", size=10),
                linecolor="rgba(255,255,255,0.15)",
                gridcolor="rgba(255,255,255,0.1)"
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(text="ATS Score Breakdown", font=dict(size=16, color="#F8FAFC", family="Outfit, sans-serif")),
        legend=dict(font=dict(color="#94A3B8")),
        height=380,
        margin=dict(l=60, r=60, t=60, b=40),
    )
    return fig


def create_role_prediction_chart(prediction_result: Dict) -> go.Figure:
    """
    Create bar chart of role prediction probabilities.

    Args:
        prediction_result: Prediction result from RolePredictor

    Returns:
        Plotly figure
    """
    if not prediction_result or "all_probabilities" not in prediction_result:
        return go.Figure()

    probs = prediction_result["all_probabilities"]

    roles = list(probs.keys())[::-1]
    confidences = list(probs.values())[::-1]

    # Highlight predicted role
    predicted = prediction_result["predicted_role"]
    bar_colors = [
        "#8B5CF6" if role == predicted else "rgba(139,92,246,0.35)"
        for role in roles
    ]

    fig = go.Figure(go.Bar(
        x=confidences,
        y=roles,
        orientation='h',
        marker=dict(
            color=bar_colors,
            line=dict(color="rgba(255,255,255,0.05)", width=1)
        ),
        text=[f"{c:.1f}%" for c in confidences],
        textposition='outside',
        textfont=dict(color="#F8FAFC", size=11),
        hovertemplate='<b>%{y}</b><br>Probability: %{x:.1f}%<extra></extra>',
    ))

    fig.update_layout(
        title=dict(
            text=f"Role Prediction | {prediction_result.get('model_type', 'N/A').replace('_', ' ').title()}",
            font=dict(size=15, color="#F8FAFC", family="Outfit, sans-serif")
        ),
        xaxis=dict(range=[0, max(confidences) * 1.3 if confidences else 110], ticksuffix="%"),
        height=max(280, len(roles) * 45),
        showlegend=False,
    )

    return apply_dark_theme(fig)


def create_skill_gap_chart(skill_gap: Dict) -> go.Figure:
    """
    Create skill gap visualization with matched vs missing skills.

    Args:
        skill_gap: Skill gap analysis result

    Returns:
        Plotly figure
    """
    matched = len(skill_gap.get("matched_required", []))
    missing = len(skill_gap.get("missing_required", []))
    optional_matched = len(skill_gap.get("matched_optional", []))
    optional_missing = len(skill_gap.get("missing_optional", []))

    fig = go.Figure()

    categories = ["Required Skills", "Nice-to-Have Skills"]
    matched_vals = [matched, optional_matched]
    missing_vals = [missing, optional_missing]

    fig.add_trace(go.Bar(
        name="You Have",
        x=categories,
        y=matched_vals,
        marker_color="#10B981",
        text=matched_vals,
        textposition='inside',
        textfont=dict(color="white", size=14, family="Inter, sans-serif"),
    ))

    fig.add_trace(go.Bar(
        name="To Learn",
        x=categories,
        y=missing_vals,
        marker_color="#EF4444",
        text=missing_vals,
        textposition='inside',
        textfont=dict(color="white", size=14, family="Inter, sans-serif"),
    ))

    fig.update_layout(
        barmode='stack',
        title=dict(
            text=f"Skill Gap: {skill_gap.get('target_role', 'Target Role')}",
            font=dict(size=16, color="#F8FAFC", family="Outfit, sans-serif")
        ),
        legend=dict(font=dict(color="#94A3B8"), bgcolor="rgba(0,0,0,0)"),
        height=300,
        showlegend=True,
    )

    return apply_dark_theme(fig)


def create_ats_progress_bars_data(component_scores: Dict, weights: Dict) -> List[Dict]:
    """
    Prepare data for Streamlit progress bars showing ATS components.

    Args:
        component_scores: Dict of component → score
        weights: Dict of component → weight

    Returns:
        List of dicts with progress bar data
    """
    progress_data = []

    label_map = {
        "keyword_optimization": "Keyword Optimization",
        "skills_relevance": "Skills Relevance",
        "structure_quality": "Resume Structure",
        "experience_section": "Experience Quality",
        "education_section": "Education Section",
        "contact_completeness": "Contact Information",
        "additional_sections": "Additional Sections",
    }

    for component, score in component_scores.items():
        weight = weights.get(component, 0)
        progress_data.append({
            "label": label_map.get(component, component.replace("_", " ").title()),
            "score": score,
            "weight": weight,
            "weighted_contribution": round(score / 100 * weight, 1),
            "color": (
                "#10B981" if score >= 80 else
                "#3B82F6" if score >= 60 else
                "#F59E0B" if score >= 40 else
                "#EF4444"
            )
        })

    return progress_data
