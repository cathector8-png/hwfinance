#!/usr/bin/env python3
import sys
import argparse
import yfinance as yf

# Visual Shell Anchors (ANSI Colors)
C_GREEN = "\033[1;32m"
C_CYAN = "\033[1;36m"
C_WHITE = "\033[1;37m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

CURRENCY_SYMBOLS = {
    'USD': '$', 'EUR': '€', 'GBP': '£', 'GBX': '£', 'GBp': '£',
    'JPY': '¥', 'CAD': 'C$', 'AUD': 'A$', 'INR': '₹', 'HKD': 'HK$',
    'CHF': 'CHF', 'CNY': '元', 'SGD': 'S$', 'KRW': '₩', 'BRL': 'R$'
}

def get_fx_rate(source_currency, target_currency):
    """Fetch real-time forex pairing indices via Yahoo Finance."""
    if source_currency == target_currency:
        return 1.0
    # Normalise UK pence indicators to standard Pounds
    src = "GBP" if source_currency in ["GBX", "GBp"] else source_currency
    tgt = "GBP" if target_currency in ["GBX", "GBp"] else target_currency
    if src == tgt:
        return 1.0
        
    pair = f"{src}{tgt}=X"
    try:
        fx = yf.Ticker(pair)
        rate = fx.fast_info.get('last_price') or fx.info.get('previousClose')
        if rate:
            return float(rate)
    except:
        pass
    return 1.0

def get_ticker_data(ticker_symbol, base_currency=None):
    """Fetch corporate metrics and execute currency translation mechanisms."""
    try:
        ticker_symbol = ticker_symbol.upper()
        ticker = yf.Ticker(ticker_symbol)
        
        info = ticker.info
        fast_info = ticker.fast_info
        cashflow = ticker.cashflow
        
        if not info or 'currency' not in info:
            raise ValueError(f"Ticker '{ticker_symbol}' returned incomplete global data profiles.")
            
        raw_price = fast_info.get('last_price') or info.get('currentPrice') or 0.0
        raw_market_cap = fast_info.get('market_cap') or info.get('marketCap') or 0.0
        div_yield = info.get('dividendYield') or 0.0
        raw_total_debt = info.get('totalDebt') or 0.0
        raw_cash = info.get('totalCash') or 0.0
        native_currency = info.get('currency', 'USD')
        
        # Pull Free Cash Flow metrics
        raw_fcf = 0.0
        if not cashflow.empty:
            ocf = cashflow.get('Operating Cash Flow') or cashflow.get('Total Cash From Operating Activities')
            capex = cashflow.get('Capital Expenditures') or cashflow.get('Total Cash From Investing Activities')
            if ocf is not None and capex is not None:
                raw_fcf = float(ocf.iloc[0] + capex.iloc[0])

        # UK Equities Normalization (Pence to Pounds conversion layer)
        if native_currency in ['GBp', 'GBX']:
            if raw_price > 10.0: raw_price /= 100.0
            raw_market_cap /= 100.0
            raw_total_debt /= 100.0
            raw_cash /= 100.0
            raw_fcf /= 100.0
            native_currency = 'GBP'

        # FX Valuation Matrix conversion
        target_curr = base_currency.upper() if base_currency else native_currency
        fx_rate = get_fx_rate(native_currency, target_curr) if base_currency else 1.0
        
        return {
            "symbol": ticker_symbol,
            "price": float(raw_price * (get_fx_rate(native_currency, target_curr) if base_currency else 1.0)),
            "market_cap": float(raw_market_cap * fx_rate),
            "dividend_yield": float(div_yield),
            "total_debt": float(raw_total_debt * fx_rate),
            "cash": float(raw_cash * fx_rate),
            "fcf": float(raw_fcf * fx_rate),
            "currency_symbol": CURRENCY_SYMBOLS.get(target_curr, f"{target_curr} "),
            "native_currency": native_currency,
            "display_currency": target_curr
        }
    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {e}")
        sys.exit(1)

def print_table_header(title, symbol, currency):
    print(f"\n{C_GREEN}+-----------------------------------------------------------+{C_RESET}")
    print(f"{C_GREEN}| {C_BOLD}{title:<32}{C_RESET}{C_GREEN} | Ticker: {C_CYAN}{symbol:<8}{C_RESET}{C_GREEN} | Unit: {C_CYAN}{currency:<3}{C_RESET}{C_GREEN} |{C_RESET}")
    print(f"{C_GREEN}+-------------------------------------+---------------------+{C_RESET}")

def print_table_row(label, value_str):
    print(f"{C_GREEN}|{C_RESET} {label:<35} {C_GREEN}|{C_RESET} {C_WHITE}{value_str:>19}{C_RESET} {C_GREEN}|{C_RESET}")

def print_table_footer():
    print(f"{C_GREEN}+-------------------------------------+---------------------+{C_RESET}\n")

def handle_pull(args, data):
    print_table_header("FINANCIAL DATA PROFILE", data['symbol'], data['display_currency'])
    show_all = (args.pull == 'all')
    cs = data['currency_symbol']
    
    if show_all or args.pull == 'stock-price':
        print_table_row("Stock Price", f"{cs}{data['price']:,.2f}")
    if show_all or args.pull == 'market-cap':
        print_table_row("Market Capitalisation", f"{cs}{data['market_cap']:,.0f}")
    if show_all or args.pull == 'dividend-yield':
        print_table_row("Dividend Yield", f"{data['dividend_yield'] * 100:.2f}%")
    if show_all or args.pull == 'total-debt':
        print_table_row("Total Balance Sheet Debt", f"{cs}{data['total_debt']:,.0f}")
    print_table_footer()

def handle_calc(args, data):
    print_table_header("VALUATION CALCULATIONS", data['symbol'], data['display_currency'])
    show_all = (args.calc == 'all')
    cs = data['currency_symbol']
    
    ev = data['market_cap'] + data['total_debt'] - data['cash']
    fcf_yield = (data['fcf'] / data['market_cap']) if data['market_cap'] > 0 else 0.0
    
    # 5-Year Intrinsic DCF Matrix
    discount_rate, growth_rate = 0.10, 0.03
    present_value_fcf = 0.0
    projected_fcf = data['fcf']
    for year in range(1, 6):
        projected_fcf *= (1 + growth_rate)
        present_value_fcf += projected_fcf / ((1 + discount_rate) ** year)
    terminal_value = (projected_fcf * (1 + growth_rate)) / (discount_rate - growth_rate)
    dcf_intrinsic_value = present_value_fcf + (terminal_value / ((1 + discount_rate) ** 5))

    if show_all or args.calc == 'fcf':
        print_table_row("Free Cash Flow (FCF)", f"{cs}{data['fcf']:,.0f}")
    if show_all or args.calc == 'ev':
        print_table_row("Enterprise Value (EV)", f"{cs}{ev:,.0f}")
    if show_all or args.calc == 'fcf-yield':
        print_table_row("Free Cash Flow Yield", f"{fcf_yield * 100:.2f}%")
    if show_all or args.calc == 'dcf':
        print_table_row("DCF Intrinsic Market Value", f"{cs}{dcf_intrinsic_value:,.0f}")
    print_table_footer()

def main():
    parser = argparse.ArgumentParser(description="Global Linux Terminal Financial Command Engine")
    parser.add_argument("ticker", help="Global stock exchange symbol token")
    parser.add_argument("--base", help="Target currency override ISO code (e.g. USD, EUR, GBP)")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pull", choices=['all', 'market-cap', 'stock-price', 'dividend-yield', 'total-debt'],
                        help="Fetch live global metrics")
    group.add_argument("--calc", choices=['all', 'fcf', 'dcf', 'ev', 'fcf-yield'],
                        help="Calculate analytical corporate valuation matrices")

    args = parser.parse_args()
    data = get_ticker_data(args.ticker, args.base)

    if args.pull:
        handle_pull(args, data)
    elif args.calc:
        handle_calc(args, data)

if __name__ == "__main__":
    main()
      
