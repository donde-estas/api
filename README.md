# Dónde Estás

## Run the server

```bash
docker-compose build  # Build API image

docker-compose run api python manage.py db init     # Create database
docker-compose run api python manage.py db migrate  # Migrate database
docker-compose run api python manage.py db upgrade  # Upgrade database

docker-compose up  # Start containers
```
