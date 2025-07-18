import pytest
from pages.login_workspace_page import LoginWorkspacePage

@pytest.mark.parametrize("url,ws_name", [("https://auth.lenzaos.com/ru?spm=a2ty_o01.29997173.0.0.429ec921JCvaii", "Testws_r8ptk7")])
def test_login_workspace(browser, url, ws_name):
    page = LoginWorkspacePage(browser)
    page.open(url)
    page.login("test@test.com", "666555", ws_name)
    page.close_modal()
    page.open_profile()
    assert page.profile_contains("Тест Пользователь")
    assert page.profile_contains("test@test.com") 