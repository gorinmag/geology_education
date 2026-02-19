server {
    listen 80;
    server_name geo-education.ru www.geo-education.ru;

    # Перенаправление на HTTPS (после установки SSL)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name geo-education.ru www.geo-education.ru;

    # SSL сертификаты (после установки через Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/geo-education.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/geo-education.ru/privkey.pem;

    # Статические файлы
    location /static/ {
        alias /home/username/geology_education/staticfiles/;
        expires 30d;
    }

    # Медиа файлы (загруженные пользователями)
    location /media/ {
        alias /home/username/geology_education/media/;
        expires 30d;
    }

    # Прокси на Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}