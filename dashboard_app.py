import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Cross-Channel Ad Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# IMPROVED COLOR SCHEME - Professional & Balanced
PLATFORM_COLORS = {
    'Facebook': '#1877F2',  # Facebook Blue
    'Google': '#34A853',    # Google Green
    'TikTok': '#FF0050'     # TikTok Pink
}

# Custom CSS with improved styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .stMetric {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #667eea;
    }
    .stMetric label {
        color: #a0a0c0 !important;
        font-size: 0.9rem !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process the advertising data from all platforms"""
    
    # Load individual platform data
    fb = pd.read_csv('01_facebook_ads.csv')
    google = pd.read_csv('02_google_ads.csv')
    tiktok = pd.read_csv('03_tiktok_ads.csv')
    
    # Standardize Facebook data
    fb_std = fb.copy()
    fb_std['platform'] = 'Facebook'
    fb_std['cost'] = fb_std['spend']
    fb_std['subgroup_id'] = fb_std['ad_set_id']
    fb_std['subgroup_name'] = fb_std['ad_set_name']
    fb_std['conversion_value'] = fb_std['conversions'] * 50
    
    # Standardize Google data
    google_std = google.copy()
    google_std['platform'] = 'Google'
    google_std['subgroup_id'] = google_std['ad_group_id']
    google_std['subgroup_name'] = google_std['ad_group_name']
    
    # Standardize TikTok data
    tiktok_std = tiktok.copy()
    tiktok_std['platform'] = 'TikTok'
    tiktok_std['subgroup_id'] = tiktok_std['adgroup_id']
    tiktok_std['subgroup_name'] = tiktok_std['adgroup_name']
    tiktok_std['conversion_value'] = tiktok_std['conversions'] * 50
    tiktok_std['video_completion_rate'] = tiktok_std['video_watch_100'] / tiktok_std['video_views']
    tiktok_std['social_engagement'] = tiktok_std['likes'] + tiktok_std['shares'] + tiktok_std['comments']
    
    # Select common columns
    common_cols = ['platform', 'date', 'campaign_id', 'campaign_name', 'subgroup_id', 
                   'subgroup_name', 'impressions', 'clicks', 'cost', 'conversions', 'conversion_value']
    
    # Create unified dataset
    unified = pd.concat([
        fb_std[common_cols + ['video_views', 'engagement_rate', 'reach', 'frequency']],
        google_std[common_cols + ['quality_score']],
        tiktok_std[common_cols + ['video_views', 'video_completion_rate', 'social_engagement']]
    ], ignore_index=True)
    
    # Convert date to datetime
    unified['date'] = pd.to_datetime(unified['date'])
    
    # Calculate KPIs
    unified['ctr'] = (unified['clicks'] / unified['impressions'] * 100).round(2)
    unified['cpc'] = (unified['cost'] / unified['clicks']).round(2)
    unified['cpa'] = (unified['cost'] / unified['conversions']).round(2)
    unified['roas'] = (unified['conversion_value'] / unified['cost'] * 100).round(2)
    unified['cpm'] = (unified['cost'] / unified['impressions'] * 1000).round(2)
    
    return unified

# Load data
unified_data = load_data()

# Header
st.markdown('<p class="main-header">📊 Cross-Channel Advertising Performance Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Unified analytics across Facebook, Google Ads, and TikTok advertising platforms</p>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🎯 Filters")

# Date range filter
min_date = unified_data['date'].min()
max_date = unified_data['date'].max()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Platform filter
platforms = st.sidebar.multiselect(
    "Select Platforms",
    options=unified_data['platform'].unique(),
    default=unified_data['platform'].unique()
)

# Campaign filter
campaigns = st.sidebar.multiselect(
    "Select Campaigns (Optional)",
    options=unified_data['campaign_name'].unique(),
    default=[]
)

# Apply filters
filtered_data = unified_data.copy()
if len(date_range) == 2:
    filtered_data = filtered_data[
        (filtered_data['date'] >= pd.to_datetime(date_range[0])) &
        (filtered_data['date'] <= pd.to_datetime(date_range[1]))
    ]
if platforms:
    filtered_data = filtered_data[filtered_data['platform'].isin(platforms)]
if campaigns:
    filtered_data = filtered_data[filtered_data['campaign_name'].isin(campaigns)]

# KEY METRICS SECTION
st.header("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

total_spend = filtered_data['cost'].sum()
total_impressions = filtered_data['impressions'].sum()
total_clicks = filtered_data['clicks'].sum()
total_conversions = filtered_data['conversions'].sum()
avg_roas = (filtered_data['conversion_value'].sum() / total_spend * 100) if total_spend > 0 else 0

with col1:
    st.metric("Total Spend", f"${total_spend:,.2f}")
with col2:
    st.metric("Impressions", f"{total_impressions:,.0f}")
with col3:
    st.metric("Clicks", f"{total_clicks:,.0f}")
with col4:
    st.metric("Conversions", f"{total_conversions:,.0f}")
with col5:
    st.metric("ROAS", f"{avg_roas:.1f}%")

st.divider()

# PLATFORM COMPARISON
st.header("🔄 Platform Performance Comparison")

platform_summary = filtered_data.groupby('platform').agg({
    'cost': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'conversion_value': 'sum',
    'ctr': 'mean',
    'cpc': 'mean',
    'cpa': 'mean'
}).reset_index()

platform_summary['roas'] = (platform_summary['conversion_value'] / platform_summary['cost'] * 100).round(2)

col1, col2 = st.columns(2)

with col1:
    # Spend by platform - Pie chart with brand colors
    fig_spend = px.pie(
        platform_summary, 
        values='cost', 
        names='platform',
        title='Ad Spend Distribution by Platform',
        color='platform',
        color_discrete_map=PLATFORM_COLORS,
        hole=0.4
    )
    fig_spend.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig_spend.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_spend, use_container_width=True)

with col2:
    # Conversions by platform - Bar chart
    fig_conv = px.bar(
        platform_summary,
        x='platform',
        y='conversions',
        title='Total Conversions by Platform',
        color='platform',
        color_discrete_map=PLATFORM_COLORS,
        text='conversions'
    )
    fig_conv.update_traces(
        texttemplate='%{text:,.0f}', 
        textposition='outside',
        textfont_size=14
    )
    fig_conv.update_layout(showlegend=False)
    st.plotly_chart(fig_conv, use_container_width=True)

# Platform efficiency metrics table
st.subheader("Platform Efficiency Metrics")
efficiency_display = platform_summary[['platform', 'cost', 'impressions', 'clicks', 'conversions', 'ctr', 'cpc', 'cpa', 'roas']].copy()
efficiency_display.columns = ['Platform', 'Spend ($)', 'Impressions', 'Clicks', 'Conversions', 'CTR (%)', 'CPC ($)', 'CPA ($)', 'ROAS (%)']
efficiency_display['Spend ($)'] = efficiency_display['Spend ($)'].apply(lambda x: f"${x:,.2f}")
efficiency_display['CPC ($)'] = efficiency_display['CPC ($)'].apply(lambda x: f"${x:.2f}")
efficiency_display['CPA ($)'] = efficiency_display['CPA ($)'].apply(lambda x: f"${x:.2f}")
efficiency_display['CTR (%)'] = efficiency_display['CTR (%)'].apply(lambda x: f"{x:.2f}%")
efficiency_display['ROAS (%)'] = efficiency_display['ROAS (%)'].apply(lambda x: f"{x:.1f}%")

st.dataframe(efficiency_display, use_container_width=True, hide_index=True)

st.divider()

# TIME SERIES ANALYSIS
st.header("📅 Performance Trends Over Time")

daily_trends = filtered_data.groupby(['date', 'platform']).agg({
    'cost': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'conversion_value': 'sum'
}).reset_index()

daily_trends['roas'] = (daily_trends['conversion_value'] / daily_trends['cost'] * 100).round(2)

col1, col2 = st.columns(2)

with col1:
    # Daily spend trend
    fig_spend_trend = px.line(
        daily_trends,
        x='date',
        y='cost',
        color='platform',
        title='Daily Ad Spend Trend',
        color_discrete_map=PLATFORM_COLORS,
        markers=True
    )
    fig_spend_trend.update_traces(line=dict(width=3), marker=dict(size=8))
    fig_spend_trend.update_layout(
        xaxis_title="Date",
        yaxis_title="Spend ($)",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_spend_trend, use_container_width=True)

with col2:
    # Daily conversions trend
    fig_conv_trend = px.line(
        daily_trends,
        x='date',
        y='conversions',
        color='platform',
        title='Daily Conversions Trend',
        color_discrete_map=PLATFORM_COLORS,
        markers=True
    )
    fig_conv_trend.update_traces(line=dict(width=3), marker=dict(size=8))
    fig_conv_trend.update_layout(
        xaxis_title="Date",
        yaxis_title="Conversions",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_conv_trend, use_container_width=True)

# ROAS trend
fig_roas = px.line(
    daily_trends,
    x='date',
    y='roas',
    color='platform',
    title='Daily ROAS Trend',
    color_discrete_map=PLATFORM_COLORS,
    markers=True
)
fig_roas.update_traces(line=dict(width=3), marker=dict(size=8))
fig_roas.update_layout(
    xaxis_title="Date",
    yaxis_title="ROAS (%)",
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
)
st.plotly_chart(fig_roas, use_container_width=True)

st.divider()

# CAMPAIGN PERFORMANCE
st.header("🎯 Top Performing Campaigns")

campaign_summary = filtered_data.groupby(['platform', 'campaign_name']).agg({
    'cost': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'conversion_value': 'sum'
}).reset_index()

campaign_summary['roas'] = (campaign_summary['conversion_value'] / campaign_summary['cost'] * 100).round(2)
campaign_summary['cpa'] = (campaign_summary['cost'] / campaign_summary['conversions']).round(2)

col1, col2 = st.columns(2)

with col1:
    # Top campaigns by ROAS
    top_roas = campaign_summary.nlargest(10, 'roas')
    fig_top_roas = px.bar(
        top_roas,
        x='roas',
        y='campaign_name',
        color='platform',
        orientation='h',
        title='Top 10 Campaigns by ROAS',
        color_discrete_map=PLATFORM_COLORS,
        text='roas'
    )
    fig_top_roas.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont_size=12)
    fig_top_roas.update_layout(
        xaxis_title="ROAS (%)",
        yaxis_title="Campaign",
        yaxis={'categoryorder': 'total ascending'},
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_top_roas, use_container_width=True)

with col2:
    # Top campaigns by conversions
    top_conv = campaign_summary.nlargest(10, 'conversions')
    fig_top_conv = px.bar(
        top_conv,
        x='conversions',
        y='campaign_name',
        color='platform',
        orientation='h',
        title='Top 10 Campaigns by Conversions',
        color_discrete_map=PLATFORM_COLORS,
        text='conversions'
    )
    fig_top_conv.update_traces(texttemplate='%{text:,.0f}', textposition='outside', textfont_size=12)
    fig_top_conv.update_layout(
        xaxis_title="Conversions",
        yaxis_title="Campaign",
        yaxis={'categoryorder': 'total ascending'},
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_top_conv, use_container_width=True)

st.divider()

# EFFICIENCY ANALYSIS
st.header("⚡ Cross-Platform Efficiency Analysis")

col1, col2 = st.columns(2)

with col1:
    # CTR vs CPC scatter with larger markers
    fig_scatter = px.scatter(
        campaign_summary,
        x='cpa',
        y='roas',
        size='conversions',
        color='platform',
        hover_data=['campaign_name'],
        title='Campaign Efficiency: CPA vs ROAS',
        color_discrete_map=PLATFORM_COLORS,
        size_max=40
    )
    fig_scatter.update_traces(marker=dict(line=dict(width=1, color='white')))
    fig_scatter.update_layout(
        xaxis_title="CPA ($)",
        yaxis_title="ROAS (%)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Platform comparison radar chart
    platform_metrics = platform_summary[['platform', 'cost', 'clicks', 'conversions']].copy()
    
    # Normalize metrics to 0-100 scale
    for col in ['cost', 'clicks', 'conversions']:
        max_val = platform_metrics[col].max()
        platform_metrics[f'{col}_norm'] = (platform_metrics[col] / max_val * 100).round(2)
    
    fig_radar = go.Figure()
    
    for platform in platform_metrics['platform']:
        platform_data = platform_metrics[platform_metrics['platform'] == platform]
        fig_radar.add_trace(go.Scatterpolar(
            r=[platform_data['cost_norm'].values[0], 
               platform_data['clicks_norm'].values[0], 
               platform_data['conversions_norm'].values[0]],
            theta=['Spend', 'Clicks', 'Conversions'],
            fill='toself',
            name=platform,
            line=dict(color=PLATFORM_COLORS[platform], width=3),
            fillcolor=PLATFORM_COLORS[platform],
            opacity=0.3
        ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        title='Platform Performance Radar (Normalized)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# KEY INSIGHTS
st.header("💡 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    best_platform_roas = platform_summary.loc[platform_summary['roas'].idxmax()]
    st.markdown(f"""
    <div class="insight-box">
    <h3>🏆 Best ROAS Platform</h3>
    <p style='font-size: 1.5rem; font-weight: bold; color: {PLATFORM_COLORS[best_platform_roas["platform"]]};'>{best_platform_roas['platform']}</p>
    <p>Delivers <strong>{best_platform_roas['roas']:.1f}% ROAS</strong> with ${best_platform_roas['conversion_value']:,.0f} in conversion value from ${best_platform_roas['cost']:,.0f} spend.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    best_platform_conv = platform_summary.loc[platform_summary['conversions'].idxmax()]
    st.markdown(f"""
    <div class="insight-box">
    <h3>📊 Most Conversions</h3>
    <p style='font-size: 1.5rem; font-weight: bold; color: {PLATFORM_COLORS[best_platform_conv["platform"]]};'>{best_platform_conv['platform']}</p>
    <p>Generated <strong>{best_platform_conv['conversions']:,.0f} conversions</strong>, representing {(best_platform_conv['conversions']/total_conversions*100):.1f}% of all conversions.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    best_campaign = campaign_summary.loc[campaign_summary['roas'].idxmax()]
    st.markdown(f"""
    <div class="insight-box">
    <h3>🎯 Top Campaign</h3>
    <p style='font-size: 1.5rem; font-weight: bold; color: {PLATFORM_COLORS[best_campaign["platform"]]};'>{best_campaign['campaign_name'][:25]}...</p>
    <p>On {best_campaign['platform']}, achieved <strong>{best_campaign['roas']:.1f}% ROAS</strong> with {best_campaign['conversions']:.0f} conversions.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Senior Marketing Analyst - Technical Assignment</strong></p>
    <p>Cross-Platform Advertising Analytics Dashboard | Data Period: January 2024</p>
</div>
""", unsafe_allow_html=True)
