from app.models import Orders, OrderItems, Inventory, Voucher, Cart, DeliveryAssignments
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class OrderRepository:
    """============================ create order ==============================="""

    def create_order(self, customer_email, cart_items, voucher_code):
        try:
            discount = 0
            # calculate discount if applicable
            if voucher_code:
                voucher = Voucher.query.filter_by(
                    vouchercode=voucher_code).first()
                if not voucher:
                    return {"error": "(repo) Invalid voucher code"}
                discount = voucher.discountpercentage / 100

            B_price = sum(
                item["quantity"] * item["price"] for item in cart_items
            )  # price before discount
            total_price = B_price * (1 - discount)  # total price

            # ----  new order ----
            new_order = Orders(
                customeremail=customer_email, totalprice=total_price, status="preparing"
            )
            db.session.add(new_order)
            db.session.flush()

            # ------- cart items to order items -------
            order_items = []
            for item in cart_items:
                order_item = OrderItems(
                    orderid=new_order.orderid,
                    productid=item["productid"],
                    quantity=item["quantity"],
                    priceatorder=item["price"],
                )
                db.session.add(order_item)
                # add order item to order_items list
                order_items.append(order_item)
            # ---------------- empty the cart ----------------
            cart = Cart.query.filter_by(customeremail=customer_email).first()
            if cart:
                for cart_item in cart.cart_items:
                    db.session.delete(cart_item)

            db.session.commit()

            return {
                "message": f"Order created successfully, voucher: {voucher_code}, price before discount: {B_price}, discount: {discount}, total price: {total_price}",
                "order_id": new_order.orderid,
                "total_price": total_price,
                "items": [
                    {"productid": i.productid, "quantity": i.quantity}
                    for i in order_items
                ],
            }
        except Exception as e:
            db.session.rollback()
            return {"error": f"(repo) error during order creation: {e}"}

    # -------------------------------------------------------------------------------

    """============================ get orders by customer ==============================="""
    """ first we will take email, get all orders ids, then get all order items by order ids one by one """

    """--------------------Get Order IDs by Customer ------------------"""

    def get_order_ids_by_customer(
        self, customer_email
    ):  # this function will return a list of order ids
        orders = Orders.query.filter_by(customeremail=customer_email).all()
        if not orders:
            return []
            # list of ids
        return [order.orderid for order in orders]

    # --------------------------- function to get orders by customer email ---
    def get_orders_by_customer(self, customer_email):
        try:
            # Get a list of order IDs for the customer
            order_ids = self.get_order_ids_by_customer(customer_email)
            if not order_ids:
                return {"message": "No orders found"}
            # Use `get_order_by_id` to get details for each order
            orders = [self.get_order_by_id(order_id) for order_id in order_ids]
            # Filter out any None values (in case an order ID doesn't exist)
            orders = [order for order in orders if order is not None]

            return orders
        except Exception as e:
            print(f"(repo) error fetching orders by customer: {e}")
            return {"error": "An error occurred while fetching orders"}

    # -------------------------------------------------------------------------------

    """============================ get order details by id ==============================="""

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
                        "productName": (
                            Inventory.query.get(item.productid).name
                            if item.productid
                            else None
                        ),
                        "quantity": item.quantity,
                        "priceAtOrder": (
                            float(
                                item.priceatorder) if item.priceatorder else 0
                        ),
                    }
                    for item in order.order_items
                ],
            }
            return order_details
        except SQLAlchemyError as e:
            return {"error": f" (repo) can't get order details, {e}"}

    # -------------------------------------------------------------------------------

    """============================ update order status ==============================="""

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

    """============================ get orders by status ==============================="""

    def get_orders_by_status(self, status):
        try:
            orders = Orders.query.filter_by(status=status).all()
            return [
                {
                    "orderID": order.orderid,
                    "customerEmail": order.customeremail,
                    "orderDate": (
                        order.orderdate.isoformat() if order.orderdate else None
                    ),
                    "totalPrice": float(order.totalprice) if order.totalprice else 0,
                }
                for order in orders
            ]
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get orders by status: {e}"}

    # -------------------------------------------------------------------------------
    """============================ get all orders ==============================="""

    def get_all_orders(self):
        try:
            return Orders.query.all()
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get all orders: {e}"}

    # -------------------------------------------------------------------------------

    def get_customerEmail_by_order_id(self, order_id):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": " (repo) order not found"}
            return order.customeremail
        except SQLAlchemyError as e:
            return {"error": f" (repo) error getting customer email: {e}"}


    def close_order(self, order_id): # to delete the order from deliveryuser assigments table and mark as Done
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": " (repo) order not found"}
            order.status = "Done"
            # delete the order from deliveryuser assignments
            delivery_assignment = DeliveryAssignments.query.filter_by(orderid=order_id).first()
            if delivery_assignment:
                db.session.delete(delivery_assignment)
            
            db.session.commit()
            return {"message": f" (repo) order closed successfully"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f" (repo) error closing order: {e}"}
        

    def get_active_order_by_customer(self, customer_email):
     try:
        # get last order with status out_for_delivery ( used in the order closing in otp verification)
        order = (
            Orders.query.filter_by(customeremail=customer_email, status="out_for_delivery")
            .order_by(Orders.orderdate.desc())
            .first()
        )
        return order
     except SQLAlchemyError as e:
        print(f"(OrderRepository) Error fetching active order: {e}")
        return None
