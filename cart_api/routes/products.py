import falcon
from playhouse.shortcuts import model_to_dict
from cart_api.database import DatabaseProducts


class Product:
    def on_get(self, req, resp, product_id):
        product = DatabaseProducts.get(id=product_id)
        resp.media = model_to_dict(product)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, product_id):
        DatabaseProducts.delete_by_id(product_id)
        resp.status = falcon.HTTP_204


# Excercise 2:
# Products route should respond to GET and POST requests
# GET products returns a list of every product in the database
# POST products creates a product and returns the data it created


class Products:
    def on_get(self, req, resp):
        response = []
        all_products = DatabaseProducts.select()
        for product in all_products:
            response.append(model_to_dict(product))
        resp.media = response
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        obj = req.get_media()
        new_product = DatabaseProducts(
            name=obj.get("name"),
            description=obj.get("description"),
            image_url=obj.get("image_url"),
            price=obj.get("price"),
            is_on_sale=obj.get("is_on_sale"),
            sale_price=obj.get("sale_price"),
        )
        new_product.save()
        resp.media = model_to_dict(new_product)
        resp.status = falcon.HTTP_201
