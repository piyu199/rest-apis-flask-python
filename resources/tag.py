from flask.views import MethodView
from flask_smorest import abort,Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import TagsSchema,TagAndItemsSchema
from models import TagModel,StoreModel,ItemModel

blp=Blueprint("Tags",__name__,description="Operation on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200,TagsSchema(many=True))
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagsSchema)
    @blp.response(200,TagsSchema)
    def post(self,tag_data,store_id):
        tag=TagModel(**tag_data,store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))

        return tag

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagToItem(MethodView):
    @blp.response(201,TagsSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)

        item.tags.add(tag)

        try:
            db.session.add()
            db.session.commit()
        except SQLAlchemyError:
            abort(500,mesage="An error occurred while inserting the tag")

        return tag

    @blp.response(200,TagAndItemsSchema)
    def delete(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, mesage="An error occurred while inserting the tag")

        return {"message":"Item removed from tag","item":item,"tag":tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagsSchema)
    def get(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202,description="Delete a tag if no item is tagged with it.")
    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted"}
        abort(404,message="Could not delete an item. make sure tag is associated with any items, then try to delete again")
