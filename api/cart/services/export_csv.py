from cart.models import CsvLog
from cart.enums import CsvLogType, CsvLogStatus
from usermodel.models import User
from django.db import transaction
from cart.tasks import order_export_task
from cart.signals import dispatch_downloaded_csv
from cart.api.serializers import CsvLogSerializer




def create_export_csv_log(user: User, query_set) -> CsvLog:
    log = CsvLog()

    action_type = CsvLogType.EXPORT
    log.type = action_type
    log.status = CsvLogStatus.NEW
    log.user = user
    log.save()
    dispatch_downloaded_csv.send(sender=CsvLog, csv_log=log, query_set=query_set)
    return log

