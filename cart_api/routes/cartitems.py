import falcon
from playhouse.shortcuts import model_to_dict

from cart_api.database import DatabaseCartItem


# Exercise 3:
# Using the database model you created in Exercise 1 create a cartitems route
# CartItems should have a responder for POST and GET
# CartItem should have responders for GET DELETE PATCH
# Your API response statuses and bodies should conform to your OpenAPI spec


class CartItems:
    def on_get(self, req, resp):
        response = []
        all_Cartproducts = DatabaseCartItem.select()
        for cartproducts in all_Cartproducts:
            response.append(model_to_dict(cartproducts))
        resp.media = response
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        cart = req.get_media()
        new_cartItem = DatabaseCartItem(
            name=cart.get("name"),
            price=cart.get("price"),
            quantity=cart.get("quantity"),
            image_url=cart.get("image_url"),
            is_on_sale=cart.get("is_on_sale"),
            sale_price=cart.get("sale_price")
        )
        new_cartItem.save()
        resp.media = model_to_dict(new_cartItem)
        resp.status = falcon.HTTP_201


class CartItem:
    def on_delete(self, req, resp, cart_id):
        DatabaseCartItem.delete_by_id(cart_id)
        resp.status = falcon.HTTP_204

    def on_get(self, req, resp, cart_id):
        cart_product = DatabaseCartItem.get(id=cart_id)
        resp.media = model_to_dict(cart_product)
        resp.status = falcon.HTTP_200
  
    def on_patch(self, req, resp, cart_id):
        cart_product = DatabaseCartItem.get(id=cart_id)
        changes = req.media
        if "quantity" in changes:
            cart_product.quantity = changes["quantity"]
            cart_product.save()
        resp.status = falcon.HTTP_204
