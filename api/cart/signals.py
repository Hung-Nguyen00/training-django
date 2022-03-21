from django.db import transaction
from django.dispatch import Signal, receiver
from cart.tasks import sending_email_to_admin_task
from cart.models import Order


dispatch_sending_email = Signal(providing_args=["order"])


@receiver(dispatch_sending_email)
def sending_email_when_user_order_trigger(sender, order: Order, **kwargs):
    # transaction.on_commit(lambda: export_avoid_timeout.delay(employee_list=query_set, csv_log_id=csv_log.id))
    transaction.on_commit(lambda: sending_email_to_admin_task.delay(order.pk))
