from typing import List, Optional

import strawberry
from strawberry.types import Info

from app.models import Movie
from app.crud import crud_movies
from app.schema import input


@strawberry.type
class Query:
    @strawberry.field
    async def movies(
        self, info: Info, filters: Optional[input.MovieFilters] = None
    ) -> List[Movie]:
        session = info.context["session"]

        movie_fields = Movie.convert_to_queryable_fields(info.selected_fields)

        movies: List[Movie] = await crud_movies.get_movies(
            session, filters, movie_fields
        )

        return [Movie.marshal(movie) for movie in movies]


movie_query = Query
