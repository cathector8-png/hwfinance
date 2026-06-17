### Installation (Debian/Kali/Ubuntu)
1. Add the repository:
   ```bash
   echo "deb [trusted=yes] [https://cathector8-png.github.io/hwfinance/repo/](https://cathector8-png.github.io/hwfinance/repo/) ./" | sudo tee /etc/apt/sources.list.d/hwfinance.list
   sudo apt update && sudo apt install hwfinance
   pip install yfinance pandas mplfinance alpaca-trade-api --break-system-packages


### 2. Manual Installation (Universal GNU/Linux)
This works on any Linux flavor (Arch, Fedora, etc.) because it doesn't rely on `apt`.

```markdown
### Universal Manual Install
1. Clone the repo:
   ```bash
   git clone https://github.com/cathector8-png/hwfinance.git
   cd hwfinance
   pip install -r Requirements
   chmod +x hwfinance
   sudo ln -s $(pwd)/hwfinance /usr/bin/hwfinance
   ```
For help enter:
```hwfinance --help```


[![Platform: Linux](https://shields.io)](https://linux.org)
[![Language: Python 3](https://shields.io)](https://python.org)

> **hwfinance** is a high-density, zero-key command-line financial analysis engine built natively for Linux. Query live pricing data, structural balance sheet metrics, and evaluate valuation modeling matrices across global exchanges instantly.

*Made by Hector Wakim*

---

## 🚀 Key Capabilities

*   **Multi-Exchange Engine:** Cross-resolves equities natively across **NASDAQ, NYSE, LSE, TSE, DAX, TSX, ASX, NSE, and Euronext**.
*   **High-Fidelity Charting:** Render professional line and candlestick charts with volume and moving averages (MA20, MA50) using `mplfinance`.
*   **Integrated Trading:** Submit live or paper trades via the **Alpaca Trade API** integration.
*   **Zero-Key API Fallback:** Bypasses external subscription keys and rate limits by shifting to unauthenticated backup endpoints.
*   **Active IP Proxy Rotation:** Randomizes your network footprint through public proxy lists if primary data streams get flagged.
*   **Automatic UK Normalisation:** Detects London Stock Exchange (LSE) penny structures (`GBX`/`GBp`) and auto-scales them to standard Pounds (`GBP`).
*   **Cross-Border FX Layer:** Pass any currency flag (`--base EUR`) to calculate and normalize foreign equities into your home currency profile.

---

##  Native Debian/Ubuntu Installation

To compile and build `hwfinance` as an integrated, native GNU/Linux package, execute the following commands in your shell:


```

---

## Command Matrix & Operational Syntax

### Execution Pattern
```bash
hwfinance <ticker> [flags]
```

### Flag Parameters


| Flag | Accepted Fields | Functional Output |
| :--- | :--- | :--- |
| `--pull` | `all`, `stock-price`, `market-cap`, `dividend-yield`, `total-debt` | Returns immediate, live fundamental asset sheets. |
| `--calc` | `all`, `fcf`, `ev`, `fcf-yield`, `dcf` | Computes complex, forward-looking valuation equations. |
| `--chart` | Period (e.g., `1d`, `1mo`, `1y`) | Renders a window-based line chart. |
| `--candle` | Period (e.g., `1d`, `1mo`, `1y`) | Renders a window-based candlestick chart. |
| `--interval` | `1m`, `5m`, `1h`, `1d`, etc. | Sets the data granularity for charts. |
| `--order` | `buy`, `sell` | Initiates a stock order via Alpaca. |
| `--qty` | Number | Specifies share quantity for an order. |
| `--config` | `set`, `get`, `delete` | Manages local API keys and settings. |
| `--base` | Any valid ISO string (`USD`, `EUR`, `GBP`, `JPY`, etc.) | Triggers active FX conversion of all output parameters. |
| `--help` | None | Overrides parser errors and displays the interactive script manual. |

### Global Ticker Notation Rules

To target different international indices, append your exchange string tokens using the following syntax structure:

*   **US Equities (NASDAQ / NYSE):** Clear input symbol directly \rightarrow `AAPL`, `TSLA`, `NVDA`
*   **London Stock Exchange (LSE):** Append `.L` \rightarrow `BP.L`, `LLOY.L`, `VOD.L`
*   **Tokyo Stock Exchange (TSE):** Append `.T` \rightarrow `7203.T`, `9984.T`
*   **Frankfurt Stock Exchange (DAX):** Append `.DE` \rightarrow `SAP.DE`, `BMW.DE`
*   **Toronto Stock Exchange (TSX):** Append `.TO` \rightarrow `SHOP.TO`

---

## 🛠️ Configuration (Trading Setup)

To use the trading features, you must configure your Alpaca API keys:

```bash
hwfinance --config set alpaca_key <YOUR_ALPACA_KEY>
hwfinance --config set alpaca_secret <YOUR_ALPACA_SECRET>
# Optional: Set base URL (defaults to paper trading)
hwfinance --config set alpaca_base_url https://api.alpaca.markets 
```

---

##  Terminal Action Examples

**Charting & Visualization:**
Render a 1-month line chart for NVIDIA:
```bash
hwfinance NVDA --chart 1mo
```

Render a 5-minute interval candlestick chart for Tesla for the last day:
```bash
hwfinance TSLA --candle 1d --interval 5m
```

**Financial Analysis:**
Pull a complete raw profile matrix for **Apple** in native US Dollars:
```bash
hwfinance AAPL --pull all
```

Evaluate advanced Enterprise Value and 5-Year DCF growth profiles for **Barclays Bank** in British Pounds:
```bash
hwfinance BARC.L --calc all
```

Query **Toyota's** stock price from the Tokyo Stock Exchange and automatically convert the metric to Euros (€):
```bash
hwfinance 7203.T --pull stock-price --base EUR
```

**Executing Orders:**
Buy 10 shares of Apple at market price:
```bash
hwfinance AAPL --order buy --qty 10
```

Sell 5 shares of Microsoft with a limit price of $400:
```bash
hwfinance MSFT --order sell --qty 5 --type limit --price 400
```

---

# hwtrading
