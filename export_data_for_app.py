"""
Export Clustered Data for Streamlit App

This script exports the clustered DataFrame from the Jupyter notebook
to a CSV file that the Streamlit app can read.

Run this after completing the Jupyter notebook analysis.
"""

import pandas as pd
import sys


def export_clustered_data(clustered_df, output_file='clustered_crypto_data.csv'):
    """
    Export clustered DataFrame to CSV for Streamlit app.

    Args:
        clustered_df: DataFrame with clustering results
        output_file: Output CSV filename
    """
    try:
        # Ensure required columns exist
        required_cols = ['CoinName', 'Algorithm', 'ProofType', 'TotalCoinsMined',
                        'TotalCoinSupply', 'PC 1', 'PC 2', 'PC 3', 'Class']

        missing_cols = [col for col in required_cols if col not in clustered_df.columns]

        if missing_cols:
            print(f"⚠️  Warning: Missing columns: {missing_cols}")
            print("The Streamlit app may not work properly.")

        # Export to CSV
        clustered_df.to_csv(output_file)
        print(f"✅ Successfully exported {len(clustered_df)} rows to {output_file}")
        print(f"\nColumns exported: {list(clustered_df.columns)}")
        print(f"Clusters: {sorted(clustered_df['Class'].unique())}")

        return True

    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Export Clustered Data for Streamlit App")
    print("=" * 60)
    print("\nThis script should be run from within the Jupyter notebook.")
    print("\nIn your notebook, after creating clustered_df, run:")
    print("\n```python")
    print("from export_data_for_app import export_clustered_data")
    print("export_clustered_data(clustered_df)")
    print("```")
    print("\nThen launch the Streamlit app:")
    print("```bash")
    print("streamlit run app.py")
    print("```")
    print("\n" + "=" * 60)
