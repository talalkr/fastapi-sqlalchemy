from typing import List, Optional

import strawberry
from strawberry.schema.config import StrawberryConfig
from strawberry.types import Info

from app.models import Movie, Director
from app.crud import crud_movies, crud_director
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

    @strawberry.field
    async def directors(self, info: Info) -> List[Director]:
        session = info.context["session"]

        director_fields = Director.convert_to_queryable_fields(info.selected_fields)

        directors = await crud_director.get_director_movies(session, director_fields)

        return [Director.marshal(director) for director in directors]


schema = strawberry.Schema(
    Query,
    config=StrawberryConfig(auto_camel_case=False),
)
