from app.models import Orders, Inventory
from app.db import db
from sqlalchemy.exc import SQLAlchemyError

class BakerRepository:
    def get_all_orders(self):
        try:
            orders = Orders.query.all()
            return [
                {
                    "orderID": order.orderid,
                    "orderDate": order.orderdate.isoformat() if order.orderdate else None,
                    "customer": {
                        "email": order.customeremail,
                    },
                    "totalPrice": float(order.totalprice),
                    "status": order.status,
                }
                for order in orders
            ]
        except SQLAlchemyError as e:
            return {"error": f"Error fetching baker orders: {e}"}

    def get_order_details(self, order_id):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": "Order not found"}

            order_details = {
                "orderID": order.orderid,
                "orderDate": order.orderdate.isoformat() if order.orderdate else None,
                "status": order.status,
                "items": [
                    {
                        "productID": item.productid,
                        "productName": Inventory.query.get(item.productid).name if item.productid else None,
                        "quantity": item.quantity,
                        "priceAtOrder": float(item.priceatorder),
                    }
                    for item in order.order_items
                ],
            }
            return order_details
        except SQLAlchemyError as e:
            return {"error": f"Error fetching order details: {e}"}

    def update_order_status(self, order_id, status):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": "Order not found"}

            order.status = status
            db.session.commit()
            return {"message": f"Order status updated to {status}"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error updating order status: {e}"}
