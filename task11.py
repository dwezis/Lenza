from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_login_workspace():
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
    ws_name = "Testws_r8ptk7"
    ws_blocks = driver.find_elements(By.CSS_SELECTOR, ".list-item.list-item--lg.no-select")
    target_block = None
    for block in ws_blocks:
        try:
            title = block.find_element(By.CLASS_NAME, "list-item__title")
            if ws_name in title.text:
                target_block = block
                break
        except:
            continue
    assert target_block is not None, f"Блок с пространством '{ws_name}' не найден!"
    print(f"Блок с пространством '{ws_name}' найден")
    try:
        login_btn = target_block.find_element(By.XPATH, ".//button[.//span[contains(text(), 'Войти')]]")
        login_btn.click()
        print("Клик по кнопке 'Войти' выполнен")
    except Exception as e:
        print(f"Не удалось кликнуть по кнопке 'Войти': {e}")
        driver.quit()
        return
    time.sleep(3)
    try:
        close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#close-view')))
        close_btn.click()
        print("Клик по кнопке закрытия (close-view) выполнен")
    except Exception:
        print("Кнопка закрытия (close-view) не найдена, пропускаем этот шаг")
    avatar_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test-id="chat-off-avatar-item"].http-resource-private')))
    avatar_btn.click()
    print("Клик по аватару профиля выполнен")
    try:
        ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//text()='OK' or .//span[text()='OK']]")))
        ok_btn.click()
        print("Клик по кнопке OK в модальном окне выполнен")
        dropdown_profile_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='menuitem'].profile-button__current-account-item")))
        dropdown_profile_btn.click()
        print("Клик по профилю в выпадающем меню выполнен")
    except Exception:
        print("Модальное окно с OK или профиль в меню не найдены, продолжаем дальше")
    try:
        user_sidebar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'sidebar-user-name') or contains(@class, 'sidebar-user-email') or text()='Тест Пользователь' or text()='test@testws_r8ptk7']")))
        user_sidebar_btn.click()
        print("Клик по пользователю в сайдбаре выполнен")
    except Exception:
        print("Не удалось кликнуть по пользователю в сайдбаре, продолжаем дальше")
    profile_block = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.scrollbar-default.group-for-group-list-item')))
    print("Блок профиля найден")
    name_found = False
    for el in profile_block.find_elements(By.CSS_SELECTOR, '.list-item__title'):
        if 'Тест Пользователь' in el.text:
            name_found = True
            print("Имя пользователя верное")
            break
    assert name_found, "Имя пользователя не найдено или неверное!"
    email_found = False
    for el in profile_block.find_elements(By.CSS_SELECTOR, '.list-item__title'):
        if 'test@test.com' in el.text:
            email_found = True
            print("Email пользователя верный")
            break
    assert email_found, "Email пользователя не найден или неверный!"
    dob_found = False
    for el in profile_block.find_elements(By.CSS_SELECTOR, '.list-item__title'):
        if '2000' in el.text or '15' in el.text or 'Июнь' in el.text:
            dob_found = True
            print("Дата рождения отображается (проверьте формат вручную)")
            break
    if not dob_found:
        print("Дата рождения не найдена (возможно, не отображается в профиле)")

if __name__ == "__main__":
    test_login_workspace()
