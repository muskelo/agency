from flask import g, request
from flask_restful import Resource, abort

import flaskr.pydantic_models as pm
from flaskr.models import ItemModel, OrderModel, UserModel, ImageModel
from flaskr.utils import with_data
from flaskr.auth import auth


class UserResource(Resource):
    @auth.auth_required()
    def get_me(self):
        return g.current_user

    @auth.auth_required(role="admin", owner={"get_f": UserModel.get_})
    def get_user(self, id):
        return UserModel.get_(id=id)

    def get(self, id):
        if int(id) != -1:
            user = self.get_user(id)

            return pm.DumpUser(data=user).dict()
        else:  # get current_user
            user = self.get_me()

            return pm.DumpCurrentUser(data=user).dict()

    @auth.auth_required(owner={"get_f": UserModel.get_})
    @with_data(pm.PatchUser)
    def patch(self, id):
        user = UserModel.update_(id, **g.request_body['data'])

        return pm.DumpUser(data=user).dict()

#     @auth.login_required(role='admin', get_item_f=UserModel.get_)
#     def delete(self, id):
#         if UserModel.get_(id=id).role == "admin":
#             abort(403, message="NOBODY can't delete admin")
#         user = UserModel.delete_(id)
#         return pm.DumpUser(data=user).dict()


class UsersListResource(Resource):
    @with_data(pm.CreateUser)
    def post(self):
        user = UserModel.create_(**g.request_body['data'])

        return pm.DumpUser(data=user).dict()


class ImagesListResource(Resource):
    @auth.auth_required(role="admin")
    def get(self):
        images = ImageModel.get_list_(
            filter_by={"user_id": g.current_user.id, "item_id": None}
        )

        return pm.DumpImagesList(data=images).dict()

    @auth.auth_required()
    def post(self):
        image_file = request.files['image']
        if not image_file:
            abort(400, message="Image required")

        item_id = request.args.get("item_id") or None

        image = ImageModel.create_(
            image_file, user_id=g.current_user.id, item_id=item_id)

        return pm.DumpImage(data=image).dict()


class ImageResource(Resource):
    def delete(self, id):
        image = ImageModel.delete_(id)

        return pm.DumpImage(data=image).dict()


class ItemResource(Resource):
    def get(self, id):
        item = ItemModel.get_(id=id)

        return pm.DumpItem(data=item).dict()

    @auth.auth_required(role="admin")
    @with_data(pm.PatchItem)
    def patch(self, id):
        item = ItemModel.update_(id, **g.request_body['data'])

        return pm.DumpItem(data=item).dict()

    @auth.auth_required(role="admin")
    def delete(self, id):
        item = ItemModel.delete_(id)

        return pm.DumpItem(data=item).dict()


class ItemsListResource(Resource):
    def get(self):

        filter_keys = ["city", "type", "rooms"]
        filter_by = {key: request.args.get(key)
                     for key in filter_keys if request.args.get(key)}

        min_price = request.args.get("min_price")
        max_price = request.args.get("max_price")

        items = ItemModel.get_list_(
            filter_by=filter_by, min_price=min_price, max_price=max_price)

        return pm.DumpItemsList(data=items).dict()

    @ auth.auth_required(role="admin")
    @ with_data(pm.CreateItem)
    def post(self):
        item = ItemModel.create_(**g.request_body['data'])

        return pm.DumpItem(data=item).dict()


class OrderResource(Resource):
    @ auth.auth_required(role="admin")
    @ with_data(pm.PatchOrder)
    def patch(self, id):
        order = OrderModel.update_(id, **g.request_body['data'])

        return pm.DumpOrder(data=order).dict()


class OrdersListResource(Resource):
    # @auth.auth_required(role="admin")
    # def get_orders_for_item(self, item_id):
    #     orders = OrderModel.get_list_(item_id=item_id)
    #     return pm.DumpOrdersListForItem(data=orders).dict()

    # @auth.auth_required(role="admin", owner={"get_f": UserModel.get_, "query_arg": "user_id"})
    # def get_orders_for_user(self, user_id):
    #     orders = OrderModel.get_list_(user_id=user_id)
    #     return pm.DumpOrdersListForUser(data=orders).dict()

    @auth.auth_required(role="admin")
    def get(self):
        filter_keys = ["item_id", "user_id"]
        filter_by = {key: request.args.get(key)
                     for key in filter_keys if request.args.get(key)}

        orders = OrderModel.get_list_(filter_by=filter_by)

        return pm.DumpOrdersList(data=orders).dict()

    @ auth.auth_required()
    @ with_data(pm.CreateOrder)
    def post(self):
        order = OrderModel.create_(
            **g.request_body['data'], user_id=g.current_user.id, status="wait")

        return pm.DumpOrder(data=order).dict()
