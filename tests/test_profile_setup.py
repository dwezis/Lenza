import pytest
from pages.profile_page import ProfilePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import random
import os

@pytest.mark.parametrize("url", ["https://auth.lenzaos.com/ru?spm=a2ty_o01.29997173.0.0.429ec921JCvaii"])
def test_profile_setup(browser, url):
    page = ProfilePage(browser)
    page.open(url)
    page.wait.until(lambda d: d.find_element(*page.START_BTN).is_displayed())
    page.wait.until(lambda d: d.find_element(*page.START_BTN).is_enabled())
    browser.find_element(*page.START_BTN).click()
    email_input = browser.find_element(*page.EMAIL_INPUT)
    email_input.clear()
    email_input.send_keys("test@test.com")
    browser.find_element(*page.CONTINUE_BTN).click()
    code_inputs = page.get_code_inputs()
    code = "666555"
    for inp in code_inputs:
        inp.clear()
    for i, digit in enumerate(code):
        code_inputs[i].send_keys(digit)
    page.wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Выбор рабочего пространства')]"))
    )
    assert page.click_create_workspace_block()
    valid_name = f"MyCompany{random.randint(10000, 99999)}"
    name_input = browser.find_element(By.CSS_SELECTOR, 'input#domain-company')
    name_input.clear()
    name_input.send_keys(valid_name)
    name_input.send_keys(Keys.TAB)
    continue_btn = page.get_continue_btn()
    page.wait.until(lambda d: not continue_btn.get_attribute("disabled"))
    continue_btn.click()
    page.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите имя"]')))

    valid_avatar = os.path.abspath("test_avatar.jpg")
    if os.path.exists(valid_avatar):
        assert page.upload_avatar(valid_avatar)
    invalid_avatar = os.path.abspath("test_avatar.txt")
    if os.path.exists(invalid_avatar):
        assert page.upload_avatar(invalid_avatar)
        
    page.fill_profile("Тест", "Пользователь")

    name_input = browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Введите имя"]')
    name_input.send_keys(Keys.TAB)

    continue_btn = page.get_continue_btn()
    page.wait.until(lambda d: not continue_btn.get_attribute("disabled"))
    is_disabled = continue_btn.get_attribute("disabled") is not None
    print("Кнопка disabled:", is_disabled)
    assert not is_disabled
    continue_btn.click() 