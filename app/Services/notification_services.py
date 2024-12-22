from firebase_admin import messaging
from app.Repositories.notification_repository import NotificationRepository
from app.models import CustomerUser

class NotificationService:
    def __init__(self):
        self.notification_repo = NotificationRepository()

    def send_notification(self, customer_email, message):
        try:
            token = self.get_customer_fcm_token(customer_email)
            if not token:
                print(f"No FCM token for customer: {customer_email}")
                return {"error": "No FCM token found"}

            # ----- Setting the message ----- 
            firebase_message = messaging.Message(
                notification=messaging.Notification(
                    title="Order Update",
                    body=message
                ),
                token=token
            )

            # ------ Send the message ------
            response = messaging.send(firebase_message)
            print(f"Notification sent: {response}")

            # ------ Save notification to database ------
            self.notification_repo.save_notification(customer_email, message)

            return {"message": "Notification sent successfully"}

        except Exception as e:
            print(f"Error in NotificationService: {e}")
            return {"error": str(e)}

    def get_customer_fcm_token(self, customer_email):
        customer = CustomerUser.query.filter_by(customeremail=customer_email).first()
        return customer.fcm_token if customer and customer.fcm_token else None
