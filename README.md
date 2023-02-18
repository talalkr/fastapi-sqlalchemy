# FastAPI + SQLAlchemy

A fork of [fastapi-sqlalchemy](https://github.com/strawberry-graphql/examples/tree/main/fastapi-sqlalchemy) except it uses async-sqlite and upgraded 3rd party packages.

This project is setup on SQLAlchemy and GraphQL API mounted on FastAPI. Fetch movies and directors.
Nesting queries is limited.
CRUDs dynamically load queried fields to reduce load on DB.

## How to use

1. [Install Poetry](https://python-poetry.org/docs/) and set path

```bash
curl -sSL https://install.python-poetry.org | python3 -
PATH=$PATH:$HOME/.local/bin
```

Make sure `pyenv` is using the same python version found in the `.python-version` file.

2. Install dependencies

Create a virtualenv with a python version that matches the project:

```bash
poetry env use 3.11.0
```
This version is based on the `.python-version` file

Use [poetry](https://python-poetry.org/) to install dependencies:

```bash
poetry install
```

Activate venv

```bash
source $(poetry env info --path)/bin/activate
```

2. Run migrations

Run [alembic](https://alembic.sqlalchemy.org/en/latest/) to create the database
and populate it with movie data:

```bash
poetry run alembic upgrade head
```

3. Run the server

Run [uvicorn](https://www.uvicorn.org/) to run the server:

```bash
poetry run uvicorn main:app --reload
```

The GraphQL API should now be available at http://localhost:8000/graphql

## Example query

```graphql
{
  movies {
    id
    title
    imdb_rating
    director {
      id
      name
    }
  }
}
```

```graphql
{
  movies(filters: { title: "The Shawshank Redemption" }) {
    id
    title
    image_url
    imdb_id
    imdb_rating
    imdb_rating_count
    year
    director {
      id
      name
    }
  }
}
```
