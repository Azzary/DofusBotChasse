from WindowManager import WindowManager
import utils
import cv2
import pytesseract
import numpy as np
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageManager():

    def __init__(self, window_manager: WindowManager):
        self.window_manager = window_manager
        self.targets = utils.load_images()

    def print_sreen(self):
        return self.window_manager.get_screenshot()

    def is_in_screen(self, img, threshold=0.75):
        pos = self.positions(img, None, threshold)
        if len(pos) == 0:
            return False
        return True

    def show_img(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cut_img(self, img, x, y, w, h):
        return img[x:x+w, y:y+h]

    def in_black_and_with(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV )

    def zoom(self, img, zoom_factor=4):
        return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)

    def empty_click(self):
        self.window_manager.click_img(self.targets["empty_click"])

    def save_img(self, img, name = "img.png"):
        cv2.imwrite(name, img)

    def positions(self, target, img = None, threshold=0.90):
        if img is None:
            img = self.print_sreen()
        result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
        w = target.shape[1]
        h = target.shape[0]
        cv2.imwrite('img.png', img)
        cv2.imwrite('img2.png', target)
        yloc, xloc = np.where(result >= threshold)
        if len(yloc) == 0:
            return []
        return yloc[0], xloc[0], h, w

    def wait_for_no_img(self, img, threshold=0.85, time_sleep =0.5, max_time=5):
        i = 0
        while i <= max_time:
            i+=1
            time.sleep(time_sleep)
            if not self.is_in_screen(img, threshold):
                return True
        return False

    def wait_for_img(self, img, threshold=0.90, time_sleep =0.5, max_time = 40):
        i = 0
        while i <= max_time:
            i += 1
            time.sleep(time_sleep)
            if self.is_in_screen(img, threshold):
                return True
        return False

    # read text from image with pytesseract
    def read_text(self, img, lang='fra', config="--psm 4 --oem 2"):
        text = pytesseract.image_to_string(img, lang)
        if text == "":
            text = pytesseract.image_to_string(img, lang, config)
        return text