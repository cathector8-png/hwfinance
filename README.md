# hwfinance 📈

[![Platform: Linux](https://img.shields.io/badge/Platform-Linux-blue.svg)](https://linux.org)
[![Language: Python 3](https://img.shields.io/badge/Language-Python%203-yellow.svg)](https://python.org)
[![Engine: yFinance](https://img.shields.io/badge/Engine-yFinance-green.svg)](https://github.com/ranarousset/yfinance)

**hwfinance** is a high-density, zero-key command-line financial analysis engine built natively for Linux. Query live pricing data, structural balance sheet metrics, and evaluate valuation modeling matrices across global exchanges instantly.

*Created by Hector Wakim*

---

## 🚀 Key Capabilities

*   **Multi-Exchange Engine:** Cross-resolves equities natively across **NASDAQ, NYSE, LSE, TSE, DAX, TSX, ASX, NSE, and Euronext**.
*   **Multi-Ticker Comparison:** Analyse multiple stocks in a single command with a unified comparison table.
*   **High-Fidelity Charting:** Render professional line and candlestick charts with volume and moving averages (MA20, MA50) using `mplfinance`.
*   **Headless ASCII Charting:** Render Unicode-based line and candlestick charts directly in the terminal — no GUI or X11 needed. Activates automatically in SSH/headless environments.
*   **Interactive REPL Shell:** Launch a persistent `hwfinance>` prompt to run multiple queries without startup overhead.
*   **Integrated Trading:** Submit live or paper trades via the **Alpaca Trade API** integration, with an interactive confirmation guard before any order is placed.
*   **Portfolio & Account View:** Inspect all open positions, unrealized P&L, account equity, cash, and buying power directly from Alpaca.
*   **Flexible Output Formats:** Export data as `table`, `csv`, `tsv`, or `markdown` for pipelines and documents.
*   **Fuzzy Ticker Search:** If a ticker fails to resolve, hwfinance searches Yahoo Finance and presents a numbered list of candidates to pick from.
*   **Environment Variable Credentials:** Reads standard Alpaca env vars (`APCA_API_KEY_ID`, `APCA_API_SECRET_KEY`) in addition to the config file.
*   **Zero-Key API Fallback:** Bypasses external subscription keys and rate limits by shifting to unauthenticated backup endpoints using active IP proxy rotation.
*   **Automatic UK Normalisation:** Detects London Stock Exchange (LSE) penny structures (`GBX`/`GBp`) and auto-scales them to standard Pounds (`GBP`).
*   **Cross-Border FX Layer:** Pass any currency flag (`--base EUR`) to calculate and normalize foreign equities into your home currency profile.
*   **Pipeline Ready:** Output raw program state as JSON for seamless integration with other CLI tools.

---

## 🛠️ Installation

Install globally using `npm`:

```bash
npm install -g hwfinance
```

---

## 🕹️ Command Matrix & Operational Syntax

### Execution Pattern
```bash
hwfinance <ticker(s)> [flags]
```

### Parameters

| Flag | Accepted Fields | Functional Output |
| :--- | :--- | :--- |
| `--pull` | `all`, `stock-price`, `market-cap`, `dividend-yield`, `total-debt` | Returns immediate, live fundamental asset sheets. |
| `--calc` | `all`, `fcf`, `ev`, `fcf-yield`, `multiples`, `dcf` | Computes complex, forward-looking valuation equations. |
| `--chart` | Period (e.g., `1d`, `1mo`, `1y`) | Renders a window-based line chart. |
| `--candle` | Period (e.g., `1d`, `1mo`, `1y`) | Renders a window-based candlestick chart. |
| `--interval` | `1m`, `5m`, `1h`, `1d`, etc. | Sets the data granularity for charts. |
| `-t`, `--text-chart` | None | Forces terminal-based ASCII/Unicode chart rendering. Auto-activates if `DISPLAY` is unset. |
| `-f`, `--format` | `table`, `csv`, `tsv`, `markdown` | Sets the tabular output format (default: `table`). |
| `--order` | `buy`, `sell` | Initiates a stock order via Alpaca (with confirmation prompt). |
| `--qty` | Number | Specifies share quantity for an order. |
| `--type` | `market`, `limit` | Sets order type (Default: `market`). |
| `--price` | Number | Sets limit price for limit orders. |
| `-y`, `--yes` | None | Bypasses the interactive order confirmation prompt (for scripts). |
| `--portfolio` | None | Displays all open Alpaca positions with unrealized P&L. |
| `--account` | None | Displays account equity, cash, buying power, and daily P&L. |
| `--config` | `set`, `get`, `delete` | Manages local API keys and settings. |
| `--base` | ISO Code (`USD`, `EUR`, `GBP`, etc.) | Triggers active FX conversion of all output parameters. |
| `--json` | None | Outputs raw data as JSON for automation. |
| `-i`, `--shell` | None | Launches an interactive financial command REPL shell. |
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

### Option 1: Environment Variables (Recommended for scripts & CI)

```bash
export APCA_API_KEY_ID=<YOUR_ALPACA_KEY>
export APCA_API_SECRET_KEY=<YOUR_ALPACA_SECRET>
export APCA_API_BASE_URL=https://api.alpaca.markets  # omit for paper trading
```

### Option 2: Config File

```bash
hwfinance --config set alpaca_key <YOUR_ALPACA_KEY>
hwfinance --config set alpaca_secret <YOUR_ALPACA_SECRET>
# Optional: Set base URL (defaults to paper trading)
hwfinance --config set alpaca_base_url https://api.alpaca.markets
```

Environment variables always take precedence over the config file.

---

## 📖 Terminal Action Examples

### Multi-Ticker Comparison
```bash
# Compare price, market cap, and yield for three stocks at once
hwfinance AAPL MSFT NVDA --pull all

# Compare valuations across multiple tickers
hwfinance AAPL TSLA GOOGL --calc multiples

# Read tickers from stdin
echo "AAPL MSFT TSLA" | hwfinance --pull stock-price
```

### Output Format Exports
```bash
# Export a comparison table as CSV
hwfinance AAPL MSFT --pull all --format csv > prices.csv

# Generate a markdown table for pasting into a doc
hwfinance AAPL MSFT NVDA --calc multiples --format markdown

# Tab-separated for spreadsheet import
hwfinance AAPL MSFT --pull all --format tsv
```

### Visualisation
```bash
# Render a 1-month line chart for NVIDIA (GUI)
hwfinance NVDA --chart 1mo

# Render 5-minute interval candles for Tesla (GUI)
hwfinance TSLA --candle 1d --interval 5m

# Force terminal-based ASCII chart (works over SSH / headless)
hwfinance AAPL --chart 1mo -t

# Terminal-based candlestick chart
hwfinance AAPL --candle 1mo -t
```

### Financial Analysis
```bash
# Pull complete fundamental profile for Apple
hwfinance AAPL --pull all

# Evaluate Enterprise Value and DCF for Barclays (LSE)
hwfinance BARC.L --calc all

# Query Toyota (TSE) with automatic conversion to Euros
hwfinance 7203.T --pull stock-price --base EUR
```

### Executing Orders
```bash
# Buy 10 shares of Apple at market price (shows confirmation prompt)
hwfinance AAPL --order buy --qty 10

# Sell 5 shares of Microsoft with a limit price of $400
hwfinance MSFT --order sell --qty 5 --type limit --price 400

# Skip the confirmation prompt for use in scripts
hwfinance AAPL --order buy --qty 10 -y
```

### Portfolio & Account
```bash
# View all open positions with unrealized P&L
hwfinance --portfolio

# View account equity, cash, and buying power
hwfinance --account

# View both together
hwfinance --portfolio --account
```

### Interactive REPL Shell
```bash
# Launch the persistent interactive shell
hwfinance --shell
# or
hwfinance -i
# or simply run hwfinance with no arguments in an interactive terminal

# Inside the shell:
# hwfinance> AAPL --pull all
# hwfinance> MSFT TSLA --calc multiples --format markdown
# hwfinance> help
# hwfinance> exit
```

### Advanced Pipeline Integration
```bash
# Pipe JSON output to jq for custom parsing
hwfinance MSFT --pull all --json | jq '.price'

# Multi-ticker JSON array output
hwfinance AAPL MSFT --pull all --json | jq '.[].price'
```

---

## 🛡️ License
Distributed under the GPL-3.0 License. See `LICENSE` for more information.
