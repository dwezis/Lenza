import pytest
from pages.code_page import CodePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

@pytest.mark.parametrize("url", ["https://auth.lenzaos.com/ru"])
def test_code_validation(browser, url):
    page = CodePage(browser)
    page.open(url)
    page.click_start()
    page.enter_email("test@test.com")
    page.click_continue()
    page.click_back()
    email_input = browser.find_element(*page.EMAIL_INPUT)
    assert email_input.is_displayed()
    email_input.clear()
    email_input.send_keys("test@test.com")
    email_input.send_keys(Keys.ENTER)
    page.get_code_inputs()
    page.fill_code("666555")
    page.wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Выбор рабочего пространства')]"))
    )