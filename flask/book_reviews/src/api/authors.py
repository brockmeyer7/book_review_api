from flask import Blueprint, jsonify, abort, request
from ..models import Author, db

bp = Blueprint('authors', __name__, url_prefix='/authors')


@bp.route('', methods=['GET', 'POST'])
def authors():
    if request.method == 'GET':
        authors = Author.query.all()
        result = []
        for a in authors:
            result.append(a.serialize())
        return jsonify(result)

    if request.method == 'POST':
        if 'first_name' not in request.json or 'last_name' not in request.json or 'birthdate' not in request.json:
            return abort(400)

        a = Author(request.json['first_name'], request.json['last_name'],
                   birthdate=request.json['birthdate'])

        if 'website' in request.json:
            a.website = request.json['website']

        try:
            db.session.add(a)
            db.session.commit()
            return jsonify(a.serialize())
        except:
            return jsonify(False)


@bp.route('/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def specified_author(id: int):
    if request.method == 'GET':
        a = Author.query.get_or_404(id)
        return jsonify(a.serialize())

    if request.method in ['PUT', 'PATCH']:
        options = ['first_name', 'last_name', 'birthdate', 'website']
        count = 0
        for o in options:
            if o in request.json:
                count += 1
        if count == 0:
            return abort(400)
        a = Author.query.get_or_404(id)

        if 'first_name' in request.json:
            a.first_name = request.json['first_name']
        if 'last_name' in request.json:
            a.last_name = request.json['last_name']
        if 'birthdate' in request.json:
            a.birthdate = request.json['birthdate']
        if 'website' in request.json:
            a.website = request.json['website']

        try:
            db.session.commit()
            return jsonify(a.serialize())
        except:
            return jsonify(False)

    if request.method == 'DELETE':
        a = Author.query.get_or_404(id)
        try:
            db.session.delete(a)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
