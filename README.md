# Стек
<img src="https://img.shields.io/badge/Python-4169E1?style=for-the-badge"/> <img src="https://img.shields.io/badge/Django-008000?style=for-the-badge"/> <img src="https://img.shields.io/badge/DRF-800000?style=for-the-badge"/> <img src="https://img.shields.io/badge/Docker-00BFFF?style=for-the-badge"/> <img src="https://img.shields.io/badge/PostgreSQL-87CEEB?style=for-the-badge"/> <img src="https://img.shields.io/badge/Nginx-67c273?style=for-the-badge"/> <img src="https://img.shields.io/badge/Nginx-06bd1e?style=for-the-badge"/>

# Описание проекта:

**Проект VkTest**

Проект Books это сервис, в котором пользователи могут регистрироваться,
добавлять книги, комментировать книги, удалять или редактировать свои книги и комментарии.

# Как запустить проект:

*Клонировать репозиторий и перейти в него в командной строке:*
```
https://github.com/qzonic/FlyCode.git
```
```
cd FlyCode/
```

*Теперь необходимо собрать Docker-контейнеры:*
```
docker-compose up -d
```

*После сборки контейнеров, нужно прописать следующие команды по очереди:*
```
docker-compose exec web python manage.py migrate
```

```
docker-compose exec web python manage.py createsuperuser
```

```
docker-compose exec web python manage.py collectstatic --no-input
```

Так же вы можете заполнить базу некоторыми данными:
```
docker-compose exec web python3 manage.py loaddata db.json
```

*Теперь проект доступен по адресу:*
```
http://localhost/
```

*Эндпоинты для взаимодействия с API можно посмотреть в документации по адресу:*
```
http://localhost/api/redoc/
```

### Автор
[![telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/qzonic)
