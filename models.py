from database import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from typing import List


class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(255),unique=True,nullable=False)

class GenreManagment(Base):
    __tablename__ = 'genre_managment'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movies.id'))
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'))

class Movie(Base):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    description: Mapped[str] = mapped_column(String(255),nullable=False)
    release_year: Mapped[int] = mapped_column(Integer,nullable=False)
    genres: Mapped[List[Genre]] = relationship(secondary="genre_managment")
