from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List
from main.models import Director

# TODO: add exception handling
class DirectorCrud:
    async def get_directors(self, session: AsyncSession) -> List[Director]:
        query = select(Director)
        result = await session.execute(query)
        return result.scalars().unique().all()

    # TODO: use load_only to avoid loading entire object
    async def get_director_movies(
        self, session: AsyncSession, director_fields
    ) -> List[Director]:
        query = select(Director)

        if "movies" in director_fields:
            query = query.options(
                joinedload(Director.movies).load_only(*director_fields.pop("movies")),
            )

        query = query.options(load_only(*director_fields))

        results = (await session.execute(query)).unique().fetchall()
        return [res[0] for res in results]


crud_director = DirectorCrud()
