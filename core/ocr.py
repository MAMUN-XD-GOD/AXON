import pytesseract
import cv2
import re

def extract_text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)

    text = pytesseract.image_to_string(blur)

    return text


def detect_pair(text):
    pattern = r"[A-Z]{3}\/[A-Z]{3}"
    m = re.search(pattern, text)

    if m:
        return m.group(0)

    # OTC brokers
    pattern2 = r"[A-Z]{3,5}"
    m2 = re.search(pattern2, text)

    return m2.group(0) if m2 else "UNKNOWN"


def detect_timeframe(text):
    if "1m" in text.lower(): return "1M"
    if "5m" in text.lower(): return "5M"
    if "15m" in text.lower(): return "15M"
    if "1h" in text.lower(): return "1H"
    if "4h" in text.lower(): return "4H"

    # Quotex format “M1”
    m = re.search(r"M\d+", text)
    if m:
        return m.group(0)

    return "UNKNOWN"


def extract_ocr_data(img):
    text = extract_text(img)

    return {
        "pair": detect_pair(text),
        "timeframe": detect_timeframe(text),
        "raw_text": text
  }
