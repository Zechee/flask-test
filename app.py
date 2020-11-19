from flask import Flask, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager

from marshmallow import ValidationError

from config import app_config

from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout, UserInfo

app = Flask(__name__)
app.config.from_object(app_config['development'])
db.init_app(app)
ma.init_app(app)
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify({'errmsg': err.messages}), 400


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.prefix = '/api'

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserInfo, "/userinfo")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":

    app.run(port=5000, debug=True)