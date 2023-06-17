### Nginx configuration

Dockerfile
-
```dockerfile
FROM nginx:1.21-alpine

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
```

Собираем образ и копируем файл с настройками, заменив настройки по умолчанию на настройке в файле `nginx.conf`.

Файл nginx.conf
-
```
upstream django_one {
    server web:8001;
}

server {

    listen 80;

    location / {
        proxy_pass http://django_one;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /app/static/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```
upstream определяет, куда nginx будет отправлять запросы после их получения.  
Содержит список серверов и их IP-адреса, однако в нашем случае docker-compose создает сеть между контейнерами, поэтому мы можем указать имя сервиса `web` и порт `8001`  
Выбираем свободный порт **8001**, так как на 8000 порту уже запущен portainer контейнер (Веб-интерфейс для управления контейнерами)  
Также стоит помнить, что при старте веб-сервера gunicorn мы уже указали данный порт в файле `entrypoint.sh`. Таким образом, мы связываем nginx с нашим gunicorn веб-сервером.

entrypoint.sh
-
```shell
#!/bin/sh

python manage.py collectstatic --no-input

gunicorn django_one.wsgi:application -b 0.0.0.0:8001
```

Далее идет настройка nginx сервера, здесь мы указываем порт `80`, на который будут отправляться запросы при взаимодействии с сервисом. 
Переменная `proxy_pass` указывает куда отправлять полученный трафик.  
Также важно указать, статическую и медиа папку, поскольку nginx будет отвечать за раздачу изображений, стилей и скриптов. Для этого указываем путь к папкам в `doсker-compose` файле и `nginx.conf`, в нашем случае `/app/static/` и `/app/media/`.

docker-compose.prod.yml
-
```yaml
version: '3.8'

services:
  web:
    container_name: gunicorn_django
    build:
      context: .
    volumes:
      - static:/app/static/
      - media:/app/media/
    expose:
      - 8001
    env_file:
      - .env.prod
    depends_on:
      - db
  db:
    container_name: postgres
    image: postgres:15
    volumes:
      - learn_django_postgres_data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"
    env_file:
      - .env.prod.db
  nginx:
    container_name: nginx
    build: ./nginx
    volumes:
      - static:/app/static/
      - media:/app/media
    ports:
      - "80:80"
    depends_on:
      - web
volumes:
  learn_django_postgres_data:
    external: true
  static:
  media:
```
