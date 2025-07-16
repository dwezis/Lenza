from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_language_switch():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    url = "https://auth.lenzaos.com"
    driver.get(url)
    time.sleep(2)

    def open_lang_menu():
        for _ in range(3):
            try:
                lang_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.lang-switch')))
                driver.execute_script("arguments[0].click()", lang_btn)
                time.sleep(0.5)
                return True
            except Exception:
                time.sleep(1)
        return False

    def collect_all_lang_texts():
        open_lang_menu()
        try:
            menu = driver.find_element(By.CLASS_NAME, "context-menu--modal")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", menu)
            time.sleep(0.5)
        except Exception:
            pass
        lang_texts = []
        seen = set()
        lang_options = driver.find_elements(By.CSS_SELECTOR, ".context-menu--modal .context-menu__option.list-item")
        for el in lang_options:
            try:
                has_flag = el.find_element(By.CSS_SELECTOR, 'svg') is not None
            except Exception:
                has_flag = False
            try:
                lang_text = el.find_element(By.CSS_SELECTOR, '.list-item__title').text.strip()
            except Exception:
                lang_text = el.text.strip()
            if has_flag and lang_text not in seen:
                lang_texts.append(lang_text)
                seen.add(lang_text)
        return lang_texts

    lang_texts = collect_all_lang_texts()
    print(f"Найдено языков: {len(lang_texts)}: {lang_texts}")

    for lang_text in lang_texts:
        open_lang_menu()
        try:
            menu = driver.find_element(By.CLASS_NAME, "context-menu--modal")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", menu)
            time.sleep(0.3)
        except Exception:
            pass
        lang_options = driver.find_elements(By.CSS_SELECTOR, ".context-menu--modal .context-menu__option.list-item")
        found = False
        for el in lang_options:
            try:
                el_text = el.find_element(By.CSS_SELECTOR, '.list-item__title').text.strip()
            except Exception:
                el_text = el.text.strip()
            if el_text == lang_text:
                el.click()
                print(f"Клик по языку: {lang_text}")
                found = True
                break
        if not found:
            print(f"Язык {lang_text} не найден в списке (возможно, уже выбран)")
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "lang-switch")))
        time.sleep(0.5)

def click_all_languages(driver):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    wait = WebDriverWait(driver, 10)
    lang_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "lang-switch")))
    lang_btn.click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "context-menu--modal")))
    language_elements = driver.find_elements(By.CSS_SELECTOR, ".context-menu--modal .context-menu__option.list-item")
    language_texts = [el.text.strip() for el in language_elements if el.text.strip()]
    print("Языки:", language_texts)

    for lang in language_texts:
        lang_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "lang-switch")))
        lang_btn.click()
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "context-menu--modal")))
        language_elements = driver.find_elements(By.CSS_SELECTOR, ".context-menu--modal .context-menu__option.list-item")
        found = False
        for el in language_elements:
            if lang in el.text:
                el.click()
                found = True
                print(f"Клик по языку: {lang}")
                break
        if not found:
            print(f"Язык {lang} не найден в списке (возможно, уже выбран)")
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "lang-switch")))
        time.sleep(0.5)
    print("Все языки были выбраны и страница перезагружена после каждого.")

if __name__ == "__main__":
    test_language_switch()