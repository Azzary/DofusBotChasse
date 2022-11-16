from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import os
import logging
import warnings
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
from selenium.webdriver.support.ui import Select
import jellyfish, json

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
# Only display possible problems
selenium_logger.setLevel(logging.WARNING)


x_xpath = '//*[@id="huntposx"]'
y_xpath = '//*[@id="huntposy"]'

indice_text = "/html/body/div[1]/div/div/main/div/div[7]/div/label/div/div/div[2]/i"

direction = {
"top"    : '//*[@id="hunt-solver-data"]/div[2]/div[1]/label',
"bottom" : '//*[@id="hunt-solver-data"]/div[2]/div[3]/label',
"right"  : '//*[@id="hunt-solver-data"]/div[2]/div[2]/label[2]',
"left"   : '//*[@id="hunt-solver-data"]/div[2]/div[2]/label[1]'}

#auto_copyloting = "/html/body/div[1]/div/div/main/div/div[8]/div"

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
        self.driver.get("https://www.dofuspourlesnoobs.com/resolution-de-chasse-aux-tresors.html")
        # set height and width to driver
        self.driver.set_window_size(1920/2, 1080/2)
        #self.click_button(xpath=auto_copyloting)
        self.driver.find_element(by=By.XPATH, value='//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
        self.indices = self.get_all_indice()
        self.change_x_y(x, y)

    # get value of input x y
    def get_x_y(self):
        x = self.driver.find_element(by=By.XPATH, value=x_xpath).get_attribute("value")
        y = self.driver.find_element(by=By.XPATH, value=y_xpath).get_attribute("value")
        return x, y


    def select_item(self, indice):
        select = Select(self.driver.find_element_by_id('clue-choice-select'))
        select.select_by_visible_text(indice)
        

    def change_x_y(self, x, y):
        self.change_input(x_xpath, x)
        self.change_input(y_xpath, y)

    def indice_name_corection(self, curr_indice):
        distance = 0
        best_indice = ""
        for indice in self.indices:
            new_dist = jellyfish.jaro_distance(curr_indice, indice)
            if new_dist > distance:
                best_indice = indice
                distance = new_dist
        return best_indice

    def find_next_position(self, xpath, indice:str):
        indice = indice.replace("œ", "oe")
        if "Phorreur" in indice:
            return None
        indice = self.indice_name_corection(indice)
        self.click_button(direction[xpath])
        self.select_item(indice)
        self.driver.find_element(by=By.XPATH, value='//*[@id="hunt-elt3"]').click()
        return self.get_x_y()

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
            x,y = self.get_x_y()
            self.change_x_y(100, 100)
            self.change_x_y(x, y)
            self.click_button(xpath)

    def get_all_indice(self):
        select_box = self.driver.find_element_by_id('clue-choice-select')
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        indices = []
        for element in options:
            indices.append(element.get_attribute('innerHTML'))
        return indices

if __name__ == "__main__":
    bot = SeleniumBot(5, -18)
    json_object = json.dumps(bot.indices, indent=4)
    
    # Writing to sample.json
    with open("indices.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_object)
    print(bot.find_next_position("bottom", "Bonbonb-leu"))
