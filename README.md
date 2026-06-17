# hwfinance 

[![Platform: Linux](https://img.shields.io/badge/Platform-Linux-blue.svg)](https://linux.org)
[![Language: Python 3](https://img.shields.io/badge/Language-Python%203-yellow.svg)](https://python.org)
[![Engine: yFinance](https://img.shields.io/badge/Engine-yFinance-green.svg)](https://github.com/ranarousset/yfinance)

**hwfinance** is a high-density, zero-key command-line financial analysis engine built natively for Linux. Query live pricing data, structural balance sheet metrics, and evaluate valuation modeling matrices across global exchanges instantly.

*Created by Hector Wakim*

---

## Key Capabilities

*   **Multi-Exchange Engine:** Cross-resolves equities natively across **NASDAQ, NYSE, LSE, TSE, DAX, TSX, ASX, NSE, and Euronext**.
*   **High-Fidelity Charting:** Render professional line and candlestick charts with volume and moving averages (MA20, MA50) using `mplfinance`.
*   **Integrated Trading:** Submit live or paper trades via the **Alpaca Trade API** integration.
*   **Zero-Key API Fallback:** Bypasses external subscription keys and rate limits by shifting to unauthenticated backup endpoints using active IP proxy rotation.
*   **Automatic UK Normalisation:** Detects London Stock Exchange (LSE) penny structures (`GBX`/`GBp`) and auto-scales them to standard Pounds (`GBP`).
*   **Cross-Border FX Layer:** Pass any currency flag (`--base EUR`) to calculate and normalize foreign equities into your home currency profile.
*   **Pipeline Ready:** Output raw program state as JSON for seamless integration with other CLI tools.

---

## Installation

Install globally using `npm`:

```bash
npm install -g hwfinance
```

---

##  Command Matrix & Operational Syntax

### Execution Pattern
```bash
hwfinance <ticker> [flags]
```

### Parameters

| Flag | Accepted Fields | Functional Output |
| :--- | :--- | :--- |
| `--pull` | `all`, `stock-price`, `market-cap`, `dividend-yield`, `total-debt` | Returns immediate, live fundamental asset sheets. |
| `--calc` | `all`, `fcf`, `ev`, `fcf-yield`, `multiples`, `dcf` | Computes complex, forward-looking valuation equations. |
| `--chart` | Period (e.g., `1d`, `1mo`, `1y`) | Renders a window-based line chart. |
| `--candle` | Period (e.g., `1d`, `1mo`, `1y`) | Renders a window-based candlestick chart. |
| `--interval` | `1m`, `5m`, `1h`, `1d`, etc. | Sets the data granularity for charts. |
| `--order` | `buy`, `sell` | Initiates a stock order via Alpaca. |
| `--qty` | Number | Specifies share quantity for an order. |
| `--type` | `market`, `limit` | Sets order type (Default: `market`). |
| `--price` | Number | Sets limit price for limit orders. |
| `--config` | `set`, `get`, `delete` | Manages local API keys and settings. |
| `--base` | ISO Code (`USD`, `EUR`, `GBP`, etc.) | Triggers active FX conversion of all output parameters. |
| `--json` | None | Outputs raw data as JSON for automation. |
| `--help` | None | Displays the interactive script manual. |

### Global Ticker Notation Rules

| Market | Suffix | Example |
| :--- | :--- | :--- |
| **US (NASDAQ/NYSE)** | None | `AAPL`, `TSLA`, `NVDA` |
| **London (LSE)** | `.L` | `BP.L`, `LLOY.L`, `VOD.L` |
| **Tokyo (TSE)** | `.T` | `7203.T`, `9984.T` |
| **Frankfurt (DAX)** | `.DE` | `SAP.DE`, `BMW.DE` |
| **Toronto (TSX)** | `.TO` | `SHOP.TO` |

---

## ⚙️ Configuration (Trading Setup)

To enable trading features, configure your Alpaca API credentials:

```bash
hwfinance --config set alpaca_key <YOUR_ALPACA_KEY>
hwfinance --config set alpaca_secret <YOUR_ALPACA_SECRET>
# Optional: Set base URL (defaults to paper trading)
hwfinance --config set alpaca_base_url https://api.alpaca.markets 
```

---

##  Terminal Action Examples

**Visualisation:**
```bash
# Render a 1-month line chart for NVIDIA
hwfinance NVDA --chart 1mo

# Render 5-minute interval candles for Tesla
hwfinance TSLA --candle 1d --interval 5m
```

**Financial Analysis:**
```bash
# Pull complete fundamental profile for Apple
hwfinance AAPL --pull all

# Evaluate Enterprise Value and DCF for Barclays (LSE)
hwfinance BARC.L --calc all

# Query Toyota (TSE) with automatic conversion to Euros
hwfinance 7203.T --pull stock-price --base EUR
```

**Executing Orders:**
```bash
# Buy 10 shares of Apple at market price
hwfinance AAPL --order buy --qty 10

# Sell 5 shares of Microsoft with a limit price of $400
hwfinance MSFT --order sell --qty 5 --type limit --price 400
```

**Advanced Pipeline Integration:**
```bash
# Pipe JSON output to jq for custom parsing
hwfinance MSFT --pull all --json | jq '.price'
```

---

##  License
idgaf what you do with this, i use gpl license 2 or 3, contact me at cat.hector8@gmail for any demands
