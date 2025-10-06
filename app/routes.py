from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/healthz')
def health():
    return jsonify({"status": "okay?"}), 200

# The below route is newly added
@bp.route('/hello')
def hello():
    return jsonify({"message": "Hello World???"}), 200
