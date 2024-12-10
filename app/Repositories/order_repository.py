from app.models import Orders, OrderItems, Inventory, Voucher
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class OrderRepository:

    '''============================ create order ==============================='''
    def create_order(self, customer_email, cart_items, voucher_code=None):
        try:
            discount = 0
            # calculate discount if applicable
            if voucher_code:
                voucher = Voucher.query.filter_by(vouchercode=voucher_code).first()
                if not voucher:
                    return {"error": "(repo) Invalid voucher code"}
                discount = voucher.discountpercentage / 100
            total_price = sum(item["quantity"] * item["price"] for item in cart_items) * (1-discount) # total price

            # ----  new order ----
            new_order = Orders(customeremail=customer_email, totalprice=total_price, status="preparing")
            db.session.add(new_order)
            db.session.flush()  # get the order ID

            # ------ cart items to the order ----- 
            for item in cart_items:
                order_item = OrderItems(
                    orderid=new_order.orderid,
                    productid=item["productid"],
                    customcakeid=item.get("customcakeid"),  
                    quantity=item["quantity"],
                    priceatorder=item["price"],
                )
                db.session.add(order_item)

            db.session.commit()
            return {"Order created successfully"}

        except Exception as e:
            db.session.rollback() 
            return {"error": f"(repo) failed to create order: {e}"}
        
    # -------------------------------------------------------------------------------

    '''============================ get orders by customer ==============================='''
        
    def get_orders_by_customer(self,customer_email):
        try:
            orders = Orders.query.filter_by(customeremail=customer_email).all() # customer orders
            return [
                {
                    "orderID": order.orderid,
                    "orderDate": order.orderdate.isoformat(),
                    "status": order.status,
                    "totalPrice": float(order.totalprice),
                    "items": [
                        {
                            "productID": item.productid,
                            "productName": Inventory.query.get(item.productid).name,
                            "quantity": item.quantity,
                            "priceAtOrder": float(item.priceatorder),
                        }
                        for item in order.order_items # go to order_items table to get the items of current order
                    ],
                }
                for order in orders # loop on orders
            ]
        except SQLAlchemyError as e:
            return {"error": f" (repo) can't get orders by customer {e}"}
    # -------------------------------------------------------------------------------
        
    '''============================ get order by id ==============================='''
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
            return {"error": f" (repo) can't get order details, {e}"}
    # -------------------------------------------------------------------------------

    '''============================ update order status ==============================='''

    def update_order_status(self, order_id, status):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": " (repo) order not found"}
            order.status = status
            db.session.commit()
            return {"message": f" (repo) order status updated to {status}"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f" (repo) error updating order status: {e}"}
    # -------------------------------------------------------------------------------
        
    '''============================ get orders by status ==============================='''
    def get_orders_by_status(self,status):
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
            return {"error": f"(repo) can't get orders by status: {e}"}
        
    # -------------------------------------------------------------------------------

    '''============================ get all orders ==============================='''
    def get_all_orders(self):
        try:
            return Orders.query.all()
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get all orders: {e}"}
    # -------------------------------------------------------------------------------