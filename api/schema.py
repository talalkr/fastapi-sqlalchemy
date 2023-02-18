from typing import List, Optional

import strawberry
from strawberry.schema.config import StrawberryConfig
from strawberry.types import Info

from main.models import Movie
from crud import crud_movies, crud_director
from api import definitions


@strawberry.type
class Query:
    @strawberry.field
    async def movies(
        self, info: Info, filters: Optional[definitions.MovieFilters] = None
    ) -> List[definitions.Movie]:
        session = info.context["session"]

        movie_fields = definitions.Movie.convert_to_queryable_fields(
            info.selected_fields
        )

        movies: List[Movie] = await crud_movies.get_movies(
            session, filters, movie_fields
        )

        return [definitions.Movie.marshal(movie) for movie in movies]

    @strawberry.field
    async def directors(self, info: Info) -> List[definitions.Director]:
        session = info.context["session"]

        director_fields = definitions.Director.convert_to_queryable_fields(
            info.selected_fields
        )

        directors = await crud_director.get_director_movies(session, director_fields)

        return [definitions.Director.marshal(director) for director in directors]


schema = strawberry.Schema(
    Query,
    config=StrawberryConfig(auto_camel_case=False),
)
