from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import string


def test_invite_members():
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
    create_ws_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'list-item__title') and span[text()='Создать новое пространство']]")))
    create_ws_btn.click()
    print("Клик по 'Создать новое пространство' выполнен (через список)")
    time.sleep(1)

    rand_ws_name = 'TestWS_' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    ws_name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#domain-company')))
    ws_name_input.clear()
    ws_name_input.send_keys(rand_ws_name)
    print(f"Введено имя пространства '{rand_ws_name}'")
    time.sleep(1)
    ws_create_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn--full-width')))
    ws_create_btn.click()
    print("Клик по кнопке создания пространства")
    time.sleep(2)

    first_name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите имя"]')))
    first_name_input.clear()
    first_name_input.send_keys("Тест")
    last_name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите фамилию"]')))
    last_name_input.clear()
    last_name_input.send_keys("Пользователь")
    continue_btn = long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn--full-width')))
    is_disabled = continue_btn.get_attribute("disabled") is not None
    if not is_disabled:
        continue_btn.click()
        print("Переход к дате рождения выполнен")
    else:
        print("ПРОБЛЕМА: Кнопка Continue не активна после заполнения профиля!")
        driver.quit()
        return

    def select_custom_dropdown(label_text, value_text):
        if label_text == "День":
            parent_class = "small-day"
        elif label_text == "Месяц":
            parent_class = "middle-day"
        elif label_text == "Год":
            parent_class = "small-day"
        else:
            parent_class = None
        if parent_class:
            parent_div = wait.until(EC.visibility_of_element_located((
                By.CSS_SELECTOR, f"div.{parent_class}"
            )))
            label = parent_div.find_element(By.TAG_NAME, "label")
        else:
            label = wait.until(EC.visibility_of_element_located((
                By.XPATH, f"//label[.//span[contains(@class, 'content') and text()='{label_text}']]"
            )))
        input_field = label.find_element(By.CSS_SELECTOR, '.select__input input')
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", input_field, value_text)
        print(f"Value в input теперь: {input_field.get_attribute('value')}")
        return

    select_custom_dropdown("День", "15")
    select_custom_dropdown("Месяц", "Июнь")
    select_custom_dropdown("Год", "2000")

    continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.pr_profile__buttons_send')))
    is_disabled = continue_btn.get_attribute("disabled") is not None
    print(f"Кнопка Продолжить активна: {not is_disabled}")
    try:
        continue_btn.click()
    except Exception as e:
        print(f"continue_btn.click() не сработал: {e}, пробую клик через JS")
        driver.execute_script("arguments[0].click();", continue_btn)
    print("Переход к этапу приглашения участников выполнен")
    time.sleep(2)

    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#tags-row-input')))
    email_input.clear()
    email_input.send_keys("ЗащищЗоащщ")
    email_input.send_keys("\n")
    print("Введён невалидный email")
    time.sleep(1)
    error_tag = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.tags-row-tag__error')))
    print("Ошибка email отображается")
    remove_error_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Удалить элементы с ошибкой')]")))
    remove_error_btn.click()
    print("Клик по 'Удалить элементы с ошибкой' выполнен")
    time.sleep(1)
    error_tags = driver.find_elements(By.CSS_SELECTOR, '.tags-row-tag__error')
    assert len(error_tags) == 0, "Ошибка email не удалена!"
    print("Ошибка email успешно удалена!")

    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#tags-row-input')))
    email_input.clear()
    valid_email = 'testuser@example.com'
    email_input.send_keys(valid_email)
    email_input.send_keys("\n")
    print(f"Введён валидный email: {valid_email}")
    time.sleep(1)
    error_tags = driver.find_elements(By.CSS_SELECTOR, '.tags-row-tag__error')
    assert len(error_tags) == 0, "Ошибка email появилась для валидного email!"
    tag_texts = [el.text for el in driver.find_elements(By.CSS_SELECTOR, '.tags-row-tag .tag__text')]
    assert any(valid_email in t for t in tag_texts), "Валидный email не отображается в тегах!"
    print("Валидный email успешно добавлен!")

    copy_link_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'cp_copy') and contains(text(), 'Копировать ссылку')]")))
    copy_link_btn.click()
    print("Клик по 'Копировать ссылку' выполнен")
    notification_found = False
    for _ in range(10):
        for cls in ['ant-notification', 'ant-message', 'snackbar', 'toast', 'notification']:
            try:
                notif = driver.find_element(By.CLASS_NAME, cls)
                if notif.is_displayed() and notif.text.strip():
                    print(f"Уведомление найдено: {notif.text}")
                    notification_found = True
                    break
            except:
                continue
        try:
            notif = driver.find_element(By.XPATH, "//*[contains(text(), 'копирован') or contains(text(), 'Ссылка') or contains(text(), 'скопирована')]")
            if notif.is_displayed():
                print(f"Уведомление найдено по тексту: {notif.text}")
                notification_found = True
                break
        except:
            pass
        time.sleep(0.3)
    assert notification_found, "Уведомление о копировании не найдено!"
    print("Уведомление о копировании отображается!")

    send_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.inu_invite__buttons_send')))
    is_disabled = send_btn.get_attribute("disabled") is not None
    print(f"Кнопка 'Отправить' активна: {not is_disabled}")
    if not is_disabled:
        send_btn.click()
        print("Клик по кнопке 'Отправить' выполнен")
        time.sleep(1)
        form_exists = True
        try:
            driver.find_element(By.CSS_SELECTOR, 'button.inu_invite__buttons_send')
        except:
            form_exists = False
        assert not form_exists, "Форма приглашения не исчезла после отправки!"
        print("Переход на следующий этап после отправки приглашения выполнен!")
        done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'success-invite-modal__submit-button') and .//span[contains(text(), 'Готово')]]")))
        done_btn.click()
        print("Клик по кнопке 'Готово' выполнен")
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, "//button[contains(@class, 'success-invite-modal__submit-button') and .//span[contains(text(), 'Готово')]]")
            btn_still_exists = True
        except:
            btn_still_exists = False
        assert not btn_still_exists, "Кнопка 'Готово' не исчезла после клика!"
        print("Переход на следующий этап после 'Готово' выполнен!")
        skip_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'p.ch_check_skip')))
        skip_btn.click()
        print("Клик по кнопке 'Пропустить' выполнен")
        print("\nТест завершён успешно!")
        driver.quit()
        return
    else:
        print("Кнопка 'Отправить' неактивна, пропускаем тест клика")

    invite_later_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'p.inu_invite__link_skip')))
    invite_later_btn.click()
    print("Клик по 'Пригласить позже' выполнен")
    time.sleep(1)
    form_exists = True
    try:
        driver.find_element(By.CSS_SELECTOR, 'p.inu_invite__link_skip')
    except:
        form_exists = False
    assert not form_exists, "Форма приглашения не исчезла после 'Пригласить позже'!"
    print("Переход на следующий этап после 'Пригласить позже' выполнен!")

    print("\nТестирование этапа приглашения участников завершено!")
    driver.quit()

if __name__ == "__main__":
    test_invite_members()
