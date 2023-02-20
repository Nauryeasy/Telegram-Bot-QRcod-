import cv2
from pyzbar.pyzbar import decode
import re


def get_link_qr_code():
    img = cv2.imread("src/img.png")
    data = decode(img)
    link = data[0].data.decode("utf-8")
    expression = r'(http?://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?://(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    regex = re.compile(expression, re.IGNORECASE)
    if regex.match(link):
        return link
    else:
        return False
