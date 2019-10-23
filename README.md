# Dónde Estás

<!-- markdownlint-disable MD024 -->

## Testing the server

### Run the server

```bash
docker-compose build  # Build API image

docker-compose run web python manage.py db init  # Create database (first time only)

docker-compose up  # Start containers
```

### Migrate the database

```bash
docker-compose run web python manage.py db migrate  # Migrate database
docker-compose run web python manage.py db upgrade  # Upgrade database
```

### Run Ghost Client

```bash
python3 ghost_client.py action *args
```

Where `action` is the name of the endpoint to test and `*args` are the arguments recieved by the endpoint (order varies from method to method, for more info check `ghost_client.py`).

## Endpoints

Every endpoint gets a query string with the parameters described.

Upon any unexpected internal server error, the response code will be `503` and the `json` will look like:

```json
{
  "payload": "Generic message detailing the failure",
  "success": false
}
```

### GET /missing

#### Parameters

No parameters

#### Response

The request returns code `200` upon success. The return `json` will look like:

```json
{
  "payload": [
    {
      "created_date": "Wed, 23 Oct 2019 04:31:30 GMT",
      "found": false,
      "found_date": null,
      "id": 1,
      "key_digest": "$2b$12$qaWmfu.nG2Akb/sLoLdrj.wid6DM0i55zTHFI36UH.r4G..rv8SjK",
      "last_name": "Martínez",
      "name": "Ariel"
    },
    {
      "created_date": "Wed, 23 Oct 2019 04:31:43 GMT",
      "found": false,
      "found_date": null,
      "id": 3,
      "key_digest": "$2b$12$NyknKBZurcmen1gYV0V3OuPzDm2gOjsvS2SoY5J03zRVjXcmm0d5a",
      "last_name": "Leal",
      "name": "Daniel"
    },
    {
      "created_date": "Wed, 23 Oct 2019 04:32:29 GMT",
      "found": false,
      "found_date": null,
      "id": 27,
      "key_digest": "$2b$12$Xir8RZtDwq2vW4Bp7Iw/S.TGpu0g6N0KkmIJ.eeOlYM7y.vUwXi4K",
      "last_name": "Irarrázaval",
      "name": "Alfonso"
    }
  ],
  "success": true
}
```

### PATCH /missing/\<id>

#### Parameters

`plain_key` corresponds to the secret key given to the reporter and to the missing person.

```json
{
  "plain_key": "brxmDs9U6cG56N8K"
}
```

#### Response

If the request fails (it may fail because the person has already been found (code `409`), because the `plain_key` was incorrect (code `401`) or because the `id` could not be found in the database (code `404`)), the `json` will look like:

```json
{
  "payload": "Generic message detailing the failure",
  "success": false
}
```

The request returns code `200` upon success. The return `json` will look like:

```json
{
  "payload": "Person found successfully",
  "success": true
}
```

### GET /found

#### Parameters

No parameters

#### Response

The request returns code `200` upon success. The return `json` will look like:

```json
{
  "payload": [
    {
      "created_date": "Wed, 23 Oct 2019 04:31:30 GMT",
      "found": true,
      "found_date": "Wed, 23 Oct 2019 04:37:21 GMT",
      "id": 1,
      "key_digest": "$2b$12$qaWmfu.nG2Akb/sLoLdrj.wid6DM0i55zTHFI36UH.r4G..rv8SjK",
      "last_name": "Martínez",
      "name": "Ariel"
    },
    {
      "created_date": "Wed, 23 Oct 2019 04:31:43 GMT",
      "found": true,
      "found_date": "Wed, 23 Oct 2019 06:17:02 GMT",
      "id": 3,
      "key_digest": "$2b$12$NyknKBZurcmen1gYV0V3OuPzDm2gOjsvS2SoY5J03zRVjXcmm0d5a",
      "last_name": "Leal",
      "name": "Daniel"
    }
  ],
  "success": true
}
```

### POST /person

#### Parameters

```json
{
  "first_name": "Daniel",
  "last_name": "Leal",
  "missing_mail": "daniel_leal@email.example",
  "contact_mail": "fonsi_irarrazaval@email.example"
}
```

#### Response

The request returns code `200` upon success. The return `json` will look like:

```json
{
  "payload": {
    "person": {
      "created_date": "Wed, 23 Oct 2019 05:31:06 GMT",
      "found": false,
      "found_date": null,
      "id": 8,
      "key_digest": "$2b$12$uTCD1kGChKsP0OU7MAz3NuIPoMcBDXTNNnua9zzM4DbaEox4g87mG",
      "last_name": "Leal",
      "name": "Daniel"
    },
    "plain_key": "brxmDs9U6cG56N8K",
  },
  "success": true
}
```

### GET /person/\<id>

#### Parameters

No parameters

#### Response

If the request fails (it may fail because the `id` could not be found in the database (code `404`)), the `json` will look like:

```json
{
  "payload": "Generic message detailing the failure",
  "success": false
}
```

The request returns code `200` upon success. The return `json` will look like:

```json
{
  "payload": {
    "created_date": "Wed, 23 Oct 2019 04:32:29 GMT",
    "found": false,
    "found_date": null,
    "id": 7,
    "key_digest": "$2b$12$Xir8RZtDwq2vW4Bp7Iw/S.TGpu0g6N0KkmIJ.eeOlYM7y.vUwXi4K",
    "last_name": "Leal",
    "name": "Daniel"
  },
  "success": true
}
```

### DELETE /person/\<id>

#### Parameters

`plain_key` corresponds to the secret key given to the reporter and to the missing person.

```json
{
  "plain_key": "brxmDs9U6cG56N8K"
}
```

#### Response

If the request fails (it may fail because the `plain_key` was incorrect (code `401`) or because the `id` could not be found in the database (code `404`)), the `json` will look like:

```json
{
  "payload": "Generic message detailing the failure",
  "success": false
}
```

The request returns code `200` upon success. The return `json` will look like:

```json
{
  "payload": "Person removed successfully",
  "success": true
}
```
