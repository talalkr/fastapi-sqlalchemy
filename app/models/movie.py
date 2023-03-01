from typing import List, Optional, Dict, Any, Union

import strawberry
from strawberry.types.nodes import SelectedField
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


@strawberry.type
class Movie(Base):
    __tablename__ = "movies"

    id: int = Column(Integer, primary_key=True, index=True, nullable=False)
    title: str = Column(String, unique=True, nullable=False)
    imdb_id: str = Column(String, unique=True, index=True, nullable=False)
    year: int = Column(Integer, nullable=False)
    image_url: str = Column(String, nullable=False)
    imdb_rating: float = Column(Float, nullable=False)
    imdb_rating_count: str = Column(String, nullable=False)

    director_id: int = Column(Integer, ForeignKey("directors.id"), nullable=False)
    director: Optional[
        strawberry.LazyType["Director", "app.models.director"]
    ] = relationship("Director", lazy="noload", back_populates="movies")

    @classmethod
    def marshal(cls, instance: "Movie"):
        # __dict__ is used to avoid accessing the instance's fields directly
        # This will prevent loading columns that weren't fetched in the DB query
        return cls(
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
        director_fields: Union[SelectedField, List[SelectedField]] = movie_fields.pop(
            "director", []
        )

        if director_fields:
            movie_fields["director"]: List[str] = [
                selection.name for selection in director_fields
            ]

        return movie_fields
