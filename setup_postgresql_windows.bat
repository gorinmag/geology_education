@echo off
echo ========================================
echo Настройка PostgreSQL для Django проекта
echo ========================================
echo.

REM Проверка наличия PostgreSQL в PATH
where psql >nul 2>nul
if %errorlevel% neq 0 (
    echo [ОШИБКА] PostgreSQL не найден в PATH!
    echo Убедитесь, что PostgreSQL установлен и добавлен в PATH
    echo.
    echo Типичный путь: C:\Program Files\PostgreSQL\13\bin
    echo.
    pause
    exit /b 1
)

echo [OK] PostgreSQL найден
echo.

REM Создание базы данных
echo Создание базы данных geology_db...
psql -U postgres -c "CREATE DATABASE geology_db;" 2>nul
if %errorlevel% neq 0 (
    echo База данных уже существует или ошибка создания
) else (
    echo База данных успешно создана
)

echo.
echo Настройка пользователя postgres...
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'postgres';"

echo.
echo Проверка подключения...
psql -U postgres -d geology_db -c "\dt" 2>nul
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось подключиться к базе данных
    echo.
    echo Возможные проблемы:
    echo 1. Пароль postgres неверный
    echo 2. Сервер PostgreSQL не запущен
    echo 3. База данных не создана
) else (
    echo [OK] Подключение к базе данных успешно
)

echo.
echo ========================================
echo Настройка PostgreSQL завершена
echo ========================================
pause