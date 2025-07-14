from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_create_new_workspace():
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

    confirm_btn = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, 'button.btn--full-width[disabled=""]') or d.find_element(By.CSS_SELECTOR, 'button.btn--full-width:not([disabled])'))
    if confirm_btn.get_attribute("disabled") is None:
        confirm_btn.click()
        print("Код подтверждён")
    else:
        print("Кнопка подтверждения кода неактивна!")
        driver.quit()
        return
    time.sleep(2)

    wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Создать новое рабочее пространство')]")))
    print("Страница выбора рабочего пространства загружена")

    create_ws_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Создать новое рабочее пространство')]/ancestor::div[contains(@class, 'ns_create_new_ws')]")))
    create_ws_btn.click()
    print("Клик по 'Создать новое рабочее пространство' выполнен")

    time.sleep(2)
    print("Тест завершён: переход к созданию нового пространства выполнен")
    driver.quit()

if __name__ == "__main__":
    test_create_new_workspace()
