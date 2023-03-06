from db import db

class StoreModel(db.Model):
    __tablename__="stores"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    item=db.relationship("ItemsModel",back_populates="stores",lazy="dynamic",cascade="all,delete")
    tags=db.relationship("TagsModel",back_populates="store",lazy="dynamic")