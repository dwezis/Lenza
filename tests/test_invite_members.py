import pytest
from pages.invite_page import InvitePage
from selenium.webdriver.common.by import By

@pytest.mark.parametrize("url", ["https://auth.lenzaos.com/ru?spm=a2ty_o01.29997173.0.0.429ec921JCvaii"])
def test_invite_members(browser, url):
    page = InvitePage(browser)
    page.open(url)
    page.login_and_create_workspace("test@test.com", "666555")
    ws_name = page.create_workspace()
    page.fill_profile("Тест", "Пользователь")
    page.set_birthday("15", "Июнь", "2000")
    inputs = browser.find_elements(By.TAG_NAME, "input")
    for i, inp in enumerate(inputs):
        print(f"Input {i}: id={inp.get_attribute('id')}, class={inp.get_attribute('class')}, placeholder={inp.get_attribute('placeholder')}")
    assert page.invite_invalid_email("ЗащищЗоащщ")
    assert page.invite_valid_email("testuser@example.com")
    assert page.copy_link()
    assert page.send_invite() or page.invite_later() 