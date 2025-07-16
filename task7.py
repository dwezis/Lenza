from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def test_profile_setup():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    long_wait = WebDriverWait(driver, 20)
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
    def find_existing_ws_block(driver):
        ws_blocks = driver.find_elements(By.CSS_SELECTOR, ".list-item.list-item--lg.no-select")
        for block in ws_blocks:
            try:
                title = block.find_element(By.CLASS_NAME, "list-item__title")
                if "Mycompany2024" in title.text:
                    return block
            except:
                continue
        return None
    existing_block = WebDriverWait(driver, 15).until(find_existing_ws_block)
    if existing_block is None:
        print("Не найдено рабочее пространство 'Mycompany2024'")
        driver.quit()
        return
    try:
        join_btn = existing_block.find_element(By.XPATH, ".//button[.//span[contains(text(), 'Присоединиться')]]")
        join_btn.click()
        print("Клик по кнопке 'Присоединиться' выполнен")
    except Exception as e:
        print(f"Не удалось кликнуть по кнопке 'Присоединиться': {e}")
        driver.quit()
        return
    try:
        privacy_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Мне понятно. Вперед!')]]"))
        )
        privacy_btn.click()
        print("Клик по кнопке 'Мне понятно. Вперед!' выполнен")
    except Exception as e:
        print(f"Не удалось кликнуть по кнопке 'Мне понятно. Вперед!': {e}")
        driver.quit()
        return
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'профиль') or contains(text(), 'Профиль') or contains(text(), 'личных данных')]")))
    except:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите имя"]')))
    avatar_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.avatar__img-upload-input')))
    valid_avatar = os.path.abspath("test_avatar.jpg")
    if os.path.exists(valid_avatar):
        avatar_input.send_keys(valid_avatar)
        print("Валидная аватарка загружена")
        time.sleep(1)
    else:
        print("Валидная аватарка не найдена, пропускаем тест загрузки")
    invalid_avatar = os.path.abspath("test_avatar.txt")
    if os.path.exists(invalid_avatar):
        try:
            avatar_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.avatar__img-upload-input')))
            avatar_input.send_keys(invalid_avatar)
            print("Невалидная аватарка (txt) отправлена, проверьте появление ошибки")
            time.sleep(1)
        except Exception as e:
            print(f"Input для загрузки аватарки не найден после загрузки валидной: {e}. Пропускаем негативный тест.")
    else:
        print("Файл test_avatar.txt не найден, пропускаем негативный тест аватарки")
    first_name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите имя"]')))
    first_name_input.clear()
    first_name_input.send_keys("Тест")
    print("Введено имя пользователя")
    time.sleep(0.5)
    last_name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите фамилию"]')))
    last_name_input.clear()
    last_name_input.send_keys("Пользователь")
    print("Введена фамилия пользователя")
    time.sleep(0.5)
    continue_btn = long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn--full-width')))
    is_disabled = continue_btn.get_attribute("disabled") is not None
    print(f"Кнопка Continue активна: {not is_disabled}")
    if not is_disabled:
        continue_btn.click()
        print("Переход к следующему этапу профиля выполнен")
    else:
        print("ПРОБЛЕМА: Кнопка Continue не активна после заполнения профиля!")
    print("\nТестирование этапа профиля завершено!")
    driver.quit()

if __name__ == "__main__":
    test_profile_setup()
