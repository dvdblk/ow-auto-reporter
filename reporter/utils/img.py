import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab


def take_screenshot(bbox=None):
    """
    Return a cv2 img of the OW screen in grayscale.
    """
    shot = ImageGrab.grab(bbox=bbox)
    return cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2GRAY)


def get_reason_index_from_img(reason_text: str, img, tesseract_path: str) -> None:
    """
    Return the index of the reason to select in the image.
    """
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    ocr_reasons = filter(lambda x: x != "", pytesseract.image_to_string(img).splitlines())
    for i, ocr_reason in enumerate(ocr_reasons):
        if ocr_reason == reason_text:
            return i
    return None
