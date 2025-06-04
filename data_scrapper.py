import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

class AideddNavigator():
    def __init__(self, driver):
        self.driver = driver

    def accept_cookies(self):
        self.driver.find_element(By.ID, "cmpwelcomebtnyes").click()

    def multiple_select(self, checkbox_id: str, select_id: str, options: list[str]=None):
        checkbox = self.driver.find_element(By.ID, checkbox_id)
        if options is None and not checkbox.is_selected():
            checkbox.click()
        elif type(options) is list and options:
            checkbox.click()
            if checkbox.is_selected():
                checkbox.click()
            select_list = self.driver.find_element(By.ID, select_id)
            action = webdriver.ActionChains(self.driver)
            action.key_down(Keys.CONTROL)
            for option_text in options:
                option = select_list.find_element(By.XPATH, f"//option[contains(text(), '{option_text}')]")
                if not option.is_selected():
                    action.click(option)
            action.key_up(Keys.CONTROL).perform()

    def select_level(self, select_name:str, level:int):
        print(f"Selecting level {level} in {select_name}")
        select = self.driver.find_element(By.NAME, select_name)
        select = Select(select)
        # select.find_element(By.XPATH, f'//option[@selected="selected"]').click()  # Deselect any previously selected option
        select.select_by_value(str(level))  # Select the desired level by value
        # select.find_element(By.XPATH, f'//option[@value="{level}"]').selected = "selected"  # Select the desired level

    def filter_by(self, classes:list[str]=None, schools:list[str]=None, level_min: int = 0, level_max: int = 9, sources:list[str]=["Player's Handbook"]):
        # Select classes
        self.multiple_select("selectAllF1", "FormF1", classes)
        sleep(5)
        # Select schools
        self.multiple_select("selectAllF2", "FormF2", schools)
        # Select level range
        print(f"Selecting levels from {level_min} to {level_max}")
        self.select_level(select_name="nivMin", level=level_min)
        self.select_level(select_name="nivMax", level=level_max)
        # Select sources
        self.multiple_select("selectAllS", "FormSource", sources)
        self.driver.find_element(By.ID, "opt_tcoe").click()  # Select Tasha's Cauldron of Everything

        # Select all display options
        coche_group = self.driver.find_element(By.CLASS_NAME, "coche")
        input_list = coche_group.find_elements(By.TAG_NAME, "input")
        for input in input_list:
            if not input.is_selected():
                input.click()

        # Click on the filter button
        self.driver.find_element(By.NAME, "filtrer").click()

    def get_all_lines(self):
        table = self.driver.find_element(By.ID, "liste")
        rows = table.find_elements(By.TAG_NAME, "tr")
        spells = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                spell = {
                    "lien": cells[1].find_element(By.TAG_NAME, "a").get_attribute("href"),
                    "nom": cells[1].text,
                    "nom_VF": cells[2].text,
                    "nom_VO": cells[3].text,
                    "niveau": cells[4].text,
                    "école": cells[5].text,
                    "temps_d'incantation": cells[6].text,
                    "portée": cells[7].text,
                    "composantes": cells[8].text,
                    "concentration": True if cells[9].text else False,
                    "rituel": True if cells[10].text else False,
                    "description": cells[11].text,
                    "source": cells[12].text
                }
                spells.append(spell)
        print(f"Found {len(spells)} spells.")
        return spells

    def get_spell_details(self, spell_url: str):
        self.driver.get(spell_url)
        sleep(2)
        spell_details = {}
        content = self.driver.find_element(By.CLASS_NAME, "col1")
        spell_details["nom"] = content.find_element(By.TAG_NAME, "h1").text
        spell_details["nom_VO"] = content.find_element(By.XPATH, "").text


if __name__ == "__main__":
    driver = webdriver.Edge()
    driver.get("https://www.aidedd.org/dnd-filters/sorts.php")

    navigator = AideddNavigator(driver)
    navigator.accept_cookies()
    navigator.filter_by(
        classes=["Barde"],
        schools=None,
        level_min=0,
        level_max=9,
        sources=["Player´s Handbook"]
    )
    spells = navigator.get_all_lines()
    for spell in spells[:5]:
        print(spell)
    sleep(30)
