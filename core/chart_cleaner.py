import cv2

def preprocess_chart(img):
    # Remove grid noise
    blur = cv2.GaussianBlur(img, (5,5), 0)

    # Increase contrast
    lab = cv2.cvtColor(blur, cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3)
    cl = clahe.apply(l)
    final = cv2.merge((cl,a,b))
    final = cv2.cvtColor(final, cv2.COLOR_LAB2BGR)

    return final
