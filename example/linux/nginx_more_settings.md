# Основной контекст nginx (вне server блоков)
# Включение сжатия gzip для уменьшения размера передаваемых данных
gzip on;                          # Включает gzip сжатие
gzip_vary on;                     # Добавляет заголовок Vary для прокси
gzip_min_length 1024;             # Минимальный размер для сжатия (1KB)
gzip_proxied any;                 # Сжимать ответы от проксированных серверов
gzip_comp_level 6;                # Уровень сжатия (1-9, 6 - оптимальный)
gzip_types                        # Типы файлов для сжатия
    application/atom+xml
    application/javascript
    application/json
    application/ld+json
    application/manifest+json
    application/rss+xml
    application/vnd.geo+json
    application/vnd.ms-fontobject
    application/x-font-ttf
    application/x-web-app-manifest+json
    application/xhtml+xml
    application/xml
    font/opentype
    image/bmp
    image/svg+xml
    image/x-icon
    text/cache-manifest
    text/css
    text/plain
    text/vcard
    text/vnd.rim.location.xloc
    text/vtt
    text/x-component
    text/x-cross-domain-policy;

# Зона для ограничения запросов (защита от DDoS)
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;  # 10 запросов в секунду с одного IP

# настройки сервера
server {
    # Блок виртуального сервера
    listen 80 default_server;      # Слушать порт 80 для IPv4 как сервер по умолчанию
    listen [::]:80 default_server; # Слушать порт 80 для IPv6 как сервер по умолчанию
    
    server_name example.com www.example.com;  # Домены сервера
    
    # Безопасность - скрыть версию nginx в заголовках
    server_tokens off;
    
    # Заголовки безопасности
    add_header X-Frame-Options "SAMEORIGIN" always;         # Защита от clickjacking
    add_header X-XSS-Protection "1; mode=block" always;     # Защита от XSS
    add_header X-Content-Type-Options "nosniff" always;     # Запрет смены MIME-типов
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;  # Контроль реферера
    
    # Максимальный размер загружаемых файлов
    client_max_body_size 10M;
    
    # Обслуживание статических файлов Django
    location /static/ {
        alias /home/user/django/static/;  # Физический путь к статическим файлам
        
        # Кэширование в браузере - 1 год (файлы с хэшем в имени)
        expires 1y;
        add_header Cache-Control "public, immutable";  # immutable - файлы не меняются
        add_header Vary "Accept-Encoding";             # Учитывать кодировку
        
        # Запрет выполнения скриптов в статических файлах
        location ~* \.(php|py|pl)$ {
            deny all;
        }
    }
    
    # Обслуживание медиа-файлов Django
    location /media/ {
        alias /home/user/django/media/;    # Физический путь к медиа-файлам
        
        # Кэширование в браузере - 30 дней (файлы могут обновляться)
        expires 30d;
        add_header Cache-Control "public";  # Кэшировать, но без immutable
        add_header Vary "Accept-Encoding";
        
        # Запрет выполнения скриптов
        location ~* \.(php|py|pl)$ {
            deny all;
        }
    }
    
    # Защита от доступа к скрытым и системным файлам
    location ~ /\. {
        deny all;                    # Запретить доступ
        access_log off;              # Не логировать
        log_not_found off;           # Не логировать 404
    }
    
    location ~* (\.env|\.git|\.htaccess|\.bak) {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Защита от common exploits и ботов
    location ~* (wp-admin|phpmyadmin|administrator) {
        deny all;
    }
    
    # Health check endpoint (для мониторинга)
    location /health/ {
        access_log off;              # Не логировать health checks
        proxy_pass http://127.0.0.1:8000/health/;  # Проксировать на бэкенд
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # API endpoints с rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;  # Ограничение 10 r/s с burst до 20

                # zone=api - указывает на зону, которую мы создали ранее с помощью limit_req_zone.
                # burst=20 - позволяет обрабатывать до 20 запросов сверх лимита (10 r/s) в очереди.
                # nodelay - означает, что эти 20 запросов обрабатываются без задержки, но затем запросы сверх этого будут отклоняться.

                # Пояснение:
                # Без nodelay запросы, превышающие лимит, будут обрабатываться с задержкой, чтобы соответствовать заданной скорости.
                # С nodelay первые 20 запросов (в дополнение к 10 в секунду) обрабатываются сразу, но затем, пока очередь не очистится,
                # новые запросы сверх лимита будут отклоняться с кодом 503.
        
        proxy_pass http://127.0.0.1:8000;     # Проксировать на Django
        include proxy_params;                  # Включить общие proxy настройки
    }
    
    # Основное приложение - все остальные запросы
    location / {
        proxy_pass http://127.0.0.1:8000;     # Проксировать на Gunicorn/UWSGI
        
        # Основные proxy заголовки
        proxy_set_header Host $http_host;              # Оригинальный Host
        proxy_set_header X-Real-IP $remote_addr;       # Реальный IP клиента
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # Цепочка прокси
        proxy_set_header X-Forwarded-Proto $scheme;    # Оригинальный протокол
        proxy_set_header X-Forwarded-Host $server_name;# Имя сервера
        
        # Отключить перенаправления от бэкенда
        proxy_redirect off;
        
        # Настройки буферизации для улучшения производительности
        proxy_buffering on;                   # Включить буферизацию
        proxy_buffer_size 4k;                 # Размер буфера для заголовков
        proxy_buffers 8 4k;                   # 8 буферов по 4KB
        proxy_busy_buffers_size 8k;           # Размер busy буферов
        
        # Таймауты
        proxy_connect_timeout 30s;            # Таймаут подключения к бэкенду
        proxy_send_timeout 30s;               # Таймаут отправки данных бэкенду
        proxy_read_timeout 30s;               # Таймаут чтения ответа от бэкенда
        
        # Дополнительные заголовки
        add_header P3P 'CP="ALL DSP COR PSAa OUR NOR ONL UNI COM NAV"';  # Для старых браузеров
        add_header Access-Control-Allow-Origin *;      # CORS - разрешить все домены
    }
    
    # Обработка ошибок - кастомные страницы
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /404.html {
        root /usr/share/nginx/html;           # Путь к статическим HTML страницам ошибок
        internal;                             # Только для внутренних redirect'ов
    }
    
    location = /50x.html {
        root /usr/share/nginx/html;
        internal;
    }
}

# Дополнительный файл proxy_params (если используется include)
# /etc/nginx/proxy_params: