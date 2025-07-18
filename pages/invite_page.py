from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

class InvitePage:
    START_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    CONTINUE_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    CODE_INPUTS = (By.CSS_SELECTOR, '.code-input__field')
    CREATE_WS_BTN = (By.XPATH, "//div[contains(@class, 'list-item__title') and span[text()='Создать новое пространство']]")
    WS_NAME_INPUT = (By.CSS_SELECTOR, 'input#domain-company')
    WS_CREATE_BTN = (By.CSS_SELECTOR, 'button.btn--full-width')
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Введите имя"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Введите фамилию"]')
    CONTINUE_BTN2 = (By.CSS_SELECTOR, 'button.btn--full-width')
    DAY_INPUT = (By.CSS_SELECTOR, 'div.small-day .select__input input')
    MONTH_INPUT = (By.CSS_SELECTOR, 'div.middle-day .select__input input')
    YEAR_INPUT = (By.CSS_SELECTOR, 'div.small-day:last-of-type .select__input input')
    BIRTH_CONTINUE_BTN = (By.CSS_SELECTOR, 'button.pr_profile__buttons_send')
    INVITE_INPUT = (By.CSS_SELECTOR, 'input#tags-row-input')
    ERROR_TAG = (By.CSS_SELECTOR, '.tags-row-tag__error')
    REMOVE_ERROR_BTN = (By.XPATH, "//span[contains(text(), 'Удалить элементы с ошибкой')]")
    TAG_TEXT = (By.CSS_SELECTOR, '.tags-row-tag .tag__text')
    COPY_LINK_BTN = (By.XPATH, "//p[contains(@class, 'cp_copy') and contains(text(), 'Копировать ссылку')]")
    SEND_BTN = (By.CSS_SELECTOR, 'button.inu_invite__buttons_send')
    INVITE_LATER_BTN = (By.CSS_SELECTOR, 'p.inu_invite__link_skip')
    DONE_BTN = (By.XPATH, "//button[contains(@class, 'success-invite-modal__submit-button') and .//span[contains(text(), 'Готово')]]")
    SKIP_BTN = (By.CSS_SELECTOR, 'p.ch_check_skip')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 20)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.element_to_be_clickable(self.START_BTN))

    def login_and_create_workspace(self, email, code):
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
        self.wait.until(EC.element_to_be_clickable(self.CREATE_WS_BTN)).click()

    def create_workspace(self):
        rand_ws_name = 'TestWS_' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        ws_name_input = self.wait.until(EC.visibility_of_element_located(self.WS_NAME_INPUT))
        ws_name_input.clear()
        ws_name_input.send_keys(rand_ws_name)
        ws_create_btn = self.wait.until(EC.element_to_be_clickable(self.WS_CREATE_BTN))
        ws_create_btn.click()
        return rand_ws_name

    def fill_profile(self, first_name, last_name):
        first_name_input = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        last_name_input = self.wait.until(EC.visibility_of_element_located(self.LAST_NAME_INPUT))
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        continue_btn = self.long_wait.until(EC.presence_of_element_located(self.CONTINUE_BTN2))
        is_disabled = continue_btn.get_attribute("disabled") is not None
        if not is_disabled:
            continue_btn.click()

    def set_birthday(self, day, month, year):
        day_input = self.wait.until(EC.visibility_of_element_located(self.DAY_INPUT))
        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", day_input, day)
        month_input = self.wait.until(EC.visibility_of_element_located(self.MONTH_INPUT))
        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", month_input, month)
        year_input = self.wait.until(EC.visibility_of_element_located(self.YEAR_INPUT))
        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", year_input, year)
        continue_btn = self.wait.until(EC.element_to_be_clickable(self.BIRTH_CONTINUE_BTN))
        is_disabled = continue_btn.get_attribute("disabled") is not None
        if not is_disabled:
            continue_btn.click()

    def invite_invalid_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.INVITE_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        email_input.send_keys("\n")
        error_tag = self.wait.until(EC.visibility_of_element_located(self.ERROR_TAG))
        remove_error_btn = self.wait.until(EC.element_to_be_clickable(self.REMOVE_ERROR_BTN))
        remove_error_btn.click()
        error_tags = self.driver.find_elements(*self.ERROR_TAG)
        return len(error_tags) == 0

    def invite_valid_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.INVITE_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        email_input.send_keys("\n")
        error_tags = self.driver.find_elements(*self.ERROR_TAG)
        tag_texts = [el.text for el in self.driver.find_elements(*self.TAG_TEXT)]
        return len(error_tags) == 0 and any(email in t for t in tag_texts)

    def copy_link(self):
        copy_link_btn = self.wait.until(EC.element_to_be_clickable(self.COPY_LINK_BTN))
        copy_link_btn.click()
        notification_found = False
        for _ in range(10):
            for cls in ['ant-notification', 'ant-message', 'snackbar', 'toast', 'notification']:
                try:
                    notif = self.driver.find_element(By.CLASS_NAME, cls)
                    if notif.is_displayed() and notif.text.strip():
                        notification_found = True
                        break
                except:
                    continue
            try:
                notif = self.driver.find_element(By.XPATH, "//*[contains(text(), 'копирован') or contains(text(), 'Ссылка') or contains(text(), 'скопирована')]")
                if notif.is_displayed():
                    notification_found = True
                    break
            except:
                pass
            self.driver.implicitly_wait(0.3)
        return notification_found

    def send_invite(self):
        send_btn = self.wait.until(EC.presence_of_element_located(self.SEND_BTN))
        is_disabled = send_btn.get_attribute("disabled") is not None
        if not is_disabled:
            send_btn.click()
            try:
                self.driver.find_element(*self.SEND_BTN)
                form_exists = True
            except:
                form_exists = False
            return not form_exists
        return False

    def click_done(self):
        done_btn = self.wait.until(EC.element_to_be_clickable(self.DONE_BTN))
        done_btn.click()
        try:
            self.driver.find_element(*self.DONE_BTN)
            btn_still_exists = True
        except:
            btn_still_exists = False
        return not btn_still_exists

    def skip_check(self):
        skip_btn = self.wait.until(EC.element_to_be_clickable(self.SKIP_BTN))
        skip_btn.click()
        return True

    def invite_later(self):
        invite_later_btn = self.wait.until(EC.element_to_be_clickable(self.INVITE_LATER_BTN))
        invite_later_btn.click()
        try:
            self.driver.find_element(*self.INVITE_LATER_BTN)
            form_exists = True
        except:
            form_exists = False
        return not form_exists 