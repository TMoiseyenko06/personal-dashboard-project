import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Movie as MovieModel
from models import Genre as GenreModel
from database import db
from sqlalchemy.orm import Session
from sqlalchemy import select

class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel

class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel 
        


class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    genres = graphene.List(Genre)
    movies_by_genre = graphene.Field(graphene.List(Movie), id=graphene.Int(required=True))
    genre_by_movie = graphene.Field(graphene.List(Genre), id=graphene.Int(required=True))

    def resolve_genres(self,info):
        return db.session.execute(db.select(GenreModel)).scalars()

    def resolve_movies(self,info):
        return db.session.execute(db.select(MovieModel)).scalars()
    
    def resolve_movies_by_genre(self,info,id):
        genre = db.session.get(GenreModel, id)
        if not genre:
            return []
        movies = db.session.execute(select(MovieModel).where(MovieModel.genres.contains(genre))).scalars().all()
        return movies
    
    def resolve_genre_by_movie(self,info,id):
        movie = db.session.get(MovieModel, id)
        return movie.genres

    

    
class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self,info,name):
        with Session(db.engine) as session:
            with session.begin():
                genre = GenreModel(name=name)
                session.add(genre)
                session.commit()
            session.refresh(genre)
            return AddGenre(genre=genre)
        
class AddMovie(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        release_year = graphene.String(required=True)
        genres = graphene.List(graphene.Int,required=True)

    movie = graphene.Field(Movie)
        
    def mutate(self,info,name,description,release_year,genres):
        with Session(db.engine) as session:
            with session.begin():
                genres = session.execute(select(GenreModel).where(GenreModel.id.in_(genres))).scalars().all()
                movie = MovieModel(name=name,description=description,release_year=release_year,genres=genres)
                session.add(movie)
                session.commit()
            session.refresh(movie)
            return AddMovie(movie=movie)
        
class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self,info,id,name):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.get(GenreModel, id)
                genre.name = name
                session.commit
            return UpdateGenre(genre=genre)
        
class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        release_year = graphene.String(required=True)
        genres = graphene.List(graphene.Int,required=True)

    movie = graphene.Field(Movie)

    def mutate(self,info,id,name,description,release_year,genres):
        with Session(db.engine) as session:
            with session.begin():
                genres = session.execute(select(GenreModel).where(GenreModel.id.in_(genres))).scalars().all()
                movie = session.get(MovieModel, id)
                movie.name = name
                movie.description = description
                movie.release_year = release_year
                movie.genres = genres
                session.commit()
            return UpdateMovie(movie=movie)
        
class DeleteMessage(graphene.ObjectType):
    message = graphene.String()

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = DeleteMessage

    def mutate(self,info,id):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.get(GenreModel, id)
                session.delete(genre)
                session.commit()
            return DeleteMessage(message="Genre Deleted Successfully")
            
class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = DeleteMessage

    def mutate(self,info,id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.get(MovieModel, id)
                session.delete(movie)
                session.commit()
            return DeleteMessage(message="Movie Deleted Successfully")
        


class Mutation(graphene.ObjectType):
    createGenre = AddGenre.Field()
    createMovie = AddMovie.Field()
    updateGenre = UpdateGenre.Field()
    updateMovie = UpdateMovie.Field()
    deleteGenre = DeleteGenre.Field()
    deleteMovie = DeleteMovie.Field()
