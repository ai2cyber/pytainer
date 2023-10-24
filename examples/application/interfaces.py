from abc import ABC


class IOrderRepository(ABC):
    def save_order_to_db(self, order: object) -> None:
        raise NotImplementedError()


class IMailingClient(ABC):
    def send_mail_to_recipient(self, sender: str, recipient: str, content: str) -> None:
        raise NotImplementedError()


class IOrderService(ABC):
    def place_order(self, user: str, order: object) -> None:
        raise NotImplementedError()
