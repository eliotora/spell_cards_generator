import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import json
import os
import warnings

class AideddNavigator():
    def __init__(self, driver):
        self.driver = driver

    def get(self, url: str):
        """
        Navigate to the specified URL.
        :param url: The URL to navigate to.
        """
        self.driver.get(url)

    def accept_cookies(self):
        sleep(3)
        try:
            self.driver.find_element(By.ID, "cmpwelcomebtnyes").click()

        except:
            try:
                self.driver.find_element(By.ID, "cmpbntyestxt").click()
            except:
                print(f"Could not accept cookies")

    def multiple_select(self, checkbox_id: str, select_id: str, options: list[str]=None):
        checkbox = self.driver.find_element(By.ID, checkbox_id)
        checkbox.click()  # Ensure the checkbox is clicked to enable multiple selection
        checkbox.click()  # Click again to ensure it is selected
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
        select = self.driver.find_element(By.NAME, select_name)
        select = Select(select)
        # select.find_element(By.XPATH, f'//option[@selected="selected"]').click()  # Deselect any previously selected option
        select.select_by_value(str(level))  # Select the desired level by value
        # select.find_element(By.XPATH, f'//option[@value="{level}"]').selected = "selected"  # Select the desired level

    def spell_filter_by(self, classes:list[str]=None, schools:list[str]=None, level_min: int = 0, level_max: int = 9, sources:list[str]=["Player's Handbook"]):
        # Select classes
        self.multiple_select("selectAllF1", "FormF1", classes)
        sleep(5)
        # Select schools
        self.multiple_select("selectAllF2", "FormF2", schools)
        # Select level range
        self.select_level(select_name="nivMin", level=level_min)
        self.select_level(select_name="nivMax", level=level_max)
        # Select sources
        self.multiple_select("selectAllS", "FormSource", sources)

        tasha_list = self.driver.find_element(By.ID, "opt_tcoe")  # Select Tasha's Cauldron of Everything
        if not tasha_list.is_selected():
            tasha_list.click()

        # Select all display options
        coche_group = self.driver.find_element(By.CLASS_NAME, "coche")
        input_list = coche_group.find_elements(By.TAG_NAME, "input")
        for input in input_list:
            if not input.is_selected():
                input.click()

        # Click on the filter button
        self.driver.find_element(By.NAME, "filtrer").click()

    def feat_filter_by(self, sources:list[str]=["Player's Handbook"]):
        # Select sources
        self.multiple_select("selectAllS", "FormSource", sources)

        # Select all display options
        coche_group = self.driver.find_element(By.CLASS_NAME, "coche")
        input_list = coche_group.find_elements(By.TAG_NAME, "input")
        for input in input_list:
            if not input.is_selected():
                input.click()

        # Click on the filter button
        self.driver.find_element(By.NAME, "filtrer").click()

    def spell_get_all_lines(self):
        table = self.driver.find_element(By.ID, "liste")
        rows = table.find_elements(By.TAG_NAME, "tr")
        spells = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                spell = {
                    "lien": cells[1].find_element(By.TAG_NAME, "a").get_attribute("href"),
                    "nom": cells[1].text,
                    "description_short": cells[11].text,
                    # "source": cells[12].text
                }
                spells.append(spell)
        print(f"Found {len(spells)} spells.")
        return spells

    def feat_get_all_lines(self):
        table = self.driver.find_element(By.ID, "liste")
        rows = table.find_elements(By.TAG_NAME, "tr")
        feats = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                feat = {
                    "lien": cells[1].find_element(By.TAG_NAME, "a").get_attribute("href"),
                    "nom": cells[1].text,
                    "description_short": cells[5].text,
                    # "source": cells[12].text
                }
                feats.append(feat)
        print(f"Found {len(feats)} feats.")
        return feats

    def get_spell_details(self, spell, spell_url: str):
        self.driver.get(spell_url)
        sleep(2)
        content = self.driver.find_element(By.CLASS_NAME, "col1")
        trad = content.find_element(By.CLASS_NAME, "trad")

        spell["nom_VO"] = trad.find_element(By.TAG_NAME, "a").text
        if len(trad.text.split("[")) > 2:
            spell["nom_VF"] = trad.text.split("[")[2].split("]")[0].strip()
        else:
            spell["nom_VF"] = None
        level_school = content.find_element(By.CLASS_NAME, "ecole").text
        spell["niveau"] = int(level_school.split(" - ")[0].split("niveau ")[1])
        spell["école"] = level_school.split(" - ")[1].split(" (")[0]
        spell["rituel"] = True if "rituel" in level_school else False
        spell["temps_d'incantation"] = content.find_element(By.CLASS_NAME, "t").text.split(": ")[1]
        spell["portée"] = content.find_element(By.CLASS_NAME, "r").text.split(": ")[1]
        composantes_text = content.find_element(By.CLASS_NAME, "c").text.split(": ")[1]
        if "(" in composantes_text:
            composantes = composantes_text.split(" (")[0].split(", ")
            composantes[-1] = " (".join([composantes[-1], composantes_text.split(" (")[1]])
        else:
            composantes = composantes_text.split(", ")
        spell["composantes"] = composantes
        spell["durée"] = content.find_element(By.CLASS_NAME, "d").text.split(": ")[1]
        spell["concentration"] = True if "concentration" in content.find_element(By.CLASS_NAME, "d").text else False
        description = content.find_element(By.CLASS_NAME, "description").get_attribute("innerHTML")
        spell["description"] = description.split("<strong><em>Aux niveaux supérieurs</em></strong>. ")[0].strip()
        spell["à_niveau_supérieur"] = description.split("<strong><em>Aux niveaux supérieurs</em></strong>. ")[1].strip() if "<strong><em>Aux niveaux supérieurs</em></strong>. " in description else ""

    def get_feat_details(self, feat, feat_url: str):
        self.driver.get(feat_url)
        sleep(2)
        content = self.driver.find_element(By.CLASS_NAME, "col1")
        trad = content.find_element(By.CLASS_NAME, "trad")

        feat["nom_vo"] = trad.find_element(By.TAG_NAME, "a").text
        if len(trad.text.split("[")) > 2:
            feat["nom_vf"] = trad.text.split("[")[2].split("]")[0].strip()
        else:
            feat["nom_vf"] = None
        try:
            prerequisite = content.find_element(By.CLASS_NAME, "prerequis").text
            feat["prérequis"] = prerequisite.split(" : ")[1]
        except:
            feat["prérequis"] = ""
        description = content.find_element(By.CLASS_NAME, "description").get_attribute("innerHTML")
        feat["description"] = description

def spells_scrap_source(source:str, navigator: AideddNavigator):
    """
    Scraps the spells from the given source.
    :param source: The source to scrap.
    :param driver: The webdriver to use.
    """
    navigator.driver.get("https://www.aidedd.org/dnd-filters/sorts.php")
    navigator.accept_cookies()

    for classe in ["Artificier", "Barde", "Clerc", "Druide", "Ensorceleur", "Magicien", "Occultiste", "Paladin", "Rôdeur"]:
        spells = scrap_class_spell_list(classe, source, navigator)
        if spells:
            write_spell_list_to_json(classe, spells, f"data_imports/{source}/spell_lists/")
            print(f"Spells for {classe} from {source} written to JSON.")
        else:
            print(f"No spells found for {classe} in {source}.")

    spells = scrap_spells_from_source(source, navigator)
    if spells:
        write_spells_to_json(spells, f"data_imports/{source}/spells/")
        print(f"All spells from {source} written to JSON.")
    else:
        print(f"No spells found in {source}.")

def scrap_class_spell_list(classe:str, source:str, navigator):
    """
    Scraps the spells for a given class and source.
    :param classe: The class to scrap.
    :param source: The source to scrap.
    :param navigator: The navigator to use.
    :return: A list of spells.
    """
    navigator.filter_by(
        classes=[classe],
        schools=None,
        level_min=0,
        level_max=9,
        sources=[source]
    )
    sleep(1)
    spells = navigator.get_all_lines()
    return spells

def scrap_spells_from_source(source:str, navigator):
    """
    Scraps all spells from a given source.
    :param source: The source to scrap.
    :param navigator: The navigator to use.
    :return: A list of spells.
    """
    navigator.filter_by(
        classes=None,
        schools=None,
        level_min=0,
        level_max=9,
        sources=[source]
    )
    sleep(1)
    spells = navigator.get_all_lines()

    for spell in spells:
        navigator.get_spell_details(spell, spell["lien"])

    return spells

def write_spells_to_json(spells:list, path:str):
    """
    Writes the spells to a JSON file.
    :param spells: The list of spells to write.
    :param path: The path to the JSON file.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    print(f"Writing {len(spells)} spells to JSON in {path}")

    for spell in spells:
        spell_to_write = {k: v for k, v in spell.items() if k not in ["lien"]}
        spell_name = spell_to_write["nom"].replace(" ", "_").replace("/", "_")
        spell_path = os.path.join(path, f"{spell_name}.json")
        with open(spell_path, 'w', encoding='utf-8') as f:
            json.dump(spell_to_write, f, ensure_ascii=False, indent=4)

def write_spell_list_to_json(classe:str, spells:list, path:str):
    """
    Writes the spells of a class to a JSON file.
    :param classe: The class name.
    :param spells: The list of spells to write.
    :param path: The path to the JSON file.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    data = {
        "classe": classe,
        "sorts": [
            spell["nom"] for spell in spells if "nom" in spell
        ]
    }

    class_path = os.path.join(path, f"{classe}.json")

    print(f"Writing {len(data['sorts'])} spells for {classe} to JSON in {class_path}")
    with open(class_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def feat_scrap_source(source:str, navigator: AideddNavigator):
    """
    Scraps the feats from the given source.
    :param source: The source to scrap.
    :param driver: The webdriver to use.
    """
    navigator.driver.get("https://www.aidedd.org/dnd-filters/dons.php")
    navigator.accept_cookies()

    feats = scrap_feats_from_source(source, navigator)
    if feats:
        write_feats_to_json(feats, f"data_imports/{source}/feats/")
        print(f"All feats from {source} written to JSON.")
    else:
        print(f"No feats found in {source}.")

def scrap_feats_from_source(source:str, navigator:AideddNavigator):
    """
    Scraps all feats from a given source.
    :param source: The source to scrap.
    :param navigator: The navigator to use.
    :return: A list of feats.
    """
    navigator.feat_filter_by(
        sources=[source]
    )
    sleep(1)
    feats = navigator.feat_get_all_lines()

    for feat in feats:
        navigator.get_feat_details(feat, feat["lien"])

    return feats

def write_feats_to_json(feats:list, path:str):
    """
    Writes the feats to a JSON file.
    :param feats: The list of feats to write.
    :param path: The path to the JSON file.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    print(f"Writing {len(feats)} feats to JSON in {path}")

    for feat in feats:
        feat_to_write = {k: v for k, v in feat.items() if k not in ["lien"]}
        feat_name = feat_to_write["nom"].replace(" ", "_").replace("/", "_")
        feat_path = os.path.join(path, f"{feat_name}.json")
        with open(feat_path, 'w', encoding='utf-8') as f:
            json.dump(feat_to_write, f, ensure_ascii=False, indent=4)


def eldritch_scrap_source(source:str, navigator: AideddNavigator):
    """
    Scraps the eldritch from the given source.
    :param source: The source to scrap.
    :param driver: The webdriver to use.
    """
    navigator.driver.get("https://www.aidedd.org/dnd-filters/manifestations-occultes.php")
    navigator.accept_cookies()

    eldritchs = scrap_eldritchs_from_source(source, navigator)
    if eldritchs:
        write_eldritchs_to_json(eldritchs, f"data_imports/{source}/eldritchs/")
        print(f"All eldritchs from {source} written to JSON.")
    else:
        print(f"No eldritchs found in {source}.")

def scrap_eldritchs_from_source(source:str, navigator:AideddNavigator):
    """
    Scraps all eldritchs from a given source.
    :param source: The source to scrap.
    :param navigator: The navigator to use.
    :return: A list of eldritchs.
    """
    navigator.feat_filter_by(
        sources=[source]
    )
    sleep(1)
    eldritchs = navigator.feat_get_all_lines()

    for eldritch in eldritchs:
        navigator.get_feat_details(eldritch, eldritch["lien"])

    return eldritchs

def write_eldritchs_to_json(eldritchs:list, path:str):
    """
    Writes the eldritchs to a JSON file.
    :param eldritchs: The list of eldritchs to write.
    :param path: The path to the JSON file.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    print(f"Writing {len(eldritchs)} eldritchs to JSON in {path}")

    for eldritch in eldritchs:
        eldritch_to_write = {k: v for k, v in eldritch.items() if k not in ["lien"]}
        eldritch_name = eldritch_to_write["nom"].replace(" ", "_").replace("/", "_")
        eldritch_path = os.path.join(path, f"{eldritch_name}.json")
        with open(eldritch_path, 'w', encoding='utf-8') as f:
            json.dump(eldritch_to_write, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    options = Options()
    options.add_argument("--log-level=3")

    service = Service(log_path=os.devnull)

    driver = webdriver.Edge(service=service, options=options)

    navigator = AideddNavigator(driver)

    eldritch_scrap_source("Player´s Handbook", navigator)
    eldritch_scrap_source("Xanathar´s Guide to Everything", navigator)
    eldritch_scrap_source("Tasha´s Cauldron of Everything", navigator)
    # feat_scrap_source("Fizban´s Treasury of Dragons", navigator)
    # feat_scrap_source("Settings", navigator)
    # feat_scrap_source("Extra (divers)", navigator)
    driver.quit()
    exit()

