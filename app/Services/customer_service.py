from app.Repositories.customer_repository import CustomerRepository

class CustomerService:
    def __init__(self):
        self.customer_repo = CustomerRepository()

    def get_all_products(self):
        return self.customer_repo.get_all_products()
