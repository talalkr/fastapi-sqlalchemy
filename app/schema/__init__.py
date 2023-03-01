import strawberry

from strawberry.tools import merge_types
from strawberry.schema.config import StrawberryConfig

from .director import query_director
from .movie import movie_query

queries = (query_director, movie_query)

Query = merge_types("Query", queries)

schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
