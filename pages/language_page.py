from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LanguagePage:
    LANG_SWITCH = (By.CLASS_NAME, "lang-switch")
    CONTEXT_MENU = (By.CLASS_NAME, "context-menu--modal")
    LANG_OPTION = (By.CSS_SELECTOR, ".context-menu--modal .context-menu__option.list-item")
    LANG_TITLE = (By.CSS_SELECTOR, ".list-item__title")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.element_to_be_clickable(self.LANG_SWITCH))

    def open_lang_menu(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.LANG_SWITCH))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.visibility_of_element_located(self.CONTEXT_MENU))

    def get_language_elements(self):
        return self.driver.find_elements(*self.LANG_OPTION)

    def get_language_texts(self):
        self.open_lang_menu()
        elements = self.get_language_elements()
        texts = []
        for el in elements:
            try:
                text = el.find_element(*self.LANG_TITLE).text.strip()
            except Exception:
                text = el.text.strip()
            if text:
                texts.append(text)
        return texts

    def select_language(self, lang_text):
        self.open_lang_menu()
        elements = self.get_language_elements()
        for idx, el in enumerate(elements):
            try:
                text = el.find_element(*self.LANG_TITLE).text.strip()
            except Exception:
                text = el.text.strip()
            print(f"[{idx}] '{text}' vs '{lang_text}'")
            if text == lang_text:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                self.driver.execute_script("arguments[0].click();", el)
                return True
        return False 