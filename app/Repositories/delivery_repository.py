from app.models import DeliveryAssignments, Orders, CustomerUser, OrderItems
from app.db import db
from sqlalchemy.exc import SQLAlchemyError

class DeliveryRepository:


    ''' ============================ assigned orders =============================== '''
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
                number_of_items = db.session.query(OrderItems).filter_by(orderid=order.orderid).count()
                result.append(
                    {
                        "customerName": customer.firstname + " " + customer.lastname,
                        "phone": customer.phonenum,
                        "location": customer.addressgooglemapurl,
                        "numberOfItems": number_of_items,
                        "status": order.status,
                        "price": float(order.totalprice),
                    }
                )
            return result
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get assigned orders: {e}"}
        # -------------------------------------------------------------------------------



    ''' ============================ assign delivery user =============================== '''
    def assign_delivery_user(self, order_id):
        try:
            order = Orders.query.get(order_id)
            if not order:
                return {"error": "Order not found"}
            
            # search for all delivery users and if he has < 5 orders assigned, get his mail and assign the order to him
            delivery_users = DeliveryAssignments.query.all()
            # ---- calculate the number of orders assigned to each delivery user ----
            delivery_emails = [user.deliveryemail for user in delivery_users]
            for delivery_user in delivery_users:
                if delivery_emails.count(delivery_user.deliveryemail) < 5:
                    delivery_email = delivery_user.deliveryemail
                    break

            assignment = DeliveryAssignments(orderid=order_id,deliveryemail=delivery_email)
            db.session.add(assignment)
            db.session.commit()
            return {"message": f"Order {order_id} assigned to {delivery_email}"}
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f" (repo) {delivery_email} error assigning delivery user: {e}"}
    # -------------------------------------------------------------------------------


    ''' ============================ get deliveryman name =============================== '''
    def get_deliveryman_name(self, delivery_email):
        try:
            deliveryman = DeliveryAssignments.query.filter_by(deliveryemail=delivery_email).first()
            if deliveryman:
                name = deliveryman.delivery_user.firstname + " " + deliveryman.delivery_user.lastname
                return name
            else:
                return None
        except SQLAlchemyError as e:
            return {"error": f"(repo) can't get deliveryman name: {e}"}