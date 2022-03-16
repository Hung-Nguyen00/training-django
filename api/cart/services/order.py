from usermodel.models import User
from cart.models import Order
from cart.enums import OrderStatus
import random
import string
import datetime

class OrderService:
    def __init__(self, user: User):
        self.user = user
    
    def create_code(self, length: int = 6):
        current_date = str(datetime.date.today().strftime("%d/%m/%Y")).replace("/", "")
        code = ''.join((random.choice(string.ascii_uppercase) for x in range(length))) + current_date
        check_order = Order.objects.filter(code=code).exists()
        while check_order:
            code, checked = self.create_code()
            if checked:
                check_order = False
        return code, True     
    
    def create_order_if_not_exists(self):
        order, created = Order.objects.get_or_create(user=self.user, status=OrderStatus.IS_SHOPPING, defaults={})
        return order
    