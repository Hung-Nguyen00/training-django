from notification.services.message import NotificationMessage
import django.conf



class UserOrderedNotification(NotificationMessage):
    def __init__(self, assignee, order_id: int):
        self._assignee = assignee
        self.order_id = order_id
        
    
    @property
    def user(self):
        return self._assignee

    @property
    def payload(self):
        assignee = self._assignee
        order_id = self.order_id
        return {
            "assignee_first_name": assignee.first_name,
            "preview_link": django.conf.settings.FRONTEND_URL + "/orderdetails/" + str(order_id),
        }

    @property
    def verb(self) -> str:
        return "There is a user ordering products"

    @property
    def title(self) -> str:
        assignee = self._assignee
        return "Hi {0}, please check your order management site".format(assignee.first_name)

    @property
    def content(self):
        assignee = self._assignee
        return "{0} {1} <{2}> Please check your order management site".format(
            assignee.first_name,
            assignee.last_name,
            assignee.email,
        )

    @property
    def template(self):
        return "order/ordered.html"