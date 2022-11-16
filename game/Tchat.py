import time


class Tchat():

    def __init__(self, bot):
        self.bot = bot
        self.window_manager = bot.window_manager
        self.image_manager = bot.image_manager
        self.targets = self.image_manager.targets

    def send_in_chat(self, text):
        self.window_manager.click_img(self.targets["chat"], [40,8])
        self.window_manager.press("/")
        self.window_manager.press_entree()
        for lettre in text:
            self.window_manager.press(lettre)
        self.window_manager.press_entree()
        
    
    
    def use_auto_palote(self, x, y):
        self.send_in_chat(f"/travel {x} {y}")
        if(not self.image_manager.wait_for_img(self.targets["ok_popup"], 0.8, 0.01, 4)):
            return
        self.window_manager.press_entree()

        screenshot = self.window_manager.get_screenshot()     
        nb = 0   
        while nb < 40 and not self.image_manager.is_in_screen(self.targets["is_arrived"], 0.95):
            new_screen = self.window_manager.get_screenshot()
            if(len(self.image_manager.positions(screenshot, new_screen, 0.98)) != 0):
                nb+=1
            else:
                nb=0
                screenshot = new_screen 
            time.sleep(0.1)
            
        self.send_in_chat("/")