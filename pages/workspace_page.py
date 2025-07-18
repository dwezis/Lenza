from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WorkspacePage:
    START_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    CONTINUE_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    CODE_INPUTS = (By.CSS_SELECTOR, '.code-input__field')
    WS_BLOCK = (By.CLASS_NAME, 'ws_workspace__accounts_new_item')
    WS_HEADER = (By.XPATH, "//*[contains(text(), 'Выбор рабочего пространства')]")
    CREATE_WS_HEADER = (By.XPATH, "//h1 | //h2 | //div[contains(text(), 'Рабочее пространство') or contains(text(), 'Workspace')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.element_to_be_clickable(self.START_BTN))

    def login(self, email, code):
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

    def find_create_ws_block(self):
        ws_blocks = self.driver.find_elements(*self.WS_BLOCK)
        for block in ws_blocks:
            if "Создать новое пространство" in block.text:
                return block
        return None

    def click_create_ws_block(self):
        block = self.find_create_ws_block()
        if block:
            block.click()
            self.wait.until(EC.presence_of_element_located(self.CREATE_WS_HEADER))
            return True
        return False 