import csv
from core.utils import mkdir
from django.conf import settings
import time
from cart.models import CsvLog, Order
from cart.enums import CsvLogStatus

from core import utils

logger = utils.get_logger(__name__)


def order_export_csv(csv_log_id, order_ids):
    size = 0
    csv_log = CsvLog.objects.get(id=csv_log_id)
    order_list = Order.objects.filter(id__in=order_ids)
    fields = [
        "code",
        "address",
        "status",
        "total",
        "shipping_fee",
        "products",
    ]
    csv_folder = f"csv/{time.strftime('%Y/%m/%d')}"
    folder_path = mkdir(f"{settings.MEDIA_ROOT}/{csv_folder}")
    file_name = f"{int(time.time())}.csv"
    file_path = f"{folder_path}/{file_name}"
    order_value_list = [(
        order.code,
        order.address,
        order.status,
        order.total,
        order.shipping_fee,
        ", ".join(str(name) for name in order.products)
    ) for order in order_list]

    with open(file_path, "w+", newline="", encoding="utf-8-sig") as file_output:
        writer = csv.writer(file_output)
        writer.writerow(fields)
        for order in order_value_list:
            writer.writerow(order)
            size += len(order)

    csv_log.file_size = size
    csv_log.file_path = f"{csv_folder}/{file_name}"
    csv_log.status = CsvLogStatus.DONE
    csv_log.save()
    return csv_log
