import random
import string
import hashlib
import secrets
from faker import Faker
from random_word import RandomWords
from book_reviews.src import models as m
from book_reviews.src import create_app

USER_COUNT = 50
SERIES_COUNT = 3
AUTHOR_COUNT = 20
BOOK_COUNT = 100
POST_COUNT = 100
RATING_COUNT = 1000
POST_COUNT = 100
READING_CHALLENGE_COUNT = 25


def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    )

    salt = secrets.token_hex(16)

    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def truncate_tables():
    """Delete all rows from database tables"""
    m.db.session.execute(m.books_genres_table.delete())
    m.db.session.execute(m.books_awards_table.delete())
    m.db.session.execute(m.books_users_table.delete())
    m.db.session.execute(m.authors_books_table.delete())
    m.User.query.delete()
    m.Book.query.delete()
    m.Rating.query.delete()
    m.ReadingChallenge.query.delete()
    m.Award.query.delete()
    m.Post.query.delete()
    m.Author.query.delete()
    m.Series.query.delete()
    m.Genre.query.delete()
    m.db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()
    rw = RandomWords()

    # Create users
    last_user = None
    for _ in range(USER_COUNT):
        birthdate_bool = random.choice([True, False])
        bio_bool = random.choice([True, False])
        first_name = fake.unique.first_name()
        last_user = m.User(
            first_name=first_name,
            last_name=fake.unique.last_name(),
            username=first_name.lower() + str(random.randint(1, 150)),
            password=random_passhash()
        )
        if birthdate_bool:
            last_user.birthdate = fake.date_of_birth(
                minimum_age=18, maximum_age=105)
        if bio_bool:
            last_user.bio = fake.sentence()
        m.db.session.add(last_user)

    # Insert users
    m.db.session.commit()

    # Create genres
    genres = ['Fantasy', 'Science Fiction', 'Romance', 'Thriller',
              'Mystery', 'Western', 'History', 'Contemporary', 'Poetry', 'Dystopian']
    last_genre = None
    for g in genres:
        last_genre = m.Genre(
            name=g
        )
        m.db.session.add(last_genre)

    # Insert genres
    m.db.session.commit()

    # Create series
    last_series = None
    for _ in range(SERIES_COUNT):
        series_title_length = random.randint(1, 3)
        for i in range(series_title_length):
            if i == 0:
                series_title = rw.get_random_word().capitalize()
            else:
                series_title = series_title + " " + rw.get_random_word().capitalize()
        last_series = m.Series(
            title=series_title
        )
        m.db.session.add(last_series)

    # Insert series
    m.db.session.commit()

    # Create awards
    awards = ['Pulitzer Prize', 'Nobel Prize', 'Hugo Award',
              'National Book Award', 'John Newberry Medal', 'Booker Prize']
    last_award = None
    for a in awards:
        last_award = m.Award(
            name=a
        )
        m.db.session.add(last_award)

    # Insert awards
    m.db.session.commit()

    # Create Authors
    last_author = None
    for _ in range(AUTHOR_COUNT):
        website_bool = random.randint(0, 1)
        last_author = m.Author(
            first_name=fake.unique.first_name(),
            last_name=fake.unique.last_name(),
            birthdate=fake.date_of_birth(minimum_age=18, maximum_age=80)
        )
        if website_bool == 1:
            last_author.website = "http://" + \
                last_author.first_name.lower() + last_author.last_name.lower() + ".com"
        m.db.session.add(last_author)

    # Insert Authors
    m.db.session.commit()

    # Create Books
    last_book = None
    for _ in range(BOOK_COUNT):
        book_title_length = random.randint(1, 3)
        for i in range(book_title_length):
            if i == 0:
                book_title = rw.get_random_word().capitalize()
            else:
                book_title = book_title + " " + rw.get_random_word().capitalize()
        last_book = m.Book(
            title=book_title,
            publication_year=fake.year(),
            page_count=random.randint(100, 1000)
        )
        m.db.session.add(last_book)

    # Insert books
    m.db.session.commit()

    # Add book genre, awards, author
    for book_id in range(last_book.id - BOOK_COUNT + 1, last_book.id + 1):
        book_genre_pairs = set()
        book_award_pairs = set()
        book_author_pairs = set()
        genre_count = random.randint(1, 2)
        award_count = random.randint(0, 2)
        author_rand = random.randint(1, 10)
        if author_rand > 1:
            author_count = 1
        else:
            author_count = 2
        # Add genres to books
        while len(book_genre_pairs) < genre_count:
            book_genre = (book_id, random.randint(
                last_genre.id - len(genres) + 1, last_genre.id))
            if book_genre in book_genre_pairs:
                continue
            book_genre_pairs.add(book_genre)
        # Add awards to books
        while len(book_award_pairs) < award_count:
            book_award = (book_id, random.randint(
                last_award.id - len(awards) + 1, last_award.id))
            if book_award in book_award_pairs:
                continue
            book_award_pairs.add(book_award)
        # Add authors to books
        while len(book_author_pairs) < author_count:
            book_author = (book_id, random.randint(
                last_author.id - AUTHOR_COUNT + 1, last_author.id))
            if book_author in book_author_pairs:
                continue
            book_author_pairs.add(book_author)
        new_book_genres = [{"book_id": pair[0], "genre_id": pair[1]}
                           for pair in list(book_genre_pairs)]
        new_book_awards = [{"book_id": pair[0], "award_id": pair[1]}
                           for pair in list(book_award_pairs)]
        new_book_authors = [{"book_id": pair[0], "author_id": pair[1]}
                            for pair in list(book_author_pairs)]

        insert_genre_query = m.books_genres_table.insert().values(new_book_genres)
        m.db.session.execute(insert_genre_query)
        if award_count != 0:
            insert_award_query = m.books_awards_table.insert().values(new_book_awards)
            m.db.session.execute(insert_award_query)
        insert_author_query = m.authors_books_table.insert().values(new_book_authors)
        m.db.session.execute(insert_author_query)

    m.db.session.commit()

    # Add books to series

    for series_id in range(last_series.id - SERIES_COUNT + 1, last_series.id + 1):
        author_id = random.randint(
            last_author.id - AUTHOR_COUNT + 1, last_author.id)
        books = m.Author.query.get_or_404(author_id).books
        for i, book in enumerate(books):
            book.series_id = series_id,
            book.series_order = i + 1
            m.db.session.commit()

    # Create posts
    last_post = None
    for _ in range(POST_COUNT):
        last_post = m.Post(
            title=rw.get_random_word(),
            content=fake.sentence(),
            user_id=random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        )

        last_post.created_at = fake.past_datetime()
        m.db.session.add(last_post)

    # Insert posts
    m.db.session.commit()

    # Create Ratings
    last_rating = None
    for _ in range(RATING_COUNT):
        has_content = random.randint(0, 1)
        last_rating = m.Rating(
            rating=random.randint(1, 5),
            book_id=random.randint(
                last_book.id - BOOK_COUNT + 1, last_book.id),
            user_id=random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        )
        if has_content == 1:
            last_rating.content = fake.sentence()
        last_rating.created_at = fake.past_datetime()
        m.db.session.add(last_rating)

    # Insert Ratings
    m.db.session.commit()

    # Create Reading_Challenges
    user_ids = [i for i in range(
        last_user.id - USER_COUNT + 1, last_user.id + 1)]
    last_rc = None
    for _ in range(READING_CHALLENGE_COUNT):
        last_rc = m.ReadingChallenge(
            goal=random.randint(1, 20),
            user_id=random.choice(user_ids)
        )
        user_ids.remove(last_rc.user_id)
        last_rc.books_read = random.randint(0, last_rc.goal)
        m.db.session.add(last_rc)

    # Insert reading challenges
    m.db.session.commit()

    # Add user books
    status_options = ['Read', 'Currently Reading', 'Want to Read']
    for user_id in range(last_user.id - USER_COUNT + 1, last_user.id + 1):
        user_book_items = set()
        user_book_pairs = set()
        book_count = random.randint(1, 10)
        while len(user_book_items) < book_count:
            user_book = [
                user_id,
                random.randint(last_book.id - BOOK_COUNT + 1, last_book.id),
            ]
            if tuple(user_book) in user_book_pairs:
                continue
            user_book_pairs.add(tuple(user_book))
            user_book.append(random.choice(status_options))
            user_book_items.add(tuple(user_book))
        new_user_books = [{"user_id": item[0], "book_id": item[1], "status": item[2]}
                          for item in list(user_book_items)]
        insert_book_query = m.books_users_table.insert().values(new_user_books)
        m.db.session.execute(insert_book_query)

    m.db.session.commit()


# run script
if __name__ == '__main__':
    main()
