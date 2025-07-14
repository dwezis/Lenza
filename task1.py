from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_languages():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    languages = [
        "English (США)", "English (Великобритания)",
        "Deutsch (Германия)", "Español (Испания)",
        "Français (Франция)", "Italiano (Италия)",
        "Português (Бразилия)", "Русский (Россия)",
        "العربية (Оаэ)", "日本語 (Япония)",
        "繁體中文 (Китай)", "한국어 (Корея)", "हिन्दी (Индия)"
    ]

    driver = None
    try:
        print("Запуск теста языков...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 10)
        driver.get("https://auth.lenzaos.com")
        print("Страница открыта")
        time.sleep(3)

        for i, language in enumerate(languages, 1):
            print(f"{i}/{len(languages)}: {language}")
            try:
                lang_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".lang-switch"))
                )
                try:
                    lang_button.click()
                except:
                    driver.execute_script("arguments[0].click();", lang_button)
                time.sleep(2)
                language_element = None
                selectors = [
                    f"//div[contains(text(), '{language}')]",
                    f"//div[normalize-space()='{language}']",
                    f"//*[contains(text(), '{language}')]"
                ]
                for selector in selectors:
                    try:
                        language_element = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except:
                        continue
                if language_element is None:
                    raise Exception(f"Не удалось найти элемент для языка: {language}")
                language_element.click()
                print(f"✓ Переключен на {language}")
                time.sleep(2)
            except Exception as e:
                print(f"✗ Ошибка для {language}: {e}")
                try:
                    driver.current_url
                except:
                    print("Сессия браузера потеряна, пересоздаем...")
                    driver.quit()
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    wait = WebDriverWait(driver, 10)
                    driver.get("https://auth.lenzaos.com")
                    time.sleep(3)
                    continue
                driver.refresh()
                time.sleep(3)
                continue
        print("Тест завершён")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        if driver:
            driver.quit()
            print("Браузер закрыт")

if __name__ == "__main__":
    test_languages()