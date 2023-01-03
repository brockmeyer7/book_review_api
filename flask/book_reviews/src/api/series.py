from flask import Blueprint, jsonify, abort, request
from ..models import Series, db

bp = Blueprint('series', __name__, url_prefix='/series')


@bp.route('', methods=['GET', 'POST'])
def series():
    if request.method == 'GET':
        series = Series.query.all()
        result = []
        for s in series:
            result.append(s.serialize())
        return jsonify(result)

    if request.method == 'POST':
        if 'title' not in request.json:
            return abort(400)

        s = Series(request.json['title'])
        try:
            db.session.add(s)
            db.session.commit()
            return jsonify(s.serialize())
        except:
            return jsonify(False)


@bp.route('/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def specified_series(id: int):
    if request.method == 'GET':
        s = Series.query.get_or_404(id)
        return jsonify(s.serialize())

    if request.method in ['PUT', 'PATCH']:
        if 'title' not in request.json:
            return abort(400)
        s = Series.query.get_or_404(id)
        s.title = request.json['title']
        try:
            db.session.commit()
            return jsonify(s.serialize())
        except:
            return jsonify(False)

    if request.method == 'DELETE':
        s = Series.query.get_or_404(id)
        try:
            db.session.delete(s)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
