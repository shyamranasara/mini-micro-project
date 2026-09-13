import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sys
import plotly.express as px
import plotly.graph_objects as go

# Ensure root directory is importable for theme module
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from theme import apply_figma_theme, apply_plotly_figma_theme, PRIMARY, SECONDARY, DANGER, WARNING
except ImportError:
    apply_figma_theme = lambda: None
    apply_plotly_figma_theme = lambda fig: fig
    PRIMARY = "#6366F1"
    SECONDARY = "#10B981"
    DANGER = "#EF4444"
    WARNING = "#F59E0B"

st.set_page_config(page_title="Heart Risk Assessment ML", page_icon="❤️", layout="wide")

@st.cache_resource
def load_heart_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'heart_model.pkl')
    scaler_path = os.path.join(base_dir, 'scaler.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        return None, None
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

@st.cache_data
def load_dataset():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'heart.csv')
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None

def render_heart_app():
    apply_figma_theme()
    
    st.markdown('<div class="hero-title">❤️ Cardiovascular Clinical Risk Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Random Forest medical classification model evaluating 13 clinical vitals to predict cardiovascular risk tiers.</div>', unsafe_allow_html=True)
    
    model, scaler = load_heart_model()
    df = load_dataset()
    
    if model is None or scaler is None:
        st.error("Pre-trained model or scaler not found. Please run `python 'Heart Attack Analysis/train_model.py'` first.")
        return

    st.markdown("---")
    
    st.subheader("🩺 Clinical Vital Inputs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.write("**Patient Profile & Blood Press.**")
        age = st.slider("Age (Years)", 20, 90, 55)
        sex = st.selectbox("Biological Sex", options=[1, 0], format_func=lambda x: "Male" if x == 1 else "Female")
        cp = st.selectbox("Chest Pain Type (cp)", options=[0, 1, 2, 3], 
                          format_func=lambda x: ["0: Typical Angina", "1: Atypical Angina", "2: Non-anginal", "3: Asymptomatic"][x])
        trtbps = st.slider("Resting Blood Pressure (mm Hg)", 90, 200, 130)
        chol = st.slider("Serum Cholesterol (mg/dl)", 100, 600, 240)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.write("**Metabolic & Cardiac Metrics**")
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1], format_func=lambda x: "True (>120)" if x == 1 else "False (<=120)")
        restecg = st.selectbox("Resting ECG Results", options=[0, 1, 2], 
                               format_func=lambda x: ["0: Normal", "1: ST-T Wave Abnormality", "2: Hypertrophy"][x])
        thalachh = st.slider("Max Heart Rate Achieved (thalachh)", 70, 220, 150)
        exng = st.selectbox("Exercise Induced Angina", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.write("**Electrocardiogram & Fluoroscopy**")
        oldpeak = st.slider("ST Depression (oldpeak)", 0.0, 6.2, 1.0, step=0.1)
        slp = st.selectbox("ST Segment Slope", options=[0, 1, 2], format_func=lambda x: ["0: Upsloping", "1: Flat", "2: Downsloping"][x])
        caa = st.slider("Major Colored Vessels (caa)", 0, 4, 0)
        thall = st.selectbox("Thalassemia Stress Result", options=[0, 1, 2, 3], format_func=lambda x: ["0: Null", "1: Fixed Defect", "2: Normal", "3: Reversable"][x])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Calculate inference live
    input_data = np.array([[age, sex, cp, trtbps, chol, fbs, restecg, thalachh, exng, oldpeak, slp, caa, thall]])
    scaled_input = scaler.transform(input_data)
    
    prob = model.predict_proba(scaled_input)[0][1] * 100
    pred = model.predict(scaled_input)[0]

    st.subheader("📈 Assessment & Risk Stratification")
    
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        if prob > 65:
            st.error("⚠️ ELEVATED CARDIOVASCULAR RISK DETECTED")
            st.metric("Estimated Risk Probability", f"{prob:.1f}%")
            st.write("Clinical classification model indicates high probability of ischemic heart disease patterns.")
            st.info("💡 **Recommendation**: Immediate clinical follow-up with specialized ECG & troponin diagnostics.")
        elif prob > 35:
            st.warning("⚡ MODERATE CARDIOVASCULAR RISK")
            st.metric("Estimated Risk Probability", f"{prob:.1f}%")
            st.write("Patient demonstrates moderate risk factors warranting preventative lifestyle modifications.")
        else:
            st.success("✅ LOW CARDIOVASCULAR RISK PROFILE")
            st.metric("Estimated Risk Probability", f"{prob:.1f}%")
            st.write("Vital parameters conform to low-risk physiological norms.")
        st.markdown('</div>', unsafe_allow_html=True)
            
    with res_col2:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Cardiac Risk Index (%)", 'font': {'color': '#F8FAFC', 'size': 16}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#94A3B8'},
                'bar': {'color': DANGER if prob > 65 else (WARNING if prob > 35 else SECONDARY)},
                'steps': [
                    {'range': [0, 35], 'color': "rgba(16, 185, 129, 0.15)"},
                    {'range': [35, 65], 'color': "rgba(245, 158, 11, 0.15)"},
                    {'range': [65, 100], 'color': "rgba(239, 68, 68, 0.15)"}
                ]
            }
        ))
        fig = apply_plotly_figma_theme(fig)
        fig.update_layout(height=240)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if df is not None:
        st.markdown("---")
        st.subheader("📊 Clinical Feature Importance & Data Insights")
        
        feat_col, data_col = st.columns([1, 1])
        
        with feat_col:
            feature_names = ['age', 'sex', 'cp', 'trtbps', 'chol', 'fbs', 'restecg', 'thalachh', 'exng', 'oldpeak', 'slp', 'caa', 'thall']
            importances = model.feature_importances_
            feat_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values('Importance', ascending=True)
            
            fig_feat = px.bar(feat_df, x='Importance', y='Feature', orientation='h', title="Random Forest Feature Importance Weights", color='Importance', color_continuous_scale='Tealgrn')
            fig_feat.update_layout(height=360)
            fig_feat = apply_plotly_figma_theme(fig_feat)
            st.plotly_chart(fig_feat, use_container_width=True)
            
        with data_col:
            corr = df.corr()
            fig_corr = px.imshow(corr, text_auto=".1f", aspect="auto", color_continuous_scale="Purples", title="Clinical Feature Correlation Matrix")
            fig_corr.update_layout(height=360)
            fig_corr = apply_plotly_figma_theme(fig_corr)
            st.plotly_chart(fig_corr, use_container_width=True)

if __name__ == "__main__":
    render_heart_app()
