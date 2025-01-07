## 🚀 Многосервисное FastAPI-приложение: TODO и Short URL сервисы

### 📋 Описание проекта
Итоговый проект по курсу "Основы программной инженерии" представляет собой многосервисное FastAPI-приложение, включающее два микросервиса:  
- **TODO-сервис** — Управление задачами (CRUD-операции).  
- **Short URL-сервис** — Сокращение длинных URL-адресов и редирект по коротким ссылкам.  

Оба сервиса используют SQLite для хранения данных и работают в рамках одного Docker-контейнера, управляемого через `supervisord`.  

---

## 📂 Структура итогового проекта
```
my_project/
│
├── app/
│   ├── todo_service/
│   │   └── main.py
│   ├── short_url_service/
│   │   └── main.py
│   ├── requirements.txt
│   └── supervisord.conf
│
└── Dockerfile
```

---

## ⚙️ Требования
- Docker  
- Python 3.9 и выше  

---

## 🛠 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd my_project
```

### 2. Сборка Docker-образа
```bash
docker build -t my_project .
```

### 3. Создание тома для базы данных
```bash
docker volume create app_data
```

### 4. Запуск контейнера
```bash
docker run -d \
  -p 8000:8000 \
  -p 8001:8001 \
  -v app_data:/app/data \
  --name my_project_container \
  my_project
```

---

## 🔍 Доступ к сервисам
- **TODO-сервис**: [http://localhost:8000/docs](http://localhost:8000/docs)  
- **Short URL-сервис**: [http://localhost:8001/docs](http://localhost:8001/docs)  

Swagger-документация доступна по этим адресам для каждого микросервиса.  

---

## 📜 Описание эндпоинтов

### 1. TODO-сервис (порт 8000)
| Метод | URL               | Описание                        | Пример тела запроса                   |
|-------|-------------------|---------------------------------|--------------------------------------|
| POST  | /items            | Создание новой задачи           | `{"title": "Task 1", "description": "Описание задачи"}` |
| GET   | /items            | Получение всех задач            | —                                    |
| GET   | /items/{item_id}  | Получение задачи по ID          | —                                    |
| PUT   | /items/{item_id}  | Обновление задачи по ID         | `{"title": "Task 1 Updated", "completed": true}` |
| DELETE| /items/{item_id}  | Удаление задачи по ID           | —                                    |

---

### 2. Short URL-сервис (порт 8001)
| Метод | URL               | Описание                        | Пример тела запроса                   |
|-------|-------------------|---------------------------------|--------------------------------------|
| POST  | /shorten          | Создание короткой ссылки        | `{"url": "https://example.com/longpath"}` |
| GET   | /{short_id}       | Редирект по короткому ID        | —                                    |
| GET   | /stats/{short_id} | Получение информации о ссылке   | —                                    |

---

## 🔧 Конфигурация Supervisord
`supervisord` управляет двумя процессами FastAPI, запуская их на разных портах.

**Конфигурация:** `app/supervisord.conf`
```ini
[supervisord]
nodaemon=true

[program:todo_service]
command=uvicorn todo_service.main:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
stderr_logfile=/dev/stdout
stdout_logfile=/dev/stdout

[program:short_url_service]
command=uvicorn short_url_service.main:app --host 0.0.0.0 --port 8001
autostart=true
autorestart=true
stderr_logfile=/dev/stdout
stdout_logfile=/dev/stdout
```

---

## 🗃️ Хранение данных
- Все данные сохраняются в SQLite базе данных, расположенной в `/app/data/app.db`.  
- Для сохранности данных используется **Docker Volume**: `app_data`.  

---

## 🛠 Локальный запуск (без Docker)
Если требуется протестировать сервисы локально (без Docker), выполните следующие шаги:

### 1. Установка зависимостей
```bash
pip install -r app/requirements.txt
```

### 2. Запуск TODO-сервиса
```bash
uvicorn app.todo_service.main:app --host 0.0.0.0 --port 8000
```

### 3. Запуск Short URL-сервиса
```bash
uvicorn app.short_url_service.main:app --host 0.0.0.0 --port 8001
```

---

## 🧪 Тестирование работы сервисов

### 1. Проверка TODO-сервиса
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"title":"First Task", "description":"Description here"}' \
  http://localhost:8000/items
```
```bash
curl http://localhost:8000/items
```

### 2. Проверка Short URL-сервиса
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' \
  http://localhost:8001/shorten
```