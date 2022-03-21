import time 
from notification.services.manager import NotificationManager
from cart.mails.email_frame import UserOrderedNotification
from usermodel.models import User


class OrderEmailService:
    
    @staticmethod
    def send_mail_to_admin_when_user_ordered(order_id: int):
        users = User.objects.filter(is_staff=True, is_active=True)
        for user in users:
            time.sleep(5)
            NotificationManager.send(UserOrderedNotification(user, order_id))
            
    