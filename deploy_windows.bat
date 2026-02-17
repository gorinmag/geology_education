@echo off
chcp 1251 >nul
title Установка проекта Geology Education
color 0A

echo ========================================
echo    УСТАНОВКА ПРОЕКТА GEOLOGY EDUCATION
echo ========================================
echo.

REM Проверка наличия Python
echo [1/8] Проверка Python...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не установлен или не добавлен в PATH
    echo Скачайте Python с https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% найден
echo.

REM Создание виртуального окружения
echo [2/8] Создание виртуального окружения...
if exist venv (
    echo Виртуальное окружение уже существует
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ОШИБКА] Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
    echo [OK] Виртуальное окружение создано
)
echo.

REM Активация виртуального окружения
echo [3/8] Активация виртуального окружения...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось активировать виртуальное окружение
    pause
    exit /b 1
)
echo [OK] Виртуальное окружение активировано
echo.

REM Обновление pip
echo [4/8] Обновление pip...
python -m pip install --upgrade pip
echo.

REM Установка зависимостей
echo [5/8] Установка зависимостей...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось установить зависимости
    echo.
    echo Попробуйте установить psycopg2-binary вместо psycopg2
    echo.
    pause
    exit /b 1
)
echo [OK] Зависимости установлены
echo.

REM Создание папок для медиа-файлов
echo [6/8] Создание папок для медиа-файлов...
if not exist media mkdir media
if not exist media\courses mkdir media\courses
if not exist media\lessons mkdir media\lessons
if not exist media\lessons\images mkdir media\lessons\images
if not exist media\lessons\videos mkdir media\lessons\videos
echo [OK] Папки созданы
echo.

REM Создание папки для статических файлов
if not exist static mkdir static
if not exist static\css mkdir static\css
if not exist static\js mkdir static\js
echo.

REM Применение миграций
echo [7/8] Применение миграций...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось применить миграции
    echo.
    echo Проверьте подключение к PostgreSQL
    pause
    exit /b 1
)
echo [OK] Миграции применены
echo.

REM Создание суперпользователя
echo [8/8] Создание суперпользователя...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin') | python manage.py shell
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось создать суперпользователя
) else (
    echo [OK] Суперпользователь создан (логин: admin, пароль: admin)
)
echo.

echo ========================================
echo    УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!
echo ========================================
echo.
echo Для запуска сервера выполните:
echo    run_server.bat
echo.
echo Или вручную:
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo Сайт будет доступен по адресу:
echo    http://127.0.0.1:8000/
echo.
echo Админ-панель:
echo    http://127.0.0.1:8000/admin/
echo    Логин: admin
echo    Пароль: admin
echo.
pause