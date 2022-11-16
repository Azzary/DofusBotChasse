import time
import game.zaap
import game.ChasseAuTresorResolve

class ChasseAuTresor():

    X_HUNT_ENTRY = -25
    Y_HUNT_ENTRY = -36

    def __init__(self, bot):
        self.bot = bot
        self.window_manager = bot.window_manager
        self.image_manager = bot.image_manager
        self.targets = self.image_manager.targets
        self.ch_resolve = game.ChasseAuTresorResolve.ChasseAuTresorResolve(bot)

    def take_hunt(self):
        if not (self.bot.havre_sac.go_hb() and self.bot.havre_sac.use_zaap("Champs de Cania")):
            return False
        self.bot.Tchat.use_auto_palote(ChasseAuTresor.X_HUNT_ENTRY, ChasseAuTresor.Y_HUNT_ENTRY)
        self.entre_in_malle()
        self.speak_for_take_hunt()
        self.bot.Tchat.use_auto_palote(ChasseAuTresor.X_HUNT_ENTRY, ChasseAuTresor.Y_HUNT_ENTRY)
        self.go_pos_hunt()

    def go_pos_hunt(self):
        hunt_pos = self.get_start_point()
        if(hunt_pos == None):
            return self.take_hunt()
        self.bot.x = hunt_pos[0]
        self.bot.y = hunt_pos[1]
        self.bot.selenium_bot.x = hunt_pos[0]
        self.bot.selenium_bot.y = hunt_pos[1]
        print("Start point found, go to next chasse")
        print("Start point: " + str(self.bot.x) + " " + str(self.bot.y))
        closer_zaap = game.zaap.get_zaap(int(self.bot.x), int(self.bot.y))
        print("Closer zaap: " + str(closer_zaap["name"]))      
        self.bot.havre_sac.go_hb()
        self.bot.havre_sac.use_zaap(closer_zaap["name"])
        
        if abs(closer_zaap["coor"]['x'] - int(self.bot.x)) + abs(closer_zaap["coor"]['y'] - int(self.bot.y)) != 0:
            self.bot.Tchat.use_auto_palote(self.bot.selenium_bot.x, self.bot.selenium_bot.y)
        self.bot.selenium_bot.change_x_y(self.bot.x, self.bot.y)

    def quit_chasse(self):
        self.window_manager.click_img(self.targets["chasse_grande"])
        self.window_manager.click_img(self.targets["quit_chasse"])
        self.window_manager.press_entree()
        
    def get_start_point(self):
        res = self.read_pos()
        if res is None:
            print("No start point found, go to next chasse")
            self.window_manager.click_img(self.targets["empty_click"])
            time.sleep(1)
            return None
        return res

    def read_pos(self, zoom = 2):
        pos = self.image_manager.positions(self.targets['start_point'])
        if len(pos) == 0:
            return None
        img = self.image_manager.cut_img(self.image_manager.print_sreen(), pos[0], pos[1]+pos[3]+4, pos[2], pos[3])
        self.image_manager.save_img(img, "d.png")
        img = self.image_manager.zoom(img, zoom)
        text = self.image_manager.read_text(img)
        for elem_char in ["[", "]", "\n", "(", ")"]:
            text = text.replace(elem_char, "")
        if(text == ""):
            return self.read_pos(zoom + 1)
        return text.split(",") 



    def entre_in_malle(self):
        self.window_manager.click_img(self.targets["door_chasse_house"])
        while not self.image_manager.wait_for_no_img(self.targets["door_chasse_house_check"]):
            self.window_manager.click_img(self.targets["door_chasse_house"])
        
        self.window_manager.click_img(self.targets["house_first_sum"])
        while not self.image_manager.wait_for_no_img(self.targets["house_first_sum_check"]):
            self.window_manager.click_img(self.targets["house_first_sum"])
        self.image_manager.wait_for_img(self.targets["chasse"])


    def speak_for_take_hunt(self):
        self.image_manager.empty_click()
        if not self.image_manager.is_in_screen(self.targets["chasse"]):
            return False
        self.window_manager.click_img(self.targets["chasse"])
        if not self.image_manager.wait_for_img(self.targets["take_chasse"], 0.90, 0.1, 1):
            return self.speak_for_take_hunt()
        self.window_manager.click_img(self.targets["take_chasse"], [20,20], 3, 0.75)
        if not self.image_manager.wait_for_img(self.targets["have_chasse"], 0.8, 0.5, 30):
            return self.speak_for_take_hunt() 
        return True


    def is_in_hunt(self):
        if(self.image_manager.is_in_screen(self.targets["have_chasse2"])):
            self.window_manager.click_img(self.targets["chasse_grande"], [5,5], 1)
            return True
        return self.image_manager.is_in_screen(self.targets["have_chasse"])

    def do_hunt_step(self):
        self.ch_resolve.do_hunt_step()