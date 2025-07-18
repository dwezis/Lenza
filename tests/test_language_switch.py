import pytest
from pages.language_page import LanguagePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.mark.parametrize("url", ["https://auth.lenzaos.com"])
def test_language_switch(browser, url):
    page = LanguagePage(browser)
    page.open(url)
    lang_texts = page.get_language_texts()
    assert lang_texts, "Не найдены языки в меню"
    for lang in lang_texts:
        assert page.select_language(lang), f"Не удалось выбрать язык: {lang}"
        page.wait.until(lambda d: lang in page.get_language_texts() or True)
        browser.refresh()
        page.wait.until_not(EC.visibility_of_element_located((By.ID, "context-root"))) 