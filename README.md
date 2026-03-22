# Wellness Backend API

Проект Wellness — это бэкенд-система для отслеживания здоровья, питания и физической активности.

## 🚀 Деплой и доступ

Приложение развернуто на VPS сервере и доступно по следующим адресам:

*   **IP сервера**: `72.56.6.10`
*   **Админ-панель**: [http://72.56.6.10/admin/](http://72.56.6.10/admin/)
*   **Документация API (Swagger)**: [http://72.56.6.10/api/docs/](http://72.56.6.10/api/docs/)
*   **Redoc**: [http://72.56.6.10/api/redoc/](http://72.56.6.10/api/redoc/)

## 🛠 Технологический стек

*   **Framework**: Django 4.2 + Django REST Framework
*   **Database**: PostgreSQL 14
*   **Cache/Task Queue**: Redis 7
*   **Web Server**: Nginx + Uvicorn (ASGI)
*   **Containerization**: Docker & Docker Compose
*   **CI/CD**: GitHub Actions

## 📖 Документация API

Для генерации документации используется `drf-spectacular`. В Swagger UI поддерживается авторизация через JWT (Bearer Token).

1. Перейдите в `/api/docs/`.
2. Нажмите кнопку **Authorize**.
3. Введите ваш JWT токен в формате: `Bearer <your_token>`.

## 💻 Разработка и деплой

### CI/CD Pipeline
При каждом пуше в ветку `main` автоматически запускается процесс:
1. Проверка кода (Linting).
2. Запуск тестов.
3. Деплой на сервер через SSH.
4. Сборка Docker-образов и применение миграций.

### Локальный запуск
```bash
docker-compose up --build
```

### Создание суперпользователя на сервере
```bash
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```
cd wellness-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка базы данных PostgreSQL
```sql
CREATE DATABASE wellness_db;
CREATE USER wellness_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE wellness_db TO wellness_user;
```

### 4. Настройка переменных окружения
Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

Заполните `.env`:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=wellness_db
DATABASE_USER=wellness_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
REDIS_URL=redis://localhost:6379/1
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key
```

### 5. Применение миграций
```bash
python manage.py migrate
```

### 6. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 7. Запуск сервера
```bash
python manage.py runserver
```

## API Endpoints

### Аутентификация
- `POST /api/auth/register/` - Регистрация
- `POST /api/auth/login/` - Вход
- `GET /api/auth/profile/` - Профиль пользователя

### Профили
- `GET/PUT /api/profiles/` - Профиль и цели

### Дневник питания
- `GET /api/food-diary/search/?q=query` - Поиск продуктов
- `GET/POST /api/food-diary/entries/` - Записи дневника
- `GET /api/food-diary/summary/?date=YYYY-MM-DD` - Сводка калорий

### Упражнения
- `GET /api/exercises/` - Список упражнений
- `GET/POST /api/exercises/plans/` - Планы тренировок

### Прогресс
- `GET/POST /api/progress/weight/` - Замеры веса
- `GET/POST /api/progress/goals/` - Цели
- `GET /api/progress/analytics/` - Аналитика

## Тестирование
```bash
python manage.py test
```

## Развертывание
1. Установите переменные окружения для продакшена
2. Соберите статические файлы: `python manage.py collectstatic`
3. Используйте gunicorn: `gunicorn wellness_backend.wsgi:application`