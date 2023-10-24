from pytainer import Container

from .application.interfaces import IMailingClient, IOrderRepository, IOrderService
from .application.services import MailingClient, OrderRepository, OrderService

# Construct your instances
order_repository = OrderRepository()
mailing_client = MailingClient()
order_service = OrderService(order_repository, mailing_client)

container = Container()
container.register_instance(IOrderService, order_service)
container.register_instance(IOrderRepository, order_repository)
container.register_instance(IMailingClient, mailing_client)

# Verify the container
container.verify()

# Resolve your service
order_service: IOrderService = container.resolve(IOrderService)
order_service.place_order("customer", {"custom_order": "custom_object"})
