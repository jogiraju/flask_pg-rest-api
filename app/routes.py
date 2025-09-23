from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/healthz')
def health():
    return jsonify({"status": "ok"}), 200

# The below route is newly added
@bp.route('/')
def hello():
    return jsonify({"message": "Hello World!"}), 200


