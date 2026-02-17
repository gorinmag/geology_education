@echo off
chcp 1251 >nul
title Запуск сервера Geology Education
color 0A

echo ========================================
echo    ЗАПУСК СЕРВЕРА GEOLOGY EDUCATION
echo ========================================
echo.

REM Проверка наличия виртуального окружения
if not exist venv (
    echo [ОШИБКА] Виртуальное окружение не найдено!
    echo Запустите сначала deploy_windows.bat
    pause
    exit /b 1
)

REM Активация виртуального окружения
echo Активация виртуального окружения...
call venv\Scripts\activate.bat
echo [OK]
echo.

REM Проверка наличия миграций
echo Проверка миграций...
python manage.py showmigrations | findstr "\[ \]" >nul
if %errorlevel% neq 0 (
    echo Применение миграций...
    python manage.py migrate
)
echo [OK]
echo.

REM Сбор статических файлов
echo Сбор статических файлов...
python manage.py collectstatic --noinput
echo [OK]
echo.

REM Запуск сервера
echo Запуск сервера разработки...
echo.
echo Сервер будет доступен по адресу: http://127.0.0.1:8000/
echo Для остановки нажмите Ctrl+C
echo.
echo ========================================
echo.

python manage.py runserver

if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Сервер остановлен с ошибкой
    pause
)