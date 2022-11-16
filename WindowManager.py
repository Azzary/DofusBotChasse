import win32api
import win32gui
import win32con
import pyautogui
import win32ui
import numpy as np
import cv2
import utils
import time
import win32api as api
import array
import win32process
import win32api as api
import win32console as con
import pyperclip as pc

class WindowManager:

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        # get window size
        x0, y0, x1, y1 = win32gui.GetWindowRect(self.hwnd)
        self.height = 1039
        self.width = 974
        win32gui.MoveWindow(self.hwnd, x0, y0, self.width, self.height, True)

    # click img
    def click_img(self, img, pos_to_add=[0, 0], timeout=10, threshold=0.90, clickc=True, sleep = 0.3):
        has_timed_out = False
        i = 0
        while (not has_timed_out):
            matches = self.positions(img, threshold=threshold)
            i += 1
            if (len(matches) == 0):
                threshold -= 0.011
                has_timed_out = i > timeout
                if(timeout != 1):
                    time.sleep(0.5)
                continue
            y, x, h, w = matches
            pos_click_x = x + w/2
            pos_click_y = y + h/2
            # move the cursor to x , y
            if clickc:
                self.click(pos_click_x, pos_click_y, sleep)
                time.sleep(0.2)
            return True

        return False

    def double_click(self, x, y):
        self._click(x , y)
        self._click(x , y)
        time.sleep(0.3)

    def get_text_select(self):
        t, p = win32process.GetWindowThreadProcessId(self.hwnd)
        return self.send_ctrl_c()

    def send_ctrl_c(self):
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, 0x11, 0)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32api.VkKeyScan("c"), 0)
        time.sleep(0.1)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32api.VkKeyScan("c"), 0)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, 0x11, 0)
        return pc.paste()

    def press(self, key):
        # str key to virtual key
        if key.isdigit() or key == "/":
            win32api.PostMessage(self.hwnd, win32con.WM_CHAR, ord(key), 0)
            return

        vk_code = win32api.VkKeyScan(key)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, 0)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, None, 0)
        time.sleep(0.05)

    def click(self, x, y, sleep = 0.3):
        self._click(x , y)
        time.sleep(sleep)
        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE,
                             0, win32api.MAKELONG(0, 0))

    def _click(self, x, y):
        x = int(x)
        y = int(y)
        x -= 5
        y -= 31
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, lParam)
        time.sleep(0.1)
        win32gui.SendMessage(
            self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,
                             win32con.MK_LBUTTON, lParam)


    def positions(self, target, img=None, threshold=0.90):
        if img is None:
            img = self.get_screenshot()
        # save img

        result = cv2.matchTemplate(target, img, cv2.TM_CCOEFF_NORMED)
        w = target.shape[1]
        h = target.shape[0]
        yloc, xloc = np.where(result >= threshold)
        if len(yloc) == 0:
            return []
        return yloc[0], xloc[0], h, w

    # takes a screenshot of the game
    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.width, self.height),
                   dcObj, (0, 0), win32con.SRCCOPY)
        bmp = dataBitMap.GetBitmapBits(True)
        # transform to numpy array for cv2
        img = np.frombuffer(bmp, dtype='uint8')
        img = img.reshape(self.height, self.width, 4)
        img = img[:, :, :3]

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        return img


    def show_img(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def press_entree(self):
        win32api.PostMessage(
            self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP,
                             win32con.VK_RETURN, 0)



def get_name():
    for x in pyautogui.getAllWindows():
        print(x.title)




if __name__ == "__main__":
    targets = utils.load_images()
    window_manager = WindowManager("Name - Dofus 2.xx.x.xx")
    #window_manager.click(33, 905)
    time.sleep(0.2)
    window_manager.double_click(125, 877)
    text = window_manager.get_text_select()
    # window_manager.press_entree()dddd

    # click_pos = {"top":(40, 105), "bottom":(40, 925), "left":(3,185), "right":(950,185)}
    # x = 800
    # y = 615
    # window_manager.click(click_pos["left"][0], click_pos["left"][1])
    # window_manager.click_img(targets['zaap_cherche'], [50,5])
    # for lettre in "Coin des ":
    #     window_manager.press(lettre)

