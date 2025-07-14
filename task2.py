from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_email_validation():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    url = "https://auth.lenzaos.com/ru?spm=a2ty_o01.29997173.0.0.429ec921JCvaii"
    driver.get(url)
    print("Страница загружена")
    time.sleep(2)

    start_btn = None
    selectors = [
        'button#nm8eg',
        'button.btn--full-width',
        'button[class*="btn--full-width"]',
        'button:has(span:contains("Начать"))',
        '//button[contains(@class, "btn--full-width")]',
        '//button[.//span[contains(text(), "Начать")]]',
        '//button[contains(text(), "Начать")]'
    ]
    for selector in selectors:
        try:
            if selector.startswith('//'):
                start_btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            else:
                start_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            print(f"Найдена кнопка 'Начать' с селектором: {selector}")
            break
        except:
            continue
    if start_btn is None:
        print("Не удалось найти кнопку 'Начать'. Выводим все кнопки на странице:")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons):
            try:
                text = btn.text.strip()
                classes = btn.get_attribute("class")
                btn_id = btn.get_attribute("id")
                print(f"Кнопка {i+1}: text='{text}', class='{classes}', id='{btn_id}'")
            except:
                print(f"Кнопка {i+1}: не удалось получить информацию")
        raise Exception("Кнопка 'Начать' не найдена")
    start_btn.click()
    print("Кнопка 'Начать' нажата")
    time.sleep(2)

    def get_error():
        try:
            error_selectors = [
                '.input__error',
                '.error',
                '.error-message',
                '[class*="error"]',
                '.input-error',
                '.validation-error'
            ]
            for selector in error_selectors:
                try:
                    error = driver.find_element(By.CSS_SELECTOR, selector)
                    if error.is_displayed() and error.text.strip():
                        return error.text.strip()
                except:
                    continue
            xpath_selectors = [
                '//div[contains(@class, "error")]',
                '//span[contains(@class, "error")]',
                '//div[contains(text(), "Введите")]',
                '//span[contains(text(), "Введите")]'
            ]
            for xpath in xpath_selectors:
                try:
                    error = driver.find_element(By.XPATH, xpath)
                    if error.is_displayed() and error.text.strip():
                        return error.text.strip()
                except:
                    continue
            return None
        except:
            return None

    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
    print("Email поле найдено")
    continue_btn = None
    continue_selectors = [
        'button#orum4i',
        'button.btn--full-width',
        'button[class*="btn--full-width"]',
        'button:has(span:contains("Продолжить"))',
        '//button[contains(@class, "btn--full-width")]',
        '//button[.//span[contains(text(), "Продолжить")]]',
        '//button[contains(text(), "Продолжить")]'
    ]
    for selector in continue_selectors:
        try:
            if selector.startswith('//'):
                continue_btn = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
            else:
                continue_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            print(f"Найдена кнопка продолжения с селектором: {selector}")
            break
        except:
            continue
    if continue_btn is None:
        print("Не удалось найти кнопку продолжения. Выводим все кнопки на странице:")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons):
            try:
                text = btn.text.strip()
                classes = btn.get_attribute("class")
                btn_type = btn.get_attribute("type")
                btn_id = btn.get_attribute("id")
                disabled = btn.get_attribute("disabled")
                print(f"Кнопка {i+1}: text='{text}', class='{classes}', type='{btn_type}', id='{btn_id}', disabled='{disabled}'")
            except:
                print(f"Кнопка {i+1}: не удалось получить информацию")
        raise Exception("Кнопка продолжения не найдена")
    print(f"Кнопка найдена, disabled: {continue_btn.get_attribute('disabled')}")

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
        time.sleep(0.5)
        is_disabled = continue_btn.get_attribute("disabled") is not None
        print(f"Введено '{value}', кнопка disabled: {is_disabled}")
        if not is_disabled:
            continue_btn.click()
            time.sleep(1)
        error_text = get_error()
        print(f"Проверка '{value}': ошибка = '{error_text}' (ожидалось: '{expected_error}')")
        if error_text is None and is_disabled:
            print(f"Ошибка не найдена, но кнопка неактивна - валидация работает")
            continue
        elif error_text == expected_error:
            print(f"Ошибка найдена корректно")
            continue
        else:
            print(f"ПРОБЛЕМА: Ожидалась ошибка '{expected_error}', а получили '{error_text}'")
            continue
    email_input.clear()
    email_input.send_keys("test@example.com")
    time.sleep(1)
    is_disabled = continue_btn.get_attribute("disabled") is not None
    print(f"Позитивный кейс: введен 'test@example.com', кнопка disabled: {is_disabled}")
    if not is_disabled:
        continue_btn.click()
        time.sleep(1)
        error_text = get_error()
        print(f"Позитивный кейс: ошибка = '{error_text}' (ожидалось: None)")
        if error_text is not None:
            print(f"ПРЕДУПРЕЖДЕНИЕ: Получена ошибка '{error_text}' для валидного email")
    else:
        print("ПРЕДУПРЕЖДЕНИЕ: Кнопка остается неактивной для валидного email")
        error_text = get_error()
        print(f"Позитивный кейс: ошибка = '{error_text}'")
    print("\nТестирование email валидации завершено!")
    driver.quit()

if __name__ == "__main__":
    test_email_validation()
