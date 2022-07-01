# fastapi_minio

Проект **fastapi_minio** предназначен для загрузки изображений в формате jpeg в S3-совместимое объектное хранилище MinIO.
За один запрос API позволяет загружать до 15 изображений.
При загрузке изображений их имена, дата создания, и код запроса также сохраняются в базе данных.
В результате по коду запроса можно получить информацию о загруженнных изображениях и при необходимости удалить их из базы данных и из объектного хранилища.

### Стэк технологий:
- Python
- FastAPI
- MinIO
- PostgreSQL
- Docker

### Документация и возможности API:
К проекту подключен ReDoc и Swagger.
Для просмотра документации используйте эндпойнты `redoc/` или `docs/`.

### Как запустить проект:
- Склонируйте репозиторий на свой компьютер
- Создайте `.env` файл в корневой директории, рядом с файлом `docker-compose.yaml`. В `.env` файле должны содержаться следующие переменные:
    >MINIO_URL='minio:9000' # имя хоста (контейнера) и порт для доступа к объектному хранилищу
    >MINIO_ACCESS_KEY=admin # имя пользователя для доступа к объектному хранилищу
    >MINIO_SECRET_KEY=minio123 #пароль для доступа к объектному хранилищу
    >DATABASE_NAME=postgres # название БД\ 
    >POSTGRES_USER=postgres # имя пользователя для доступа к БД
    >POSTGRES_PASSWORD=postgres123 # пароль для доступа к БД
    >DATABASE_HOST=db # имя хоста (контейнера) для подключения к БД
    >DATABASE_PORT=5432 # порт для подключения к БД
    >DATABASE_URL="postgresql://postgres:postgres123@db/postgres" # url подключения к БД
- Из корня проекта соберите образ при помощи docker-compose
`$ docker-compose up -d --build`

### Примеры использования:
**Получить документацию:**
```
http://localhost/redoc/
```
**Загрузить изображения:**
```
curl -X 'POST' \
  'http://localhost/frames/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@sample_c49b0e98b2689903e604cf55bf86c02e.jpg;type=image/jpeg' \
  -F 'files=@sample_4eda57cea398464c52c79e08a0b5f5c2.jpg;type=image/jpeg'
 
[
  {
    "filename": "785f4214-998d-4bd1-9f5a-40af6e459f3e.jpg"
  },
  {
    "filename": "7ca0d8ef-8354-4504-a910-676efead65db.jpg"
  }
]
```
**Получить список изображений по коду запроса:**
```
curl -X 'GET' \
  'http://localhost/frames/1' \
  -H 'accept: application/json'
  
[
  {
    "filename": "785f4214-998d-4bd1-9f5a-40af6e459f3e.jpg",
    "created_at": "2022-06-30T20:58:42.957506+00:00"
  },
  {
    "filename": "7ca0d8ef-8354-4504-a910-676efead65db.jpg",
    "created_at": "2022-06-30T20:58:43.004084+00:00"
  }
]
```

### Запуск тестов:
```
docker-compose exec -it web bash -c 'cd /app/fastapi_minio/ && pytest'
```