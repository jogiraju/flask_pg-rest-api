from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_restful import Api, Resource
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    __tablename__ = 'pgusers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    
class Users(Resource):
    # read
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            return {'user': user.to_dict()}, 200
        else:
            users = User.query.all()
            return {'users': [user.to_dict() for user in users]}, 200

    # create - to post multiple user records add them in the request body as: { "users": [{},{},...] }
    def post(self):
        data = request.get_json()
        users = data.get('users')
        if users and isinstance(users,list):
            new_users = []
            for user in users:
                username = user.get('username')
                email = user.get('email')
                if not username or not email:
                    return {'error': 'Username and email are required'}, 400
                else:
                   new_users.append(User(username=username, email=email))
            if len(new_users) > 0:
                db.session.add_all(new_users)
                db.session.commit() 
                return {'message': 'All Users added successfully'}, 201       
        else:     
            username = data.get('username')
            email = data.get('email')
            if not username or not email:
                return {'error': 'Username and email are required'}, 400
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User added successfully'}, 201

    # update
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        if not username or not email:
            return {'error': 'Username and email are required'}, 400
        user.username = username
        user.email = email
        db.session.commit()
        return {'message': 'User updated successfully'}, 201

    # delete
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 201

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    
    from . import routes
    app.register_blueprint(routes.bp)

    # applies CORS headers to all routes, enabling resources to be accessed
    CORS(app)
    app.json.compact = False    
    api = Api(app)
    # use api.add_resource to add the paths
    api.add_resource(Users, '/users', '/users/<int:user_id>')

    return app
