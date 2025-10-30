"""
Example Usage: Cryptocurrency AI Insights Generator

This script demonstrates how to use the crypto_ai_insights module
to analyze cryptocurrency clusters and generate AI-powered insights.

Run this after executing the Jupyter notebook to generate cluster data.
"""

import pandas as pd
from crypto_ai_insights import CryptoAIAnalyzer, compare_clusters


def example_basic_analysis():
    """
    Example 1: Basic cluster analysis
    """
    print("=" * 60)
    print("EXAMPLE 1: Basic Cluster Analysis")
    print("=" * 60)

    # Note: In real usage, load your clustered_df from the notebook
    # For this example, we'll show the structure

    print("\nStep 1: Load clustered data from your notebook")
    print("```python")
    print("clustered_df = pd.read_csv('clustered_crypto_data.csv')")
    print("```")

    print("\nStep 2: Initialize the AI analyzer")
    print("```python")
    print("analyzer = CryptoAIAnalyzer(clustered_df)")
    print("```")

    print("\nStep 3: Generate insights for a specific cluster")
    print("```python")
    print("profile = analyzer.generate_cluster_profile(cluster_id=0)")
    print("print(f'Cluster Name: {profile[\"name\"]}')")
    print("print(f'Risk Level: {profile[\"risk_assessment\"][\"level\"]}')")
    print("print(f'Size: {profile[\"size\"]} coins')")
    print("```")


def example_comprehensive_report():
    """
    Example 2: Generate comprehensive report
    """
    print("\n\n" + "=" * 60)
    print("EXAMPLE 2: Generate Comprehensive Report")
    print("=" * 60)

    print("\nGenerate a full Markdown report with all cluster insights:")
    print("```python")
    print("analyzer = CryptoAIAnalyzer(clustered_df)")
    print("report = analyzer.export_analysis_report('my_crypto_analysis.md')")
    print("print('Report generated: my_crypto_analysis.md')")
    print("```")

    print("\nThe report includes:")
    print("- Executive summary")
    print("- Detailed cluster profiles")
    print("- Risk assessments")
    print("- Investment recommendations")
    print("- Market overview")


def example_market_summary():
    """
    Example 3: Get market summary
    """
    print("\n\n" + "=" * 60)
    print("EXAMPLE 3: Market Summary")
    print("=" * 60)

    print("\nGet an overview of the entire cryptocurrency market:")
    print("```python")
    print("analyzer = CryptoAIAnalyzer(clustered_df)")
    print("summary = analyzer.generate_market_summary()")
    print("")
    print("print(f'Total Cryptocurrencies: {summary[\"total_cryptocurrencies\"]}')")
    print("print(f'Number of Clusters: {summary[\"total_clusters\"]}')")
    print("print(f'Risk Distribution: {summary[\"risk_distribution\"]}')")
    print("```")


def example_cluster_comparison():
    """
    Example 4: Compare multiple clusters
    """
    print("\n\n" + "=" * 60)
    print("EXAMPLE 4: Cluster Comparison")
    print("=" * 60)

    print("\nCompare multiple clusters side-by-side:")
    print("```python")
    print("from crypto_ai_insights import compare_clusters")
    print("")
    print("analyzer = CryptoAIAnalyzer(clustered_df)")
    print("comparison_df = compare_clusters(analyzer, [0, 1, 2, 3])")
    print("")
    print("print(comparison_df)")
    print("```")

    print("\nOutput will be a DataFrame with:")
    print("- Cluster ID and Name")
    print("- Size and Risk Level")
    print("- Dominant Algorithm and Proof Type")
    print("- Recommended Allocation %")


def example_llm_prompt_generation():
    """
    Example 5: Generate LLM prompts for external AI services
    """
    print("\n\n" + "=" * 60)
    print("EXAMPLE 5: LLM Prompt Generation")
    print("=" * 60)

    print("\nGenerate structured prompts for Claude/GPT-4:")
    print("```python")
    print("analyzer = CryptoAIAnalyzer(clustered_df)")
    print("prompt = analyzer.generate_llm_prompt_for_insights(cluster_id=0)")
    print("")
    print("# Send to your LLM API")
    print("# import anthropic")
    print("# client = anthropic.Anthropic(api_key='your-key')")
    print("# response = client.messages.create(")
    print("#     model='claude-3-5-sonnet-20241022',")
    print("#     messages=[{'role': 'user', 'content': prompt}]")
    print("# )")
    print("```")


def example_workflow():
    """
    Example 6: Complete workflow
    """
    print("\n\n" + "=" * 60)
    print("EXAMPLE 6: Complete Workflow")
    print("=" * 60)

    print("\nComplete workflow from notebook to insights:")
    print("""
STEP 1: Run the Jupyter notebook
    - Load crypto_data.csv
    - Preprocess data
    - Apply PCA and K-means clustering
    - Save clustered_df

STEP 2: Use AI Insights Generator
```python
from crypto_ai_insights import CryptoAIAnalyzer

# Load your clustered data
analyzer = CryptoAIAnalyzer(clustered_df)

# Analyze each cluster
for cluster_id in range(4):  # Assuming 4 clusters
    profile = analyzer.generate_cluster_profile(cluster_id)

    print(f"\\n{'='*50}")
    print(f"Cluster {cluster_id}: {profile['name']}")
    print(f"{'='*50}")
    print(f"Risk: {profile['risk_assessment']['color']} {profile['risk_assessment']['level']}")
    print(f"Size: {profile['size']} coins ({profile['percentage']})")
    print(f"\\nKey Features:")
    for feature in profile['key_features']:
        print(f"  - {feature}")
    print(f"\\nRecommended Allocation: {profile['investment_insights']['recommended_allocation']}")
    print(f"Strategy: {profile['investment_insights']['investment_strategy']}")

# Generate comprehensive report
analyzer.export_analysis_report('full_analysis.md')
print("\\nFull report exported to: full_analysis.md")
```

STEP 3: Review and share your insights!
    """)


def print_sample_output():
    """
    Show sample output format
    """
    print("\n\n" + "=" * 60)
    print("SAMPLE OUTPUT FORMAT")
    print("=" * 60)

    print("""
==================================================
Cluster 0: Established Major Cryptocurrencies
==================================================
Risk: 🟢 Low (3.2/10)
Size: 145 coins (27.3% of market)

Key Features:
  - Market Leaders
  - High Liquidity
  - Strong Community
  - Proven Technology

Recommended Allocation: 20-40% (Core Holdings)
Strategy: Long-term hold strategy (HODL). Consider dollar-cost averaging for accumulation.

Notable Coins:
  - Bitcoin (SHA-256): 85.4% mined
  - Ethereum (Ethash): 100.0% mined
  - Litecoin (Scrypt): 75.0% mined

Investment Insights:
  - Opportunity: Exposure to industry-leading cryptocurrencies
  - Consideration: Regulatory scrutiny on major coins
  - Warning: ✓ No major red flags identified
    """)


def main():
    """
    Main function to run all examples
    """
    print("\n")
    print("█" * 60)
    print("   CRYPTOCURRENCY AI INSIGHTS - USAGE EXAMPLES")
    print("█" * 60)

    example_basic_analysis()
    example_comprehensive_report()
    example_market_summary()
    example_cluster_comparison()
    example_llm_prompt_generation()
    example_workflow()
    print_sample_output()

    print("\n\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("""
1. Run the Jupyter notebook: crypto_clustering.ipynb
2. Load your clustered_df DataFrame
3. Import and use CryptoAIAnalyzer
4. Generate insights and reports!

For more information:
- README_ENHANCED.md: Complete documentation
- AI_PM_APPROACH.md: Product management methodology
- PORTFOLIO_SHOWCASE.md: How to present this project

Questions? Check the documentation or open an issue on GitHub.
    """)

    print("=" * 60)
    print("Happy analyzing! 🚀")
    print("=" * 60)


if __name__ == "__main__":
    main()
