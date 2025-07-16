from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys

def test_workspace_name():
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

    start_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn--full-width')))
    start_btn.click()
    print("Кнопка 'Начать' нажата")
    time.sleep(1)

    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
    email_input.clear()
    email_input.send_keys("test@test.com")
    print("Введен email: test@test.com")
    time.sleep(1)

    continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn--full-width')))
    continue_btn.click()
    print("Кнопка 'Продолжить' нажата")
    time.sleep(1)

    code_inputs = wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, ".code-input__field"))
    code = "666555"
    for i, digit in enumerate(code):
        code_inputs[i].clear()
        code_inputs[i].send_keys(digit)
    print("Введён код 666555")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Выбор рабочего пространства')]")))

    def find_create_ws_block(driver):
        ws_blocks = driver.find_elements(By.CLASS_NAME, "ws_workspace__accounts_new_item")
        for block in ws_blocks:
            if "Создать новое пространство" in block.text:
                return block
        return None

    target_block = WebDriverWait(driver, 15).until(find_create_ws_block)
    if target_block is None:
        print("Не найден блок 'Создать новое пространство'")
        driver.quit()
        return

    try:
        target_block.click()
        print("Клик по блоку 'Создать новое пространство' выполнен")
    except Exception as e:
        print(f"Не удалось кликнуть по блоку: {e}")
        driver.quit()
        return

    name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#domain-company')))
    long_wait = WebDriverWait(driver, 20)
    continue_btn = long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn--full-width')))
    back_btn = long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.d_domain__back-link')))
    back_btn.click()
    print("Клик по кнопке 'Назад' выполнен")
    time.sleep(1)
    driver.forward()
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Выбор рабочего пространства')]")))

    def find_create_ws_block_after_back(driver):
        ws_blocks = driver.find_elements(By.CLASS_NAME, "ws_workspace__accounts_new_item")
        for block in ws_blocks:
            if "Создать новое пространство" in block.text:
                return block
        return None

    target_block = WebDriverWait(driver, 15).until(find_create_ws_block_after_back)
    if target_block is None:
        print("Не найден блок 'Создать новое пространство' после возврата")
        driver.quit()
        return

    try:
        target_block.click()
        print("Клик по блоку 'Создать новое пространство' после возврата выполнен")
    except Exception as e:
        print(f"Не удалось кликнуть по блоку после возврата: {e}")
        driver.quit()
        return

    continue_btn = long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn--full-width')))

    negative_cases = [
        ("", "required"),
        ("Тест", "Latin characters only"),
        ("@#$%", "Latin characters only"),
        ("a", "too short"),
        ("veryveryveryveryveryveryveryverylongname", "too long")
    ]
    for value, expected_error in negative_cases:
        name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#domain-company')))
        name_input.clear()
        name_input.send_keys(value)
        time.sleep(0.5)
        is_disabled = continue_btn.get_attribute("disabled") is not None
        print(f"Введено '{value}', кнопка disabled: {is_disabled}")
        error_text = None
        error_selectors = [
            '.input__error', '.error', '.error-message', '[class*="error"]', '.input-error', '.validation-error',
            '//div[contains(@class, "error")]', '//span[contains(@class, "error")]',
            '//div[contains(text(), "Latin")]', '//span[contains(text(), "Latin")]'
        ]
        for selector in error_selectors:
            try:
                if selector.startswith('//'):
                    error = driver.find_element(By.XPATH, selector)
                else:
                    error = driver.find_element(By.CSS_SELECTOR, selector)
                if error.is_displayed() and error.text.strip():
                    error_text = error.text.strip()
                    break
            except:
                continue
        print(f"Проверка '{value}': ошибка = '{error_text}' (ожидалось: '{expected_error}')")
        if error_text and expected_error in error_text:
            print("Ошибка найдена корректно")
        elif is_disabled:
            print("Ошибка не найдена, но кнопка неактивна — валидация работает")
        else:
            print(f"ПРОБЛЕМА: Ожидалась ошибка '{expected_error}', а получили '{error_text}'")
        time.sleep(0.5)

    valid_name = "MyCompany2024"
    name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#domain-company')))
    name_input.clear()
    name_input.send_keys(valid_name)
    time.sleep(0.5)
    time.sleep(5)
    is_disabled = continue_btn.get_attribute("disabled") is not None
    print(f"Введено валидное имя '{valid_name}', кнопка disabled: {is_disabled}")
    if not is_disabled:
        continue_btn.click()
        print("Переход к следующему этапу с валидным именем выполнен")
        driver.back()
        time.sleep(1)
    else:
        print("ПРОБЛЕМА: Кнопка неактивна для валидного имени!")
    print("\nТестирование этапа имени воркспейса завершено!")
    driver.quit()

if __name__ == "__main__":
    test_workspace_name()
