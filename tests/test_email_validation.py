import pytest
from pages.email_page import EmailPage

@pytest.mark.parametrize("url", ["https://auth.lenzaos.com/ru"])
def test_email_validation(browser, url):
    page = EmailPage(browser)
    page.open(url)
    page.click_start()
    email_input = page.get_email_input()
    continue_btn = page.get_continue_btn()
    negative_cases = [
        ("", "Введите email"),
        ("test", "Введите корректный email"),
        ("test@", "Введите корректный email"),
        ("test@domain", "Введите корректный email"),
        ("@domain.com", "Введите корректный email"),
        ("test@domain..com", "Введите корректный email"),
    ]
    for value, expected_error in negative_cases:
        email_input.clear()
        email_input.send_keys(value)
        browser.implicitly_wait(1)
        is_disabled = continue_btn.get_attribute("disabled") is not None
        if not is_disabled:
            continue_btn.click()
        error_text = page.get_error()
        assert (error_text and expected_error in error_text) or (error_text is None and is_disabled)
    email_input.clear()
    email_input.send_keys("test@example.com")
    browser.implicitly_wait(1)
    is_disabled = continue_btn.get_attribute("disabled") is not None
    if not is_disabled:
        continue_btn.click()
        error_text = page.get_error()
        assert error_text is None
    else:
        error_text = page.get_error()
        assert error_text is None 