from flask import Blueprint, jsonify, abort, request
from ..models import Genre, db

bp = Blueprint('genres', __name__, url_prefix='/genres')


@bp.route('', methods=['GET', 'POST'])
def genres():
    if request.method == 'GET':
        genres = Genre.query.all()
        result = []
        for g in genres:
            result.append(g.serialize())
        return jsonify(result)

    if request.method == 'POST':
        if 'name' not in request.json:
            return abort(400)

        g = Genre(request.json['name'])
        try:
            db.session.add(g)
            db.session.commit()
            return jsonify(g.serialize())
        except:
            return jsonify(False)
