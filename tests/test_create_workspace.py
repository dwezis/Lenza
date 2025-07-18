import pytest
from pages.workspace_page import WorkspacePage

@pytest.mark.parametrize("url", ["https://auth.lenzaos.com/ru"])
def test_create_new_workspace(browser, url):
    page = WorkspacePage(browser)
    page.open(url)
    page.login("test@test.com", "666555")
    assert page.click_create_ws_block(), "Не удалось кликнуть по блоку 'Создать новое пространство' или не появилось подтверждение перехода" 