import strawberry

from typing import List, Optional, Dict, Any
from strawberry.types.nodes import SelectedField

from main.models import Director as DirectorModel, Movie as MovieModel


@strawberry.type
class Director:
    id: int
    name: str = None
    movies: List["Movie"] = None

    @classmethod
    def marshal(cls, instance: DirectorModel):
        # __dict__ is used to avoid accessing the instance's fields directly
        # This will prevent loading columns that weren't fetched in the DB query
        return cls(
            id=instance.__dict__.get("id", None),
            name=instance.__dict__.get("name", None),
            movies=instance.__dict__.get("movies", None),
        )

    @classmethod
    def convert_to_queryable_fields(
        self, fields: List[SelectedField]
    ) -> Dict[str, List]:
        """
        Convert SelectedFields from the schema into queryable fields for the Movie model
        """
        director_fields: Dict[str, Any] = {
            selection.name: selection.selections
            for field in fields
            for selection in field.selections
        }

        # Iterate SelectedFields of Director to be used in 'joinedload'
        # change type hint to 'SelectedField | List[SelectedField]' after upgrading python version
        movies_fields: SelectedField = director_fields.pop("movies", [])

        if movies_fields:
            director_fields["movies"]: List[str] = [
                selection.name for selection in movies_fields
            ]

        return director_fields


@strawberry.input
class MovieFilters:
    title: Optional[str] = strawberry.UNSET


@strawberry.type
class Movie:
    id: int
    title: str = None
    imdb_id: str = None
    year: int = None
    image_url: str = None
    imdb_rating: float = None
    imdb_rating_count: str = None
    instance: strawberry.Private[MovieModel] = None
    director: "Director" = None

    @classmethod
    def marshal(cls, instance: MovieModel):
        # __dict__ is used to avoid accessing the instance's fields directly
        # This will prevent loading columns that weren't fetched in the DB query
        return cls(
            instance=instance,
            id=instance.__dict__.get("id", None),
            imdb_id=instance.__dict__.get("imdb_id", None),
            title=instance.__dict__.get("title", None),
            year=instance.__dict__.get("year", None),
            image_url=instance.__dict__.get("image_url", None),
            imdb_rating=instance.__dict__.get("imdb_rating", None),
            imdb_rating_count=instance.__dict__.get("imdb_rating_count", None),
            director=instance.__dict__.get("director", None),
        )

    @classmethod
    def convert_to_queryable_fields(
        self, fields: List[SelectedField]
    ) -> Dict[str, List]:
        """
        Convert SelectedFields from the schema into queryable fields for the Movie model
        """
        movie_fields: Dict[str, Any] = {
            selection.name: selection.selections
            for field in fields
            for selection in field.selections
        }

        # Iterate SelectedFields of Director to be used in 'joinedload'
        # change type hint to 'SelectedField | List[SelectedField]' after upgrading python version
        director_fields: SelectedField = movie_fields.pop("director", [])

        if director_fields:
            movie_fields["director"]: List[str] = [
                selection.name for selection in director_fields
            ]

        return movie_fields
