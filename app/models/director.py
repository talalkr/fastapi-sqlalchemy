from typing import List, Dict, Any, Union

import strawberry
from strawberry.types.nodes import SelectedField
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


@strawberry.type
class Director(Base):
    __tablename__ = "directors"

    id: int = Column(Integer, primary_key=True, index=True, nullable=False)
    name: str = Column(String, unique=True, index=True, nullable=False)

    movies: List[strawberry.LazyType["Movie", "app.models.movie"]] = relationship(
        "Movie", lazy="noload", back_populates="director"
    )

    @classmethod
    def marshal(cls, instance: "Director"):
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
        movies_fields: Union[SelectedField, List[SelectedField]] = director_fields.pop(
            "movies", []
        )
        print(movies_fields)

        if movies_fields:
            director_fields["movies"]: List[str] = [
                selection.name for selection in movies_fields
            ]

        return director_fields
