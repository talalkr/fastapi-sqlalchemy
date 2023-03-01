from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List
from app.models.movie import Movie

# TODO: add exception handling
class MovieCrud:
    async def get_movies(
        self, session: AsyncSession, filters, movie_fields
    ) -> List[Movie]:
        query = select(Movie).order_by(Movie.imdb_rating.desc())

        if "director" in movie_fields:
            query = query.options(
                joinedload(Movie.director).load_only(*movie_fields.pop("director")),
            )

        query = query.options(load_only(*movie_fields))

        if filters and filters.title:
            query = query.where(Movie.title == filters.title)

        results = (await session.execute(query)).unique().fetchall()
        return [res[0] for res in results]


crud_movies = MovieCrud()
