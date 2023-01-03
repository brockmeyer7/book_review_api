from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

books_genres_table = db.Table(
    'books_genres',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.id', ondelete='CASCADE'),
              primary_key=True
              ),
    db.Column('genre_id', db.Integer, db.ForeignKey(
        'genres.id', ondelete='CASCADE'), primary_key=True)
)

books_awards_table = db.Table(
    'books_awards',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.id', ondelete='CASCADE'),
              primary_key=True
              ),
    db.Column('award_id', db.Integer,
              db.ForeignKey('awards.id', ondelete='CASCADE'),
              primary_key=True
              )
)

authors_books_table = db.Table(
    'authors_books',
    db.Column('author_id', db.Integer,
              db.ForeignKey('authors.id', ondelete='CASCADE'),
              primary_key=True
              ),
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.id', ondelete='CASCADE'),
              primary_key=True
              )
)


books_users_table = db.Table(
    'books_users',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.id', ondelete='CASCADE'),
              primary_key=True
              ),
    db.Column('user_id', db.Integer,
              db.ForeignKey('users.id', ondelete='CASCADE'),
              primary_key=True
              ),
    db.Column('status', db.Text, nullable=False)
)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    page_count = db.Column(db.Integer, nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey(
        'series.id', ondelete='SET NULL'))
    series_order = db.Column(db.Integer)
    authors = db.relationship('Author', secondary=authors_books_table, lazy='subquery',
                              backref=db.backref('books', lazy=True), passive_deletes=True)
    genres = db.relationship('Genre', secondary=books_genres_table, lazy='subquery',
                             backref=db.backref('books', lazy=True), passive_deletes=True)
    awards = db.relationship('Award', secondary=books_awards_table, lazy='subquery',
                             backref=db.backref('books', lazy=True), passive_deletes=True)
    ratings = db.relationship('Rating', backref='books', passive_deletes=True)

    def __init__(self, title: str, publication_year: int, page_count: int):
        self.title = title
        self.publication_year = publication_year
        self.page_count = page_count

    def serialize(self):
        authors_result = []
        genres_result = []
        awards_result = []
        for author in self.authors:
            a = Author.query.get_or_404(author.id).serialize()
            authors_result.append(a)

        for genre in self.genres:
            g = Genre.query.get_or_404(genre.id).serialize()
            genres_result.append(g)

        for award in self.awards:
            a = Award.query.get_or_404(award.id).serialize()
            awards_result.append(a)
        return {
            'id': self.id,
            'title': self.title,
            'publication_year': self.publication_year,
            'page_count': self.page_count,
            'series_id': self.series_id,
            'series_order': self.series_order,
            'authors': authors_result,
            'genres': genres_result,
            'awards': awards_result
        }


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    website = db.Column(db.Text, unique=True)

    def __init__(self, first_name: str, last_name: str, birthdate):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthdate': self.birthdate,
            'website': self.website
        }


class Series(db.Model):
    __tablename__ = 'series'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    books = db.relationship('Book', backref='books', passive_deletes=True)

    def __init__(self, title: str):
        self.title = title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title
        }


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    birthdate = db.Column(db.Date)
    bio = db.Column(db.Text)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    books = db.relationship('Book', secondary='books_users',
                            lazy='subquery', backref=db.backref('users', lazy=True), passive_deletes=True)
    reading_challenge = db.relationship(
        'ReadingChallenge', backref='user', passive_deletes=True)
    ratings = db.relationship('Rating', backref='user', passive_deletes=True)

    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'bio': self.bio,
            'birthdate': self.birthdate
        }


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, title: str, content: str, user_id: int):
        self.user_id = user_id
        self.title = title
        self.content = content

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'user_id': self.user_id
        }


class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.utcnow())
    content = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'books.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, rating: int, book_id: int, user_id: int):
        self.rating = rating
        self.book_id = book_id
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'created_at': self.created_at,
            'content': self.content,
            'book_id': self.book_id,
            'user_id': self.user_id
        }


class ReadingChallenge(db.Model):
    __tablename__ = 'reading_challenges'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal = db.Column(db.Integer, nullable=False)
    books_read = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), unique=True, nullable=False)

    def __init__(self, goal: int, user_id: int):
        self.goal = goal
        self.books_read = 0
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'goal': self.goal,
            'books_read': self.books_read,
            'user_id': self.user_id
        }


class Award(db.Model):
    __tablename__ = 'awards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
