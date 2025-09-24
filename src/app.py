"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Profile, Post, UserGroup, Group
from sqlalchemy import select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    query = select(User).where(User.id == id)
    data = db.session.execute(query).scalar_one()

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': data.serialize()
    }
    return jsonify(response_body), 200


@app.route('/profile/<int:id>', methods=['GET'])
def get_one_profile(id):
    query = select(Profile).where(Profile.id == id)
    data = db.session.execute(query).scalar_one()

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': data.serialize()
    }
    return jsonify(response_body), 200




@app.route('/user', methods=['GET'])
def handle_hello():
    query = select(User)
    data = db.session.execute(query).scalars().all()
    print(data) 
    print(data[0].posts)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': [user.serialize() for user in data]
    }

    return jsonify(response_body), 200


@app.route('/profile', methods=['GET'])
def handle_all_profiles():
    query = select(Profile)
    data = db.session.execute(query).scalars().all()
    print(data) 
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': [profile.serialize() for profile in data]
    }

    return jsonify(response_body), 200


@app.route('/profile', methods=['POST'])
def handle_new_profile():
    data = request.json
    new_profile = Profile(bio = data["bio"], user_id=data["user_id"])
    db.session.add(new_profile)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': new_profile.serialize()
    }

    return jsonify(response_body), 200

@app.route('/post', methods=['POST'])
def handle_new_post():
    data = request.json
    new_post = Post(title = data["title"], user_id=data["user_id"], content=data["content"])
    db.session.add(new_post)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': new_post.serialize()
    }

    return jsonify(response_body), 200


@app.route('/post', methods=['GET'])
def handle_all_posts():
    query = select(Post)
    data = db.session.execute(query).scalars().all()
    print(data) 
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': [post.serialize() for post in data]
    }

    return jsonify(response_body), 200



@app.route('/user_groups', methods=['GET'])
def handle_all_user_groups():
    query = select(UserGroup)
    data = db.session.execute(query).scalars().all()
    print(data) 
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': [user_group.serialize() for user_group in data]
    }

    return jsonify(response_body), 200

@app.route('/group', methods=['GET'])
def handle_all_groups():
    query = select(Group)
    data = db.session.execute(query).scalars().all()
    print(data) 
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': [group.serialize() for group in data]
    }

    return jsonify(response_body), 200

@app.route('/user_group', methods=['POST'])
def handle_new_user_group():
    data = request.json
    new_user_group = UserGroup(user_id=data["user_id"], group_id=data["group_id"])
    db.session.add(new_user_group)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': new_user_group.serialize()
    }

    return jsonify(response_body), 200



@app.route('/group', methods=['POST'])
def handle_new_group():
    data = request.json
    new_group = Group(name=data["name"])
    db.session.add(new_group)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        'data': new_group.serialize()
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
