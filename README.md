# praktikum_new_diplom

- в терминале выполните команды из директории проекта:

  - `docker-compose up -d --build` - собираем и запускаем инфраструктуру
  - `docker-compose exec backend python manage.py migrate --noinput` - выполняем миграции
  - `docker-compose exec backend python manage.py collectstatic --no-input` - собираем статику
  - `docker-compose exec backend python manage.py loaddata fixtures.json` - загружаем тестовые данные

попробовал пересобрать всю инфраструктуру
исправил почти все
readme допишу при деплое, пока по коду пройдусь
скачивание поправлю, отправил на ревью и вылезли другие косяки, а отменить ревью нельзя




----
.env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
