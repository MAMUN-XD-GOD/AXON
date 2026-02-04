import cv2
import numpy as np

def extract_candles(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # Find candle-like shapes (simple version)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    candles = []

    for c in contours:
        x,y,w,h = cv2.boundingRect(c)

        if w < 4 or h < 20:  # ignore noise
            continue

        # Candle body region
        body = img[y:y+h, x:x+w]
        o = y+h        # open approx
        c_p = y        # close approx
        high = y
        low = y+h

        candles.append((o, high, low, c_p))

    candles = sorted(candles, key=lambda x: x[0])

    return candles[-80:]  # limit last 80 candles
