I am working on adding it to linux as a package,

The command to install it will be:
    sudo apt install hwfinance 
For help enter hwfinance --help


[![Platform: Linux](https://shields.io)](https://linux.org)
[![Language: Python 3](https://shields.io)](https://python.org)

> **hwfinance** is a high-density, zero-key command-line financial analysis engine built natively for Linux. Query live pricing data, structural balance sheet metrics, and evaluate valuation modeling matrices across global exchanges instantly.

*Made by Hector Wakim*

---

## 🚀 Key Capabilities

*   **Multi-Exchange Engine:** Cross-resolves equities natively across **NASDAQ, NYSE, LSE, TSE, DAX, TSX, ASX, NSE, and Euronext**.
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

##  Terminal Action Examples

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

---

