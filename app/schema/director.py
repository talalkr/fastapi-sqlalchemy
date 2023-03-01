from typing import List

import strawberry
from strawberry.types import Info

from app.models import Director
from app.crud import crud_director


@strawberry.type
class Query:
    @strawberry.field
    async def directors(self, info: Info) -> List[Director]:
        session = info.context["session"]

        director_fields = Director.convert_to_queryable_fields(info.selected_fields)

        directors = await crud_director.get_director_movies(session, director_fields)

        return [Director.marshal(director) for director in directors]


query_director = Query
