from app.models import (
    DeliveryUser,
    BakeryUser,
    DeliveryAssignments,
    Inventory,
    Voucher,
    Rawmaterials,
    CustomerUser,
    OrderItems,
    Orders,
)
from app.db import db
from argon2 import PasswordHasher
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from app.Repositories.delivery_repository import DeliveryRepository

encrypt = PasswordHasher()


class AdminRepository:
    def __init__(self, delivery_repo: DeliveryRepository):
        self.delivery_repo = delivery_repo

    """ ============================ get all staff users =============================== """

    # ---- get all staff users ----
    def get_staff_users(self):
        stafflist = {}
        delivery_users = DeliveryUser.query.all()
        for user in delivery_users:
            stafflist[user.deliveryemail] = {
                "name": user.firstname + " " + user.lastname,
                "email": user.deliveryemail,
                "phone": user.phonenum,
                "role": "delivery",
            }
        bakery_users = BakeryUser.query.all()
        for user in bakery_users:
            stafflist[user.bakeryemail] = {
                "name": user.firstname + " " + user.lastname,
                "email": user.bakeryemail,
                "phone": user.phonenum,
                "role": "baker",
            }
        return stafflist

    """ ============================ get all customers =============================== """

    # ---- get all customers ----
    def get_customers(self):
        customers = CustomerUser.query.all()
        customer_list = []
        for customer in customers:
            customer_list.append(
                {
                    "name": customer.firstname + " " + customer.lastname,
                    "email": customer.customeremail,
                    "phone": customer.phonenum,
                }
            )
        return customer_list

    """ ============================ add staff user =============================== """

    # ---- add baker user ----
    def add_bakery_user(self, firstname, lastname, email, phone, password):
        try:
            hashed_password = encrypt.hash(password)
            bakery_user = BakeryUser(
                firstname=firstname,
                lastname=lastname,
                bakeryemail=email,
                phonenum=phone,
                password=hashed_password,
            )
            db.session.add(bakery_user)
            db.session.commit()
            return {"message": f"baker user {email} was added"}
        except Exception as e:
            return {"error": f"(repo) error adding baker user: {e}"}

    # ---- add delivery user ----
    def add_delivery_user(self, firstname, lastname, email, phone, password):
        try:
            # phone number wont be used till we edit the model
            hashed_password = encrypt.hash(password)
            delivery_user = DeliveryUser(
                firstname=firstname,
                lastname=lastname,
                phonenum=phone,
                deliveryemail=email,
                password=hashed_password,
            )
            db.session.add(delivery_user)
            db.session.commit()
            return {"message": f"delivery user {email} was added"}
        except Exception as e:
            return {"error": f"(repo) error adding delivery user: {e}"}

    """ ============================ delete staff user =============================== """

    # ---- delete baker user ----
    def delete_baker_user(self, email):
        try:
            baker = BakeryUser.query.filter_by(bakeryemail=email).first()
            if baker:
                db.session.delete(baker)
                db.session.commit()
                return {"message": "baker deleted successfully"}
            else:
                return {
                    "error": f"(repo) error deleting baker user: user not found"}
        except Exception as e:
            return {"error": f"(repo) error deleting baker user: {e}"}

    # ---- delete delivery user ----
    def delete_delivery_user(self, email):
        try:
            # get all orders assigned to the delivery user
            orders = Orders.query.filter_by(deliveryemail=email).all()
            if orders:
                # reassign the orders
                for order in orders:
                    new_delivery_email = (
                        self.delivery_repo.find_available_delivery_user()
                    )
                    if new_delivery_email:
                        order.deliveryemail = new_delivery_email
                    else:
                        return {
                            "error": "No available delivery users to reassign orders."
                        }
                db.session.commit()

            # delete the delivery user
            delivery_user = DeliveryUser.query.filter_by(
                deliveryemail=email).first()
            if delivery_user:
                db.session.delete(delivery_user)
                db.session.commit()
                return {
                    "message": "Delivery user deleted successfully and orders reassigned."
                }
            else:
                return {"error": "Delivery user not found."}

        except Exception as e:
            db.session.rollback()
            return {
                "error": f"(repo) Error deleting delivery user and reassigning orders: {e}"
            }

    """ ============================ add/edit voucher =============================== """

    # ---- view all vouchers ----
    def get_vouchers(self):
        vouchers = Voucher.query.all()
        voucher_list = {}
        for voucher in vouchers:
            voucher_list[voucher.vouchercode] = {
                "discount_percentage": voucher.discountpercentage,
            }
        return voucher_list

    # ---- add voucher ----
    def add_voucher(self, voucher_code, discount_percentage):
        voucher = Voucher(
            vouchercode=voucher_code, discountpercentage=discount_percentage
        )
        db.session.add(voucher)
        db.session.commit()
        return voucher

    # ---- edit voucher ----
    def edit_voucher(self, voucher_code, discount_percentage):
        voucher = Voucher.query.filter_by(voucher_code=voucher_code)
        if voucher:
            voucher.discountpercentage = discount_percentage
            db.session.commit()
            return voucher
        return None

    def delete_voucher(self, voucher_code):
        voucher = Voucher.query.filter_by(voucher_code=voucher_code)
        if voucher:
            db.session.delete(voucher)

    """ ============================ edit raw product or raw materials prices =============================== """

    # ------ get all raw products ------
    def prducts_rawMats(self):
        rawItems = Rawmaterials.query.all()
        products = Inventory.query.all()
        itemsList = {}
        for product in products:
            itemsList[product.name] = {
                "product_id": product.productid,
                "price": product.price,
            }
        for raw_product in rawItems:
            itemsList[raw_product.item] = {
              
                "price": raw_product.price,
            }
        return itemsList

    def edit_product(self, price, product_id, rawItem=None):
        product = Inventory.query.filter_by(product_id=product_id)
        if product:
            product.price = price
            db.session.commit()

        elif rawItem:
            rawItem.price = price
            db.session.commit()

    """ ============================ get dashboard data =============================== """

    # ============================ get dashboard data ========================
    def get_dashboard_data(
        self,
    ):  # top 5 sold items of all time, total of all prices in the last 5 days
        try:
            # Define the date 5 days ago
            five_days_ago = datetime.now() - timedelta(days=5)

            # 1. Total price of orders grouped by order date (last 5 days)
            total_prices_5_days = (
                db.session.query(
                    func.date(Orders.orderdate).label("order_date"),
                    func.sum(Orders.totalprice).label("total_price"),
                )
                .filter(Orders.orderdate >= five_days_ago)
                .group_by(func.date(Orders.orderdate))
                .order_by(func.date(Orders.orderdate))
                .all()
            )

            # Prepare data for date and total price
            total_price_data = [
                {
                    "Date": record.order_date.strftime("%d/%m/%Y"),
                    "Total Price": float(record.total_price),
                }
                for record in total_prices_5_days
            ]

            # 2. Best 5 sold items (productid, total_quantity, total_price)
            best_sold_items = (
                db.session.query(
                    OrderItems.productid,
                    func.sum(OrderItems.quantity).label("total_quantity"),
                    func.sum(OrderItems.priceatorder).label("total_price"),
                )
                .join(Orders, Orders.orderid == OrderItems.orderid)
                .group_by(OrderItems.productid)
                .order_by(desc("total_quantity"))
                .limit(5)
                .all()
            )

            # Optional: Fetch product names (assuming you have a Product table)
            product_data = []
            for item in best_sold_items:
                product = (
                    db.session.query(Inventory)
                    .filter_by(productid=item.productid)
                    .first()
                )
                product_name = product.name if product else "Customized Cake"
                product_data.append(
                    {
                        "itemName": product_name,
                        "price": float(item.total_price),
                        "qty": int(item.total_quantity),
                    }
                )

            # Prepare the final dashboard data
            dashboard_data = {
                "total_price_by_date": total_price_data,
                "best_sold_items": product_data,
            }

            return {"status": "success", "data": dashboard_data}

        except Exception as e:
            return {"status": "error", "message": str(e)}
