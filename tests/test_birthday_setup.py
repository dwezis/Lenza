import pytest
from pages.birthday_page import BirthdayPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import random

@pytest.mark.parametrize("url", ["https://auth.lenzaos.com/ru?spm=a2ty_o01.29997173.0.0.429ec921JCvaii"])
def test_birthday_setup(browser, url):
    page = BirthdayPage(browser)
    page.open(url)
    page.login_and_join_workspace("test@test.com", "666555", "")
    assert page.click_create_workspace_block("Создать новое пространство")
    valid_name = f"MyCompany{random.randint(10000, 99999)}"
    name_input = browser.find_element(By.CSS_SELECTOR, 'input#domain-company')
    name_input.clear()
    name_input.send_keys(valid_name)
    name_input.send_keys(Keys.TAB)
    continue_btn = page.get_continue_btn()
    page.wait.until(lambda d: not continue_btn.get_attribute("disabled"))
    continue_btn.click()
    page.fill_profile("Тест", "Пользователь")
    page.set_birthday("15", "Июнь", "2000")
    continue_btn = page.get_birthday_continue_btn()
    is_disabled = continue_btn.get_attribute("disabled") is not None
    assert not is_disabled
    continue_btn.click() 