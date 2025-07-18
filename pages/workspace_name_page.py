from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WorkspaceNamePage:
    START_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    CONTINUE_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    CODE_INPUTS = (By.CSS_SELECTOR, '.code-input__field')
    WS_BLOCK = (By.CLASS_NAME, 'ws_workspace__accounts_new_item')
    WS_HEADER = (By.XPATH, "//*[contains(text(), 'Выбор рабочего пространства')]")
    NAME_INPUT = (By.CSS_SELECTOR, 'input#domain-company')
    BACK_BTN = (By.CSS_SELECTOR, 'p.d_domain__back-link')
    CONTINUE_BTN2 = (By.CSS_SELECTOR, 'button.btn--full-width')
    ERROR_SELECTORS = [
        (By.CSS_SELECTOR, '.input__error'),
        (By.CSS_SELECTOR, '.error'),
        (By.CSS_SELECTOR, '.error-message'),
        (By.CSS_SELECTOR, '[class*="error"]'),
        (By.CSS_SELECTOR, '.input-error'),
        (By.CSS_SELECTOR, '.validation-error'),
        (By.XPATH, '//div[contains(@class, "error")]'),
        (By.XPATH, '//span[contains(@class, "error")]'),
        (By.XPATH, '//div[contains(text(), "Latin")]'),
        (By.XPATH, '//span[contains(text(), "Latin")]'),
    ]

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 20)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.element_to_be_clickable(self.START_BTN))

    def login_and_goto_name(self, email, code):
        self.wait.until(EC.element_to_be_clickable(self.START_BTN)).click()
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()
        code_inputs = self.wait.until(lambda d: d.find_elements(*self.CODE_INPUTS))
        for i, digit in enumerate(code):
            code_inputs[i].clear()
            code_inputs[i].send_keys(digit)
        self.wait.until(EC.visibility_of_element_located(self.WS_HEADER))
        ws_blocks = self.driver.find_elements(*self.WS_BLOCK)
        for block in ws_blocks:
            if "Создать новое пространство" in block.text:
                block.click()
                break
        self.long_wait.until(EC.visibility_of_element_located(self.NAME_INPUT))

    def set_workspace_name(self, name):
        name_input = self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))
        name_input.clear()
        name_input.send_keys(name)

    def get_continue_btn(self):
        return self.long_wait.until(EC.presence_of_element_located(self.CONTINUE_BTN2))

    def get_error(self):
        for by, selector in self.ERROR_SELECTORS:
            try:
                el = self.driver.find_element(by, selector)
                if el.is_displayed() and el.text.strip():
                    return el.text.strip()
            except:
                continue
        return None

    def click_back(self):
        btn = self.long_wait.until(EC.presence_of_element_located(self.BACK_BTN))
        btn.click() 