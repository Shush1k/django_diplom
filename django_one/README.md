# Запуск приложения Django (без Docker, Nginx, Gunicorn)

1. Настройка подключения к БД Postgres (стоит локально на машине)
2. Файл .env
   ```
   POSTGRES_USER='movie'
   POSTGRES_PASSWORD=my_secret_password
   POSTGRES_DB_NAME='movie'
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   
   DEBUG=1
   SECRET_KEY=your_secret_key_hash
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   ```

---

# Запуск приложения через Docker контейнеры (сложный вариант)

1. Настроить подключение к БД Postgres (отдельный сервер)
2. Файл .env.prod.db
    ```
    POSTGRES_USER='movie'
    POSTGRES_PASSWORD=my_secret_password
    POSTGRES_DB='movie'
    ```
3. Файл .env.prod (Host ip-адрес к БД, у меня сервер был в локальной сети)
    ```
    POSTGRES_USER='movie'
    POSTGRES_PASSWORD=my_secret_password
    POSTGRES_DB_NAME='movie'
    POSTGRES_HOST=192.168.88.135
    POSTGRES_PORT=5432
    
    DEBUG=0
    SECRET_KEY=your_secret_key_hash
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    ```
4. `docker-compose -f docker-compose.prod.yml up --build` билд приложения
