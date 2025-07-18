import pytest
from pages.workspace_name_page import WorkspaceNamePage
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

@pytest.mark.parametrize("url", ["https://auth.lenzaos.com/ru?spm=a2ty_o01.29997173.0.0.429ec921JCvaii"])
def test_workspace_name(browser, url):
    page = WorkspaceNamePage(browser)
    page.open(url)
    page.login_and_goto_name("test@test.com", "666555")
    continue_btn = page.get_continue_btn()
    negative_cases = [
        ("", "required"),
        ("Тест", "Latin characters only"),
        ("@#$%", "Latin characters only"),
        ("a", "too short")
    ]
    for value, expected_error in negative_cases:
        page.set_workspace_name(value)
        browser.implicitly_wait(1)
        is_disabled = continue_btn.get_attribute("disabled") is not None
        error_text = page.get_error()
        assert (error_text and expected_error in error_text) or is_disabled
    valid_name = f"MyCompany{random.randint(10000, 99999)}"
    page.set_workspace_name(valid_name)
    name_input = browser.find_element(By.CSS_SELECTOR, 'input#domain-company')
    name_input.send_keys(Keys.TAB)
    page.wait.until(lambda d: not continue_btn.get_attribute("disabled"))
    is_disabled = continue_btn.get_attribute("disabled") is not None
    assert not is_disabled
    continue_btn.click()

def test_workspace_name_back(browser, url="https://auth.lenzaos.com/ru?spm=a2ty_o01.29997173.0.0.429ec921JCvaii"):
    page = WorkspaceNamePage(browser)
    page.open(url)
    page.login_and_goto_name("test@test.com", "666555")
    page.get_continue_btn()
    page.click_back()
    ws_header = browser.find_element(*page.WS_HEADER)
    assert ws_header.is_displayed() 