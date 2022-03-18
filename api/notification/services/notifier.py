from typing import List

from core.utils import get_logger
from notification.services.message import NotificationMessage
from notification.services.result import SendNotificationResult
from notification.services.storage import NotificationStorage
from notification.transports import Transport, MailerTransport

logger = get_logger(__name__)


class Notifier:
    _transports: List[Transport] = [MailerTransport()]

    def add_transport(self, transport: Transport):
        self._transports.append(transport)

    def reset_transports(self):
        self._transports = []

    @classmethod
    def send(cls, message: NotificationMessage) -> SendNotificationResult:

        try:
            result = SendNotificationResult(success=False)
            badge = NotificationStorage.get_badge(message=message)
            for transport in cls._transports:
                result = transport.send(message=message, badge=badge)
            return result
        except Exception as ex:
            logger.error("_send_sync failed: {}".format(str(ex)))
            result = SendNotificationResult(success=False, error=str(ex))
            return result
