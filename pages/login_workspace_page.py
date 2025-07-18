from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginWorkspacePage:
    START_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    CONTINUE_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    CODE_INPUTS = (By.CSS_SELECTOR, '.code-input__field')
    WS_BLOCKS = (By.CSS_SELECTOR, '.list-item.list-item--lg.no-select')
    WS_TITLE = (By.CLASS_NAME, 'list-item__title')
    LOGIN_BTN = (By.XPATH, ".//button[.//span[contains(text(), 'Войти')]]")
    CLOSE_BTN = (By.CSS_SELECTOR, 'button#close-view')
    AVATAR_BTN = (By.CSS_SELECTOR, 'div[data-test-id="chat-off-avatar-item"].http-resource-private')
    OK_BTN = (By.XPATH, "//button[.//text()='OK' or .//span[text()='OK']]")
    DROPDOWN_PROFILE_BTN = (By.CSS_SELECTOR, "div[role='menuitem'].profile-button__current-account-item")
    USER_SIDEBAR_BTN = (By.XPATH, "//span[contains(@class, 'sidebar-user-name') or contains(@class, 'sidebar-user-email') or text()='Тест Пользователь' or text()='test@testws_r8ptk7']")
    PROFILE_BLOCK = (By.CSS_SELECTOR, 'div.scrollbar-default.group-for-group-list-item')
    PROFILE_TITLE = (By.CSS_SELECTOR, '.list-item__title')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 20)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.element_to_be_clickable(self.START_BTN))

    def login(self, email, code, ws_name):
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
        target_block = None
        for block in ws_blocks:
            try:
                title = block.find_element(*self.WS_TITLE)
                if ws_name in title.text:
                    target_block = block
                    break
            except:
                continue
        assert target_block is not None
        login_btn = target_block.find_element(*self.LOGIN_BTN)
        login_btn.click()

    def close_modal(self):
        try:
            close_btn = self.wait.until(EC.element_to_be_clickable(self.CLOSE_BTN))
            close_btn.click()
        except:
            pass

    def open_profile(self):
        avatar_btn = self.wait.until(EC.element_to_be_clickable(self.AVATAR_BTN))
        avatar_btn.click()
        try:
            ok_btn = self.wait.until(EC.element_to_be_clickable(self.OK_BTN))
            ok_btn.click()
            dropdown_profile_btn = self.wait.until(EC.element_to_be_clickable(self.DROPDOWN_PROFILE_BTN))
            dropdown_profile_btn.click()
        except:
            pass
        try:
            user_sidebar_btn = self.wait.until(EC.element_to_be_clickable(self.USER_SIDEBAR_BTN))
            user_sidebar_btn.click()
        except:
            pass

    def get_profile_block(self):
        return self.wait.until(EC.visibility_of_element_located(self.PROFILE_BLOCK))

    def profile_contains(self, text):
        block = self.get_profile_block()
        for el in block.find_elements(*self.PROFILE_TITLE):
            if text in el.text:
                return True
        return False 