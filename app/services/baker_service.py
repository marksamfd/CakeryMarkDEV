from app.models import Orders, DeliveryUser, DeliveryAssignments
from app.db import db




'''=================================== Baker HomePage ===================================='''
# ------------------------------------------ All orders to be baked ------------------------------------------
def get_baker_orders():
    orders = Orders.query.all()
    return [
        {
            "orderID": order.orderid,
            "orderDate": order.orderdate.isoformat() if order.orderdate else None,
            "customer": {
                "name": f"{order.customer.firstname} {order.customer.lastname}",
                "phone": order.customer.phonenum,
            },
        }
        for order in orders
    ]

'''=================================== Baker | View order ===================================='''
# -------------------------------- Get details of a specific order --------------------------------
def get_order_details(order_id):
    order = Orders.query.get(order_id)
    if not order:
        return None

    return {
        "orderID": order.orderid,
        "orderDate": order.orderdate.isoformat() if order.orderdate else None,
        "customer": {
            "name": f"{order.customer.firstname} {order.customer.lastname}",
            "phone": order.customer.phonenum,
        },
        "items": [
            {
                "productID": item.productid,
                "quantity": item.quantity,
            }
            for item in order.order_items
        ],
    }


'''=================================== Baker | View order ===================================='''
# --------------------------------  assign delivery man function --------------------------------
def assign_delivery_user(orderid):
    # find the order
    order = Orders.query.get(orderid)
    if not order:
        return {'Order not found'}

    # Find a delivery user with fewer than 5 assigned orders
    delivery_user = (
        db.session.query(DeliveryUser)
        .outerjoin(DeliveryAssignments, DeliveryUser.deliveryemail == DeliveryAssignments.deliveryemail)
        .group_by(DeliveryUser.deliveryemail)
        .having(db.func.count(DeliveryAssignments.id) < 5)
        .first()
    )
    if not delivery_user:
        return {'No available delivery users'}

    # assigning
    assignment = DeliveryAssignments(deliveryemail=delivery_user.deliveryemail, orderid=orderid)
    db.session.add(assignment)
    # order.status = "Prepared"  # Update the order status to Prepared
    db.session.commit()
    return {f"Order assigned to {delivery_user.deliveryemail}"}



# -------------------------------- Update order status --------------------------------
def update_order_status(orderid, status):
    order = Orders.query.get(orderid)
    if not order:
        return {'Order not found'}
    
    # update status
    order.status = status

    # if prepared, call assiggning function for delivery man who has less than 5 orders, this just will update database
    if status == "Prepared":
        assignment_result = assign_delivery_user(orderid)
        if "error" in assignment_result:
            return assignment_result
    db.session.commit()
    return {f'Order status updated to {status}'}

