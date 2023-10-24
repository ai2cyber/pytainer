from .interfaces import IMailingClient, IOrderRepository, IOrderService


class OrderRepository(IOrderRepository):
    def save_order_to_db(self, order: object) -> None:
        print(f'Saved order: "{order}" to database.')


class MailingClient(IMailingClient):
    def send_mail_to_recipient(self, sender: str, recipient: str, content: str) -> None:
        print(f"{sender}->{recipient}:\n{content}")


class OrderService(IOrderService):
    def __init__(self, order_repository: IOrderRepository, mailing_client: IMailingClient) -> None:
        self.order_repository = order_repository
        self.mailing_client = mailing_client

    def place_order(self, user: str, order: object) -> None:
        # Send email to user
        self.mailing_client.send_mail_to_recipient(
            "shop",
            user,
            f'You succedsfully placed the order for "{order}".',
        )

        # Save information to database
        self.order_repository.save_order_to_db(order)

        # Print success message
        print(f'User: "{user}" placed order: "{order}".')
