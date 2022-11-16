import ImageManager
import WindowManager
# as BotSelenium parceque des qu'on ecrit sel (pour self) c'est lui qui est en premier
import SeleniumBot as BotSelenium
import time
import game.Tchat, game.ChasseAuTresor, game.HavreSac
import json
import time
import datetime

class bot:

    def __init__(self):
        with open('config.json', 'r') as f:
            data = json.load(f)
        with open('MapPositions.json', 'r') as f:
            self.map_pos = json.load(f)
        self.window_manager = ImageManager.WindowManager(data["window_name"])
        self.image_manager = ImageManager.ImageManager(self.window_manager)
        self.x = "0"
        self.y = "0"
        self.havre_sac = game.HavreSac.HavreSac(self)
        self.Tchat = game.Tchat.Tchat(self)
        self.chasse_au_tresor = game.ChasseAuTresor.ChasseAuTresor(self)
        self.targets = self.image_manager.targets
        self.selenium_bot = BotSelenium.SeleniumBot(self.x, self.y)
        if(self.chasse_au_tresor.is_in_hunt()):
            if input("HunterXHunter pos or player pos") == "1": 
                self.x, self.y = self.get_player_pos()
            else:
                self.chasse_au_tresor.go_pos_hunt()
            self.selenium_bot.change_x_y(self.x, self.y)
        self.loop_bot()

    def get_player_pos(self):
        self.Tchat.send_in_chat("/mapid")
        time.sleep(0.1)
        pos = self.image_manager.positions(self.targets["carte_courante"])
        if(pos == []):
            return self.get_player_pos()
        y = pos[1] + pos[3] + 10
        self.window_manager.double_click(y, pos[0])
        mapid = self.window_manager.get_text_select()
        time.sleep(0.3)
        self.window_manager.click_img(self.targets["close2"], [25,7], 1, 0.7)
        # print(test)
        # return 100 , 100
        # img = self.image_manager.cut_img(self.image_manager.print_sreen(), pos[0], pos[1]+pos[3], pos[2]-22, pos[3])
        # img = self.image_manager.zoom(img, zoom)
        # img = self.image_manager.in_black_and_with(img)
        # self.image_manager.save_img(img)
        # mapid = self.image_manager.read_text(img).replace("\n", "")
        mapid = mapid + ".0"
        if(mapid in self.map_pos):
            return self.map_pos[mapid]["posX"], self.map_pos[mapid]["posY"]
        return self.get_player_pos()


    def get_pa(self, zoom = 1):
        pos = self.image_manager.positions(self.targets["get_pa"])
        pa = ""
        if(pos != None):
            img = self.image_manager.cut_img(self.image_manager.print_sreen(), pos[0]+5, pos[1]+pos[3], pos[2]-10, pos[3]-15)
            img = self.image_manager.in_black_and_with(img)
            img = self.image_manager.zoom(img, zoom)
            self.image_manager.save_img(img)
            pa = self.image_manager.read_text(img).replace("\n", "")
        if pa.isnumeric() and pa != "":
            return int(pa) 
        else:
            return self.get_pa(min(zoom + 1, 8))

    def loop_bot(self):
        self.old_screen = self.image_manager.print_sreen()
        self.nb_stuck = 0
        self.unix_time = self.get_unix()
        while True:
            self.close_popup()
            self.check_if_is_stuck()
            if (self.image_manager.is_in_screen(self.targets['in_fight'])):
                self.chasse_au_tresor.ch_resolve.do_combat()
            elif(not self.chasse_au_tresor.is_in_hunt()):
                self.chasse_au_tresor.take_hunt()
            else:
                self.chasse_au_tresor.do_hunt_step()

    def check_if_is_stuck(self):
        if self.unix_time + 60 > self.get_unix():
            return
        if(self.image_manager.is_in_screen(self.old_screen, 0.8)):
            self.nb_stuck += 1
            if(self.image_manager.is_in_screen(self.targets["in_fight"])):
                if self.nb_stuck > 60 * 2:
                    self.leave_fight()
                    self.nb_stuck = 0
            elif(self.nb_stuck > 20):
                self.chasse_au_tresor.quit_chasse()
                self.nb_stuck = 0
        else:
            self.nb_stuck = 0
            self.old = self.image_manager.print_sreen() 
    
    def leave_fight(self):
        self.window_manager.click_img(self.targets["leave_fight"])
        time.sleep(0.2)
        self.window_manager.press_entree()


    def get_unix(self):
        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
        return (unix_timestamp)
        

    def close_popup(self):
        if self.window_manager.click_img(self.targets["lvl_up"], [5,5], 1, 0.8):
            time.sleep(0.5)
        self.window_manager.click_img(self.targets["close"], [25,7], 1, 0.7)
        self.window_manager.click_img(self.targets["end_combat"], [25,7], 1, 0.7)
    

            





if __name__ == '__main__':
    bot = bot()