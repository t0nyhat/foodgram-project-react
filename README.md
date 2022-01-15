# praktikum_new_diplom

- в терминале выполните команды из директории проекта:

  - `docker-compose up -d --build` - собираем и запускаем инфраструктуру
  - `docker-compose exec backend python manage.py migrate --noinput` - выполняем миграции
  - `docker-compose exec web python manage.py collectstatic --no-input` - собираем статику
  - `docker-compose exec web python manage.py loaddata fixtures.json` - загружаем тестовые данные

попробовал пересобрать всю инфраструктуру
исправил почти все
readme допишу при деплое, пока по коду пройдусь
скачивание корзины мне все-равно не нравится
по фронту не работет измененние рецепта, понять не могу почему



----
.env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
