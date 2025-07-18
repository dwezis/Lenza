from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class ProfilePage:
    START_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    CONTINUE_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    CODE_INPUTS = (By.CSS_SELECTOR, '.code-input__field')
    WS_BLOCKS = (By.CSS_SELECTOR, '.list-item.list-item--lg.no-select')
    WS_TITLE = (By.CLASS_NAME, 'list-item__title')
    JOIN_BTN = (By.XPATH, ".//button[.//span[contains(text(), 'Присоединиться')]]")
    PRIVACY_BTN = (By.XPATH, "//button[.//span[contains(text(), 'Мне понятно. Вперед!')]]")
    AVATAR_INPUT = (By.CSS_SELECTOR, 'input.avatar__img-upload-input')
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Введите имя"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Введите фамилию"]')
    CONTINUE_BTN2 = (By.CSS_SELECTOR, 'button.btn--full-width')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 20)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.element_to_be_clickable(self.START_BTN))

    def login_and_join_workspace(self, email, code, ws_name):
        self.wait.until(EC.element_to_be_clickable(self.START_BTN)).click()
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()
        code_inputs = self.wait.until(lambda d: d.find_elements(*self.CODE_INPUTS))
        for i, digit in enumerate(code):
            code_inputs[i].clear()
            code_inputs[i].send_keys(digit)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Выбор рабочего пространства')]")))
        ws_blocks = self.driver.find_elements(*self.WS_BLOCKS)
        for block in ws_blocks:
            try:
                title = block.find_element(*self.WS_TITLE)
                if ws_name in title.text:
                    join_btn = block.find_element(*self.JOIN_BTN)
                    join_btn.click()
                    break
            except:
                continue
        self.wait.until(EC.element_to_be_clickable(self.PRIVACY_BTN)).click()
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'профиль') or contains(text(), 'Профиль') or contains(text(), 'личных данных')]")))
        except:
            self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))

    def upload_avatar(self, path):
        avatar_input = self.wait.until(EC.presence_of_element_located(self.AVATAR_INPUT))
        if os.path.exists(path):
            avatar_input.send_keys(os.path.abspath(path))
            self.wait.until(lambda d: avatar_input.get_attribute('value'))
            return True
        return False

    def fill_profile(self, first_name, last_name):
        first_name_input = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        last_name_input = self.wait.until(EC.visibility_of_element_located(self.LAST_NAME_INPUT))
        last_name_input.clear()
        last_name_input.send_keys(last_name)

    def get_continue_btn(self):
        return self.long_wait.until(EC.presence_of_element_located(self.CONTINUE_BTN2))

    def click_create_workspace_block(self, text="Создать новое пространство"):
        ws_blocks = self.driver.find_elements(By.CSS_SELECTOR, '.ws_workspace__accounts_new_item')
        for block in ws_blocks:
            try:
                title = block.find_element(By.CLASS_NAME, 'list-item__title')
                if text in title.text:
                    block.click()
                    return True
            except:
                continue
        return False

    def get_code_inputs(self):
        return self.wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, '.code-input__field')) 