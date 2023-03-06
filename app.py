from flask import Flask, jsonify
from flask_smorest import Api
from resources.item import blp as Itemblueprint
from resources.store import blp as Storeblueprint
from resources.tag import blp as Tagblueprint
from resources.user import blp as Userblueprint
from db import db
import models
import os
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

db_url = None

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger_ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = r"https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICAIONS"] = False
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)

app.config["JWT_SECRET_KEY"] = "215681521285574490940322083675105761439"
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header,jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header,jwt_payload):
    return (
        jsonify(
            {
                "description":"The token has been revoked.","error":"token_revoked"
            }
        ),401,
    )

@jwt.expired_token_loader
def expired_token_callback(jwt_header,jwt_payload):
    return (
        jsonify({"message":"the token has expired.","error":"token_expired"}),401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return(
        jsonify({"message":"Siggnature verification failed.","error":"invalid_token"}),401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return(
        jsonify(
            {
                "message":"Request does not contain an access token",
                "error":"authorization required"
            }
        ),401,
    )

api.register_blueprint(Itemblueprint)
api.register_blueprint(Storeblueprint)
api.register_blueprint(Tagblueprint)
api.register_blueprint(Userblueprint)

app.run(debug=True)
