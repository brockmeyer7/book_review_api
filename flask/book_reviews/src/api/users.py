from flask import Blueprint, jsonify, abort, request
from ..models import User, Post, Book, ReadingChallenge, Rating, db
import hashlib
import secrets


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        users = User.query.all()
        result = []
        for u in users:
            result.append(u.serialize())
        return jsonify(result)

    if request.method == 'POST':
        if 'username' not in request.json or 'password' not in request.json or 'first_name' not in request.json or 'last_name' not in request.json:
            return abort(404)

        if len(request.json['username']) < 5 or len(request.json['password']) < 8:
            return abort(400)

        u = User(
            username=request.json['username'],
            password=scramble(request.json['password']),
            first_name=request.json['first_name'],
            last_name=request.json['last_name']
        )

        if 'bio' in request.json:
            u.bio = request.json['bio']

        if 'birthdate' in request.json:
            u.birthdate = request.json['birthdate']
        try:
            db.session.add(u)
            db.session.commit()
            return jsonify(u.serialize())
        except:
            return jsonify(False)


@bp.route('/<int:id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def specific_user(id: int):
    if request.method == 'GET':
        u = User.query.get_or_404(id)
        return jsonify(u.serialize())
    if request.method == 'DELETE':
        u = User.query.get_or_404(id)
        try:
            db.session.delete(u)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
    if request.method in ['PUT', 'PATCH']:
        options = ['first_name', 'last_name',
                   'username', 'birthdate', 'bio', 'password']
        count = 0
        for o in options:
            if o in request.json:
                count += 1
        if count == 0:
            return abort(400)
        u = User.query.get_or_404(id)
        if 'username' in request.json:
            u.username = request.json['username']
        if 'password' in request.json:
            u.password = request.json['password']
        if 'first_name' in request.json:
            u.first_name = request.json['first_name']
        if 'last_name' in request.json:
            u.last_name = request.json['last_name']
        if 'birthdate' in request.json:
            u.birthdate = request.json['birthdate']
        if 'bio' in request.json:
            u.bio = request.json['bio']
        try:
            db.session.commit()
            return jsonify(u.serialize())
        except:
            return jsonify(False)


@bp.route('/<int:id>/posts', methods=['GET', 'POST'])
def posts(id: int):
    if request.method == 'GET':
        u = User.query.get_or_404(id)
        result = []
        for p in u.posts:
            result.append(p.serialize())
        return jsonify(result)

    if request.method == 'POST':
        if 'title' not in request.json or 'content' not in request.json:
            return abort(404)

        p = Post(
            user_id=id,
            title=request.json['title'],
            content=request.json['content']
        )

        db.session.add(p)
        db.session.commit()
        return jsonify(p.serialize())


@bp.route('/<int:user_id>/posts/<int:post_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def post_id(user_id: int, post_id: int):
    def find_post(u: User, post_id: int):
        for p in u.posts:
            if p.id == post_id:
                return p
        return False

    if request.method == 'GET':
        u = User.query.get_or_404(user_id)
        result = find_post(u, post_id)
        if result != False:
            return jsonify(result.serialize())
        return abort(404)

    if request.method in ['PUT', 'PATCH']:
        u = User.query.get_or_404(user_id)
        if 'title' not in request.json and 'content' not in request.json:
            return abort(400)
        p = find_post(u, post_id)
        if p == False:
            return abort(404)
        if 'title' in request.json:
            p.title = request.json['title']
        if 'content' in request.json:
            p.content = request.json['content']
        try:
            db.session.commit()
            return jsonify(p.serialize())
        except:
            return jsonify(False)

    if request.method == 'DELETE':
        u = User.query.get_or_404(user_id)
        p = find_post(u, post_id)
        if p == False:
            return abort(404)
        try:
            db.session.delete(p)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)


@bp.route('<int:id>/books', methods=['GET', 'POST'])
def user_books(id: int):
    if request.method == 'GET':
        u = User.query.get_or_404(id)
        result = []
        for b in u.books:
            result.append(b.serialize())
        return jsonify(result)

    if request.method == 'POST':
        if 'book_id' not in request.json or 'status' not in request.json:
            return abort(400)
        b = Book.query.get_or_404(request.json['book_id'])
        if request.json['status'] == 1:
            status = 'Read'
        elif request.json['status'] == 2:
            status = 'Currently Reading'
        elif request.json['status'] == 3:
            status = 'Want to Read'
        else:
            return abort(400)
        query = f"INSERT INTO books_users (book_id, user_id, status) VALUES ({b.id}, {id}, '{status}');"
        try:
            db.engine.execute(query)
            return jsonify(True)
        except:
            return jsonify(False)


@bp.route('/<int:id>/books/<int:book_id>', methods=['GET', 'DELETE'])
def specific_book(id: int, book_id: int):
    if request.method == 'GET':
        u = User.query.get_or_404(id)
        for b in u.books:
            if b.id == book_id:
                return jsonify(b.serialize())
        return abort(404)
    if request.method == 'DELETE':
        u = User.query.get_or_404(id)
        for b in u.books:
            if b.id == book_id:
                try:
                    db.session.delete(b)
                    db.session.commit()
                    return jsonify(True)
                except:
                    return abort(False)
        return abort(404)


@bp.route('/<int:id>/ratings', methods=['GET'])
def get_ratings(id: int):
    u = User.query.get_or_404(id)
    result = []
    for r in u.ratings:
        result.append(r.serialize())
    return jsonify(result)


@bp.route('/<int:id>/books/<int:book_id>/rating', methods=['GET', 'POST', 'PUT', 'PATCH'])
def rating(id: int, book_id: int):
    if request.method == 'GET':
        try:
            r = Rating.query.filter_by(user_id=id, book_id=book_id).first()
            return jsonify(r.serialize())
        except:
            return jsonify(False)
    if request.method == 'POST':
        if 'rating' not in request.json:
            return abort(400)
        r = Rating(rating=request.json['rating'], user_id=id, book_id=book_id)

        if 'content' in request.json:
            r.content = request.json['content']
        try:
            db.session.add(r)
            db.session.commit()
            return jsonify(r.serialize())
        except:
            return jsonify(False)
    if request.method in ['PUT', 'PATCH']:
        if 'rating' not in request.json and 'content' not in request.json:
            return abort(400)
        try:
            r = Rating.query.filter_by(user_id=id, book_id=book_id).first()
        except:
            return abort(404)
        if 'rating' in request.json:
            r.rating = request.json['rating']
        if 'content' in request.json:
            r.content = request.json['content']
        try:
            db.session.commit()
            return jsonify(r.serialize())
        except:
            return jsonify(False)


@bp.route('/<int:id>/reading_challenge', methods=['GET', 'POST'])
def reading_challenge(id: int):
    if request.method == 'POST':

        if 'goal' not in request.json:
            return abort(400)

        rc = ReadingChallenge(goal=request.json['goal'], user_id=id)

        try:
            db.session.add(rc)
            db.session.commit()
            return jsonify(rc.serialize())
        except:
            return jsonify(False)

    if request.method == 'GET':
        try:
            rc = ReadingChallenge.query.filter_by(user_id=id).first()
            return jsonify(rc.serialize())
        except:
            return abort(404)
