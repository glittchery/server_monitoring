# Server Monitoring (Pulse)

Веб-приложение для мониторинга доступности сайтов и DNS-сервисов. Pulse регулярно выполняет HTTPS- и DNS over HTTPS-проверки, сохраняет результаты в PostgreSQL и показывает состояние сервисов, время ответа и историю проверок в удобной панели управления.

## Возможности

- регистрация и вход пользователей с JWT-аутентификацией через cookie;
- создание, редактирование и удаление мониторов;
- HTTPS- и DNS over HTTPS-проверки;
- автоматический запуск проверок с заданным интервалом;
- ручной запуск проверки из панели управления;
- хранение истории, HTTP-статусов, времени ответа и причин ошибок;
- фильтрация истории проверок по периоду;
- обзор состояния сервисов, аптайма и среднего времени ответа;
- светлая и тёмная темы интерфейса;
- демонстрационный режим, не требующий подключения к API.

## Технологии

### Backend

- Python 3.12
- FastAPI и Uvicorn
- SQLAlchemy (async)
- PostgreSQL и asyncpg
- AuthX / JWT
- HTTPX и dnspython

### Frontend

- React 19
- TypeScript
- Vite
- Radix UI
- Recharts
- Lucide Icons

## Структура проекта

```text
server_monitoring/
├── src/
│   ├── api/             # HTTP-эндпоинты и Pydantic-схемы
│   ├── database/        # модели, подключение и запросы к PostgreSQL
│   ├── monitoring/      # реализация HTTPS- и DNS-проверок
│   ├── services/        # бизнес-логика и планировщик
│   ├── auth_config.py   # конфигурация JWT из переменных окружения
│   └── main.py          # точка входа FastAPI
├── frontend/            # React-приложение
├── .env.example         # шаблон переменных окружения backend
├── compose.yaml         # PostgreSQL, backend и frontend
├── Dockerfile
├── requirements.txt
└── README.md
```

## Требования

- Python 3.12+
- PostgreSQL
- Node.js 20+ и npm — для запуска frontend в режиме разработки
- Docker — опционально

## Настройка окружения

Backend ожидает следующие переменные окружения:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_password
DB_NAME=server_monitoring
JWT_SECRET_KEY=replace_with_a_long_random_value
JWT_COOKIE_SECURE=false
```

Создайте локальный файл окружения из безопасного шаблона:

```bash
cp .env.example .env
```

Файл `.env` исключён из Git. Backend читает настройки из окружения процесса и не загружает `.env` автоматически.

Перед локальным запуском экспортируйте переменные из файла:

```bash
set -a
source .env
set +a
```

Перед публикацией замените `JWT_SECRET_KEY` на длинное случайное значение и установите `JWT_COOKIE_SECURE=true`, если приложение работает через HTTPS.

Для frontend скопируйте пример конфигурации:

```bash
cp frontend/.env.example frontend/.env
```

Переменная `BACKEND_PROXY_TARGET` задаёт адрес FastAPI-сервиса, на который dev-сервер Vite перенаправляет запросы `/api`. Клиентская переменная `VITE_API_BASE_URL` позволяет переопределить базовый URL API при сборке frontend; по умолчанию используется `/api`.

## Локальный запуск

### 1. Backend

Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установите зависимости, загрузите переменные окружения и запустите API:

```bash
pip install -r requirements.txt
set -a
source .env
set +a
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

При старте приложение создаст необходимые таблицы и запустит фоновый планировщик проверок.

После запуска доступны:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Frontend

В отдельном терминале выполните:

```bash
cd frontend
npm ci
npm run dev
```

Панель управления будет доступна по адресу `http://localhost:5173`. Если backend недоступен, интерфейс можно открыть в демонстрационном режиме.

## Запуск всего приложения в Docker

На сервере установите Docker с Compose plugin, скопируйте пример окружения и замените значения `DB_PASS` и `JWT_SECRET_KEY`:

```bash
cp .env.example .env
nano .env
```

После настройки всё приложение запускается одной командой:

```bash
docker compose up -d --build
```

Compose автоматически:

- запускает PostgreSQL с постоянным Docker volume;
- ждёт готовности базы данных;
- запускает FastAPI и проверяет `/health`;
- собирает React-приложение и раздаёт его через Nginx;
- проксирует запросы frontend с `/api` на backend.

По умолчанию приложение доступно на `http://SERVER_IP`, а Swagger UI — на `http://SERVER_IP/docs`. Порт можно изменить через `APP_PORT`, например `APP_PORT=8080` в `.env`. Для просмотра состояния и логов используйте:

```bash
docker compose ps
docker compose logs -f
```

Для обновления после получения нового кода снова выполните `docker compose up -d --build`. Остановить приложение можно командой `docker compose down`; данные PostgreSQL сохранятся в volume `pulse_postgres_data`.

## Основные API-маршруты

| Метод | Маршрут | Назначение |
|---|---|---|
| `POST` | `/api/auth/register` | Регистрация пользователя |
| `POST` | `/api/auth/login` | Вход в систему |
| `PATCH` | `/api/auth/account` | Изменение учётных данных |
| `DELETE` | `/api/auth/account` | Удаление аккаунта |
| `POST` | `/api/monitors/create_new` | Создание монитора |
| `GET` | `/api/monitors/user_monitors` | Список мониторов пользователя |
| `PATCH` | `/api/monitors/{monitor_id}` | Изменение монитора |
| `DELETE` | `/api/monitors/{monitor_id}` | Удаление монитора |
| `POST` | `/api/checks` | Ручной запуск проверки |
| `GET` | `/api/monitors/{monitor_id}/checks` | История проверок |
| `DELETE` | `/api/monitor/{monitor_id}/checks` | Удаление истории за период |

Параметры запросов и схемы ответов всегда можно посмотреть в Swagger UI.

## Демо

Публичная документация API: [server-monitoring.akarmain.ru/docs](http://server-monitoring.akarmain.ru/docs)

## Авторы

- [akarmain](https://github.com/akarmain) — frontend и deploy.
- [glittchery](https://github.com/glittchery) — backend и deploy.
