from django.http import HttpResponse
from cart.services.send_mail import OrderEmailService
from core.celery import app
from cart.services.write_csv import order_export_csv
from cart.models import Order


@app.task(autoretry_for=(Exception,))
def sending_email_to_admin_task(order_id: int):
    OrderEmailService.send_mail_to_admin_when_user_ordered(order_id=order_id)
    
@app.task(serializer='json')
def order_export_task(csv_log_id, order_ids):
    order_export_csv(csv_log_id, order_ids)