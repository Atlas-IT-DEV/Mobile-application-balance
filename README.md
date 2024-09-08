<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=100&size=32&pause=1000&center=true&vCenter=true&multiline=true&repeat=false&random=false&width=950&lines=Airpods" alt="Typing SVG" /></a>

---

Краткая инструкция по запуску

## Структура репозитория

**server**
```
    .
    ├── logs # - папка храенения логов
    |   ├── setup #
    |   |   ├── *.log #
    |   └── app.log #
    ├── setup - кастомный установщик среды
    |   ├── check_local_modules.py - проверка локальных модулей
    |   ├── debug_info.py - вывод информации
    |   ├── setup_common.py
    |   ├── setup_windows.py - установочное меню
    |   └── validate_requirements.py - валидация модулей
    ├── src
    |   ├── database
    |   |   ├── models.py - модели
    |   |   └── my_connector.py - класс для подключения к базе данных
    |   ├── repository - репозитории
    |   |   ├── category_repository.py
    |   |   ├── characteristic_repository.py
    |   |   ├── company_repository.py
    |   |   ├── currency_repository.py
    |   |   ├── image_comment_repository.py
    |   |   ├── image_product_repository.py
    |   |   ├── image_repository.py
    |   |   ├── order_product_repository.py
    |   |   ├── order_repository.py
    |   |   ├── order_product_repository.py
    |   |   ├── product_characteristic_repository.py
    |   |   ├── product_comment_repository.py
    |   |   ├── product_repository.py
    |   |   ├── promotion_repository.py
    |   |   └── user_repository.py
    |   ├── service - сервисы
    |   |   ├── category_services.py
    |   |   ├── characteristic_services.py
    |   |   ├── company_services.py
    |   |   ├── currency_services.py
    |   |   ├── file_services.py
    |   |   ├── image_comment_services.py
    |   |   ├── image_product_services.py
    |   |   ├── image_services.py
    |   |   ├── order_product_services.py
    |   |   ├── product_characteristic_services.py
    |   |   ├── product_comment_services.py
    |   |   ├── product_services.py
    |   |   ├── promotion_services.py
    |   |   └── user_services.py
    |   ├── utils
    |   |   ├── custom_logging.py - кастомный лог
    |   |   ├── exam_services.py - проверка на дубликаты
    |   |   ├── hashing.py - хеширование паролей
    |   |   ├── return_url_object.py - скрипт для формирования ссылок на изображения
    |   |   └── write_file_into_server.py - запись файлов на сервер
    |   └── validator
    |   |   └── validate.py - валидация моделей
    ├── venv - виртуальная среда
    ├── .env - переменные среды
    ├── .gitignore
    ├── Airpods.sql - файл с базой данных
    ├── Airpods.svg # 
    ├── clear_setup_log - очистка логов
    ├── config.py - скрипт для работы с переменными средами
    ├── create_sql.py - скрипт для авто создания и заполнения базы данных
    ├── Create_SQL.txt # 
    ├── Insert_SQL.txt # 
    ├── logging.yaml - конфигурационный файл для лога
    ├── main.bat - запуск сервера на windows
    ├── main.py
    ├── main.sh - запуск сервера на linux
    ├── requirements.txt
    ├── setup.bat - установка среды на windows
    ├── setup.log # - файл лога
    ├── setup.sh - установка среды на linux
    ├── test_image.png - тестовое изображение
    ├── test_main.bat - тесты на windows
    ├── test_main.py
    └── test_main.sh - тесты на linux
```

  ## Требования
- Python 3.8+ (установлен на сервере)
- `pm2` (для управления процессами сервера на Linux/MacOS)

## Установка и настройка

### 1. Установка виртуальной среды и зависимостей

#### Linux/MacOS

1. Клонируйте репозиторий на сервер:
    ```bash
    git clone https://github.com/username/repo.git
    cd repo
    ```

2. Запустите скрипт для установки виртуальной среды и всех необходимых зависимостей:
    ```bash
    bash setup.sh
    ```

#### Windows

1. Клонируйте репозиторий на сервер:
    ```bash
    git clone https://github.com/username/repo.git
    cd repo
    ```

2. Запустите скрипт для установки виртуальной среды и всех необходимых зависимостей:
    ```cmd
    setup.bat
    ```

### 2. Запуск тестов

#### Linux/MacOS

Для запуска автоматической проверки тестов с использованием `pytest`, выполните:
```bash
bash test_main.sh
