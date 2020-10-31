from datetime import date

from TMB.domain.model import *

import pytest


@pytest.fixture()
def movie():
    return Movie(
        'test movie',
        2020,
        101
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('New Zealand')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id == 101
    assert movie.date == 2020
    assert movie.title == 'test movie'

    assert repr(
        movie) == '<Movie test movie, 2020>'


def test_movie_less_than_operator():
    movie_1 = Movie(
        'a', 2012, None
    )

    movie_2 = Movie(
        'a', 2014, None
    )

    assert movie_1 < movie_2


def test_genre_construction(genre):
    assert genre.genre_name == 'New Zealand'

    for movie in genre.tagged_movies:
        assert False

    assert not genre.is_applied_to(Movie(None, None, None))


def test_make_comment_establishes_relationships(movie, user):
    comment_text = 'COVID-19 in the USA!'
    comment = make_comment(comment_text, user, movie)

    # Check that the User object knows about the Comment.
    assert comment in user.comments

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Movie knows about the Comment.
    assert comment in movie.comments

    # Check that the Comment knows about the Movie.
    assert comment.movie is movie


def test_make_genre_associations(movie, genre):
    make_genre_association(movie, genre)

    # Check that the Movie knows about the Genre.
    assert genre in movie.genres

    # check that the Genre knows about the Movie.
    assert genre.is_applied_to(movie)
    assert movie in genre.tagged_movies


def test_make_genre_associations_with_movie_already_tagged(movie, genre):
    make_genre_association(movie, genre)

    with pytest.raises(ModelException):
        make_genre_association(movie, genre)
