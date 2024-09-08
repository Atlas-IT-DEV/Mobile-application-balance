@echo off

:: Деактивация активной среды
call .\venv\Scripts\deactivate.bat

:: Проверка на локальные модули
python.exe .\setup\check_local_modules.py --no_question

:: Активация виртуальной среды
call .\venv\Scripts\activate.bat
set PATH=%PATH%;%~dp0venv\Lib\site-packages\torch\lib

:: Валидация requirements
python.exe .\setup\validate_requirements.py

:: Очистка setup.log (если требуется)
python.exe .\clear_setup_log.py

:: Запуск сервера main.py.
if %errorlevel% equ 0 (
    REM Проверка, был ли батник запущен двойным кликом
    if /i "%comspec% /c %~0 " equ "%cmdcmdline:"=%" (
        REM echo Этот скрипт запущен с помощью двойного нажатия.
        cmd /k pytest
    ) else (
        REM echo Этот скрипт был запущен с помощью командной строки.
        pytest
    )
)