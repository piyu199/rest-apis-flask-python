from flask.views import MethodView
from flask_smorest import abort,Blueprint
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import ItemSchema,ItemUpdateSchema,UserSchema
from models import ItemModel,UserModel
from passlib import pbkdf2_sha256
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from blocklist import BLOCKLIST


blp=Blueprint("Users",__name__,description="Operation on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first()
            abort(409,message="A user with the username already exists")

        user=UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message":"User created successfully."},201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        return user

    def delete(self,user_id):
        user=UserModel.query.geet_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted"},200


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user=UserModel.query.filter(UserModel.username==user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token= create_access_token(identity=user.id)
            return {"access_token":access_token}
        abort(401,message="Invalid Credentials")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"successfully logged out"}
