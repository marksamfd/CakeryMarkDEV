from app.Repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self):
        self.notification_repo = NotificationRepository()

    def send_notification(self, customer_email, message):
        # sending notification
        print(f"Sending push notification to {customer_email}: {message}")

        self.notification_repo.save_notification(customer_email, message)
