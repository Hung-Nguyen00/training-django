from celery import shared_task
from cart.services.send_mail import OrderEmailService
from core.celery import app


@app.task(autoretry_for=(Exception,))
def sending_email_to_admin_task(order_id: int):
    OrderEmailService.send_mail_to_admin_when_user_ordered(order_id=order_id)