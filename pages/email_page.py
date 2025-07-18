from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EmailPage:
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    START_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    CONTINUE_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
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

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.START_BTN))

    def click_start(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.START_BTN))
        btn.click()

    def get_email_input(self):
        return self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))

    def get_continue_btn(self):
        return self.wait.until(EC.presence_of_element_located(self.CONTINUE_BTN))

    def get_error(self):
        for by, selector in self.ERROR_SELECTORS:
            try:
                el = self.driver.find_element(by, selector)
                if el.is_displayed() and el.text.strip():
                    return el.text.strip()
            except:
                continue
        return None 