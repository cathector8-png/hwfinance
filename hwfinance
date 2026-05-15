#!/usr/bin/env python3
import sys
import argparse
import json
import urllib.request
import urllib.parse
import re
import random
import yfinance as yf

# Visual Shell Anchors (ANSI Colors)
C_GREEN = "\033[1;32m"
C_CYAN = "\033[1;36m"
C_WHITE = "\033[1;37m"
C_BOLD = "\033[1m"
C_YELLOW = "\033[1;33m"
C_RED = "\033[1;31m"
C_RESET = "\033[0m"

CURRENCY_SYMBOLS = {
    'USD': '$', 'EUR': '€', 'GBP': '£', 'GBX': '£', 'GBp': '£',
    'JPY': '¥', 'CAD': 'C$', 'AUD': 'A$', 'INR': '₹', 'HKD': 'HK$',
    'CHF': 'CHF', 'CNY': '元', 'SGD': 'S$', 'KRW': '₩', 'BRL': 'R$'
}

def print_custom_help():
    """Renders a comprehensive terminal help matrix detailing syntax, format rules, and capabilities."""
    print(f"\n{C_GREEN}+-----------------------------------------------------------------------+")
    print(f"|                       {C_BOLD}REFINANCE - CLI ENGINE MANUAL{C_RESET}{C_GREEN}                           |")
    print(f"|                       made by hector wakim                            |")
    print(f"+-----------------------------------------------------------------------+{C_RESET}")
    print(f"\n{C_BOLD}USAGE SNTX:{C_RESET}")
    print(f"  hwfinance <ticker> [flags]")
    print(f"  hwfinance --help")
    
    print(f"\n{C_BOLD}GLOBAL CAPABILITIES & OPERATIONS:{C_RESET}")
    print(f"  {C_CYAN}--pull <option>{C_RESET}  Extract live market data points directly.")
    print(f"                 Options: {C_WHITE}all, stock-price, market-cap, dividend-yield, total-debt{C_RESET}")
    print(f"  {C_CYAN}--calc <option>{C_RESET}  Execute corporate finance logic valuation formulas.")
    print(f"                 Options: {C_WHITE}all, fcf, dcf, ev, fcf-yield{C_RESET}")
    print(f"  {C_CYAN}--base <ISO>{C_RESET}     Override asset currency. Auto-converts to target index.")
    print(f"                 Examples: {C_WHITE}--base USD, --base EUR, --base GBP{C_RESET}")
    
    print(f"\n{C_BOLD}INTERNATIONAL TICKER SYNTAX GUIDE:{C_RESET}")
    print(f"  To analyze international equities accurately, append the regional market suffix:")
    print(f"  • {C_GREEN}US Markets (NASDAQ, NYSE):{C_RESET} Direct symbol without suffix ({C_WHITE}AAPL, TSLA, JPM{C_RESET})")
    print(f"  • {C_GREEN}London Stock Exchange (LSE):{C_RESET} Append '.L' suffix ({C_WHITE}BP.L, LLOY.L, AZN.L{C_RESET})")
    print(f"  • {C_GREEN}Tokyo Stock Exchange (TSE):{C_RESET} Append '.T' suffix ({C_WHITE}7203.T, 9984.T{C_RESET})")
    print(f"  • {C_GREEN}Frankfurt Stock Exchange (DAX):{C_RESET} Append '.DE' or '.F' suffix ({C_WHITE}SAP.DE, BMW.DE{C_RESET})")
    print(f"  • {C_GREEN}Toronto Stock Exchange (TSX):{C_RESET} Append '.TO' suffix ({C_WHITE}SHOP.TO, RY.TO{C_RESET})")
    
    print(f"\n{C_BOLD}SYSTEM FAILSAFE PROTECTION MECHANISMS:{C_RESET}")
    print(f"  • {C_YELLOW}Automatic Currency Normalisation:{C_RESET} Automatically scales UK assets out of Pence (GBX) to Pounds (GBP).")
    print(f"  • {C_YELLOW}Zero-Key API Fallback Handler:{C_RESET} Bypasses credential rate limits via secondary unauthenticated endpoints.")
    print(f"  • {C_YELLOW}Active IP Proxy Rotation Core:{C_RESET} Changes network footprints on fallback errors to prevent terminal bans.")
    
    print(f"\n{C_BOLD}EXAMPLES OF CORRECT COMMANDS:{C_RESET}")
    print(f"  hwfinance AAPL --pull all                     {C_GREEN}# Pull everything for Apple in USD{C_RESET}")
    print(f"  hwfinance BARC.L --calc all                   {C_GREEN}# Compute complex calculations for Barclays in GBP{C_RESET}")
    print(f"  hwfinance 7203.T --pull stock-price --base EUR {C_GREEN}# Get Toyota price converted to Euros{C_RESET}")
    print(f"{C_GREEN}+-----------------------------------------------------------------------+{C_RESET}\n")

class CustomArgumentParser(argparse.ArgumentParser):
    """Intercepts standard argument errors to force the output of our custom terminal help manual."""
    def error(self, message):
        print(f"\n{C_RED}{C_BOLD}SYNTAX ERROR DETECTED:{C_RESET} {message}")
        print_custom_help()
        sys.exit(2)

def get_free_proxy_list():
    try:
        url = "proxyscrape.com"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            proxies = response.read().decode('utf-8').strip().split('\r\n')
            if not proxies or len(proxies) < 5:
                url_b = "proxy-list.download"
                req_b = urllib.request.Request(url_b, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_b, timeout=5) as res_b:
                    proxies = res_b.read().decode('utf-8').strip().split('\r\n')
            return [p for p in proxies if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', p)]
    except:
        return []

def query_public_fallback(ticker_symbol):
    symbol_clean = ticker_symbol.upper()
    url = f"yahoo.com{symbol_clean}?interval=1d&range=1d"
    proxies = get_free_proxy_list()
    random.shuffle(proxies)
    
    for proxy in proxies[:5]:
        try:
            proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_handler)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux)'})
            with opener.open(req, timeout=4) as response:
                json_data = json.loads(response.read().decode())
                meta = json_data['chart']['result']['meta']
                return {
                    "price": float(meta.get('regularMarketPrice', 0.0)),
                    "market_cap": 0.0, "dividend_yield": 0.0, "total_debt": 0.0, "cash": 0.0, "fcf": 0.0,
                    "currency": meta.get('currency', 'USD'), "proxy_used": proxy
                }
        except:
            continue
    raise ValueError("All IP proxy rotation channels failed to resolve endpoint.")

def get_open_fx_rate(source_currency, target_currency):
    if source_currency == target_currency:
        return 1.0
    src = "GBP" if source_currency in ["GBX", "GBp"] else source_currency
    tgt = "GBP" if target_currency in ["GBX", "GBp"] else target_currency
    if src == tgt:
        return 1.0
    try:
        fx = yf.Ticker(f"{src}{tgt}=X".upper())
        rate = fx.fast_info.get('last_price') or fx.info.get('previousClose')
        if rate: return float(rate)
    except:
        pass
    return 1.0

def get_ticker_data(ticker_symbol, base_currency=None):
    ticker_symbol = ticker_symbol.upper()
    used_fallback = False
    proxy_info = None
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        fast_info = ticker.fast_info
        cashflow = ticker.cashflow
        
        if not info or 'currency' not in info:
            raise ValueError("Primary endpoint parsing timeout.")
            
        raw_price = fast_info.get('last_price') or info.get('currentPrice') or 0.0
        raw_market_cap = fast_info.get('market_cap') or info.get('marketCap') or 0.0
        div_yield = info.get('dividendYield') or 0.0
        raw_total_debt = info.get('totalDebt') or 0.0
        raw_cash = info.get('totalCash') or 0.0
        native_currency = info.get('currency', 'USD')
        
        raw_fcf = 0.0
        if not cashflow.empty:
            ocf = cashflow.get('Operating Cash Flow') or cashflow.get('Total Cash From Operating Activities')
            capex = cashflow.get('Capital Expenditures') or cashflow.get('Total Cash From Investing Activities')
            if ocf is not None and capex is not None:
                raw_fcf = float(ocf.iloc + capex.iloc)
                
    except Exception as e:
        try:
            fallback_data = query_public_fallback(ticker_symbol)
            raw_price = fallback_data["price"]
            raw_market_cap = fallback_data["market_cap"]
            div_yield = fallback_data["dividend_yield"]
            raw_total_debt = fallback_data["total_debt"]
            raw_cash = fallback_data["cash"]
            raw_fcf = fallback_data["fcf"]
            native_currency = fallback_data["currency"]
            proxy_info = fallback_data["proxy_used"]
            used_fallback = True
        except Exception as fallback_error:
            print(f"{C_YELLOW}Primary Engine Failure:{C_RESET} {e}")
            print(f"{C_YELLOW}Public Proxy Engine Failure:{C_RESET} {fallback_error}")
            sys.exit(1)

    if native_currency in ['GBp', 'GBX']:
        if raw_price > 10.0: raw_price /= 100.0
        raw_market_cap /= 100.0; raw_total_debt /= 100.0; raw_cash /= 100.0; raw_fcf /= 100.0
        native_currency = 'GBP'

    target_curr = base_currency.upper() if base_currency else native_currency
    fx_rate = get_open_fx_rate(native_currency, target_curr)
    
    return {
        "symbol": ticker_symbol,
        "price": float(raw_price * fx_rate), "market_cap": float(raw_market_cap * fx_rate),
        "dividend_yield": float(div_yield), "total_debt": float(raw_total_debt * fx_rate),
        "cash": float(raw_cash * fx_rate), "fcf": float(raw_fcf * fx_rate),
        "currency_symbol": CURRENCY_SYMBOLS.get(target_curr, f"{target_curr} "),
        "native_currency": native_currency, "display_currency": target_curr,
        "fallback_triggered": used_fallback, "proxy_used": proxy_info
    }

def print_table_header(title, symbol, currency, fallback_triggered, proxy_used):
    provider_status = f"{C_YELLOW}Proxy: {proxy_used}{C_RESET}" if fallback_triggered else f"{C_CYAN}[yFinance Direct]{C_RESET}"
    print(f"\n{C_GREEN}+-----------------------------------------------------------+{C_RESET}")
    print(f"{C_GREEN}| {C_BOLD}{title:<32}{C_RESET}{C_GREEN} | Ticker: {C_CYAN}{symbol:<8}{C_RESET}{C_GREEN} | Unit: {C_CYAN}{currency:<3}{C_RESET}{C_GREEN} |{C_RESET}")
    print(f"{C_GREEN}| {C_WHITE}made by hector wakim{C_RESET:<38}{C_GREEN} | Net IP: {provider_status:<22} {C_GREEN}|{C_RESET}")
    print(f"{C_GREEN}+-------------------------------------+---------------------+{C_RESET}")

def print_table_row(label, value_str):
    print(f"{C_GREEN}|{C_RESET} {label:<35} {C_GREEN}|{C_RESET} {C_WHITE}{value_str:>19}{C_RESET} {C_GREEN}|{C_RESET}")

def print_table_footer():
    print(f"{C_GREEN}+-------------------------------------+---------------------+{C_RESET}\n")

def handle_pull(args, data):
    print_table_header("REFINANCE", data['symbol'], data['display_currency'], data['fallback_triggered'], data['proxy_used'])
    show_all = (args.pull == 'all')
    cs = data['currency_symbol']
    if show_all or args.pull == 'stock-price': print_table_row("Stock Price", f"{cs}{data['price']:,.2f}")
    if show_all or args.pull == 'market-cap': print_table_row("Market Capitalisation", f"{cs}{data['market_cap']:,.0f}")
    if show_all or args.pull == 'dividend-yield': print_table_row("Dividend Yield", f"{data['dividend_yield'] * 100:.2f}%")
    if show_all or args.pull == 'total-debt': print_table_row("Total Balance Sheet Debt", f"{cs}{data['total_debt']:,.0f}")
    print_table_footer()

def handle_calc(args, data):
    print_table_header("REFINANCE", data['symbol'], data['display_currency'], data['fallback_triggered'], data['proxy_used'])
    show_all = (args.calc == 'all')
    cs = data['currency_symbol']
    
    ev = data['market_cap'] + data['total_debt'] - data['cash']
    fcf_yield = (data['fcf'] / data['market_cap']) if data['market_cap'] > 0 else 0.0
    
    discount_rate, growth_rate = 0.10, 0.03
    present_value_fcf = 0.0
    projected_fcf = data['fcf']
    for year in range(1, 6):
        projected_fcf *= (1 + growth_rate)
        present_value_fcf += projected_fcf / ((1 + discount_rate) ** year)
    terminal_value = (projected_fcf * (1 + growth_rate)) / (discount_rate - growth_rate)
    dcf_intrinsic_value = present_value_fcf + (terminal_value / ((1 + discount_rate) ** 5))

    if show_all or args.calc == 'fcf': print_table_row("Free Cash Flow (FCF)", f"{cs}{data['fcf']:,.0f}")
    if show_all or args.calc == 'ev': print_table_row("Enterprise Value (EV)", f"{cs}{ev:,.0f}")
    if show_all or args.calc == 'fcf-yield': print_table_row("Free Cash Flow Yield", f"{fcf_yield * 100:.2f}%")
    if show_all or args.calc == 'dcf': print_table_row("DCF Intrinsic Market Value", f"{cs}{dcf_intrinsic_value:,.0f}")
    print_table_footer()

def main():
    # Use custom error parser to trap all wrong syntax entries 
    parser = CustomArgumentParser(description="Global Linux Terminal Financial Command Engine", add_help=False)
    
    # Enable common help flags
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("ticker", nargs="?", help="Global stock exchange symbol token")
    parser.add_argument("--base", help="Target currency override ISO code")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--pull", choices=['all', 'market-cap', 'stock-price', 'dividend-yield', 'total-debt'])
    group.add_argument("--calc", choices=['all', 'fcf', 'dcf', 'ev', 'fcf-yield'])

    args = parser.parse_args()

    # Trigger help page manually or on missing parameters
    if args.help or not args.ticker or (not args.pull and not args.calc):
        print_custom_help()
        sys.exit(0)

    data = get_ticker_data(args.ticker, args.base)
    if args.pull:
        handle_pull(args, data)
    elif args.calc:
        handle_calc(args, data)

if __name__ == "__main__":
    main()
            
