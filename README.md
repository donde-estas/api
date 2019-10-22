# Dónde Estás

## Testing the server

### Run the server

```bash
docker-compose build  # Build API image

docker-compose run api python manage.py db init  # Create database (first time only)

docker-compose up  # Start containers
```

### Migrate the database

```bash
docker-compose run api python manage.py db migrate  # Migrate database
docker-compose run api python manage.py db upgrade  # Upgrade database
```

### Run Ghost Client

```bash
python3 ghost_client.py action *args
```

Where `action` is the name of the endpoint to test and `*args` are the arguments recieved by the endpoint (order varies from method to method, for more info check `ghost_client.py`).
