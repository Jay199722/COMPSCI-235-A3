from datetime import date, datetime
from typing import List

import pytest

from TMB.domain.model import *
from TMB.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 6 Movies.
    assert number_of_movies == 100


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        'test3',
        2020,
        103
    )
    movie.genres = None
    movie.actors = None
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(103) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'guardians of the galaxy'

    # Check that the Movie is commented as expected.
    comment_one = [comment for comment in movie.comments if comment.comment == 'Oh yes, this film has arrived New Zealand'][
        0]
    comment_two = [comment for comment in movie.comments if comment.comment == 'Yeah Freddie, good news'][0]

    assert comment_one.user.username == 'fmercury'
    assert comment_two.user.username == "thorke"

    # Check that the Movie is tagged as expected.
    assert Genre('action') in movie.genres
    assert Genre('adventure') in movie.genres


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(101)
    assert movie is None


def test_repository_can_retrieve_movie_ids_by_date(in_memory_repo):
    movies = in_memory_repo.get_movie_ids_for_date('2015')

    # Check that the query returned 3 Movies.
    assert len(movies) == 8


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_date(in_memory_repo):
    movies = in_memory_repo.get_movie_ids_for_date('2028')
    assert len(movies) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 18

    genre_one = [genre for genre in genres if genre.genre_name == 'action'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'adventure'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'sci-fi'][0]
    genre_four = [genre for genre in genres if genre.genre_name == 'horror'][0]

    assert genre_one.number_of_tagged_movies == 39
    assert genre_two.number_of_tagged_movies == 40
    assert genre_three.number_of_tagged_movies == 18
    assert genre_four.number_of_tagged_movies == 8


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'guardians of the galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'the departed'


def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([2, 5, 6])

    assert len(movies) == 3
    assert movies[
               0].title == 'prometheus'
    assert movies[1].title == "suicide squad"
    assert movies[2].title == 'the great wall'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([2, 200])

    assert len(movies) == 1
    assert movies[
               0].title == 'prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 200])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('horror')

    assert movie_ids == [3, 23, 28, 35, 43, 57, 62, 98]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('United States')

    assert len(movie_ids) == 0


def test_repository_returns_date_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(6)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date == 2016


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date is None


def test_repository_returns_date_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(3)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date == 2016


def test_repository_returns_none_when_there_are_no_subsequent_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(100)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date is None


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Motoring')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    comment = make_comment("Trump's onto it!", user, movie)

    in_memory_repo.add_comment(comment)

    assert comment in in_memory_repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    comment = Comment(None, movie, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_comment(comment)


def test_repository_does_not_add_a_comment_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    comment = Comment(None, movie, "Trump's onto it!", datetime.today())

    user.add_comment(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Movie doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_comments()) == 3



