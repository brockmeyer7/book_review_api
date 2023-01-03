from flask import Blueprint, jsonify, abort, request
from ..models import Book, Author, Genre, Award, db

bp = Blueprint('books', __name__, url_prefix='/books')


@bp.route('', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        books = Book.query.all()
        result = []
        for b in books:
            result.append(b.serialize())
        return jsonify(result)

    if request.method == 'POST':
        req = ['title', 'publication_year', 'page_count', 'authors', 'genres']
        for value in req:
            if value not in request.json:
                return abort(400)
        books = Book.query.all()
        result = []
        for b in books:
            result.append(b.serialize())
        for r in result:
            if request.json['title'] in r['title']:
                return jsonify(False)

        b = Book(
            title=request.json['title'],
            publication_year=request.json['publication_year'],
            page_count=request.json['page_count']
        )

        if 'series_id' in request.json or 'series_order' in request.json:
            if 'series_id' not in request.json or 'series_order' not in request.json:
                return abort(400)

            b.series_id = request.json['series_id']
            b.series_order = request.json['series_order']

        for author_id in request.json['authors']:
            a = Author.query.get_or_404(author_id)
            b.authors.append(a)
        for genre_id in request.json['genres']:
            g = Genre.query.get_or_404(genre_id)
            b.genres.append(g)
        if 'awards' in request.json:
            for award_id in request.json['awards']:
                a = Award.query.get_or_404(award_id)
                b.awards.append(a)
        try:
            db.session.add(b)
            db.session.commit()
            return jsonify(b.serialize())
        except:
            return jsonify(False)


@bp.route('/<int:id>/avg_rating', methods=['GET'])
def average(id: int):
    result = {"average": average}
    return jsonify(True)


@ bp.route('/<int:id>/ratings', methods=['GET'])
def ratings(id: int):
    b = Book.query.get_or_404(id)
    result = []
    for rating in b.ratings:
        result.append(rating.serialize())
    return jsonify(result)
