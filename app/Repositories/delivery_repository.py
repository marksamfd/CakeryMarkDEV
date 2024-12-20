from app.models import (
    DeliveryAssignments,
    Orders,
    CustomerUser,
    OrderItems,
    DeliveryUser,
)
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class DeliveryRepository:
    """============================ assigned orders ==============================="""

    def get_assigned_orders(self, delivery_email):
        try:
            assigned_orders = (
                db.session.query(DeliveryAssignments, Orders, CustomerUser)
                .join(Orders, DeliveryAssignments.orderid == Orders.orderid)
                .join(CustomerUser, Orders.customeremail == CustomerUser.customeremail)
                .filter(DeliveryAssignments.deliveryemail == delivery_email)
                .all()
            )
            result = []
            for assignment, order, customer in assigned_orders:
                number_of_items = (
                    db.session.query(OrderItems)
                    .filter_by(orderid=order.orderid)
                    .count()
                )
                result.append(
                    {
                        "customerName": customer.firstname + " " + customer.lastname,
                        "phone": customer.phonenum,
                        "location": customer.addressgooglemapurl,
                        "numberOfItems": number_of_items,
                        "status": order.status,
                        "price": float(order.totalprice),
                        "order_id": order.orderid,
                    }
                )
            return result
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get assigned orders: {e}"}
        # -------------------------------------------------------------------------------

    """ ============================ assign delivery user =============================== """

    def find_available_delivery_user(self):
        # find delivery user with less than 5 orders assigned
        try:
            delivery_users = (
                db.session.query(DeliveryUser.deliveryemail)
                .outerjoin(Orders, DeliveryUser.deliveryemail == Orders.deliveryemail)
                .group_by(DeliveryUser.deliveryemail)
                .having(db.func.count(Orders.deliveryemail) < 5)
                .first()
            )
            return delivery_users.deliveryemail if delivery_users else None
        except Exception as e:
            print(f"(repo) Error finding available delivery user: {e}")
            return None

    # -------------------------------------------------------------------------------
    def assign_delivery_user(self, order_id):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": "Order not found"}

            # find available delivery user to assign the order -- using the
            # function above
            delivery_email = self.find_available_delivery_user()
            if not delivery_email:
                return {"error": "No available delivery users to assign the order"}

            # assign the order to the delivery user
            assignment = DeliveryAssignments(
                orderid=order_id, deliveryemail=delivery_email
            )
            # write the assigned delivery user to the order table 
            order.deliveryemail = delivery_email
            db.session.add(assignment)
            db.session.commit()
            return {"message": f"Order {order_id} assigned to {delivery_email}"}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"(repo) Error assigning delivery user: {e}"}

    """ ============================ get deliveryman name =============================== """

    def get_deliveryman_name(self, delivery_email):
        try:
            deliveryman = DeliveryUser.query.filter_by(
                deliveryemail=delivery_email
            ).first()
            if deliveryman:
                name = (
                    deliveryman.delivery_user.firstname
                    + " "
                    + deliveryman.delivery_user.lastname
                )
                return name
            else:
                return None
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get deliveryman name: {e}"}




    