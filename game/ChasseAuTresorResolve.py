import time
import game.zaap
from random import randint
import pyperclip as pc

class ChasseAuTresorResolve():

    def __init__(self, bot):
        self.bot = bot
        self.window_manager = bot.window_manager
        self.image_manager = bot.image_manager
        self.targets = self.image_manager.targets

    def do_hunt_step(self, zoom = 4):
        if(zoom > 8):
            return self.bot.chasse_au_tresor.quit_chasse()
            zoom = 4
        if self.window_manager.click_img(self.targets['combattre'], [0,0], 1, 0.8):
            self.do_combat()
        direction, indice = self.find_next_target(zoom)
        if direction == False: return
        if "Phorreur" in indice:
            self.bot.selenium_bot.x, self.bot.selenium_bot.y = self.bot.selenium_bot.get_x_y()
            self.find_phorreur(direction)
        else:
            lastx, lasty = self.bot.selenium_bot.get_x_y()
            new_pos = self.bot.selenium_bot.find_next_position(direction, indice)
            if (lastx, lasty) != new_pos:
                #self.bot.Tchat.use_auto_palote(new_pos[0], new_pos[1])
                self.get_past_value()
                self.click_flag()      
            else:
                lastx, lasty = self.bot.get_player_pos()
                self.bot.x, self.bot.y = lastx, lasty
                self.bot.selenium_bot.change_x_y(lastx, lasty)
                return self.do_hunt_step(zoom + 1)

    def click_flag(self):
        threshold = 0.9
        loop = True
        while loop:
            if not self.window_manager.click_img(self.targets["next_target"], [5,5], 1, threshold):
                if not self.window_manager.click_img(self.targets["next_target2"], [5,5], 1, threshold):
                    if not self.window_manager.click_img(self.targets["next_target2"], [5,5], 1, threshold):
                        threshold =- 0.02
                    else:
                        loop = False
                else:
                    loop = False
            else:
                loop = False


    def get_past_value(self):
        trav = pc.paste().split(" ")[1:]
        try:
            self.bot.Tchat.use_auto_palote(trav[0], trav[1])
        except:
            pass
        
    def find_phorreur(self, direction, nb_rep = 0):
        self.window_manager.click_img(self.targets["chasse_petite"], [0,0], 1)
        for i in range(10):
            reversed_pos = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
            click_pos = {"top":(0, -1), "bottom":(0, 1), "left":(-1, 0), "right":(1, 0)}
            x, y = click_pos[direction]
            self.bot.selenium_bot.x = int(self.bot.selenium_bot.x) + int(x)
            self.bot.selenium_bot.y = int(self.bot.selenium_bot.y) + int(y)
            self.bot.Tchat.use_auto_palote(self.bot.selenium_bot.x, self.bot.selenium_bot.y)
            list_cross = ["top", "bottom", "right", "left"]
            phorreurs_imgs = [ v for k,v in self.targets.items() if "phorreur" in k]
            for phorreur_img in phorreurs_imgs:
                if self.image_manager.is_in_screen(phorreur_img, 0.90):
                    print("phorreur FIND !!")
                    self.window_manager.click_img(self.targets["chasse_grande"], [0,0], 1)
                    self.click_flag()      
                    self.bot.selenium_bot.x, self.bot.selenium_bot.y = self.bot.get_player_pos()
                    self.bot.selenium_bot.change_x_y(self.bot.selenium_bot.x, self.bot.selenium_bot.y)
                    return True
        if(nb_rep > 4):
            self.bot.chasse_au_tresor.quit_chasse()
            return
        self.find_phorreur(reversed_pos[direction], nb_rep + 1)

    def find_next_target(self, zoom = 4):
        pos = self.image_manager.positions(self.targets['next_target'], None, 0.8)
        if len(pos) == 0:
            if self.window_manager.click_img(self.targets["next_etape"], [5,5], 1, 0.8):
                return self.find_next_target(zoom)
            else:
                return False, False
        text = self.image_manager.cut_img(self.image_manager.print_sreen(), pos[0]-2, pos[1]-185, pos[2], 180)
        # zoom on text
        text_zoom = self.image_manager.zoom(text, zoom)
        #self.show_img(text)
        cross = self.image_manager.cut_img(self.image_manager.print_sreen(), pos[0], pos[1]-205, pos[2], 18)
        real_text = self.image_manager.read_text(text_zoom)[:-1]
        if real_text == "":
            for i in range(1, 15):
                if real_text == "":
                    text_zoom = self.image_manager.zoom(text, i)
                    real_text = self.image_manager.read_text(text_zoom)[:-1]
                else:
                    break
        return (self.find_direction(cross), real_text)

    def find_direction(self, cross, threshold = 0.77):
        list_cross1 = ["top", "bottom", "right", "left"]
        self.image_manager.save_img(cross)
        #list_cross = [ v for k,v in self.targets.items() if any(cross in k for cross in list_cross1)]
        for key in list_cross1:
            if len(self.image_manager.positions(self.targets[key], cross, threshold)) != 0:
                return key
        return self.find_direction(cross, threshold - 0.01)
    
    def do_combat(self):
        if self.window_manager.click_img(self.targets["pres"], [5,5], 1):
            return
        if not self.image_manager.is_in_screen(self.targets['your_turn']):
            return time.sleep(0.2)
        print("your turn")
        for i in range(3):
            self.lauch_spell()
            if not self.image_manager.is_in_screen(self.targets['in_fight']) or not self.image_manager.is_in_screen(self.targets['your_turn']):
                break
        self.window_manager.click_img(self.targets["pass_turn"], [10,10], 4, 0.8)

    def lauch_spell(self):
        self.window_manager.click_img(self.targets["spell"], [5,5])
        print("click spell")
        time.sleep(0.2)
        self.window_manager.click_img(self.targets["coffre"], [0,0], 3, 0.8, True, 0.3)
        print("click mob")
        time.sleep(0.5)