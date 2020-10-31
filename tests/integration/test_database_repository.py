from datetime import date, datetime

import pytest

from TMB.adapters.database_repository import SqlAlchemyRepository
from TMB.domain.model import *
from TMB.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    # Check that the query returned 177 Movies.
    assert number_of_movies == 100

def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    new_movie_id = number_of_movies + 1

    movie = Movie(
        'test movie',
        2020,
        new_movie_id
    )
    movie.genres = None
    movie.actors = None
    repo.add_movie(movie)

    assert repo.get_movie(new_movie_id) == movie

def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Movie is commented as expected.
    comment_one = [comment for comment in movie.comments if comment.comment == 'Oh yes, this film has arrived New Zealand'][
        0]
    comment_two = [comment for comment in movie.comments if comment.comment == 'Yeah Freddie, good news'][0]

    assert comment_one.user.username == 'fmercury'
    assert comment_two.user.username == "thorke"

    # Check that the Movie is tagged as expected.
    assert movie.genres == 'Action,Adventure,Sci-Fi'

def test_repository_does_not_retrieve_a_non_existent_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(201)
    assert movie is None

def test_repository_can_retrieve_movies_by_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_date(2014)

    # Check that the query returned 3 Movies.
    assert len(movies) == 5

    # these movies are no jokes...
    movies = repo.get_movies_by_date(2015)

    # Check that the query returned 5 Movies.
    assert len(movies) == 8

def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_date(date(2020, 3, 8))
    assert len(movies) == 0

def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()

    assert len(genres) == 18

    genre_one = [genre for genre in genres if genre.genre_name == 'Action'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'Adventure'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'Crime'][0]
    genre_four = [genre for genre in genres if genre.genre_name == 'Horror'][0]

    assert genre_one is not None
    assert genre_two is not None
    assert genre_three is not None
    assert genre_four is not None

def test_repository_can_get_first_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'

def test_repository_can_get_last_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_last_movie()
    assert movie.title == 'The Departed'

def test_repository_can_get_movies_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([2, 5, 6])

    assert len(movies) == 3
    assert movies[
               0].title == 'Prometheus'
    assert movies[1].title == "Suicide Squad"
    assert movies[2].title == 'The Great Wall'

def test_repository_does_not_retrieve_movie_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([2, 209])

    assert len(movies) == 1
    assert movies[
               0].title == 'Prometheus'

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([0, 199])

    assert len(movies) == 0

def test_repository_returns_movie_ids_for_existing_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre('Action')

    assert movie_ids == [1,5,6,9,13,15,18,25,27,30,33,34,35,36,38,39,46,49,51,52,54,55,61,66,68,70,72,76,77,79,80,81,85,86,88,90,92,95,96]

def test_repository_returns_an_empty_list_for_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre('United States')

    assert len(movie_ids) == 0


def test_repository_returns_date_of_previous_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(6)
    previous_date = repo.get_date_of_previous_movie(movie)

    assert previous_date == 2016


def test_repository_returns_none_when_there_are_no_previous_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)
    previous_date = repo.get_date_of_previous_movie(movie)

    assert previous_date is None


def test_repository_returns_date_of_next_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(3)
    next_date = repo.get_date_of_next_movie(movie)

    assert next_date == 2016


def test_repository_returns_none_when_there_are_no_subsequent_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(100)
    next_date = repo.get_date_of_next_movie(movie)

    assert next_date is None


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre('Motoring')
    genre.tagged_movies = None
    repo.add_genre(genre)

    assert genre in repo.get_genres()


def test_repository_can_add_a_comment(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    movie = repo.get_movie(2)
    comment = make_comment("Trump's onto it!", user, movie)

    repo.add_comment(comment)

    assert comment in repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(2)
    comment = Comment(None, movie, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        repo.add_comment(comment)


def test_repository_can_retrieve_comments(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_comments()) == 3


def make_movie(new_movie_date):
    movie = Movie(
        new_movie_date,
        'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room',
        'The self-isolation deadline has been pushed back',
        'https://www.nzherald.co.nz/business/news/movie.cfm?c_id=3&objectid=12316800',
        'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'
    )
    return movie

def test_can_retrieve_an_movie_and_add_a_comment_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch Movie and User.
    movie = repo.get_movie(5)
    author = repo.get_user('thorke')

    # Create a new Comment, connecting it to the Movie and User.
    comment = make_comment('First death in Australia', author, movie)

    movie_fetched = repo.get_movie(5)
    author_fetched = repo.get_user('thorke')

    assert comment in movie_fetched.comments
    assert comment in author_fetched.comments

