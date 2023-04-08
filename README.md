![Workflow status.](https://github.com/Saggitel/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# Проект Foodgram, «Продуктовый помощник»
### На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Адрес сервера 
```
84.201.169.123
```

### Админка
```
admin@mail.ru
admin
```

### Устанвока
- Развернуть проект на удаленном сервере
- Клонировать репозиторий:
```
git@github.com:krivse/Foodgram.git
```

- Установить на сервере Docker, Docker Compose:
```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия 
```

- Создать и запустить контейнеры Docker, выполнить команду на сервере (версии команд "docker compose" или "docker-compose" отличаются в зависимости от установленной версии Docker Compose):**_
```
sudo docker compose up -d
```

- Выполнить миграции:
```
sudo docker compose exec backend python manage.py migrate
```

- Собрать статику:
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

- Наполнить базу данных содержимым из файла ingredients.json:
```
sudo docker compose exec backend python manage.py loaddata ingredients.json
```

- Создать суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

- Для остановки контейнеров Docker:
```
sudo docker compose down -v      - с их удалением
sudo docker compose stop         - без удаления
```

### Документация
Документация, содержащая примеры запросов, доступна по адресу: http://localhost/api/docs/redoc.html
### Авторы
Тимур