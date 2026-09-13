import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ensure root directory is importable for theme module
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from theme import apply_figma_theme, apply_plotly_figma_theme, COLOR_PALETTE
except ImportError:
    apply_figma_theme = lambda: None
    apply_plotly_figma_theme = lambda fig: fig
    COLOR_PALETTE = ["#6366F1", "#10B981", "#F59E0B", "#EC4899", "#3B82F6"]

st.set_page_config(page_title="Electoral Bonds Data Analytics", page_icon="🗳️", layout="wide")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df_path = os.path.join(base_dir, 'df.csv')
    comp_path = os.path.join(base_dir, 'Company.csv')
    party_path = os.path.join(base_dir, 'Party.csv')
    
    df = pd.read_csv(df_path) if os.path.exists(df_path) else None
    comp_df = pd.read_csv(comp_path) if os.path.exists(comp_path) else None
    party_df = pd.read_csv(party_path) if os.path.exists(party_path) else None
    
    return df, comp_df, party_df

def render_election_bonds_app():
    apply_figma_theme()
    
    st.markdown('<div class="hero-title">🗳️ Electoral Bonds Financial Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Deep-dive exploration into political donor companies, encashed bond values, and political party funding distribution.</div>', unsafe_allow_html=True)
    
    df, comp_df, party_df = load_data()
    
    if df is None:
        st.error("Data files not found. Please ensure df.csv, Company.csv, and Party.csv are present in directory.")
        return

    if 'Denominations' in df.columns:
        df['Denominations'] = pd.to_numeric(df['Denominations'], errors='coerce').fillna(0)

    # Key Performance Metrics
    total_bonds = len(df)
    total_amount = df['Denominations'].sum()
    total_purchasers = df['Name of the Purchaser'].nunique()
    total_parties = df['Name of the Political Party'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Bonds Encashed", f"{total_bonds:,}")
    col2.metric("Total Donated Value", f"₹{total_amount/1e7:,.2f} Cr")
    col3.metric("Corporate Purchasers", f"{total_purchasers:,}")
    col4.metric("Political Parties", f"{total_parties:,}")
    
    st.markdown("---")
    
    t1, t2, t3, t4 = st.tabs([
        "🏛️ Top Political Parties", 
        "🏢 Top Donor Companies", 
        "🔗 Donor -> Party Mapping", 
        "🔍 Search & Explorer"
    ])
    
    with t1:
        st.subheader("Total Funds Encashed by Political Parties")
        party_sum = df.groupby('Name of the Political Party')['Denominations'].agg(['sum', 'count']).reset_index()
        party_sum['Amount_Cr'] = party_sum['sum'] / 1e7
        party_sum = party_sum.sort_values(by='sum', ascending=False)
        
        fig1 = px.bar(
            party_sum.head(12), 
            x='Amount_Cr', 
            y='Name of the Political Party',
            orientation='h',
            labels={'Amount_Cr': 'Total Value (₹ Crores)', 'Name of the Political Party': 'Party Name'},
            title="Top 12 Political Parties by Total Encashed Bond Value",
            color='Amount_Cr',
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, height=480)
        fig1 = apply_plotly_figma_theme(fig1)
        st.plotly_chart(fig1, use_container_width=True)
        
        st.dataframe(party_sum[['Name of the Political Party', 'count', 'Amount_Cr']].rename(
            columns={'count': 'Number of Bonds', 'Amount_Cr': 'Amount (₹ Cr)'}
        ), use_container_width=True)

    with t2:
        st.subheader("Top Corporate Bond Purchasers")
        purchaser_sum = df.groupby('Name of the Purchaser')['Denominations'].agg(['sum', 'count']).reset_index()
        purchaser_sum['Amount_Cr'] = purchaser_sum['sum'] / 1e7
        purchaser_sum = purchaser_sum.sort_values(by='sum', ascending=False)
        
        fig2 = px.bar(
            purchaser_sum.head(12),
            x='Amount_Cr',
            y='Name of the Purchaser',
            orientation='h',
            labels={'Amount_Cr': 'Total Donated Value (₹ Crores)', 'Name of the Purchaser': 'Purchaser Name'},
            title="Top 12 Corporate Donors by Bond Purchase Amount",
            color='Amount_Cr',
            color_continuous_scale='Plasma'
        )
        fig2.update_layout(yaxis={'categoryorder': 'total ascending'}, height=480)
        fig2 = apply_plotly_figma_theme(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        
        st.dataframe(purchaser_sum[['Name of the Purchaser', 'count', 'Amount_Cr']].rename(
            columns={'count': 'Number of Bonds', 'Amount_Cr': 'Amount (₹ Cr)'}
        ), use_container_width=True)

    with t3:
        st.subheader("Explore Donor Distributions per Political Party")
        selected_party = st.selectbox("Select Target Political Party:", sorted(df['Name of the Political Party'].dropna().unique()))
        
        party_filtered = df[df['Name of the Political Party'] == selected_party]
        party_donors = party_filtered.groupby('Name of the Purchaser')['Denominations'].agg(['sum', 'count']).reset_index()
        party_donors['Amount_Cr'] = party_donors['sum'] / 1e7
        party_donors = party_donors.sort_values(by='sum', ascending=False)
        
        st.markdown(f"**Donation Breakdown for {selected_party}** (Total Funds: **₹{party_filtered['Denominations'].sum()/1e7:,.2f} Cr**)")
        
        fig3 = px.pie(
            party_donors.head(10),
            values='Amount_Cr',
            names='Name of the Purchaser',
            title=f"Top 10 Donor Distribution for {selected_party}",
            hole=0.45,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig3 = apply_plotly_figma_theme(fig3)
        st.plotly_chart(fig3, use_container_width=True)
        st.dataframe(party_donors, use_container_width=True)

    with t4:
        st.subheader("Filter and Search Bond Transactions")
        search_query = st.text_input("Search Company or Party Name:", "")
        if search_query:
            filtered_df = df[
                df['Name of the Purchaser'].str.contains(search_query, case=False, na=False) |
                df['Name of the Political Party'].str.contains(search_query, case=False, na=False)
            ]
        else:
            filtered_df = df
            
        st.write(f"Showing **{len(filtered_df):,}** matching transaction records")
        st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    render_election_bonds_app()
