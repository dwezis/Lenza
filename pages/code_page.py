from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CodePage:
    START_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    CONTINUE_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    CODE_INPUT = (By.CSS_SELECTOR, 'input[type="text"]')
    BACK_BTN = (By.CSS_SELECTOR, '.btn_back')
    CONFIRM_BTN = (By.CSS_SELECTOR, 'button[type="submit"]')
    ERROR_SELECTORS = [
        (By.CSS_SELECTOR, '.input__error'),
        (By.CSS_SELECTOR, '.error'),
        (By.CSS_SELECTOR, '.error-message'),
        (By.CSS_SELECTOR, '[class*="error"]'),
        (By.CSS_SELECTOR, '.input-error'),
        (By.CSS_SELECTOR, '.validation-error'),
        (By.XPATH, '//div[contains(@class, "error")]'),
        (By.XPATH, '//span[contains(@class, "error")]'),
        (By.XPATH, '//div[contains(text(), "Введите")]'),
        (By.XPATH, '//span[contains(text(), "Введите")]'),
    ]
    CODE_INPUTS = (By.CSS_SELECTOR, '.code-input__field')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.START_BTN))

    def click_start(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.START_BTN))
        btn.click()

    def enter_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)

    def click_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN))
        btn.click()

    def get_code_input(self):
        return self.wait.until(EC.visibility_of_element_located(self.CODE_INPUT))

    def enter_code(self, code):
        code_input = self.get_code_input()
        code_input.clear()
        code_input.send_keys(code)

    def click_confirm(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BTN))
        btn.click()

    def click_back(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.BACK_BTN))
        btn.click()

    def get_error(self):
        for by, selector in self.ERROR_SELECTORS:
            try:
                el = self.driver.find_element(by, selector)
                if el.is_displayed() and el.text.strip():
                    return el.text.strip()
            except:
                continue
        return None

    def get_code_inputs(self):
        return self.wait.until(lambda d: d.find_elements(*self.CODE_INPUTS))

    def fill_code(self, code):
        code_inputs = self.get_code_inputs()
        for inp in code_inputs:
            inp.clear()
        for i, digit in enumerate(code):
            if i < len(code_inputs):
                code_inputs[i].click()
                code_inputs[i].send_keys(digit) 