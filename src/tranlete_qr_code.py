import cv2
from pyzbar.pyzbar import decode


def get_link_qr_code():
    img = cv2.imread("src/img.png")
    data = decode(img)
    link = data[0].data.decode("utf-8")
    return link

