from app.models import DeliveryAssignments, Orders
from app.db import db
from sqlalchemy.exc import SQLAlchemyError

class DeliveryRepository:


    ''' ============================ assigned orders =============================== '''
    def get_assigned_orders(self,delivery_email):
        try:
            assigned_orders = (
                db.session.query(DeliveryAssignments, Orders)
                .join(Orders, DeliveryAssignments.orderid == Orders.orderid)
                .filter(DeliveryAssignments.deliveryemail == delivery_email)
                .all()
            )
            return [
                {
                    "orderID": order.orderid,
                    "status": order.status,
                    "customerEmail": order.customeremail,
                    "totalPrice": float(order.totalprice),
                }
                for assignment, order in assigned_orders
            ]
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get assigned orders: {e}"}
        # -------------------------------------------------------------------------------

    ''' ============================ assign delivery user =============================== '''
    def assign_delivery_user(self, order_id, delivery_email):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": "Order not found"}

            assignment = DeliveryAssignments(orderid=order_id,deliveryemail=delivery_email)
            db.session.add(assignment)
            db.session.commit()
            return {"message": f"Order {order_id} assigned to {delivery_email}"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f" (repo) error assigning delivery user: {e}"}
