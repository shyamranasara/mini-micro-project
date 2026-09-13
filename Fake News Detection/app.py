import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sys
import re
import string
import plotly.graph_objects as go
import plotly.express as px

# Ensure root directory is importable for theme module
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from theme import apply_figma_theme, apply_plotly_figma_theme, PRIMARY, SECONDARY, DANGER
except ImportError:
    apply_figma_theme = lambda: None
    apply_plotly_figma_theme = lambda fig: fig
    PRIMARY = "#6366F1"
    SECONDARY = "#10B981"
    DANGER = "#EF4444"

st.set_page_config(page_title="Fake News Verification AI", page_icon="📰", layout="wide")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text.strip()

@st.cache_resource
def load_nlp_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'model.pkl')
    vec_path = os.path.join(base_dir, 'vectorizer.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(vec_path):
        return None, None
        
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    return model, vectorizer

def render_fake_news_app():
    apply_figma_theme()
    
    st.markdown('<div class="hero-title">📰 Fake News Verification Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Natural Language Processing (NLP) TF-IDF classifier to verify article authenticity and evaluate misinformation risk.</div>', unsafe_allow_html=True)
    
    model, vectorizer = load_nlp_model()
    
    if model is None or vectorizer is None:
        st.error("Pre-trained model or vectorizer not found. Run `python 'Fake News Detection/train_model.py'` first.")
        return

    st.markdown("---")
    
    col_input, col_preset = st.columns([2, 1])
    
    preset_text = ""
    with col_preset:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.subheader("💡 Article Presets")
        st.write("Click a preset sample for instant testing:")
        if st.button("Sample 1: Alien Treaty Alert 🚨"):
            preset_text = "BREAKING: Aliens landed in broad daylight in Washington DC today and signed a secret peace treaty! Scientists stunned by flying saucers."
        if st.button("Sample 2: Central Bank Policy 📰"):
            preset_text = "The Federal Reserve announced an interest rate adjustment following its quarterly monetary policy review meeting today."
        if st.button("Sample 3: Miracle Remedy Claim 🚨"):
            preset_text = "SHOCKING SECRET: Drinking boiled lemon peel water cures all forms of cancer in 24 hours! Big Pharma hiding this secret."
        st.markdown('</div>', unsafe_allow_html=True)

    with col_input:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.subheader("🔍 Analyze News Content")
        user_text = st.text_area("Paste news headline or full article text below:", value=preset_text, height=180)
        analyze_btn = st.button("Analyze Authenticity 🚀", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn or (preset_text and user_text):
        if not user_text.strip():
            st.warning("Please enter some text to analyze.")
            return

        cleaned = clean_text(user_text)
        tfidf_input = vectorizer.transform([cleaned])
        
        pred = model.predict(tfidf_input)[0]
        probs = model.predict_proba(tfidf_input)[0]
        
        fake_prob = probs[1] * 100
        real_prob = probs[0] * 100
        
        st.markdown("---")
        st.subheader("📊 Model Classification Verdict")
        
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.markdown('<div class="figma-card">', unsafe_allow_html=True)
            if pred == 1:
                st.error("🚨 VERDICT: FAKE NEWS DETECTED")
                st.metric("Disinformation Risk", f"{fake_prob:.1f}%")
                st.write("This content matches linguistic patterns typically associated with sensationalist or unverified viral claims.")
            else:
                st.success("✅ VERDICT: VERIFIED REAL NEWS")
                st.metric("Authenticity Score", f"{real_prob:.1f}%")
                st.write("This text demonstrates factual structural composition adhering to verified news indicators.")
            st.markdown('</div>', unsafe_allow_html=True)
                
        with res_col2:
            st.markdown('<div class="figma-card">', unsafe_allow_html=True)
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=fake_prob,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Misinformation Risk Score (%)", 'font': {'color': '#F8FAFC', 'size': 16}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#94A3B8'},
                    'bar': {'color': DANGER if pred == 1 else SECONDARY},
                    'steps': [
                        {'range': [0, 40], 'color': "rgba(16, 185, 129, 0.2)"},
                        {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.2)"},
                        {'range': [70, 100], 'color': "rgba(239, 68, 68, 0.2)"}
                    ]
                }
            ))
            fig = apply_plotly_figma_theme(fig)
            fig.update_layout(height=240)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("🔑 Linguistic Token Weight Analysis")
        feature_names = vectorizer.get_feature_names_out()
        dense = tfidf_input.todense().tolist()[0]
        phrase_scores = [ (feature_names[i], dense[i]) for i in range(len(dense)) if dense[i] > 0 ]
        phrase_scores.sort(key=lambda x: x[1], reverse=True)
        
        if phrase_scores:
            words_df = pd.DataFrame(phrase_scores, columns=['Token Keyword', 'TF-IDF Weight'])
            
            fig_bar = px.bar(
                words_df.head(10),
                x='TF-IDF Weight',
                y='Token Keyword',
                orientation='h',
                title="Top Extracted TF-IDF Keyword Tokens",
                color='TF-IDF Weight',
                color_continuous_scale='Purples'
            )
            fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'}, height=350)
            fig_bar = apply_plotly_figma_theme(fig_bar)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No matching vocabulary keywords found in vectorizer vocabulary.")

if __name__ == "__main__":
    render_fake_news_app()
