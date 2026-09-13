import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly.graph_objects as go
import plotly.express as px

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')
if data_dir not in sys.path:
    sys.path.append(data_dir)

# Ensure root directory is importable for theme module
root_dir = os.path.dirname(base_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from theme import apply_figma_theme, apply_plotly_figma_theme, PRIMARY, SECONDARY, WARNING, COLOR_PALETTE
except ImportError:
    apply_figma_theme = lambda: None
    apply_plotly_figma_theme = lambda fig: fig
    PRIMARY = "#6366F1"
    SECONDARY = "#10B981"
    WARNING = "#F59E0B"

import pred_price

st.set_page_config(page_title="Used Car Price Valuation AI", page_icon="🚗", layout="wide")

def render_car_price_app():
    apply_figma_theme()
    
    st.markdown('<div class="hero-title">🚗 Vehicle Valuation Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Machine Learning regression engine estimating secondhand car resale values across Indian automotive markets.</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    car_names = pred_price.get_car_names()
    locations = pred_price.get_locations()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.write("**🏎️ Brand & Location**")
        car_name = st.selectbox("Car Model", options=car_names, index=min(10, len(car_names)-1))
        location = st.selectbox("Registration City", options=locations, index=0)
        year = st.slider("Registration Year", 2005, 2024, 2017)
        kilometers = st.number_input("Kilometers Driven", min_value=500, max_value=300000, value=45000, step=5000)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.write("**⚙️ Fuel & Ownership**")
        fuel_type = st.selectbox("Fuel Type", options=["Petrol", "Diesel", "CNG", "LPG"])
        fuel_map = {"Diesel": 1, "Petrol": 2, "CNG": 3, "LPG": 4}
        
        transmission = st.selectbox("Transmission", options=["Manual", "Automatic"])
        trans_map = {"Manual": 1, "Automatic": 2}
        
        owner_type = st.selectbox("Ownership History", options=["First Owner", "Second Owner", "Third Owner", "Fourth & Above"])
        owner_map = {"First Owner": 1, "Second Owner": 2, "Third Owner": 3, "Fourth & Above": 4}
        
        seats = st.selectbox("Seating Capacity", options=[4, 5, 7, 8], index=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.write("**🔋 Power & Engine Vitals**")
        mileage = st.slider("Fuel Mileage (km/l)", 8.0, 35.0, 18.5, step=0.5)
        engine_cc = st.slider("Engine Capacity (CC)", 600, 4500, 1200, step=50)
        power_hp = st.slider("Max Power (BHP)", 35.0, 400.0, 85.0, step=2.0)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Calculate valuation live
    predicted_val = pred_price.pred(
        name=car_name,
        location=location,
        year=year,
        kd=kilometers,
        fuel=fuel_map[fuel_type],
        trans=trans_map[transmission],
        owner=owner_map[owner_type],
        milage=mileage,
        engine=engine_cc,
        power=power_hp,
        seats=seats
    )
    
    price_lakhs = float(predicted_val[0])
    price_inr = price_lakhs * 100000
    
    st.subheader("💰 Resale Valuation Output")
    
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        st.metric("Estimated Market Price (Lakhs)", f"₹ {price_lakhs:.2f} Lakhs")
        st.metric("Equivalent Total Price (INR)", f"₹ {price_inr:,.0f}")
        
        min_est = max(0.3, price_lakhs * 0.92)
        max_est = price_lakhs * 1.08
        st.info(f"💡 **Estimated Fair Value Range**: ₹ {min_est:.2f} Lakhs — ₹ {max_est:.2f} Lakhs (subject to physical inspection).")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with res_col2:
        st.markdown('<div class="figma-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="number+gauge",
            value=price_lakhs,
            title={'text': "Market Valuation (₹ Lakhs)", 'font': {'color': '#F8FAFC', 'size': 16}},
            gauge={
                'axis': {'range': [0, max(15.0, price_lakhs * 1.5)], 'tickcolor': '#94A3B8'},
                'bar': {'color': PRIMARY},
                'steps': [
                    {'range': [0, 5], 'color': "rgba(99, 102, 241, 0.15)"},
                    {'range': [5, 12], 'color': "rgba(99, 102, 241, 0.3)"},
                    {'range': [12, 30], 'color': "rgba(99, 102, 241, 0.45)"}
                ]
            }
        ))
        fig = apply_plotly_figma_theme(fig)
        fig.update_layout(height=240)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_car_price_app()
