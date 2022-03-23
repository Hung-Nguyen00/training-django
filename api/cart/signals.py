import json
from django.db import transaction
from django.dispatch import Signal, receiver
from cart.tasks import sending_email_to_admin_task
from cart.models import Order, CsvLog
from cart.tasks import order_export_task


dispatch_sending_email = Signal(providing_args=["order"])
dispatch_downloaded_csv = Signal(providing_args=["csv_log", "query_set"])

@receiver(dispatch_sending_email)
def sending_email_when_user_order_trigger(sender, order: Order, **kwargs):
    transaction.on_commit(lambda: sending_email_to_admin_task.delay(order.pk))

@receiver(dispatch_downloaded_csv)
def export_csv_trigger(sender, csv_log: CsvLog, query_set, **kwargs):
    order_ids = list(query_set.values_list("id", flat=True))
    transaction.on_commit(lambda: order_export_task.delay(csv_log_id=csv_log.id, order_ids=order_ids))
    