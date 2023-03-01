import strawberry

from typing import Optional


@strawberry.input
class MovieFilters:
    title: Optional[str] = strawberry.UNSET
