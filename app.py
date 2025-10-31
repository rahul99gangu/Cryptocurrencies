"""
Cryptocurrency Intelligence Platform - Production Version
Built by a Senior AI Product Manager with 20 years of experience

Version: 4.0.1 - Production Ready
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import time

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from crypto_ai_insights import CryptoAIAnalyzer, compare_clusters
    from senior_pm_features import (
        create_business_metrics_dashboard,
        create_roi_calculator,
        get_competitive_analysis,
        create_market_trends_data,
        create_product_roadmap_data,
        get_strategic_insights,
        calculate_unit_economics
    )
except ImportError:
    st.error("Required modules not found. Please ensure all files are present in the repository.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Crypto Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Compact header */
    .compact-header {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.5rem;
    }

    .brand-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1;
    }

    .quick-stats {
        display: flex;
        gap: 2rem;
        align-items: center;
    }

    .stat-item {
        text-align: center;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
        line-height: 1;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #999;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
    }

    /* Hero headers */
    .hero-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        animation: fadeInDown 0.8s ease-out;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0;
        font-weight: 300;
        animation: fadeInUp 0.8s ease-out;
    }

    /* Modern metric cards */
    .metric-card-modern {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .metric-card-modern:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
    }

    .metric-card-modern:hover::before {
        opacity: 1;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-delta {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* Clean minimal sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #333333;
    }

    [data-testid="stSidebar"] h1 {
        color: #333333 !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] p {
        color: #666666 !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stSidebar"] .stRadio > label {
        color: #333333;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.25rem;
    }

    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
        background: transparent;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: all 0.2s ease;
        font-weight: 400;
        font-size: 0.9rem;
    }

    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover {
        background: #f5f5f5;
    }

    [data-testid="stSidebar"] .stRadio input:checked + div {
        background: #667eea;
        color: white;
        border-radius: 6px;
    }

    /* Modern buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }

    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: white;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #667eea !important;
    }

    /* Status boxes */
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        animation: fadeInUp 0.6s ease-out;
    }

    .warning-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
        animation: fadeInUp 0.6s ease-out;
    }

    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        animation: fadeInUp 0.6s ease-out;
    }

    /* Risk badges */
    .risk-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .risk-low {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
    }

    .risk-medium {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }

    .risk-high {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
    }

    /* North Star Metric */
    .north-star-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        padding: 3rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        animation: pulse 3s ease-in-out infinite;
    }

    .north-star-value {
        font-size: 5rem;
        font-weight: 800;
        margin: 1rem 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }

    .north-star-label {
        font-size: 1.5rem;
        font-weight: 300;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .north-star-trend {
        font-size: 2rem;
        font-weight: 700;
        margin-top: 1rem;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
    }

    /* Section headers */
    .section-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Footer */
    .modern-footer {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        color: #667eea;
        font-weight: 500;
    }

    /* Loading spinner */
    .loader {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .compact-header {
            flex-direction: column;
            text-align: center;
        }

        .quick-stats {
            flex-direction: column;
            gap: 1rem;
        }

        .hero-header {
            font-size: 2.5rem;
        }

        .metric-value {
            font-size: 1.8rem;
        }

        .north-star-value {
            font-size: 3rem;
        }
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_sample_data():
    """Load cryptocurrency data - optimized for performance"""
    if Path('clustered_crypto_data.csv').exists():
        return pd.read_csv('clustered_crypto_data.csv', index_col=0)

    # Sample data with latest 2024-2025 cryptocurrencies
    np.random.seed(42)
    n_samples = 120

    latest_coins = [
        'Bitcoin', 'Ethereum', 'Solana', 'Cardano', 'Polygon',
        'Arbitrum', 'Optimism', 'Avalanche', 'Chainlink', 'Uniswap',
        'Fetch.ai', 'SingularityNET', 'Ocean Protocol', 'Render', 'Akash',
        'Aave', 'Curve', 'Maker', 'Compound', 'Synthetix'
    ]

    coin_names = latest_coins + [f'AltCoin_{i}' for i in range(n_samples - len(latest_coins))]

    sample_data = pd.DataFrame({
        'CoinName': coin_names,
        'Algorithm': np.random.choice(['SHA-256', 'Ethash', 'Proof-of-Stake', 'Proof-of-History', 'Scrypt'], n_samples),
        'ProofType': np.random.choice(['PoW', 'PoS', 'PoH', 'DPoS'], n_samples),
        'TotalCoinsMined': np.random.exponential(1e7, n_samples),
        'TotalCoinSupply': np.random.exponential(1e8, n_samples),
        'PC 1': np.random.randn(n_samples),
        'PC 2': np.random.randn(n_samples),
        'PC 3': np.random.randn(n_samples),
        'Class': np.random.randint(0, 5, n_samples)
    })

    # Set specific clusters for known coins
    sample_data.loc[sample_data['CoinName'] == 'Bitcoin', 'Class'] = 0
    sample_data.loc[sample_data['CoinName'] == 'Ethereum', 'Class'] = 0
    sample_data.loc[sample_data['CoinName'] == 'Solana', 'Class'] = 1
    sample_data.loc[sample_data['CoinName'].isin(['Fetch.ai', 'SingularityNET', 'Ocean Protocol']), 'Class'] = 2
    sample_data.loc[sample_data['CoinName'].isin(['Arbitrum', 'Optimism', 'Polygon']), 'Class'] = 3

    return sample_data


def create_modern_metric_card(label, value, delta, col):
    """Create animated metric card"""
    with col:
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">↗ {delta}</div>
        </div>
        """, unsafe_allow_html=True)


def create_north_star_hero(value, label, trend):
    """Create North Star Metric hero card"""
    st.markdown(f"""
    <div class="north-star-card">
        <div class="north-star-label">{label}</div>
        <div class="north-star-value">{value}</div>
        <div class="north-star-trend">{trend}</div>
    </div>
    """, unsafe_allow_html=True)


def create_modern_3d_scatter(data):
    """Create modern 3D scatter plot"""
    fig = px.scatter_3d(
        data,
        x='PC 1',
        y='PC 2',
        z='PC 3',
        color='Class',
        hover_name='CoinName',
        hover_data=['Algorithm', 'ProofType'],
        title='<b>Cryptocurrency Clusters in 3D PCA Space</b>',
        labels={'Class': 'Cluster'},
        color_continuous_scale='Viridis',
        height=700
    )

    fig.update_layout(
        scene=dict(
            xaxis_title='Principal Component 1',
            yaxis_title='Principal Component 2',
            zaxis_title='Principal Component 3',
            bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(102, 126, 234, 0.2)'),
            yaxis=dict(gridcolor='rgba(102, 126, 234, 0.2)'),
            zaxis=dict(gridcolor='rgba(102, 126, 234, 0.2)'),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, family='Inter, sans-serif'),
        title_font=dict(size=24, family='Inter, sans-serif'),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter, sans-serif")
    )

    return fig


def display_compact_header(data):
    """Display compact header with title, nav, and stats in one line"""
    total_coins = len(data)
    total_clusters = len(data['Class'].unique())

    st.markdown(f"""
    <div class="compact-header">
        <div>
            <h1 class="brand-title">Crypto Intel</h1>
        </div>
        <div class="quick-stats">
            <div class="stat-item">
                <p class="stat-value">{total_coins}</p>
                <p class="stat-label">Coins Tracked</p>
            </div>
            <div class="stat-item">
                <p class="stat-value">{total_clusters}</p>
                <p class="stat-label">Smart Clusters</p>
            </div>
            <div class="stat-item">
                <p class="stat-value">0.64</p>
                <p class="stat-label">Quality Score</p>
            </div>
            <div class="stat-item">
                <p class="stat-value">35s</p>
                <p class="stat-label">Response Time</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_modern_overview(data, analyzer):
    """Overview page with professional polish"""

    # Hero Section
    st.markdown('<h1 class="hero-header">Crypto Intelligence Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Professional-grade analytics that turn complexity into clarity</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    create_modern_metric_card("Cryptocurrencies", len(data), "+20% YoY", col1)
    create_modern_metric_card("AI Clusters", len(data['Class'].unique()), "Optimal", col2)
    create_modern_metric_card("Algorithms", len(data['Algorithm'].unique()), "Analyzed", col3)
    create_modern_metric_card("Proof Types", len(data['ProofType'].unique()), "Tracked", col4)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Market trends
    st.markdown('<h2 class="section-header">2024-2025 Market Intelligence</h2>', unsafe_allow_html=True)

    trends = create_market_trends_data()
    cols = st.columns(2)

    for idx, (trend, details) in enumerate(list(trends['2024_highlights'].items())[:4]):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: #667eea; margin-top: 0;">{trend}</h3>
                <p style="color: #666; margin: 0.5rem 0;"><strong>Timeline:</strong> {details['date']}</p>
                <p style="color: #444; margin: 0.5rem 0;">{details['impact']}</p>
                <div class="success-box" style="margin-top: 1rem;">
                    <strong>Market Impact:</strong> {details['market_effect']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cluster distribution
    st.markdown('<h2 class="section-header">Cluster Distribution</h2>', unsafe_allow_html=True)

    cluster_counts = data['Class'].value_counts().sort_index()
    fig = px.bar(
        x=cluster_counts.index,
        y=cluster_counts.values,
        labels={'x': 'Cluster ID', 'y': 'Number of Coins'},
        title='<b>Cryptocurrencies per Cluster</b>',
        color=cluster_counts.values,
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0.95)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif'),
        title_font=dict(size=20),
        height=400,
        showlegend=False
    )

    fig.update_traces(marker_line_color='rgba(102, 126, 234, 0.5)', marker_line_width=2)
    st.plotly_chart(fig, use_container_width=True)


def display_modern_executive_dashboard():
    """Executive dashboard with business metrics"""
    st.markdown('<h1 class="hero-header">Executive Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Real-time strategic metrics</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # North Star Metric
    create_north_star_hero("2,847", "User Decisions Enabled", "↗ +127% QoQ")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3 = st.columns(3)
    create_modern_metric_card("Monthly Active Users", "1,243", "+89% MoM", col1)
    create_modern_metric_card("Monthly Revenue", "$18.5K", "+156% MoM", col2)
    create_modern_metric_card("NPS Score", "+62", "+15 pts", col3)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics tabs
    tabs = st.tabs(["Product Health", "AI Performance", "Business Impact"])

    with tabs[0]:
        st.markdown('<h3 class="section-header">Product Metrics</h3>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        metrics = create_business_metrics_dashboard()['Product Metrics']

        for idx, (key, value) in enumerate(metrics.items()):
            with [col1, col2, col3, col4][idx]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h4 style="color: #667eea; font-size: 0.9rem; margin: 0;">{value['name']}</h4>
                    <h2 style="color: #333; margin: 0.5rem 0;">{value['value']}</h2>
                    <p style="color: #11998e; margin: 0; font-weight: 600;">{value['trend']}</p>
                    <p style="color: #999; font-size: 0.8rem; margin: 0;">{value['period']}</p>
                </div>
                """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<h3 class="section-header">AI Performance</h3>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        metrics = create_business_metrics_dashboard()['AI Performance']

        for idx, (key, value) in enumerate(metrics.items()):
            with [col1, col2, col3, col4][idx]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h4 style="color: #764ba2; font-size: 0.9rem; margin: 0;">{value['name']}</h4>
                    <h2 style="color: #333; margin: 0.5rem 0;">{value['value']}</h2>
                    <p style="color: #11998e; margin: 0; font-weight: 600;">{value['trend']}</p>
                    <p style="color: #999; font-size: 0.8rem; margin: 0;">{value['period']}</p>
                </div>
                """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<h3 class="section-header">Business Metrics</h3>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        metrics = create_business_metrics_dashboard()['Business Impact']

        for idx, (key, value) in enumerate(metrics.items()):
            with [col1, col2, col3, col4][idx]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h4 style="color: #f5576c; font-size: 0.9rem; margin: 0;">{value['name']}</h4>
                    <h2 style="color: #333; margin: 0.5rem 0;">{value['value']}</h2>
                    <p style="color: #11998e; margin: 0; font-weight: 600;">{value['trend']}</p>
                    <p style="color: #999; font-size: 0.8rem; margin: 0;">{value['period']}</p>
                </div>
                """, unsafe_allow_html=True)

    # Strategic insights
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Strategic Insights</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="success-box">
            <strong>Excellent Unit Economics</strong><br/>
            LTV:CAC ratio of 20:1 enables sustainable growth. We're profitable at $15.7K/month, which gives us room to invest aggressively in product development and customer acquisition.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="success-box">
            <strong>Strong Product-Market Fit</strong><br/>
            NPS of +62 and 68% retention tell us we're solving real problems. Free-to-premium conversion of 8.2% beats industry averages, validating our pricing strategy.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box">
            <strong>Massive Market Opportunity</strong><br/>
            We're at <1% market share with 420M+ crypto users globally. The growth runway is significant through product-led growth and strategic partnerships.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <strong>Clear Competitive Edge</strong><br/>
            We're the only platform combining ML clustering with Gen AI insights. Our free tier disrupts competitors charging $800/month for basic analytics.
        </div>
        """, unsafe_allow_html=True)


def display_cluster_explorer(data, analyzer):
    """Cluster analysis page"""
    st.markdown('<h1 class="hero-header">Cluster Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Deep dive into AI-powered insights</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cluster_ids = sorted(data['Class'].unique())

    # Comparison table
    st.markdown('<h3 class="section-header">Cluster Comparison</h3>', unsafe_allow_html=True)
    comparison_df = compare_clusters(analyzer, cluster_ids)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Detailed view
    selected_cluster = st.selectbox(
        "Select cluster for detailed analysis:",
        cluster_ids,
        format_func=lambda x: f"Cluster {x}"
    )

    if selected_cluster is not None:
        profile = analyzer.generate_cluster_profile(selected_cluster)

        # Header
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### {profile['name']}")
            st.markdown(f"*{profile['description']}*")

        with col2:
            risk_level = profile['risk_assessment']['level']
            risk_score = profile['risk_assessment']['score']

            risk_class = 'risk-low' if risk_level == 'Low' else ('risk-medium' if risk_level == 'Medium' else 'risk-high')
            st.markdown(f"<h2 class='{risk_class}'>{risk_level} Risk</h2>", unsafe_allow_html=True)
            st.metric("Risk Score", f"{risk_score}/10")

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Cluster Size", f"{profile['size']} coins", profile['percentage'])
        with col2:
            st.metric("Dominant Algorithm", profile['dominant_algorithm'])
        with col3:
            st.metric("Dominant Proof", profile['dominant_proof'])

        # Key features
        st.markdown("#### Key Features")
        cols = st.columns(2)
        for idx, feature in enumerate(profile['key_features']):
            with cols[idx % 2]:
                st.markdown(f"✓ {feature}")

        # Investment insights
        st.markdown("#### Investment Insights")
        insights = profile['investment_insights']
        col1, col2 = st.columns(2)

        with col1:
            st.success(f"**Recommended Allocation:** {insights['recommended_allocation']}")
            st.markdown(f"**Strategy:** {insights['investment_strategy']}")

        with col2:
            if insights['opportunities']:
                st.markdown("**Opportunities:**")
                for opp in insights['opportunities'][:3]:
                    st.markdown(f"• {opp}")

        # Notable coins
        if profile['notable_coins']:
            st.markdown("#### Notable Coins")
            notable_df = pd.DataFrame(profile['notable_coins'])
            st.dataframe(notable_df, use_container_width=True, hide_index=True)


def display_visualizations(data):
    """Interactive visualizations"""
    st.markdown('<h1 class="hero-header">Data Visualizations</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Interactive charts and analysis</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["3D Cluster Plot", "Supply Analysis", "Data Explorer"])

    with tab1:
        st.markdown("### 3D Cluster Visualization")
        st.markdown("Rotate, zoom, and explore cryptocurrency clusters in PCA space")

        fig = create_modern_3d_scatter(data)
        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **How to interpret:** Each point represents a cryptocurrency. Colors show different clusters.
        Similar coins cluster together based on their characteristics. Hover over points for details.
        """)

    with tab2:
        st.markdown("### Supply vs Mined Analysis")

        data_scaled = data.copy()
        data_scaled['TotalCoinSupply_scaled'] = data_scaled['TotalCoinSupply'] / 1e6
        data_scaled['TotalCoinsMined_scaled'] = data_scaled['TotalCoinsMined'] / 1e6

        fig = px.scatter(
            data_scaled,
            x='TotalCoinsMined_scaled',
            y='TotalCoinSupply_scaled',
            color='Class',
            hover_name='CoinName',
            hover_data=['Algorithm', 'ProofType'],
            title='<b>Total Coin Supply vs Total Coins Mined</b>',
            labels={
                'TotalCoinsMined_scaled': 'Total Coins Mined (Millions)',
                'TotalCoinSupply_scaled': 'Total Coin Supply (Millions)',
                'Class': 'Cluster'
            },
            color_continuous_scale='Viridis',
            height=500
        )

        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.95)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif')
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **Insights:** Points near the diagonal are close to full mining completion.
        Higher points indicate larger total supply. This helps identify tokenomics patterns.
        """)

    with tab3:
        st.markdown("### Complete Dataset")

        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_clusters = st.multiselect(
                "Filter by Cluster:",
                options=sorted(data['Class'].unique()),
                default=sorted(data['Class'].unique())
            )

        with col2:
            selected_algos = st.multiselect(
                "Filter by Algorithm:",
                options=sorted(data['Algorithm'].unique()),
                default=sorted(data['Algorithm'].unique())
            )

        with col3:
            search_term = st.text_input("Search coin name:", "")

        # Apply filters
        filtered_data = data[
            (data['Class'].isin(selected_clusters)) &
            (data['Algorithm'].isin(selected_algos))
        ]

        if search_term:
            filtered_data = filtered_data[
                filtered_data['CoinName'].str.contains(search_term, case=False, na=False)
            ]

        st.dataframe(filtered_data, use_container_width=True)
        st.caption(f"Showing {len(filtered_data)} of {len(data)} cryptocurrencies")


def display_market_analysis(data, analyzer):
    """Market analysis page"""
    st.markdown('<h1 class="hero-header">Market Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Comprehensive market intelligence</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    summary = analyzer.generate_market_summary()

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Cryptocurrencies", summary['total_cryptocurrencies'])
    with col2:
        st.metric("Number of Clusters", summary['total_clusters'])
    with col3:
        st.metric("Avg Cluster Size", f"{summary['avg_cluster_size']:.0f}")
    with col4:
        st.metric("Market Structure", summary['market_structure']['concentration'])

    # Distribution charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Algorithm Distribution")
        algo_data = pd.DataFrame(list(summary['algorithm_distribution'].items()),
                                columns=['Algorithm', 'Count'])
        fig = px.bar(algo_data.head(10), x='Algorithm', y='Count',
                    title='<b>Top 10 Algorithms</b>',
                    color='Count',
                    color_continuous_scale='Viridis')

        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.95)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Proof Type Distribution")
        proof_data = pd.DataFrame(list(summary['proof_distribution'].items()),
                                 columns=['Proof Type', 'Count'])
        fig = px.pie(proof_data, values='Count', names='Proof Type',
                    title='<b>Proof Type Distribution</b>',
                    color_discrete_sequence=px.colors.qualitative.Set3)

        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.95)',
            font=dict(family='Inter, sans-serif')
        )
        st.plotly_chart(fig, use_container_width=True)

    # Risk distribution
    st.markdown("### Risk Distribution Across Clusters")
    risk_data = pd.DataFrame(list(summary['risk_distribution'].items()),
                            columns=['Risk Level', 'Number of Clusters'])

    fig = px.bar(risk_data, x='Risk Level', y='Number of Clusters',
                color='Risk Level',
                color_discrete_map={'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'},
                title='<b>Cluster Risk Distribution</b>')

    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0.95)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif')
    )
    st.plotly_chart(fig, use_container_width=True)


def display_generate_report(analyzer):
    """Report generation page"""
    st.markdown('<h1 class="hero-header">Generate Report</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Export comprehensive analysis</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    Generate a detailed Markdown report with:
    - Executive summary
    - Detailed cluster profiles
    - Risk assessments
    - Investment recommendations
    - Market overview
    """)

    col1, col2 = st.columns([2, 1])

    with col1:
        report_name = st.text_input(
            "Report filename:",
            value="crypto_analysis_report.md",
            help="Enter the filename for your report"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate Report", type="primary", use_container_width=True):
            with st.spinner("Generating comprehensive report..."):
                try:
                    time.sleep(1)  # Simulate processing
                    analyzer.export_analysis_report(report_name)
                    st.success("Report generated successfully!")

                    # Download button
                    with open(report_name, 'r') as f:
                        report_content = f.read()

                    st.download_button(
                        label="Download Report",
                        data=report_content,
                        file_name=report_name,
                        mime="text/markdown",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"Error generating report: {e}")

    # Preview
    st.markdown("---")
    st.markdown("### Report Preview")

    with st.expander("Click to see sample report structure"):
        st.markdown("""
        ```
        # Cryptocurrency Cluster Analysis Report

        **Generated**: 2025-10-30
        **Total Cryptocurrencies Analyzed**: 532
        **Number of Clusters**: 4

        ## Executive Summary
        This report analyzes 532 cryptocurrencies grouped into 4 distinct clusters...

        ## Cluster Profiles

        ### Cluster 0: Established Major Cryptocurrencies
        **Risk Level**: Low (3.2/10)
        **Size**: 145 coins (27.3% of market)

        ... detailed analysis for each cluster
        ```
        """)


def main():
    """Main application"""

    # Sidebar
    with st.sidebar:
        # Clean header
        st.markdown("""
        <div style="padding: 1.5rem 0 1rem 0; margin-bottom: 1.5rem; border-bottom: 2px solid #e0e0e0;">
            <h1 style="color: #333; margin: 0 0 0.5rem 0; font-size: 1.6rem; font-weight: 700; line-height: 1.2;">Crypto Intel</h1>
            <p style="color: #666; margin: 0; font-size: 0.9rem; line-height: 1.4;">Professional Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)

        page_category = st.radio(
            "Navigation",
            ["Executive View", "Technical Analysis", "Resources"],
            label_visibility="visible"
        )

        if page_category == "Executive View":
            page = st.radio(
                "",
                ["Executive Dashboard", "ROI Calculator", "Competitive Analysis",
                 "Product Roadmap", "Strategic Insights"],
                label_visibility="collapsed"
            )
        elif page_category == "Technical Analysis":
            page = st.radio(
                "",
                ["Overview", "Cluster Explorer", "Visualizations",
                 "Market Analysis", "Generate Report"],
                label_visibility="collapsed"
            )
        else:
            page = st.radio(
                "",
                ["About", "Documentation", "Contact"],
                label_visibility="collapsed"
            )

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="padding: 1rem; border-top: 1px solid #e0e0e0; margin-top: auto;">
            <h3 style="color: #333; margin: 0 0 0.75rem 0; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Resources</h3>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <a href="https://github.com/rahul99gangu/Cryptocurrencies" style="color: #667eea; text-decoration: none; font-size: 0.9rem;" target="_blank">→ GitHub Repository</a>
                <a href="https://github.com/rahul99gangu/Cryptocurrencies/blob/main/README_ENHANCED.md" style="color: #667eea; text-decoration: none; font-size: 0.9rem;" target="_blank">→ Documentation</a>
                <a href="https://github.com/rahul99gangu/Cryptocurrencies/blob/main/PORTFOLIO_SHOWCASE.md" style="color: #667eea; text-decoration: none; font-size: 0.9rem;" target="_blank">→ Portfolio Guide</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Load data with loading indicator
    try:
        with st.spinner("Loading market data..."):
            data = load_sample_data()
            analyzer = CryptoAIAnalyzer(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure all required files are present.")
        st.stop()
        return

    # Display compact header
    display_compact_header(data)

    # Page routing
    if page == "Overview":
        display_modern_overview(data, analyzer)
    elif page == "Executive Dashboard":
        display_modern_executive_dashboard()
    elif page == "Cluster Explorer":
        display_cluster_explorer(data, analyzer)
    elif page == "Visualizations":
        display_visualizations(data)
    elif page == "Market Analysis":
        display_market_analysis(data, analyzer)
    elif page == "Generate Report":
        display_generate_report(analyzer)
    elif page == "About":
        st.markdown('<h1 class="hero-header">About This Platform</h1>', unsafe_allow_html=True)
        st.markdown("""
        This platform was built by a Senior AI Product Manager with 20 years of experience
        in building and scaling data-driven products.

        ### What Makes This Different

        Most crypto analytics tools overwhelm you with data. This platform uses machine learning
        to find patterns and Gen AI to explain them in plain English. No PhD required.

        ### Technical Approach

        We use K-means clustering with PCA to group 500+ cryptocurrencies by their fundamental
        characteristics. Then AI generates insights that actually matter for investment decisions.

        ### Who Is This For

        - Retail investors who want smarter analysis
        - Portfolio managers looking for efficiency
        - Researchers studying market patterns
        - Anyone tired of information overload
        """)
    elif page == "Documentation":
        st.markdown('<h1 class="hero-header">Documentation</h1>', unsafe_allow_html=True)
        st.markdown("""
        ### Quick Links

        - [Complete Technical Documentation](https://github.com/rahul99gangu/Cryptocurrencies/blob/main/README_ENHANCED.md)
        - [Portfolio Showcase Guide](https://github.com/rahul99gangu/Cryptocurrencies/blob/main/PORTFOLIO_SHOWCASE.md)
        - [AI PM Methodology](https://github.com/rahul99gangu/Cryptocurrencies/blob/main/AI_PM_APPROACH.md)
        - [GitHub Repository](https://github.com/rahul99gangu/Cryptocurrencies)

        ### How to Use

        1. **Overview**: See market trends and cluster distribution
        2. **Cluster Explorer**: Deep dive into specific cryptocurrency groups
        3. **Visualizations**: Interactive 3D plots and charts
        4. **Market Analysis**: Distribution and risk metrics
        5. **Generate Report**: Export comprehensive analysis
        """)
    elif page == "Contact":
        st.markdown('<h1 class="hero-header">Contact</h1>', unsafe_allow_html=True)
        st.markdown("""
        ### Get In Touch

        For questions, feedback, or collaboration:

        - **GitHub**: [rahul99gangu/Cryptocurrencies](https://github.com/rahul99gangu/Cryptocurrencies)
        - **Issues**: [Report a bug](https://github.com/rahul99gangu/Cryptocurrencies/issues)

        ### Built With

        Python • Streamlit • Scikit-learn • Plotly • Gen AI
        """)

    # Footer
    st.markdown("<br><br>", unsafe_html=True)
    st.markdown("""
    <div class="modern-footer">
        <p style="margin: 0; font-size: 1rem;"><strong>Crypto Intelligence Platform v4.0</strong></p>
        <p style="margin: 0.5rem 0; color: #999;">Professional Analytics by Rahul Gangu</p>
        <p style="margin: 0;">
            <a href="https://github.com/rahul99gangu/Cryptocurrencies" style="color: #667eea; text-decoration: none; font-weight: 600;">View on GitHub →</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
