# DNF_V5

Учебный проект для практики работы с FastAPI, MongoDB, Beanie, Docker, Pytest и CI/CD.

Продолжение практики после:

- https://github.com/Osnowa/DNF_V4.git
- https://github.com/Osnowa/DNF_V3.git

## Стек

- FastAPI
- MongoDB
- Beanie
- Pydantic
- Docker / Docker Compose
- Nginx
- Pytest
- HTTPX
- Testcontainers
- GitHub Actions
- GitHub Container Registry (GHCR)
- VPS
- SSH

## Что реализовано

- Реализован CRUD для пользователей
- MongoDB используется как основная база данных
- Beanie используется для работы с MongoDB
- Реализовано тестирование API через `pytest` и `httpx.AsyncClient`
- Для тестов используется отдельный MongoDB контейнер через Testcontainers
- Покрытие тестами — **90%+**
- Настроен CI через GitHub Actions
- Реализована автоматическая сборка Docker image
- Docker image публикуется в GitHub Container Registry
- Реализован полностью рабочий CD pipeline
- GitHub Actions подключается к VPS по SSH
- На сервере автоматически выполняются `docker compose pull` и `docker compose up -d`

## CI/CD

Pipeline работает следующим образом:

```text
git push
   ↓
Tests
   ↓
Coverage ≥ 90%
   ↓
Docker Build
   ↓
Push → GHCR
   ↓
SSH → VPS
   ↓
docker compose pull
   ↓
docker compose up -d
```
Все этапы CI/CD были проверены на реальном VPS и успешно отработали.

После завершения тестирования VPS был отключён.

## Реализованные endpoints
Users
- POST /users — создание пользователя
- GET /users/{id} — получение пользователя
- PATCH /users/{id} — изменение пользователя
- DELETE /users/{id} — удаление пользователя

## Цель проекта

Практика работы с MongoDB и Beanie, а также создание и проверка полностью рабочего CI/CD pipeline с использованием GitHub Actions, Docker, GHCR, SSH и VPS.