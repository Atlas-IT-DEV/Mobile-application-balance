#!/bin/bash

# Загрузка HOST из .env файла
source .env
echo "$HOST"

# Деактивация активной среды, если таковая есть
if [ -f "./venv/bin/activate" ]; then
    deactivate 2>/dev/null
fi

# Проверка локальных модулей
python3 ./setup/check_local_modules.py --no_question

# Активация виртуальной среды
# source ./venv/bin/activate

# shellcheck disable=SC2155
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$(pwd)/venv/lib/python3.9/site-packages/torch/lib"

# Валидация requirements
python3 ./setup/validate_requirements.py

# Очистка setup.log
python3 clear_setup_log.py

# Запуск webui.py скрипта с веб интерфейсом, если предыдущие шаги прошли успешно
# shellcheck disable=SC2181
if [ $? -eq 0 ]; then
    # Проверка, был ли скрипт запущен двойным кликом или из командной строки
    # shellcheck disable=SC2128
    if [[ "$0" != "$BASH_SOURCE" ]]; then
        # Этот скрипт был запущен в контексте GUI (эквивалент двойного клика)
        echo "Этот скрипт был запущен в графическом интерфейсе."
        pm2 start "uvicorn main:app --host $HOST"
    else
        # Этот скрипт был запущен из командной строки
        echo "Этот скрипт был запущен из командной строки."
        pm2 start "uvicorn main:app --host $HOST"
    fi
fi
