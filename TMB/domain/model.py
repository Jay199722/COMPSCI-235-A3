from datetime import datetime
from typing import List, Iterable
import requests


class User:
    def __init__(
            self, username: str, password: str
    ):
        self.__username: str = username
        self.__password: str = password
        self.__comments: List[Comment] = list()
        self.__watched = list()
        self.__reviews = list()
        self.__time_spent = 0

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self.__comments)

    def add_comment(self, comment: 'Comment'):
        self.__comments.append(comment)

    @property
    def watched_movies(self):
        return self.__watched

    @watched_movies.setter
    def watched_movies(self, watched):
        if isinstance(watched, list):
            self.__watched = watched

    @property
    def reviews(self):
        return self.__reviews

    @reviews.setter
    def reviews(self, rvws):
        if isinstance(rvws, list):
            self.__reviews = rvws

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, time_spent):
        if isinstance(time_spent, int):
            self.__time_spent = time_spent

    def watch_movie(self, movie):
        self.__watched.append(movie)
        self.__time_spent += movie.runtime_minutes

    def add_review(self, review):
        self.__reviews.append(review)

    @property
    def __repr__(self):
        return f"<User {self.__username}>"

    def __eq__(self, other):
        if self.__username == other.username:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.__username < other.username:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__username + str(self.__password))

    def __repr__(self):
        return f'<User {self.__username} {self.__password}>'


class Comment:
    def __init__(
            self, user: User, movie: 'Movie', comment: str, timestamp: datetime
    ):
        self.__user: User = user
        self.__movie: Movie = movie
        self.__comment = comment
        self.__timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self.__user

    @property
    def movie(self) -> 'Movie':
        return self.__movie

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other.__user == self.__user and other.__movie == self.__movie and other.__comment == self.__comment and other.\
            __timestamp == self.__timestamp

    def __str__(self):
        return self.comment


class Movie:
    def __init__(self, title=None, year=None, movie_id: int = None):
        self.__id = movie_id
        self.__title = None
        if isinstance(title, str) and len(title) > 0:
            self.__title = title.strip()
        self.__year = None
        if isinstance(year, int) and year >= 1900:
            self.__year = year
        self.__description = None
        self.__director = None
        self.__runtime_minutes = 0
        self.__actors = []
        self.__genres = []
        self.__comments: List[Comment] = list()
        self.__hyperlink: str = f"https://www.google.com/search?q={self.__title}&rlz=1C1CHZL_enNZ777NZ777&oq=123&aqs" \
                               f"=chrome.0.69i59j69i60l3.1134j0j9&sourceid=chrome&ie=UTF-8 "
        self.__image_hyperlink: str = ''
        self.__rating = ''
        self.__votes = 0
        self.__revenue = 'N/A'
        self.__metascore = 'N/A'
        self.__voted = ''

    @property
    def votes(self):
        return self.__votes

    @votes.setter
    def votes(self, votes):
        self.__votes = votes

    @property
    def revenue(self):
        return self.__revenue

    @revenue.setter
    def revenue(self, revenue):
        self.__revenue = revenue

    @property
    def metascore(self):
        return self.__metascore

    @metascore.setter
    def metascore(self, metascore):
        self.__metascore = metascore

    @property
    def rating(self):
        return round(float(self.__rating), 2)

    @rating.setter
    def rating(self, rating):
        self.__rating = rating

    def add_rating(self, rating: float, user: User):
        if self.__voted is None:
            self.__voted = ''
        if user.username not in self.__voted:
            self.__voted+=user.username
            self.__rating = str(((float(self.__rating) * self.__votes) + rating) / (self.__votes + 1))
            self.__votes += 1
            print("successes")

    @property
    def voted(self):
        return self.__voted

    @property
    def hyperlink(self) -> str:
        return self.__hyperlink

    @property
    def image_hyperlink(self) -> str:
        return self.__image_hyperlink

    @image_hyperlink.setter
    def image_hyperlink(self, link: str):
        self.__image_hyperlink = link

    @property
    def comments(self) -> list[Comment]:
        return self.__comments

    def add_comment(self, comment: Comment):
        self.__comments.append(comment)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def date(self) -> int:
        return self.__year

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__year}>"

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, ttl):
        if isinstance(ttl, str) and len(ttl) > 0:
            self.__title = ttl.strip()

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        if isinstance(description, str) and len(description) > 0:
            self.__description = description.strip()

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, director):
        if isinstance(director, Director):
            self.__director = director

    @property
    def genres(self):
        return self.__genres

    @genres.setter
    def genres(self, genres):
        self.__genres = genres

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime):
        if isinstance(runtime, int):
            if runtime >= 0:
                self.__runtime_minutes = runtime
            else:
                raise ValueError

    @property
    def actors(self):
        return self.__actors

    @actors.setter
    def actors(self, actor_list):
        self.__actors = actor_list

    def add_genre(self, genre):
        if isinstance(genre, Genre):
            if genre not in self.__genres:
                self.__genres.append(genre)

    def remove_genre(self, genre):
        if isinstance(genre, Genre):
            if genre in self.__genres:
                self.__genres.remove(genre)
        elif isinstance(genre, str):
            for genre in self.__genres:
                if genre.genre_name == genre:
                    self.__genres.remove(genre)

    def add_actor(self, actor):
        if isinstance(actor, Actor):
            if actor not in self.__actors:
                self.__actors.append(actor)

    def remove_actor(self, actor):
        if isinstance(actor, Actor):
            if actor in self.__actors:
                self.__actors.remove(actor)
        elif isinstance(actor, str):
            for actor in self.__actors:
                if actor.actor_full_name == actor:
                    self.__actors.remove(actor)

    def __eq__(self, other):
        if self.__title == other.__title:
            return self.__year == other.__year
        else:
            return False

    def __lt__(self, other):
        if self.__title == other.__title:
            return self.__year < other.__year
        else:
            return self.__title < other.__title

    def __hash__(self):
        return hash(self.__title + str(self.__year))


class Director:
    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()
        self.__directed_movies = list()

    @property
    def directed_movies(self):
        return self.__directed_movies

    @directed_movies.setter
    def directed_movies(self, directed_movies: []):
        self.__directed_movies = directed_movies

    def add_movie(self, movie: Movie):
        self.__directed_movies.append(movie)

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @director_full_name.setter
    def director_full_name(self, full_name):
        if full_name == "" or type(full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = full_name.strip()

    def __repr__(self):
        return f"<Director {self.director_full_name}>"

    def __eq__(self, other: 'Director'):
        if type(self) == type(other):
            if self.director_full_name == other.director_full_name:
                return True
        return False

    def __lt__(self, other: 'Director'):
        if type(self) == type(other):
            if self.director_full_name < other.director_full_name:
                return True
        if type(self) != type(other):
            raise TypeError
        return False

    def __hash__(self):
        return hash(self.director_full_name)


class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()
        self.__tagged_movies: List[Movie] = list()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @genre_name.setter
    def genre_name(self, name: str):
        if name == "" or type(name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = name.strip()

    @property
    def tagged_movies(self) -> Iterable[Movie]:
        return iter(self.__tagged_movies)

    @tagged_movies.setter
    def tagged_movies(self, l):
        self.__tagged_movies = l

    @property
    def number_of_tagged_movies(self) -> int:
        if self.__tagged_movies is None:
            return 0
        return len(self.__tagged_movies)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self.__tagged_movies

    def add_movie(self, movie: Movie):
        self.__tagged_movies.append(movie)

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if self.genre_name != other.genre_name or type(other) is not Genre:
            return False
        else:
            return True

    def __lt__(self, other):
        if self.genre_name >= other.genre_name or type(other) is not Genre:
            return False
        else:
            return True

    def __hash__(self):
        return hash(self.genre_name)


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.colleagues = set()
        self.__joined_movies = list()

    @property
    def joined_movies(self):
        return self.__joined_movies

    @joined_movies.setter
    def joined_movies(self, movies: []):
        self.__joined_movies = movies

    def add_movie(self, movie: Movie):
        self.__joined_movies.append(movie)

    def joined(self, movie: Movie):
        for m in self.__joined_movies:
            if movie == m:
                return True
        return False

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @actor_full_name.setter
    def actor_full_name(self, full_name):
        if full_name == "" or type(full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = full_name.strip()

    def __repr__(self):
        return f"<Actor {self.actor_full_name}>"

    def __eq__(self, other: 'Actor'):
        if type(self) == type(other):
            if self.actor_full_name == other.actor_full_name:
                return True
        return False

    def __lt__(self, other: 'Actor'):
        if type(self) == type(other):
            if self.actor_full_name < other.actor_full_name:
                return True
        if type(self) != type(other):
            raise TypeError(f"Type error, should be actor")
        return False

    def __hash__(self):
        return hash(self.actor_full_name)

    def add_actor_colleague(self, colleague: 'Actor'):
        if type(self) != type(colleague):
            raise TypeError(f"Colleague should be actor")
        self.colleagues.add(colleague)

    def check_if_this_actor_worked_with(self, other):
        if type(self) != type(other):
            raise TypeError("Colleague should be actor")
        else:
            return other in self.colleagues


class ModelException(Exception):
    pass


def make_comment(comment_text: str, user: User, movie: Movie, timestamp: datetime = datetime.today()):
    comment = Comment(user, movie, comment_text, timestamp)
    user.add_comment(comment)
    movie.add_comment(comment)

    return comment


def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'Genre {genre.genre_name} already applied to Movie "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)


def make_director_association(movie: Movie, director: Director):
    movie.director = director
    director.add_movie(movie)


def make_actor_association(movie: Movie, actor: Actor):
    if actor.joined(movie):
        raise ModelException(f'Actor {actor.actor_full_name} already applied to Movie "{movie.title}"')

    movie.add_actor(actor)
    actor.add_movie(movie)
