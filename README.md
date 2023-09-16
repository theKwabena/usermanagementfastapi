## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

## Starting the project

```To start the project, set your .env files at the root of the project.
The env contains the required variables to start the project. The project may fail to start if these are not set
POSTGRES_SERVER - db service name (specified in dockerfile)
POSTGRES_USER - database user name 
POSTGRES_PASSWORD - database password
POSTGRES_DB - database name
SQL_ALCHEMY_DATABASE_URI - must be of the form postgresql://POSTGRES_USER:POSTGRES_PASSWORD@POSTGRES_SERVER:5432/POSTGRES_DB
FIRST_ADMIN - first admin email
FIRST_ADMIN_PASSWORD - first admin password
```

* Start the stack with Docker Compose:

```bash
docker-compose up --build
```

* Now you can open your browser and interact with these URLs:

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8000/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost:8000/redoc

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```



