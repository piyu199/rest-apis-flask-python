from marshmallow import Schema,fields


class PlaneItemSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class PlaneStoreSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)


class PlainTagSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)


class ItemSchema(PlaneItemSchema):
    store_id = fields.Int(required=True,load_only=True)
    store=fields.Nested(PlaneStoreSchema(),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)


class StoreSchema(PlaneStoreSchema):
    item=fields.List(fields.Nested(PlaneItemSchema()),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)


class TagsSchema(PlainTagSchema):
    store_id=fields.Int(load_only=True)
    store=fields.Nested(PlaneStoreSchema(),dump_only=True)
    items=fields.List(fields.Nested(PlaneItemSchema()),dump_only=True)


class TagAndItemsSchema(Schema):
    message=fields.Str()
    item=fields.Nested(ItemSchema)
    age=fields.Nested(TagsSchema)


class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True,load_only=True)

