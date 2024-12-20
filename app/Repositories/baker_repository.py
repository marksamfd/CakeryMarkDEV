from app.models import Orders, Inventory, CustomizeCake, OrderItems
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class BakerRepository:
    """============================ get all orders ==============================="""

    def get_all_orders(self):
        try:
            orders = Orders.query.all()
            return [
                {
                    "orderID": order.orderid,
                    "orderDate": order.orderdate.isoformat(),
                    "customer": {
                        "email": order.customeremail,
                    },
                    "totalPrice": float(order.totalprice),
                    "status": order.status,
                }
                for order in orders
            ]
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get all orders: {e}"}

    # -------------------------------------------------------------------------------

    """ ============================ get order details =============================== """

    def get_order_details(self, order_id):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": "Order not found"}

            order_details = {
                "orderID": order.orderid,
                "orderDate": order.orderdate.isoformat(),
                "status": order.status,
                "items": [],
                "customCake": [],
            }

            for item in order.order_items:
                item_details = {
                    "productID": item.productid,
                    "quantity": item.quantity,
                    "priceAtOrder": float(item.priceatorder),
                }

                if item.productid:
                    product = Inventory.query.get(item.productid)
                    item_details["productName"] = product.name

                if item.customcakeid:
                    custom_cake = CustomizeCake.query.get(item.customcakeid)
                    custom_cake_details = {
                        "customcakeid": custom_cake.customcakeid,
                        "cakeshape": custom_cake.cakeshape,
                        "cakesize": custom_cake.cakesize,
                        "cakeflavor": custom_cake.cakeflavor,
                        "message": custom_cake.message,
                        "layers": [
                            {
                                "innerFillings": layer.innerfillings,
                                "innerToppings": layer.innertoppings,
                                "outerCoating": layer.outercoating,
                                "outerToppings": layer.outertoppings,
                            }
                            for layer in custom_cake.layers
                        ],
                    }
                    order_details["customCake"].append(custom_cake_details)
                else:
                    order_details["items"].append(item_details)

            return order_details
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get order details: {e}"}

    # -------------------------------------------------------------------------------
    """ ============================ update order status =============================== """

    def update_order_status(self, order_id, status):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": "Order not found"}

            order.status = status
            db.session.commit()
            return {"message": f" Order status updated to {status}"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"(repo) error updating order status: {e}"}
