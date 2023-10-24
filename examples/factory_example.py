from pytainer import Container

from .application.interfaces import IMailingClient, IOrderRepository, IOrderService
from .application.services import MailingClient, OrderRepository, OrderService

# Construct your instances
order_repository = OrderRepository()
mailing_client = MailingClient()
order_service = OrderService(order_repository, mailing_client)

container = Container()
container.register_implementation(IOrderRepository, OrderRepository)
container.register_implementation(IMailingClient, MailingClient)
container.register_factory(
    IOrderService,
    lambda container: OrderService(
        container.resolve(IOrderRepository),
        container.resolve(IMailingClient),
    ),
)

# Verify the container
container.verify()

# Resolve your service
order_service: IOrderService = container.resolve(IOrderService)
order_service.place_order("customer", {"custom_order": "custom_object"})
