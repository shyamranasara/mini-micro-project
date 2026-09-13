import streamlit as st
import plotly.io as pio

# Curated Human-Designed Color Tokens (Obsidian Slate & Indigo Emerald)
PRIMARY = "#6366F1"       # Indigo Violet Accent
SECONDARY = "#10B981"     # Emerald Green Accent
WARNING = "#F59E0B"       # Warm Amber
DANGER = "#EF4444"        # Crimson Rose
ACCENT_PINK = "#EC4899"   # Neon Pink
BG_DARK = "#0B0F19"       # Deep Midnight Obsidian
CARD_BG = "rgba(30, 41, 59, 0.55)" # Glassmorphic Slate
CARD_BORDER = "rgba(99, 102, 241, 0.22)" # Subtle Indigo Stroke
TEXT_MAIN = "#F8FAFC"     # Pearl White
TEXT_MUTED = "#94A3B8"    # Cool Slate Gray

COLOR_PALETTE = ["#6366F1", "#10B981", "#F59E0B", "#EC4899", "#3B82F6", "#8B5CF6", "#14B8A6"]

def apply_figma_theme():
    """Injects Google Fonts, Glassmorphic UI CSS, and high-contrast typography styling into Streamlit."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background-color: #0B0F19 !important;
            color: #F8FAFC !important;
        }

        /* High Contrast Typography Overrides */
        p, span, label, h1, h2, h3, h4, h5, h6, li, td, th {
            color: #F8FAFC !important;
        }

        .stApp p, .stApp label, .stApp span {
            color: #F8FAFC !important;
        }

        /* Glassmorphic Container Cards */
        .figma-card {
            background: rgba(30, 41, 59, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .figma-card:hover {
            transform: translateY(-3px);
            border-color: rgba(99, 102, 241, 0.6);
            box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.25);
        }

        /* Hero Headers */
        .hero-title {
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            background: linear-gradient(135deg, #F8FAFC 0%, #818CF8 50%, #C084FC 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            color: #CBD5E1 !important;
            font-weight: 400;
            margin-bottom: 1.8rem;
            line-height: 1.6;
        }

        /* Pill Badges */
        .badge-pill {
            display: inline-flex;
            align-items: center;
            padding: 0.35rem 0.8rem;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: 9999px;
            background: rgba(99, 102, 241, 0.2);
            color: #A5B4FC !important;
            border: 1px solid rgba(99, 102, 241, 0.4);
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
            letter-spacing: 0.02em;
        }
        .badge-emerald {
            background: rgba(16, 185, 129, 0.2);
            color: #6EE7B7 !important;
            border-color: rgba(16, 185, 129, 0.4);
        }
        .badge-amber {
            background: rgba(245, 158, 11, 0.2);
            color: #FDE047 !important;
            border-color: rgba(245, 158, 11, 0.4);
        }
        .badge-rose {
            background: rgba(239, 68, 68, 0.2);
            color: #FCA5A5 !important;
            border-color: rgba(239, 68, 68, 0.4);
        }

        /* Form Widget Labels & Tooltips */
        label[data-testid="stWidgetLabel"] p, .stSlider label p, .stSelectbox label p, .stNumberInput label p, .stTextInput label p, .stTextArea label p {
            color: #F8FAFC !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        /* Inputs & Selectboxes Text & Contrast */
        .stSelectbox div[data-baseweb="select"], .stTextInput input, .stTextArea textarea, .stNumberInput input {
            background-color: #1E293B !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
            border-radius: 10px !important;
            color: #F8FAFC !important;
            font-weight: 500 !important;
        }

        /* Dropdown Popover Lists (Fix dark text on dark bg) */
        ul[data-baseweb="menu"], div[data-baseweb="popover"] {
            background-color: #1E293B !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
        }
        li[data-baseweb="option"] {
            color: #F8FAFC !important;
            background-color: #1E293B !important;
        }
        li[data-baseweb="option"]:hover, li[aria-selected="true"] {
            background-color: #334155 !important;
            color: #818CF8 !important;
        }

        /* Slider Values & Labels */
        div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"], div[data-testid="stThumbValue"] {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }

        /* Streamlit Metric Boxes */
        div[data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 1.1rem;
            border-radius: 14px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        div[data-testid="stMetricLabel"] p {
            color: #CBD5E1 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="stMetricValue"] div {
            color: #F8FAFC !important;
            font-weight: 800 !important;
        }

        /* Sidebar Styling & Radio Buttons */
        section[data-testid="stSidebar"] {
            background-color: #070A12 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span {
            color: #F8FAFC !important;
            font-weight: 500 !important;
        }
        div[role="radiogroup"] label p {
            color: #F8FAFC !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
        }

        /* Buttons Styling */
        .stButton>button {
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.5rem !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.45) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.65) !important;
            background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
        }

        /* Custom Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(30, 41, 59, 0.6);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .stTabs [data-baseweb="tab"] p {
            color: #CBD5E1 !important;
            font-weight: 600 !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #6366F1 !important;
            border-radius: 8px;
        }
        .stTabs [aria-selected="true"] p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        
        /* Dataframes & Tables */
        .stDataFrame, div[data-testid="stTable"] {
            background-color: #1E293B !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def apply_plotly_figma_theme(fig):
    """Applies a clean, modern Figma dark template to Plotly charts."""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1", size=12),
        title_font=dict(size=16, color="#F8FAFC", family="Plus Jakarta Sans, sans-serif"),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.08)',
            zerolinecolor='rgba(255, 255, 255, 0.15)',
            tickfont=dict(color="#CBD5E1")
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.08)',
            zerolinecolor='rgba(255, 255, 255, 0.15)',
            tickfont=dict(color="#CBD5E1")
        ),
        legend=dict(font=dict(color="#F8FAFC")),
        margin=dict(l=20, r=20, t=45, b=20)
    )
    return fig
