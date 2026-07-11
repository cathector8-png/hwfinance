#!/usr/bin/env julia

function parse_float(value::String, default::Float64 = 0.0)::Float64
    try
        return parse(Float64, value)
    catch
        return default
    end
end

function parse_args(args)::Dict{String, String}
    parsed = Dict{String, String}()
    i = 1
    while i <= length(args)
        arg = args[i]
        if startswith(arg, "--")
            if occursin("=", arg)
                key, value = split(arg, "=", limit=2)
                parsed[key] = value
                i += 1
            elseif i < length(args) && !startswith(args[i + 1], "--")
                parsed[arg] = args[i + 1]
                i += 2
            else
                parsed[arg] = ""
                i += 1
            end
        else
            i += 1
        end
    end
    return parsed
end

function compute_metrics(parsed)::Dict{String, Any}
    market_cap = parse_float(get(parsed, "--market_cap", "0"), 0.0)
    total_debt = parse_float(get(parsed, "--total_debt", "0"), 0.0)
    cash = parse_float(get(parsed, "--cash", "0"), 0.0)
    fcf = parse_float(get(parsed, "--fcf", "0"), 0.0)
    ebitda = parse_float(get(parsed, "--ebitda", "0"), 0.0)
    beta = parse_float(get(parsed, "--beta", "1"), 1.0)
    revenue_growth = parse_float(get(parsed, "--revenue_growth", "0.03"), 0.03)
    shares_outstanding = parse_float(get(parsed, "--shares_outstanding", "1"), 1.0)

    ev = market_cap + total_debt - cash
    net_debt = total_debt - cash
    fcf_yield = market_cap > 0.0 ? (fcf / market_cap) : 0.0
    p_fcf = fcf > 0.0 ? (market_cap / fcf) : 0.0
    ev_ebitda = ebitda > 0.0 ? (ev / ebitda) : 0.0
    nd_ebitda = ebitda > 0.0 ? (net_debt / ebitda) : 0.0

    rf = 0.040
    erp = 0.055
    discount_rate = max(0.05, min(rf + (beta * erp), 0.15))

    present_value_fcf = 0.0
    projected_fcf = fcf
    high_growth = revenue_growth
    terminal_growth = 0.025

    for year in 1:5
        projected_fcf *= (1.0 + high_growth)
        present_value_fcf += projected_fcf / ((1.0 + discount_rate) ^ year)
    end

    current_growth = high_growth
    for year in 6:10
        current_growth -= (high_growth - terminal_growth) / 5.0
        projected_fcf *= (1.0 + current_growth)
        present_value_fcf += projected_fcf / ((1.0 + discount_rate) ^ year)
    end

    terminal_value = (projected_fcf * (1.0 + terminal_growth)) / (discount_rate - terminal_growth)
    terminal_value_pv = terminal_value / ((1.0 + discount_rate) ^ 10)

    dcf_enterprise_value = present_value_fcf + terminal_value_pv
    dcf_equity_value = dcf_enterprise_value - total_debt + cash
    shares = shares_outstanding > 0.0 ? shares_outstanding : 1.0
    intrinsic_value_per_share = max(0.0, dcf_equity_value / shares)

    wacc = discount_rate
    terminal_value = terminal_value
    sensitivity = Dict(
        "discount_rate" => discount_rate,
        "high_growth" => high_growth,
        "terminal_growth" => terminal_growth,
        "intrinsic_value_per_share" => intrinsic_value_per_share,
    )

    return Dict(
        "enterprise_value" => ev,
        "net_debt" => net_debt,
        "fcf_yield" => fcf_yield,
        "price_to_fcf" => p_fcf,
        "ev_ebitda" => ev_ebitda,
        "net_debt_ebitda" => nd_ebitda,
        "capm_discount_rate" => discount_rate,
        "wacc" => wacc,
        "dcf_enterprise_value" => dcf_enterprise_value,
        "terminal_value" => terminal_value,
        "intrinsic_value_per_share" => intrinsic_value_per_share,
        "sensitivity" => sensitivity,
    )
end

function emit_json(payload::Dict{String, Any})
    symbol = get(payload, "symbol", "")
    cleaned_symbol = replace(symbol, "\"" => "\\\"")
    print("{\"symbol\":\"$cleaned_symbol\"")
    for (key, value) in payload
        if key == "symbol"
            continue
        end
        if isa(value, AbstractFloat)
            print(",\"$key\":" * string(value))
        else
            print(",\"$key\":\"" * replace(string(value), "\"" => "\\\"") * "\"")
        end
    end
    println("}")
end

function main()
    parsed = parse_args(ARGS)
    symbol = get(parsed, "--symbol", "")
    payload = compute_metrics(parsed)
    payload["symbol"] = symbol
    emit_json(payload)
end

main()
