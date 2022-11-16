import time, game.zaap


class HavreSac:

    def __init__(self, bot):
        self.bot = bot
        self.window_manager = bot.window_manager
        self.image_manager = bot.image_manager
        self.targets = self.image_manager.targets

    def is_in_hb(self):
        if (self.image_manager.is_in_screen(self.targets["zaap_cherche"])):
            return True
        return self.image_manager.is_in_screen(self.targets["in_havre_sac"])

    def use_zaap(self, zaap_name):
        self.window_manager.click_img(self.targets["chasse_petite"])
        self.window_manager.click_img(self.targets["zaap"], [5,5], 10, 0.8)
        if(self.image_manager.wait_for_img(self.targets["zaap_cherche"], 0.8, 0.1, 20)):    
            self.window_manager.click_img(self.targets["zaap_cherche"])
            time.sleep(1)
            for lettre in zaap_name:
                self.window_manager.press(lettre)
            self.window_manager.click_img(self.targets["do_tp"])
            fini = False
            max_wait = 20
            i = 0
            while not fini:
                for perso in ["personnage1", "personnage2", "personnage3", "personnage4", "personnage5", "personnage6", "personnage7"]:
                    if i == max_wait or self.image_manager.is_in_screen(self.targets[perso]):
                        fini = True
                        break
                i += 1
                time.sleep(0.2)
            self.window_manager.click_img(self.targets["chasse_grande"])
            return True
        self.window_manager.click_img(self.targets["chasse_grande"])
        return False

    def go_hb(self):
        if(self.image_manager.is_in_screen(self.targets["in_havre_sac"], 0.90)):
            return True
        self.window_manager.click_img(self.targets["havre_sac"], [5,5], 3, 0.8)
        if(self.image_manager.wait_for_img(self.targets["cant_go_in_hb"],0.90, 0.1, 5)):
            x, y = self.bot.get_player_pos()
            zaap = game.zaap.get_zaap(x, y)
            self.bot.Tchat.use_auto_palote(zaap["coor"]["x"], zaap["coor"]["y"])
            return self.go_hb()
        if(not self.image_manager.wait_for_img(self.targets["in_havre_sac"], 0.8, 0.1, 20)):
            return False
        return True

    def quit_hb(self):
        if(not self.image_manager.is_in_screen(self.targets["in_havre_sac"])):
            return True
        self.window_manager.click_img(self.targets["havre_sac"], [5,5], 3, 0.8)
        if(self.image_manager.wait_for_no_img(self.targets["in_havre_sac"], 0.8, 0.1, 20)):
            return False
        return True

