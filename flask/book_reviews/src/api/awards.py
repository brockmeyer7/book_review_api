from flask import Blueprint, jsonify, abort, request
from ..models import Award, Genre, db

bp = Blueprint('awards', __name__, url_prefix='/awards')


@bp.route('', methods=['GET', 'POST'])
def awards():
    if request.method == 'GET':
        awards = Award.query.all()
        result = []
        for a in awards:
            result.append(a.serialize())
        return jsonify(result)

    if request.method == 'POST':
        if 'name' not in request.json:
            return abort(400)

        a = Award(request.json['name'])
        try:
            db.session.add(a)
            db.session.commit()
            return jsonify(a.serialize())
        except:
            return jsonify(False)


@bp.route('/<int:id>', methods=['GET', 'DELETE'])
def award_id(id: int):
    if request.method == 'GET':
        a = Award.query.get_or_404(id)
        return jsonify(a.serialize())

    if request.method == 'DELETE':
        a = Award.query.get_or_404(id)
        try:
            db.session.delete(a)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
