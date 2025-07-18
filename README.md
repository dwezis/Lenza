# UI Automation Framework (POM)

## Описание

Этот проект — фреймворк для автоматизации UI-тестирования сайта https://auth.lenzaos.com.

Покрывает сценарии:
- Авторизация и смена языка
- Валидация email и кода
- Создание нового рабочего пространства
- Заполнение профиля, даты рождения
- Приглашение участников
- Проверка входа в рабочее пространство

## Структура проекта

- `pages/` — Page Object классы для страниц
- `tests/` — тесты (pytest)
- `fixtures/` — фикстуры для pytest
- `utils/` — утилиты и хелперы

## Требования
- Python 3.8+
- Google Chrome
- chromedriver (автоматически скачивается через webdriver_manager)
- Все зависимости из `requirements.txt`

## Установка

1. Клонируйте репозиторий
2. Создайте и активируйте виртуальное окружение:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

## Запуск тестов

Запустить все тесты:
```
pytest
```

Запустить конкретный тест:
```
pytest tests/test_profile_setup.py
```

## Примеры сценариев

- **test_language_switch** — проверка смены языка интерфейса
- **test_email_validation** — валидация email (негативные и позитивные кейсы)
- **test_code_validation** — валидация кода, возврат назад, успешный ввод
- **test_workspace_name** — проверка валидации названия рабочего пространства
- **test_profile_setup** — создание профиля, загрузка аватара, заполнение имени/фамилии
- **test_birthday_setup** — заполнение даты рождения
- **test_invite_members** — приглашение участников, проверка ошибок email
- **test_login_workspace** — вход в рабочее пространство, проверка профиля

---

**Автоматизация построена на Selenium + Pytest + POM.** 