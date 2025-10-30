"""
Cryptocurrency AI Insights Generator

This module provides Gen AI capabilities for cryptocurrency clustering analysis.
It uses Large Language Models to generate human-readable insights, investment
recommendations, and risk assessments based on clustering results.

Author: AI Product Manager
Version: 2.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime


class CryptoAIAnalyzer:
    """
    AI-powered cryptocurrency analysis engine that combines unsupervised
    machine learning with generative AI for actionable insights.
    """

    def __init__(self, clustered_data: pd.DataFrame):
        """
        Initialize the AI analyzer with clustered cryptocurrency data.

        Args:
            clustered_data: DataFrame with clustering results including
                          CoinName, Algorithm, ProofType, TotalCoinsMined,
                          TotalCoinSupply, PC components, and Class labels
        """
        self.data = clustered_data
        self.cluster_stats = self._calculate_cluster_statistics()

    def _calculate_cluster_statistics(self) -> Dict:
        """
        Calculate statistical metrics for each cluster.

        Returns:
            Dictionary with cluster statistics
        """
        stats = {}

        for cluster_id in self.data['Class'].unique():
            cluster_data = self.data[self.data['Class'] == cluster_id]

            stats[cluster_id] = {
                'size': len(cluster_data),
                'avg_supply': cluster_data['TotalCoinSupply'].mean(),
                'avg_mined': cluster_data['TotalCoinsMined'].mean(),
                'top_algorithms': cluster_data['Algorithm'].value_counts().head(3).to_dict(),
                'top_proofs': cluster_data['ProofType'].value_counts().head(3).to_dict(),
                'coins': cluster_data['CoinName'].tolist(),
                'supply_std': cluster_data['TotalCoinSupply'].std(),
                'mined_std': cluster_data['TotalCoinsMined'].std()
            }

        return stats

    def generate_cluster_profile(self, cluster_id: int) -> Dict:
        """
        Generate a comprehensive profile for a specific cluster.

        Args:
            cluster_id: The cluster ID to analyze

        Returns:
            Dictionary containing cluster profile information
        """
        if cluster_id not in self.cluster_stats:
            raise ValueError(f"Cluster {cluster_id} not found")

        stats = self.cluster_stats[cluster_id]
        cluster_data = self.data[self.data['Class'] == cluster_id]

        # Identify cluster characteristics
        characteristics = self._identify_cluster_characteristics(cluster_id)

        # Calculate risk metrics
        risk_score = self._calculate_risk_score(cluster_data)

        # Find notable coins
        notable_coins = self._find_notable_coins(cluster_data)

        profile = {
            'cluster_id': cluster_id,
            'name': characteristics['name'],
            'description': characteristics['description'],
            'size': stats['size'],
            'percentage': f"{(stats['size'] / len(self.data)) * 100:.1f}%",
            'key_features': characteristics['features'],
            'dominant_algorithm': list(stats['top_algorithms'].keys())[0],
            'dominant_proof': list(stats['top_proofs'].keys())[0],
            'risk_assessment': risk_score,
            'notable_coins': notable_coins,
            'investment_insights': self._generate_investment_insights(cluster_id, risk_score),
            'statistics': {
                'avg_supply': f"{stats['avg_supply']:,.0f}",
                'avg_mined': f"{stats['avg_mined']:,.0f}",
                'supply_volatility': 'High' if stats['supply_std'] > stats['avg_supply'] else 'Low'
            }
        }

        return profile

    def _identify_cluster_characteristics(self, cluster_id: int) -> Dict:
        """
        Identify and name cluster based on its characteristics.

        Args:
            cluster_id: The cluster ID to characterize

        Returns:
            Dictionary with cluster name, description, and key features
        """
        stats = self.cluster_stats[cluster_id]
        cluster_data = self.data[self.data['Class'] == cluster_id]

        # Analyze dominant algorithms and proof types
        top_algo = list(stats['top_algorithms'].keys())[0]
        top_proof = list(stats['top_proofs'].keys())[0]

        # Check for notable coins
        has_btc = 'Bitcoin' in stats['coins']
        has_eth = 'Ethereum' in stats['coins']

        # Determine supply characteristics
        high_supply = stats['avg_supply'] > 1e9
        low_supply = stats['avg_supply'] < 1e7

        # Generate characteristics based on patterns
        if has_btc or has_eth:
            name = "Established Major Cryptocurrencies"
            description = "Industry-leading cryptocurrencies with high market adoption and proven track records"
            features = [
                "Market Leaders",
                "High Liquidity",
                "Strong Community",
                "Proven Technology"
            ]
        elif high_supply:
            name = "High-Supply Altcoins"
            description = "Cryptocurrencies with large total supply, often targeting mass adoption"
            features = [
                "Large Supply Base",
                f"Dominant: {top_algo}",
                "Mass Market Focus",
                "Lower Individual Token Value"
            ]
        elif low_supply and top_proof == 'PoS':
            name = "Scarcity-Focused PoS Coins"
            description = "Proof-of-Stake coins with limited supply, emphasizing scarcity and staking rewards"
            features = [
                "Limited Supply",
                "Staking Mechanisms",
                "Energy Efficient",
                "Deflationary Pressure"
            ]
        elif 'Scrypt' in top_algo:
            name = "Scrypt-Based Mining Coins"
            description = "Cryptocurrencies using Scrypt algorithm, often Litecoin-inspired"
            features = [
                "Scrypt Algorithm",
                "GPU-Friendly Mining",
                "Fast Transactions",
                "Alternative to SHA-256"
            ]
        else:
            name = f"{top_algo} Cluster"
            description = f"Cryptocurrencies primarily using {top_algo} algorithm with {top_proof} consensus"
            features = [
                f"Algorithm: {top_algo}",
                f"Consensus: {top_proof}",
                "Niche Market Position",
                "Specialized Use Cases"
            ]

        return {
            'name': name,
            'description': description,
            'features': features
        }

    def _calculate_risk_score(self, cluster_data: pd.DataFrame) -> Dict:
        """
        Calculate risk assessment for a cluster.

        Args:
            cluster_data: DataFrame containing cluster cryptocurrency data

        Returns:
            Dictionary with risk score and assessment
        """
        risk_factors = []
        risk_score = 5.0  # Start at medium risk (scale 1-10)

        # Factor 1: Supply volatility
        supply_cv = cluster_data['TotalCoinSupply'].std() / (cluster_data['TotalCoinSupply'].mean() + 1)
        if supply_cv > 2:
            risk_score += 1.5
            risk_factors.append("High supply variance across cluster")

        # Factor 2: Small cluster size (less diversification)
        if len(cluster_data) < 20:
            risk_score += 1.0
            risk_factors.append("Limited cluster diversification")
        else:
            risk_score -= 0.5
            risk_factors.append("Good diversification within cluster")

        # Factor 3: Presence of established coins
        established_coins = ['Bitcoin', 'Ethereum', 'Litecoin', 'Dash', 'Monero']
        if any(coin in cluster_data['CoinName'].values for coin in established_coins):
            risk_score -= 2.0
            risk_factors.append("Contains established, proven cryptocurrencies")

        # Factor 4: Algorithm diversity
        algo_diversity = len(cluster_data['Algorithm'].unique())
        if algo_diversity == 1:
            risk_score += 0.5
            risk_factors.append("Single algorithm dependency")

        # Factor 5: Zero supply coins (unlimited inflation)
        zero_supply_pct = (cluster_data['TotalCoinSupply'] == 0).sum() / len(cluster_data)
        if zero_supply_pct > 0.3:
            risk_score += 1.0
            risk_factors.append("High percentage of unlimited supply coins")

        # Cap risk score between 1 and 10
        risk_score = max(1, min(10, risk_score))

        # Determine risk level
        if risk_score <= 3.5:
            risk_level = "Low"
            risk_color = "🟢"
        elif risk_score <= 6.5:
            risk_level = "Medium"
            risk_color = "🟡"
        else:
            risk_level = "High"
            risk_color = "🔴"

        return {
            'score': round(risk_score, 1),
            'level': risk_level,
            'color': risk_color,
            'factors': risk_factors
        }

    def _find_notable_coins(self, cluster_data: pd.DataFrame, top_n: int = 5) -> List[Dict]:
        """
        Identify the most notable coins in a cluster.

        Args:
            cluster_data: DataFrame containing cluster cryptocurrency data
            top_n: Number of notable coins to return

        Returns:
            List of notable coin dictionaries
        """
        notable = []

        # Sort by supply and mining metrics
        cluster_data_sorted = cluster_data.copy()
        cluster_data_sorted['score'] = (
            cluster_data_sorted['TotalCoinsMined'] / (cluster_data_sorted['TotalCoinSupply'] + 1)
        )

        for idx, row in cluster_data_sorted.nlargest(top_n, 'score').iterrows():
            notable.append({
                'name': row['CoinName'],
                'algorithm': row['Algorithm'],
                'proof_type': row['ProofType'],
                'mined': f"{row['TotalCoinsMined']:,.0f}",
                'supply': f"{row['TotalCoinSupply']:,.0f}",
                'completion': f"{(row['TotalCoinsMined'] / (row['TotalCoinSupply'] + 1)) * 100:.1f}%"
            })

        return notable

    def _generate_investment_insights(self, cluster_id: int, risk_score: Dict) -> Dict:
        """
        Generate AI-powered investment insights for a cluster.

        Args:
            cluster_id: The cluster ID
            risk_score: Risk assessment dictionary

        Returns:
            Dictionary with investment insights
        """
        stats = self.cluster_stats[cluster_id]

        insights = {
            'recommended_allocation': self._recommend_allocation(risk_score['score']),
            'investment_strategy': self._suggest_strategy(cluster_id, risk_score),
            'key_considerations': self._identify_considerations(cluster_id),
            'potential_opportunities': self._identify_opportunities(cluster_id),
            'warnings': self._identify_warnings(cluster_id, risk_score)
        }

        return insights

    def _recommend_allocation(self, risk_score: float) -> str:
        """Recommend portfolio allocation percentage based on risk."""
        if risk_score <= 3.5:
            return "20-40% (Core Holdings)"
        elif risk_score <= 6.5:
            return "10-20% (Moderate Position)"
        else:
            return "0-5% (Speculative Only)"

    def _suggest_strategy(self, cluster_id: int, risk_score: Dict) -> str:
        """Suggest investment strategy based on cluster characteristics."""
        stats = self.cluster_stats[cluster_id]

        if risk_score['level'] == 'Low':
            return "Long-term hold strategy (HODL). Consider dollar-cost averaging for accumulation."
        elif risk_score['level'] == 'Medium':
            return "Balanced approach with regular rebalancing. Monitor market conditions closely."
        else:
            return "High-risk, high-reward. Only invest what you can afford to lose. Short-term trading may be appropriate."

    def _identify_considerations(self, cluster_id: int) -> List[str]:
        """Identify key investment considerations."""
        stats = self.cluster_stats[cluster_id]
        considerations = []

        # Algorithm considerations
        top_algo = list(stats['top_algorithms'].keys())[0]
        if top_algo == 'SHA-256':
            considerations.append("SHA-256 coins compete directly with Bitcoin for mining resources")
        elif top_algo == 'Scrypt':
            considerations.append("Scrypt algorithm offers faster block times but different security model")

        # Proof type considerations
        top_proof = list(stats['top_proofs'].keys())[0]
        if 'PoS' in top_proof:
            considerations.append("Proof-of-Stake enables passive income through staking")
        elif top_proof == 'PoW':
            considerations.append("Proof-of-Work provides battle-tested security but higher energy costs")

        # Supply considerations
        if stats['avg_supply'] == 0:
            considerations.append("Unlimited supply may lead to inflationary pressure")

        return considerations

    def _identify_opportunities(self, cluster_id: int) -> List[str]:
        """Identify potential opportunities in the cluster."""
        stats = self.cluster_stats[cluster_id]
        opportunities = []

        # Check for established coins
        established = ['Bitcoin', 'Ethereum', 'Litecoin']
        if any(coin in stats['coins'] for coin in established):
            opportunities.append("Exposure to industry-leading cryptocurrencies with proven adoption")

        # Check for diversity
        if stats['size'] > 30:
            opportunities.append("Large cluster provides good diversification within similar assets")

        # Algorithm-specific opportunities
        if 'Equihash' in stats['top_algorithms']:
            opportunities.append("Privacy-focused cryptocurrencies with growing demand")

        if 'Ethash' in stats['top_algorithms']:
            opportunities.append("Smart contract platforms with DeFi and NFT ecosystems")

        return opportunities if opportunities else ["Research individual projects for unique value propositions"]

    def _identify_warnings(self, cluster_id: int, risk_score: Dict) -> List[str]:
        """Identify warnings and risks."""
        warnings = []

        if risk_score['score'] > 7:
            warnings.append("⚠️ HIGH RISK: Significant potential for losses")

        stats = self.cluster_stats[cluster_id]

        if stats['size'] < 10:
            warnings.append("⚠️ Small cluster may indicate niche or outdated technologies")

        # Check for high volatility
        if stats['supply_std'] > stats['avg_supply'] * 2:
            warnings.append("⚠️ High volatility in supply metrics across cluster")

        return warnings if warnings else ["✓ No major red flags identified"]

    def generate_market_summary(self) -> Dict:
        """
        Generate an overall market summary across all clusters.

        Returns:
            Dictionary with comprehensive market analysis
        """
        total_coins = len(self.data)
        num_clusters = len(self.cluster_stats)

        # Calculate overall statistics
        overall_stats = {
            'total_cryptocurrencies': total_coins,
            'total_clusters': num_clusters,
            'avg_cluster_size': total_coins / num_clusters,
            'market_structure': self._analyze_market_structure(),
            'algorithm_distribution': self._get_algorithm_distribution(),
            'proof_distribution': self._get_proof_distribution(),
            'risk_distribution': self._get_risk_distribution()
        }

        return overall_stats

    def _analyze_market_structure(self) -> Dict:
        """Analyze the overall market structure."""
        sizes = [stats['size'] for stats in self.cluster_stats.values()]

        return {
            'largest_cluster': max(sizes),
            'smallest_cluster': min(sizes),
            'concentration': 'High' if max(sizes) > len(self.data) * 0.5 else 'Balanced'
        }

    def _get_algorithm_distribution(self) -> Dict:
        """Get algorithm distribution across all cryptocurrencies."""
        return self.data['Algorithm'].value_counts().head(10).to_dict()

    def _get_proof_distribution(self) -> Dict:
        """Get proof type distribution across all cryptocurrencies."""
        return self.data['ProofType'].value_counts().head(5).to_dict()

    def _get_risk_distribution(self) -> Dict:
        """Calculate risk distribution across clusters."""
        risk_levels = {'Low': 0, 'Medium': 0, 'High': 0}

        for cluster_id in self.cluster_stats.keys():
            cluster_data = self.data[self.data['Class'] == cluster_id]
            risk = self._calculate_risk_score(cluster_data)
            risk_levels[risk['level']] += 1

        return risk_levels

    def export_analysis_report(self, filename: str = None) -> str:
        """
        Export a comprehensive analysis report in Markdown format.

        Args:
            filename: Optional filename to save the report

        Returns:
            Markdown-formatted report string
        """
        if filename is None:
            filename = f"crypto_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        report = self._generate_markdown_report()

        with open(filename, 'w') as f:
            f.write(report)

        return report

    def _generate_markdown_report(self) -> str:
        """Generate a comprehensive Markdown report."""
        report = []

        # Header
        report.append("# Cryptocurrency Cluster Analysis Report")
        report.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n**Total Cryptocurrencies Analyzed**: {len(self.data)}")
        report.append(f"\n**Number of Clusters**: {len(self.cluster_stats)}\n")

        # Executive Summary
        report.append("## Executive Summary\n")
        market_summary = self.generate_market_summary()
        report.append(f"This report analyzes {market_summary['total_cryptocurrencies']} cryptocurrencies ")
        report.append(f"grouped into {market_summary['total_clusters']} distinct clusters using unsupervised machine learning.\n")

        # Cluster Profiles
        report.append("## Cluster Profiles\n")

        for cluster_id in sorted(self.cluster_stats.keys()):
            profile = self.generate_cluster_profile(cluster_id)

            report.append(f"### Cluster {cluster_id}: {profile['name']}\n")
            report.append(f"**Risk Level**: {profile['risk_assessment']['color']} {profile['risk_assessment']['level']} ")
            report.append(f"({profile['risk_assessment']['score']}/10)\n")
            report.append(f"**Size**: {profile['size']} coins ({profile['percentage']} of market)\n")
            report.append(f"\n**Description**: {profile['description']}\n")

            # Key Features
            report.append("\n**Key Features**:")
            for feature in profile['key_features']:
                report.append(f"\n- {feature}")

            # Statistics
            report.append("\n\n**Statistics**:")
            report.append(f"\n- Dominant Algorithm: {profile['dominant_algorithm']}")
            report.append(f"\n- Dominant Proof: {profile['dominant_proof']}")
            report.append(f"\n- Average Supply: {profile['statistics']['avg_supply']}")
            report.append(f"\n- Average Mined: {profile['statistics']['avg_mined']}")

            # Investment Insights
            report.append("\n\n**Investment Insights**:")
            insights = profile['investment_insights']
            report.append(f"\n- **Recommended Allocation**: {insights['recommended_allocation']}")
            report.append(f"\n- **Strategy**: {insights['investment_strategy']}")

            # Notable Coins
            if profile['notable_coins']:
                report.append("\n\n**Notable Coins**:")
                for coin in profile['notable_coins'][:3]:
                    report.append(f"\n- **{coin['name']}** ({coin['algorithm']}): {coin['completion']} mined")

            # Warnings
            if insights['warnings']:
                report.append("\n\n**Warnings**:")
                for warning in insights['warnings']:
                    report.append(f"\n- {warning}")

            report.append("\n\n---\n")

        # Market Overview
        report.append("## Market Overview\n")
        report.append(f"\n**Algorithm Distribution** (Top 5):")
        for algo, count in list(market_summary['algorithm_distribution'].items())[:5]:
            report.append(f"\n- {algo}: {count} coins")

        report.append(f"\n\n**Proof Type Distribution**:")
        for proof, count in market_summary['proof_distribution'].items():
            report.append(f"\n- {proof}: {count} coins")

        report.append(f"\n\n**Risk Distribution Across Clusters**:")
        for level, count in market_summary['risk_distribution'].items():
            report.append(f"\n- {level} Risk: {count} clusters")

        # Disclaimer
        report.append("\n\n---\n")
        report.append("## Disclaimer\n")
        report.append("This analysis is for informational purposes only and should not be considered ")
        report.append("financial advice. Cryptocurrency investments carry significant risk. Always conduct ")
        report.append("your own research and consult with financial advisors before making investment decisions.\n")

        return ''.join(report)

    def generate_llm_prompt_for_insights(self, cluster_id: int) -> str:
        """
        Generate a structured prompt for LLM-based insight generation.

        This method creates a comprehensive prompt that can be sent to
        an LLM (like Claude or GPT-4) for generating natural language insights.

        Args:
            cluster_id: The cluster ID to generate insights for

        Returns:
            Formatted prompt string for LLM
        """
        profile = self.generate_cluster_profile(cluster_id)

        prompt = f"""You are a cryptocurrency market analyst AI assistant. Analyze the following cluster of cryptocurrencies and provide investment insights.

**CLUSTER INFORMATION:**
- Cluster ID: {profile['cluster_id']}
- Cluster Name: {profile['name']}
- Number of Coins: {profile['size']} ({profile['percentage']} of analyzed market)
- Risk Level: {profile['risk_assessment']['level']} ({profile['risk_assessment']['score']}/10)

**TECHNICAL CHARACTERISTICS:**
- Dominant Algorithm: {profile['dominant_algorithm']}
- Dominant Proof Type: {profile['dominant_proof']}
- Average Supply: {profile['statistics']['avg_supply']}
- Average Mined: {profile['statistics']['avg_mined']}
- Supply Volatility: {profile['statistics']['supply_volatility']}

**KEY FEATURES:**
{chr(10).join([f"- {f}" for f in profile['key_features']])}

**NOTABLE COINS:**
{chr(10).join([f"- {c['name']} ({c['algorithm']}): {c['completion']} mined" for c in profile['notable_coins'][:5]])}

**RISK FACTORS:**
{chr(10).join([f"- {f}" for f in profile['risk_assessment']['factors']])}

**TASK:**
Please provide:
1. A 2-3 sentence summary of this cluster's market position
2. Key differentiators from other cryptocurrency clusters
3. Investment thesis (bullish or bearish) with reasoning
4. Specific risks investors should be aware of
5. Recommended investor profile (conservative, moderate, aggressive)

Format your response as clear, actionable insights for both novice and experienced investors."""

        return prompt


# Utility Functions

def load_clustered_data(file_path: str = None, dataframe: pd.DataFrame = None) -> CryptoAIAnalyzer:
    """
    Convenience function to load clustered data and create analyzer.

    Args:
        file_path: Path to CSV file with clustered data
        dataframe: Alternatively, provide a pandas DataFrame directly

    Returns:
        CryptoAIAnalyzer instance
    """
    if dataframe is not None:
        data = dataframe
    elif file_path is not None:
        data = pd.read_csv(file_path)
    else:
        raise ValueError("Must provide either file_path or dataframe")

    return CryptoAIAnalyzer(data)


def compare_clusters(analyzer: CryptoAIAnalyzer, cluster_ids: List[int]) -> pd.DataFrame:
    """
    Generate a comparison table for multiple clusters.

    Args:
        analyzer: CryptoAIAnalyzer instance
        cluster_ids: List of cluster IDs to compare

    Returns:
        DataFrame with comparison metrics
    """
    comparison_data = []

    for cluster_id in cluster_ids:
        profile = analyzer.generate_cluster_profile(cluster_id)
        comparison_data.append({
            'Cluster ID': cluster_id,
            'Name': profile['name'],
            'Size': profile['size'],
            'Risk Level': profile['risk_assessment']['level'],
            'Risk Score': profile['risk_assessment']['score'],
            'Algorithm': profile['dominant_algorithm'],
            'Proof': profile['dominant_proof'],
            'Allocation': profile['investment_insights']['recommended_allocation']
        })

    return pd.DataFrame(comparison_data)


if __name__ == "__main__":
    print("🚀 Crypto AI Insights Generator")
    print("=" * 50)
    print("\nThis module provides AI-powered analysis for cryptocurrency clustering.")
    print("\nUsage Example:")
    print("```python")
    print("from crypto_ai_insights import CryptoAIAnalyzer")
    print("")
    print("# Load your clustered data")
    print("analyzer = CryptoAIAnalyzer(clustered_df)")
    print("")
    print("# Generate insights for a cluster")
    print("profile = analyzer.generate_cluster_profile(cluster_id=0)")
    print("")
    print("# Export comprehensive report")
    print("analyzer.export_analysis_report('my_crypto_analysis.md')")
    print("```")
    print("\n" + "=" * 50)
    print("Ready to enhance your cryptocurrency analysis with AI! 🎯")
