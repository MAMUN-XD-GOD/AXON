from core.ocr import extract_ocr_data
from core.candle_extractor import extract_candles
from core.chart_cleaner import preprocess_chart

def analyze_chart(img):

    # Clean chart
    clean_img = preprocess_chart(img)

    # OCR data
    ocr_data = extract_ocr_data(clean_img)

    # Real candles
    candles = extract_candles(clean_img)

    if len(candles) < 20:
        return {
            "status": "error",
            "message": "Chart not clear enough to detect candles.",
            "engine": "phase 4"
        }

    # Convert to price array
    prices = [c[3] for c in candles]

    # Now reuse Phase 3 logic:
    highs, lows = find_swings(prices)
    structure, ms_bias = detect_structure(highs, lows)
    ob = detect_order_blocks(candles, ms_bias)
    fvg = detect_fvg(candles)
    liquidity = detect_liquidity(highs, lows, prices)
    final_bias = calculate_bias(structure, fvg, ob, liquidity)

    signal = "BUY" if final_bias == "BULLISH" else (
             "SELL" if final_bias == "BEARISH" else "WAIT")

    return {
        "signal": signal,
        "pair": ocr_data["pair"],
        "timeframe": ocr_data["timeframe"],
        "bias": final_bias,
        "structure": structure,
        "order_block": ob,
        "fvg": fvg,
        "liquidity": liquidity,
        "candles_detected": len(candles),
        "engine_version": "Phase 4 – Real OCR + Real Candles"
    }
