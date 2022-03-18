from core.celery import app


@app.task(autoretry_for=(Exception,))
def create_employee_thumbnail_task(employee_id, user_id, **kwargs):
    return 0