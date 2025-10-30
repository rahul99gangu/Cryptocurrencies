"""
Cryptocurrency Intelligence Platform - Streamlit Web App

An interactive web interface for cryptocurrency clustering analysis
with AI-powered insights.

Author: AI Product Manager
Version: 2.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from crypto_ai_insights import CryptoAIAnalyzer, compare_clusters


# Page configuration
st.set_page_config(
    page_title="Crypto Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .cluster-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #ffffff;
    }
    .risk-low {
        color: #28a745;
        font-weight: bold;
    }
    .risk-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .risk-high {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_sample_data():
    """
    Load sample cryptocurrency data.
    In production, this would load from the Jupyter notebook output.
    """
    # Check if clustered data exists
    if Path('clustered_crypto_data.csv').exists():
        return pd.read_csv('clustered_crypto_data.csv', index_col=0)

    # Otherwise, create sample data for demo
    st.warning("Using sample data. Run the Jupyter notebook first for real data.")

    np.random.seed(42)
    n_samples = 100

    sample_data = pd.DataFrame({
        'CoinName': [f'Coin_{i}' for i in range(n_samples)],
        'Algorithm': np.random.choice(['Scrypt', 'SHA-256', 'Ethash', 'X11'], n_samples),
        'ProofType': np.random.choice(['PoW', 'PoS', 'PoW/PoS'], n_samples),
        'TotalCoinsMined': np.random.exponential(1e7, n_samples),
        'TotalCoinSupply': np.random.exponential(1e8, n_samples),
        'PC 1': np.random.randn(n_samples),
        'PC 2': np.random.randn(n_samples),
        'PC 3': np.random.randn(n_samples),
        'Class': np.random.randint(0, 4, n_samples)
    })

    # Add some known coins
    sample_data.loc[0] = ['Bitcoin', 'SHA-256', 'PoW', 17927175, 21000000, -0.15, -1.37, 0.16, 3]
    sample_data.loc[1] = ['Ethereum', 'Ethash', 'PoW', 107684222, 0, -0.16, -2.04, 0.39, 3]
    sample_data.loc[2] = ['Litecoin', 'Scrypt', 'PoW', 63039243, 84000000, -0.16, -1.05, 0.01, 3]

    return sample_data


def create_3d_scatter(data):
    """Create 3D scatter plot of clusters"""
    fig = px.scatter_3d(
        data,
        x='PC 1',
        y='PC 2',
        z='PC 3',
        color='Class',
        hover_name='CoinName',
        hover_data=['Algorithm', 'ProofType'],
        title='Cryptocurrency Clusters in 3D PCA Space',
        labels={'Class': 'Cluster'},
        color_continuous_scale='viridis',
        height=600
    )

    fig.update_layout(
        scene=dict(
            xaxis_title='Principal Component 1',
            yaxis_title='Principal Component 2',
            zaxis_title='Principal Component 3'
        ),
        font=dict(size=12)
    )

    return fig


def create_2d_supply_chart(data):
    """Create 2D scatter of supply vs mined"""
    # Scale data for better visualization
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
        title='Total Coin Supply vs Total Coins Mined',
        labels={
            'TotalCoinsMined_scaled': 'Total Coins Mined (Millions)',
            'TotalCoinSupply_scaled': 'Total Coin Supply (Millions)',
            'Class': 'Cluster'
        },
        color_continuous_scale='viridis',
        height=500
    )

    return fig


def display_cluster_profile(analyzer, cluster_id):
    """Display detailed cluster profile"""
    profile = analyzer.generate_cluster_profile(cluster_id)

    # Header with name and risk
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### {profile['name']}")
        st.markdown(f"*{profile['description']}*")

    with col2:
        risk_level = profile['risk_assessment']['level']
        risk_score = profile['risk_assessment']['score']
        risk_color = profile['risk_assessment']['color']

        risk_class = 'risk-low' if risk_level == 'Low' else ('risk-medium' if risk_level == 'Medium' else 'risk-high')
        st.markdown(f"<h2 class='{risk_class}'>{risk_color} {risk_level} Risk</h2>", unsafe_allow_html=True)
        st.metric("Risk Score", f"{risk_score}/10")

    # Metrics row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Cluster Size", f"{profile['size']} coins", profile['percentage'])

    with col2:
        st.metric("Dominant Algorithm", profile['dominant_algorithm'])

    with col3:
        st.metric("Dominant Proof", profile['dominant_proof'])

    # Key Features
    st.markdown("#### 🎯 Key Features")
    cols = st.columns(2)
    for idx, feature in enumerate(profile['key_features']):
        with cols[idx % 2]:
            st.markdown(f"✓ {feature}")

    # Statistics
    st.markdown("#### 📊 Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**Avg Supply:** {profile['statistics']['avg_supply']}")

    with col2:
        st.info(f"**Avg Mined:** {profile['statistics']['avg_mined']}")

    with col3:
        st.info(f"**Volatility:** {profile['statistics']['supply_volatility']}")

    # Investment Insights
    st.markdown("#### 💡 Investment Insights")

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

    # Risk Factors
    if profile['risk_assessment']['factors']:
        st.markdown("#### ⚠️ Risk Factors")
        for factor in profile['risk_assessment']['factors']:
            st.warning(factor)

    # Notable Coins
    if profile['notable_coins']:
        st.markdown("#### ⭐ Notable Coins")

        notable_df = pd.DataFrame(profile['notable_coins'])
        st.dataframe(notable_df, use_container_width=True, hide_index=True)

    # Warnings
    if insights['warnings']:
        st.markdown("#### 🚨 Warnings")
        for warning in insights['warnings']:
            if '✓' in warning:
                st.success(warning)
            else:
                st.error(warning)


def display_market_overview(analyzer):
    """Display market overview dashboard"""
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
                    title='Top 10 Algorithms',
                    color='Count',
                    color_continuous_scale='blues')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Proof Type Distribution")
        proof_data = pd.DataFrame(list(summary['proof_distribution'].items()),
                                 columns=['Proof Type', 'Count'])
        fig = px.pie(proof_data, values='Count', names='Proof Type',
                    title='Proof Type Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)

    # Risk Distribution
    st.markdown("### Risk Distribution Across Clusters")
    risk_data = pd.DataFrame(list(summary['risk_distribution'].items()),
                            columns=['Risk Level', 'Number of Clusters'])

    fig = px.bar(risk_data, x='Risk Level', y='Number of Clusters',
                color='Risk Level',
                color_discrete_map={'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'},
                title='Cluster Risk Distribution')
    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main application"""

    # Header
    st.markdown('<p class="main-header">🚀 Cryptocurrency Intelligence Platform</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Clustering & Insights for Smart Crypto Analysis</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Crypto+Intelligence", use_column_width=True)

        st.markdown("## 📊 Navigation")
        page = st.radio(
            "Select a view:",
            ["🏠 Overview", "🔍 Cluster Explorer", "📈 Visualizations", "📊 Market Analysis", "📝 Generate Report"]
        )

        st.markdown("---")
        st.markdown("### 🎯 About")
        st.info("""
        This platform uses unsupervised machine learning (K-means + PCA)
        and generative AI to analyze cryptocurrencies and provide
        actionable insights.
        """)

        st.markdown("### 🛠 Tech Stack")
        st.markdown("""
        - **ML:** K-Means, PCA
        - **AI:** Gen AI Insights
        - **Viz:** Plotly, Streamlit
        - **Data:** Pandas, NumPy
        """)

        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("[📘 Documentation](README_ENHANCED.md)")
        st.markdown("[💼 Portfolio Guide](PORTFOLIO_SHOWCASE.md)")
        st.markdown("[🤖 AI Module](crypto_ai_insights.py)")

    # Load data
    try:
        data = load_sample_data()
        analyzer = CryptoAIAnalyzer(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please run the Jupyter notebook first to generate clustered data.")
        return

    # Page routing
    if page == "🏠 Overview":
        st.markdown("## Welcome to the Cryptocurrency Intelligence Platform")

        st.markdown("""
        This platform transforms complex cryptocurrency data into actionable insights using:
        - **Unsupervised Machine Learning** for clustering similar cryptocurrencies
        - **Generative AI** for natural language insights and risk assessment
        - **Interactive Visualizations** for exploring patterns
        """)

        # Quick stats
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Cryptocurrencies", len(data))

        with col2:
            st.metric("Clusters", len(data['Class'].unique()))

        with col3:
            st.metric("Algorithms", len(data['Algorithm'].unique()))

        with col4:
            st.metric("Proof Types", len(data['ProofType'].unique()))

        # Sample visualization
        st.markdown("### 🎯 Cluster Distribution")
        cluster_counts = data['Class'].value_counts().sort_index()
        fig = px.bar(x=cluster_counts.index, y=cluster_counts.values,
                    labels={'x': 'Cluster ID', 'y': 'Number of Coins'},
                    title='Cryptocurrencies per Cluster',
                    color=cluster_counts.values,
                    color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)

        # Getting started
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        1. **Cluster Explorer**: Analyze detailed insights for each cluster
        2. **Visualizations**: Explore 3D PCA plots and supply charts
        3. **Market Analysis**: View market-wide statistics and trends
        4. **Generate Report**: Export comprehensive analysis as Markdown
        """)

    elif page == "🔍 Cluster Explorer":
        st.markdown("## 🔍 Cluster Explorer")
        st.markdown("Explore detailed AI-powered insights for each cryptocurrency cluster")

        # Cluster selector
        cluster_ids = sorted(data['Class'].unique())

        # Cluster comparison table
        st.markdown("### 📊 Cluster Comparison")
        comparison_df = compare_clusters(analyzer, cluster_ids)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Detailed view
        selected_cluster = st.selectbox(
            "Select a cluster to explore:",
            cluster_ids,
            format_func=lambda x: f"Cluster {x}"
        )

        if selected_cluster is not None:
            display_cluster_profile(analyzer, selected_cluster)

    elif page == "📈 Visualizations":
        st.markdown("## 📈 Interactive Visualizations")

        tab1, tab2, tab3 = st.tabs(["3D PCA Plot", "Supply vs Mined", "Data Table"])

        with tab1:
            st.markdown("### 3D Cluster Visualization")
            st.markdown("Explore cryptocurrencies in 3D principal component space")
            fig = create_3d_scatter(data)
            st.plotly_chart(fig, use_container_width=True)

            st.info("""
            **How to read this chart:**
            - Each point represents a cryptocurrency
            - Colors represent different clusters
            - Hover over points to see coin details
            - Similar coins are closer together
            """)

        with tab2:
            st.markdown("### Total Supply vs Total Mined")
            fig = create_2d_supply_chart(data)
            st.plotly_chart(fig, use_container_width=True)

            st.info("""
            **Insights:**
            - X-axis: Total coins mined (Millions)
            - Y-axis: Total coin supply (Millions)
            - Points near the diagonal are close to full mining completion
            """)

        with tab3:
            st.markdown("### Complete Data Table")

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

    elif page == "📊 Market Analysis":
        st.markdown("## 📊 Market Analysis Dashboard")
        display_market_overview(analyzer)

    elif page == "📝 Generate Report":
        st.markdown("## 📝 Generate Comprehensive Report")

        st.markdown("""
        Export a detailed Markdown report with:
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
                value=f"crypto_analysis_report.md",
                help="Enter the filename for the report"
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📥 Generate Report", type="primary"):
                try:
                    with st.spinner("Generating comprehensive report..."):
                        report_path = analyzer.export_analysis_report(report_name)

                    st.success(f"✅ Report generated successfully!")

                    # Show download button
                    with open(report_name, 'r') as f:
                        report_content = f.read()

                    st.download_button(
                        label="📥 Download Report",
                        data=report_content,
                        file_name=report_name,
                        mime="text/markdown"
                    )

                except Exception as e:
                    st.error(f"Error generating report: {e}")

        # Preview
        st.markdown("### 📄 Report Preview")

        with st.expander("Click to see sample report structure"):
            st.markdown("""
            ```
            # Cryptocurrency Cluster Analysis Report

            **Generated**: 2025-10-30 12:00:00
            **Total Cryptocurrencies Analyzed**: 532
            **Number of Clusters**: 4

            ## Executive Summary
            This report analyzes 532 cryptocurrencies grouped into 4 distinct clusters...

            ## Cluster Profiles

            ### Cluster 0: Established Major Cryptocurrencies
            **Risk Level**: 🟢 Low (3.2/10)
            **Size**: 145 coins (27.3% of market)

            **Description**: Industry-leading cryptocurrencies with high market adoption...

            **Key Features**:
            - Market Leaders
            - High Liquidity
            - Strong Community

            ... and more detailed analysis for each cluster
            ```
            """)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>🚀 Cryptocurrency Intelligence Platform v2.0</p>
            <p>Built with ❤️ using Streamlit, Scikit-learn, and Gen AI</p>
            <p>For AI Product Manager Portfolio | <a href='AI_PM_APPROACH.md'>View Methodology</a></p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
