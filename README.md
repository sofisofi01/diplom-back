# Wellness Backend - Инструкция по запуску

## Требования
- Python 3.8+
- PostgreSQL 12+
- Redis 6+

## Установка

### 1. Клонирование и настройка окружения
```bash
git clone <repository-url>
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