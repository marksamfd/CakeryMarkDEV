from app.models import Orders, OrderItems, Inventory
from app.db import db
from sqlalchemy.exc import SQLAlchemyError

class OrderRepository:
    def create_order(self, customer_email, cart_items, voucher_code=None):
        try:
            total_price = sum(item["quantity"] * item["price"] for item in cart_items)

            new_order = Orders(customeremail=customer_email, totalprice=total_price, status="preparing")
            db.session.add(new_order)
            db.session.flush()  # get the order ID

            for item in cart_items:
                order_item = OrderItems(
                    orderid=new_order.orderid,
                    productid=item["productid"],
                    customcakeid=item.get("customcakeid"),  # customcakeid not defined above, just trusting existing schema
                    quantity=item["quantity"],
                    priceatorder=item["price"]
                )
                db.session.add(order_item)

            db.session.commit()
            return {"order_id": new_order.orderid, "total_price": total_price}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error creating order: {e}"}

    def get_orders_by_customer(self, customer_email):
        try:
            orders = Orders.query.filter_by(customeremail=customer_email).all()
            return [
                {
                    "orderID": order.orderid,
                    "orderDate": order.orderdate.isoformat() if order.orderdate else None,
                    "status": order.status,
                    "totalPrice": float(order.totalprice) if order.totalprice else 0,
                    "items": [
                        {
                            "productID": item.productid,
                            "productName": Inventory.query.get(item.productid).name if item.productid else None,
                            "quantity": item.quantity,
                            "priceAtOrder": float(item.priceatorder) if item.priceatorder else 0,
                        }
                        for item in order.order_items
                    ],
                }
                for order in orders
            ]
        except SQLAlchemyError as e:
            return {"error": f"Error fetching orders: {e}"}

    def get_order_by_id(self, order_id):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return None

            order_details = {
                "orderID": order.orderid,
                "orderDate": order.orderdate.isoformat() if order.orderdate else None,
                "status": order.status,
                "totalPrice": float(order.totalprice) if order.totalprice else 0,
                "items": [
                    {
                        "productID": item.productid,
                        "productName": Inventory.query.get(item.productid).name if item.productid else None,
                        "quantity": item.quantity,
                        "priceAtOrder": float(item.priceatorder) if item.priceatorder else 0,
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

    def get_orders_by_status(self, status):
        try:
            orders = Orders.query.filter_by(status=status).all()
            return [
                {
                    "orderID": order.orderid,
                    "customerEmail": order.customeremail,
                    "orderDate": order.orderdate.isoformat() if order.orderdate else None,
                    "totalPrice": float(order.totalprice) if order.totalprice else 0,
                }
                for order in orders
            ]
        except SQLAlchemyError as e:
            return {"error": f"Error fetching orders by status: {e}"}

    def get_all_orders(self):
        try:
            return Orders.query.all()
        except SQLAlchemyError as e:
            return {"error": f"Error fetching all orders: {e}"}
