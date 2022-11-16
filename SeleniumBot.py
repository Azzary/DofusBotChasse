from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import os
import logging
import warnings
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import json, jellyfish

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
# Only display possible problems
selenium_logger.setLevel(logging.WARNING)


x_xpath = "/html/body/div[1]/div/div/main/div/div[3]/div[1]/label/div/div[1]/div[1]/input"
y_xpath = "/html/body/div[1]/div/div/main/div/div[3]/div[2]/label/div/div[1]/div[1]/input"

indice_text = "/html/body/div[1]/div/div/main/div/div[7]/div/label/div/div/div[2]/i"

direction = {
"top":"/html/body/div[1]/div/div/main/div/div[5]/div[1]/span[1]",
"bottom" : "/html/body/div[1]/div/div/main/div/div[5]/div[2]/span[2]",
"right" : "/html/body/div[1]/div/div/main/div/div[5]/div[1]/span[2]",
"left" : "/html/body/div[1]/div/div/main/div/div[5]/div[2]/span[1]"}

auto_copyloting = "/html/body/div[1]/div/div/main/div/div[8]/div"

class SeleniumBot:

    def __init__(self, x, y):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--log-level=OFF")
        warnings.filterwarnings("ignore")
        LOGGER.setLevel(logging.WARNING)
        self.x = x
        self.y = y

        self.driver = webdriver.Chrome(options=options, service_log_path='NUL')
        self.driver.get("https://dofusdb.fr/fr/tools/treasure-hunt")
        # set height and width to driver
        self.driver.set_window_size(1920/2, 1080/2)
        self.click_button(xpath=auto_copyloting)
        with open('indices.json', 'r', encoding='utf-8') as f:
            self.indices = json.load(f)
        self.change_x_y(x, y)
        print(self.get_x_y())

    # get value of input x y
    def get_x_y(self):
        x = self.driver.find_element(by=By.XPATH, value=x_xpath).get_attribute("value")
        y = self.driver.find_element(by=By.XPATH, value=y_xpath).get_attribute("value")
        return x, y

    def indice_name_corection(self, curr_indice):
        distance = 0
        best_indice = ""
        for indice in self.indices:
            new_dist = jellyfish.jaro_distance(curr_indice, indice)
            if new_dist > distance:
                best_indice = indice
                distance = new_dist
        return best_indice

    def change_x_y(self, x, y):
        self.change_input(x_xpath, x)
        self.change_input(y_xpath, y)

    def find_next_position(self, xpath, text:str):
        if "Phorreur" in text:
            return None
        text = text.replace("œ", "oe").replace("Œ", "Oe")
        text = self.indice_name_corection(text)
        text = text.replace("oe", "œ").replace("Oe", "Œ")
        self.click_button(direction[xpath])
        return self.set_text(indice_text, text)

    def set_text(self, xpath, text, nb = 0, nb_char_remove = 0):
        flag = False
        try:
            time.sleep(0.5)
            self.driver.find_element(by=By.XPATH, value=xpath).click()
            time.sleep(0.5)
            flag = True
            print(text)
            self.driver.find_element(by=By.XPATH, value=f'//*[text()[contains(., "{text[:-1]}")]]').click()
            self.x, self.y = self.get_x_y()
            return True
        except Exception:
            if not flag:
                if nb > 10:
                    # get value of input
                    x = self.driver.find_element(by=By.XPATH, value=x_xpath).get_attribute("value")
                    y = self.driver.find_element(by=By.XPATH, value=y_xpath).get_attribute("value")
                    # refresh page
                    self.driver.refresh()
                    # wait for page to load
                    time.sleep(2)
                    # change value of input
                    self.change_x_y(x, y)
                return self.set_text(xpath, text, nb+1, nb_char_remove)
            elif len(text) > 1 and nb_char_remove < 5:
                return self.set_text(xpath, text[:-1], 0, nb_char_remove + 1)
            else:
                return self.get_x_y()
        

    def get_new_pos(self):                                
        pos = self.driver.find_element(by=By.XPATH, value='//*[@id="q-app"]/div/div/main/div/div[9]/div/div[2]/span/text()').get_attribute("value")
        print(pos)
        return pos.split(",")

    # change input by xpat
    def change_input(self, xpath, value):
        _input = self.driver.find_element(by=By.XPATH, value=xpath)
        _input.send_keys(f"{Keys.CONTROL}a")
        _input.send_keys(Keys.DELETE)
        _input.send_keys(value)


    def click_button(self, xpath):
        try:
            button = self.driver.find_element(by=By.XPATH, value=xpath)
            button.click()
        except Exception:
            time.sleep(1)
            self.click_button(xpath)


if __name__ == "__main__":
    bot = SeleniumBot(0,0)
    print(bot.find_next_position("top", "Arbre à trous"))
    print(bot.get_new_pos())
    time.sleep(88888)