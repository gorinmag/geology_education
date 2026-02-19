#!/bin/bash

# Применяем миграции
python manage.py migrate --noinput

# Собираем статические файлы
python manage.py collectstatic --noinput

# Создаём суперпользователя (если не существует)
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# Запускаем Gunicorn
exec gunicorn geology_education.wsgi:application --bind 0.0.0.0:8000 --workers 3