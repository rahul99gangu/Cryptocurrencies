# Cryptocurrency Data Sources

## Overview
This project uses multiple cryptocurrency datasets to provide comprehensive analysis from historical to current market trends.

## Dataset Files

### 1. `crypto_data.csv` (Original Dataset - ~2018)
**Source:** Historical cryptocurrency data
**Size:** 1,252 cryptocurrencies
**Tradable after filtering:** 532 coins
**Time Period:** Approximately 2017-2018

**Key Characteristics:**
- Contains older cryptocurrencies and many defunct projects
- Algorithms: Scrypt, X11, SHA-256, Ethash (PoW), X13, etc.
- Proof Types: PoW, PoW/PoS hybrid systems
- Ethereum still listed as Proof-of-Work

**Notable Coins Included:**
- Bitcoin (BTC)
- Ethereum (ETH) - Pre-Merge
- Litecoin (LTC)
- Dash
- Monero (XMR)
- Ethereum Classic (ETC)
- ZCash (ZEC)

**Data Columns:**
- `CoinName`: Name of the cryptocurrency
- `Algorithm`: Mining/consensus algorithm
- `IsTrading`: Whether the coin is actively traded
- `ProofType`: Consensus mechanism type
- `TotalCoinsMined`: Current circulating supply
- `TotalCoinSupply`: Maximum supply (0 = unlimited)

---

### 2. `crypto_data_2025.csv` (Updated Dataset - 2024-2025)
**Source:** Curated from CoinGecko, CoinMarketCap, and official project documentation
**Size:** 100 cryptocurrencies
**Time Period:** October 2024 - Current
**Last Updated:** October 31, 2025

**Key Updates:**
- Modern consensus mechanisms (PoH, L2-PoS, Tendermint, Avalanche Consensus)
- Layer-2 scaling solutions (Arbitrum, Optimism, Starknet)
- AI-focused blockchain tokens
- Updated blockchain data post-Ethereum Merge (PoS)

**New Categories Included:**

#### Layer-1 Blockchains (2021-2024)
- Solana (SOL) - Proof-of-History
- Avalanche (AVAX) - Avalanche Consensus
- Sui (SUI) - Narwhal & Tusk consensus
- Aptos (APT) - AptosBFT
- Sei (SEI) - Optimized for DeFi
- Celestia (TIA) - Modular blockchain

#### Layer-2 Solutions
- Arbitrum (ARB) - Optimistic Rollup
- Optimism (OP) - Optimistic Rollup
- Starknet (STRK) - ZK-Rollup
- Immutable X (IMX) - StarkEx ZK-Rollup
- Polygon (MATIC) - Sidechain/L2

#### AI & Machine Learning Tokens (2023-2024 Trend)
- Fetch.ai (FET) - AI agents
- SingularityNET (AGIX) - AI marketplace
- Ocean Protocol (OCEAN) - Data marketplace
- Render (RNDR) - GPU rendering
- Bittensor (TAO) - Machine learning network

#### DeFi Ecosystem (Latest Protocols)
- GMX - Decentralized perpetuals (Arbitrum)
- Radiant Capital (RDNT) - Omnichain lending
- Pendle (PENDLE) - Yield trading
- Jupiter (JUP) - Solana DEX aggregator
- Jito (JTO) - Solana liquid staking

#### Trending Projects (2024)
- Worldcoin (WLD) - World ID
- Pyth Network (PYTH) - Oracle network
- Wormhole (W) - Cross-chain bridge
- Ethena (ENA) - Synthetic dollar
- Toncoin (TON) - Telegram blockchain
- Notcoin (NOT) - TON-based gaming

#### Meme Coins (2024 Cycle)
- Pepe (PEPE)
- Bonk (BONK)
- dogwifhat (WIF)

**Data Columns:** Same structure as original dataset
- `CoinName`: Name of the cryptocurrency
- `Algorithm`: Consensus mechanism/algorithm
- `IsTrading`: Trading status (all True)
- `ProofType`: Modern proof types (PoS, PoH, L2-PoS, etc.)
- `TotalCoinsMined`: Current circulating supply
- `TotalCoinSupply`: Maximum supply

---

## Data Collection Methodology (2025 Dataset)

### Sources
1. **CoinGecko API** - Market data and token information
2. **CoinMarketCap** - Historical and current supply data
3. **Official Project Documentation** - Consensus mechanisms and technical specifications
4. **Blockchain Explorers** - On-chain supply verification

### Inclusion Criteria
- Market Cap: Top 500 cryptocurrencies by market cap
- Trading Volume: Active trading on major exchanges
- Network Activity: Regular on-chain transactions
- Innovation: Projects representing new trends (AI, L2, DeFi innovations)

### Data Accuracy
- Circulating supply data as of October 2024
- Maximum supply from official tokenomics
- Consensus mechanisms verified from official documentation
- All coins confirmed actively trading

---

## Key Differences Between Datasets

| Feature | crypto_data.csv (2018) | crypto_data_2025.csv (2025) |
|---------|------------------------|----------------------------|
| **Size** | 1,252 coins | 100 coins |
| **Ethereum** | PoW (Ethash) | PoS (Beacon Chain) |
| **Consensus Types** | Mainly PoW, PoS, PoW/PoS | PoH, L2-PoS, Tendermint, BFT variants |
| **Layer-2 Coverage** | None | Extensive (ARB, OP, STRK, IMX) |
| **AI Tokens** | None | FET, AGIX, OCEAN, RNDR, TAO |
| **Meme Coins** | Dogecoin era | 2024 cycle (PEPE, BONK, WIF) |
| **Dead Projects** | Many included | Filtered out |

---

## Using the Datasets

### For Historical Analysis
Use `crypto_data.csv` to:
- Analyze cryptocurrency evolution 2017-2018
- Study early blockchain algorithms
- Compare PoW era vs modern PoS era
- Research defunct projects and market dynamics

### For Current Market Analysis
Use `crypto_data_2025.csv` to:
- Analyze current market trends
- Study modern consensus mechanisms
- Explore AI and DeFi sectors
- Layer-2 scaling solutions analysis
- Current tokenomics and supply dynamics

### Combined Analysis
- Track how the cryptocurrency landscape has evolved
- Compare algorithm distribution across time periods
- Analyze the shift from PoW to PoS consensus
- Identify emerging trends and categories

---

## Data Updates

The `crypto_data_2025.csv` dataset should be updated quarterly to maintain accuracy:

**Update Schedule:**
- **Q1 2025:** January 31
- **Q2 2025:** April 30
- **Q3 2025:** July 31
- **Q4 2025:** October 31

**Update Process:**
1. Fetch latest market data from CoinGecko/CoinMarketCap APIs
2. Verify circulating supply from blockchain explorers
3. Add new projects above $100M market cap
4. Remove delisted or inactive projects
5. Update consensus mechanisms for upgraded networks
6. Document changes in CHANGELOG.md

---

## API Access (For Real-Time Data)

For real-time cryptocurrency data in production:

### CoinGecko API
- **Free Tier:** 30 calls/min, no API key required
- **Demo Plan:** 10,000 calls/month, $0
- **Analyst Plan:** $129/month, 500 calls/min
- **Docs:** https://www.coingecko.com/en/api/documentation

### CoinMarketCap API
- **Basic Plan:** $0 (limited endpoints)
- **Startup Plan:** $79/month, 14 endpoints with historical
- **Hobbyist Plan:** $99/month, 19 endpoints
- **Docs:** https://coinmarketcap.com/api/documentation/v1/

---

## Data License & Attribution

### Original Dataset (crypto_data.csv)
- **License:** Public domain / Educational use
- **Attribution:** Cryptocurrency community data compilation

### 2025 Dataset (crypto_data_2025.csv)
- **Source:** Aggregated from public blockchain data and market APIs
- **License:** MIT License (see LICENSE file)
- **Attribution:** Data compiled from CoinGecko, CoinMarketCap, and official project sources
- **Disclaimer:** For educational and portfolio demonstration purposes. Not financial advice.

---

## Contributing

To contribute updated cryptocurrency data:

1. **Fork the repository**
2. **Update crypto_data_2025.csv** with verified data
3. **Document sources** in your pull request
4. **Include verification** (blockchain explorer links)
5. **Submit pull request** with description of changes

---

## Contact & Questions

For questions about data sources or to report inaccuracies:
- **GitHub Issues:** https://github.com/rahul99gangu/Cryptocurrencies/issues
- **Label:** `data-quality` or `data-request`

---

**Last Updated:** October 31, 2025
**Next Scheduled Update:** January 31, 2026
