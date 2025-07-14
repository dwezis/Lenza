from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_code_validation():
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
    start_selectors = [
        'button.btn--full-width',
        'button[class*="btn--full-width"]',
        '//button[contains(@class, "btn--full-width")]',
        '//button[.//span[contains(text(), "Начать")]]',
        '//button[contains(text(), "Начать")]'
    ]
    for selector in start_selectors:
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
        raise Exception("Кнопка 'Начать' не найдена")
    start_btn.click()
    print("Кнопка 'Начать' нажата")
    time.sleep(2)

    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
    email_input.clear()
    email_input.send_keys("test@test.com")
    print("Введен email: test@test.com")
    time.sleep(1)

    continue_btn = None
    continue_selectors = [
        'button.btn--full-width',
        'button[class*="btn--full-width"]',
        '//button[contains(@class, "btn--full-width")]',
        '//button[.//span[contains(text(), "Продолжить")]]',
        '//button[contains(text(), "Продолжить")]'
    ]
    for selector in continue_selectors:
        try:
            if selector.startswith('//'):
                continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            else:
                continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            print(f"Найдена кнопка продолжения с селектором: {selector}")
            break
        except:
            continue
    if continue_btn is None:
        raise Exception("Кнопка продолжения не найдена")
    continue_btn.click()
    print("Кнопка продолжения нажата")
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

    code_input = None
    code_selectors = [
        'input[type="text"]',
        'input[type="number"]',
        'input[placeholder*="код"]',
        'input[placeholder*="code"]',
        'input[class*="code"]',
        '//input[contains(@placeholder, "код")]',
        '//input[contains(@placeholder, "code")]'
    ]
    for selector in code_selectors:
        try:
            if selector.startswith('//'):
                code_input = wait.until(EC.visibility_of_element_located((By.XPATH, selector)))
            else:
                code_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            print(f"Найдено поле ввода кода с селектором: {selector}")
            break
        except:
            continue
    if code_input is None:
        print("Поле ввода кода не найдено. Выводим все input поля:")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for i, inp in enumerate(inputs):
            try:
                input_type = inp.get_attribute("type")
                placeholder = inp.get_attribute("placeholder")
                classes = inp.get_attribute("class")
                print(f"Input {i+1}: type='{input_type}', placeholder='{placeholder}', class='{classes}'")
            except:
                print(f"Input {i+1}: не удалось получить информацию")
        raise Exception("Поле ввода кода не найдено")

    back_btn = None
    try:
        back_btn = driver.find_element(By.CSS_SELECTOR, ".btn_back")
        if back_btn.is_displayed():
            print("Найдена кнопка 'Назад' по селектору .btn_back")
    except Exception as e:
        print("Кнопка 'Назад' не найдена:", e)
        back_btn = None

    if back_btn:
        print("Тестируем возврат на предыдущий этап...")
        back_btn.click()
        time.sleep(2)
        try:
            email_input_after_back = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
            print("Успешно вернулись на страницу ввода email")
            continue_btn_after_back = None
            for selector in continue_selectors:
                try:
                    if selector.startswith('//'):
                        continue_btn_after_back = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    else:
                        continue_btn_after_back = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            if continue_btn_after_back:
                continue_btn_after_back.click()
                print("Снова перешли к вводу кода")
                time.sleep(2)
                for selector in code_selectors:
                    try:
                        if selector.startswith('//'):
                            code_input = wait.until(EC.visibility_of_element_located((By.XPATH, selector)))
                        else:
                            code_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                        break
                    except:
                        continue
        except:
            print("Не удалось вернуться на страницу ввода email")
    else:
        print("Кнопка 'Назад' не найдена")

    confirm_btn = None
    confirm_selectors = [
        'button[type="submit"]',
        'button.btn--full-width',
        'button[class*="btn--full-width"]',
        '//button[contains(text(), "Подтвердить")]',
        '//button[contains(text(), "Confirm")]',
        '//button[contains(text(), "Продолжить")]',
        '//button[contains(text(), "Continue")]'
    ]
    for selector in confirm_selectors:
        try:
            if selector.startswith('//'):
                confirm_btn = driver.find_element(By.XPATH, selector)
            else:
                confirm_btn = driver.find_element(By.CSS_SELECTOR, selector)
            print(f"Найдена кнопка подтверждения с селектором: {selector}")
            break
        except:
            continue
    if confirm_btn is None:
        print("Кнопка подтверждения не найдена")

    negative_cases = [
        ("", "Введите код"),
        ("123", "Неверный код"),
        ("12345", "Неверный код"),
        ("abcdef", "Неверный код"),
        ("666554", "Неверный код"),
        ("666556", "Неверный код")
    ]
    print("\n=== Тестирование негативных сценариев ===")
    for value, expected_error in negative_cases:
        code_input.clear()
        code_input.send_keys(value)
        time.sleep(0.5)
        if confirm_btn:
            is_disabled = confirm_btn.get_attribute("disabled") is not None
            print(f"Введен код '{value}', кнопка disabled: {is_disabled}")
            if not is_disabled:
                confirm_btn.click()
                time.sleep(1)
        error_text = get_error()
        print(f"Проверка кода '{value}': ошибка = '{error_text}' (ожидалось: '{expected_error}')")
        if error_text is None and is_disabled:
            print(f"Ошибка не найдена, но кнопка неактивна - валидация работает")
        elif error_text == expected_error:
            print(f"Ошибка найдена корректно")
        else:
            print(f"ПРОБЛЕМА: Ожидалась ошибка '{expected_error}', а получили '{error_text}'")
    print("\n=== Тестирование позитивного сценария ===")
    code_input.clear()
    code_input.send_keys("666555")
    time.sleep(1)
    if confirm_btn:
        is_disabled = confirm_btn.get_attribute("disabled") is not None
        print(f"Введен правильный код '666555', кнопка disabled: {is_disabled}")
        if not is_disabled:
            confirm_btn.click()
            time.sleep(2)
            error_text = get_error()
            if error_text is None:
                print("Позитивный тест: код принят, ошибок нет")
            else:
                print(f"Позитивный тест: получена ошибка '{error_text}'")
        else:
            print("ПРЕДУПРЕЖДЕНИЕ: Кнопка остается неактивной для правильного кода")
    else:
        print("Кнопка подтверждения не найдена для позитивного теста")
    print("\nТестирование ввода кода завершено!")
    driver.quit()

if __name__ == "__main__":
    test_code_validation()
