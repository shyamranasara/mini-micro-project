import streamlit as st
import os
import sys
import importlib.util
from theme import apply_figma_theme, PRIMARY, SECONDARY, ACCENT_PINK

# Set central page configuration
st.set_page_config(
    page_title="Mini-Micro ML Projects Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global Figma Design System
apply_figma_theme()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_sub_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def render_home():
    st.markdown('<div class="hero-title">⚡ Mini-Micro ML Project Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">A curated collection of human-designed machine learning dashboards, analytical engines, and real-time clinical & economic models crafted by <b>Shyam Ranasara</b>.</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Portfolio Statistics Summary
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Featured Projects", "4 Active Modules")
    m2.metric("Core ML Domains", "Classification, Reg., NLP, EDA")
    m3.metric("Interactive Dashboards", "100% Functional")
    m4.metric("Inference Engine", "Offline Pickled (.pkl)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🎯 Explore Machine Learning Applications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="figma-card">
            <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">🗳️ 1. Electoral Bonds Analytics</h3>
            <span class="badge-pill">Financial Flow</span>
            <span class="badge-pill badge-emerald">Plotly Analytics</span>
            <span class="badge-pill">Political Funding</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #94A3B8; line-height: 1.6;">
                Comprehensive exploratory analysis linking corporate bond purchases directly to political party encashment records. Interactive charts, top donor rankings, and denomination distribution.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="figma-card">
            <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">❤️ 3. Heart Attack Risk Predictor</h3>
            <span class="badge-pill badge-rose">Clinical Risk ML</span>
            <span class="badge-pill">Random Forest</span>
            <span class="badge-pill badge-emerald">80.3% Accuracy</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #94A3B8; line-height: 1.6;">
                Medical classifier evaluating 13 clinical vitals (age, blood pressure, cholesterol, ECG, thal) to predict cardiovascular risk tiers with real-time risk gauges.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="figma-card">
            <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">📰 2. Fake News Detection AI</h3>
            <span class="badge-pill">NLP Verification</span>
            <span class="badge-pill badge-emerald">TF-IDF Vectorizer</span>
            <span class="badge-pill">Text Classifier</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #94A3B8; line-height: 1.6;">
                Natural Language Processing pipeline detecting online misinformation and fake headlines in real-time, complete with keyword TF-IDF weight extraction.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="figma-card">
            <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">🚗 4. Used Car Price Valuation AI</h3>
            <span class="badge-pill badge-amber">Price Regression</span>
            <span class="badge-pill">HistGradientBoosting</span>
            <span class="badge-pill">Label Encoders</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #94A3B8; line-height: 1.6;">
                Automated vehicle valuation engine predicting resale car prices in Lakhs INR based on brand model, location, registration year, mileage, engine CC, and power.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **Navigation Tip**: Select any project from the sidebar menu on the left to launch its interactive dashboard.")

def main():
    st.sidebar.markdown("""
    <div style="padding: 0.5rem 0; text-align: center;">
        <h2 style="font-weight: 800; background: linear-gradient(135deg, #6366F1, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">⚡ ML Studio</h2>
        <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 0.2rem;">By Shyam Ranasara</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    app_choice = st.sidebar.radio(
        "Select Application Dashboard:",
        [
            "🏠 Studio Overview",
            "🗳️ Election Bonds Analytics",
            "📰 Fake News Detection AI",
            "❤️ Heart Attack Risk Predictor",
            "🚗 Used Car Price Valuation"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Theme & Architecture")
    st.sidebar.markdown("""
    - **Design**: Figma Obsidian Slate & Indigo
    - **Engine**: Python 3.14 + Streamlit
    - **ML Suite**: Scikit-Learn (Random Forest, Gradient Boosting, TF-IDF)
    - **Graphics**: Plotly Interactive
    """)
    st.sidebar.caption("© Mini-Micro ML Project Studio")

    if app_choice == "🏠 Studio Overview":
        render_home()
    elif app_choice == "🗳️ Election Bonds Analytics":
        eb_path = os.path.join(ROOT_DIR, "Election Bonds", "app.py")
        mod = load_sub_module("election_bonds_app", eb_path)
        mod.render_election_bonds_app()
    elif app_choice == "📰 Fake News Detection AI":
        fn_path = os.path.join(ROOT_DIR, "Fake News Detection", "app.py")
        mod = load_sub_module("fake_news_app", fn_path)
        mod.render_fake_news_app()
    elif app_choice == "❤️ Heart Attack Risk Predictor":
        ha_path = os.path.join(ROOT_DIR, "Heart Attack Analysis", "app.py")
        mod = load_sub_module("heart_app", ha_path)
        mod.render_heart_app()
    elif app_choice == "🚗 Used Car Price Valuation":
        cp_path = os.path.join(ROOT_DIR, "car_price", "app.py")
        mod = load_sub_module("car_price_app", cp_path)
        mod.render_car_price_app()

if __name__ == "__main__":
    main()
