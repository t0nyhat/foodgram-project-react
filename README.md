# praktikum_new_diplom

полное и красивое readme допишу при деплое, пока по коду пройдусь

-создать в папке infra фалй '.env' c содержимым:

  DB_ENGINE=django.db.backends.postgresql
  DB_NAME=postgres
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  DB_HOST=db
  DB_PORT=5432


- в терминале выполните команды из директории проекта:

  - `docker-compose up -d --build` - собираем и запускаем инфраструктуру
  - `docker-compose exec backend python manage.py migrate --noinput` - выполняем миграции
  - `docker-compose exec backend python manage.py collectstatic --no-input` - собираем статику
  - `docker-compose exec backend python manage.py loaddata fixtures.json` - загружаем тестовые данные

в тестовых данных созданы:
-админиcтратор
  login: admin
  pass: admin
-пользователь 1
  login: test1@mail.ru
  pass: foodgram-project-react
  2 рецепта и подписка на 2 пользователя
-пользователь 2
  login: test2@mail.ru
  pass: foodgram-project-react
  2 рецепта


?
Я обновил фронт, до той версии которая в ветке яндекса актуальна, но 
мне кажется есть баги с отображением количества в козине и любимого


