from pytainer import Container

from .application.interfaces import IMailingClient, IOrderRepository, IOrderService
from .application.services import MailingClient, OrderRepository, OrderService

container = Container()
# Registration order does not affect functionality
container.register_implementation(IOrderService, OrderService)
container.register_implementation(IOrderRepository, implementation=OrderRepository)
container.register_implementation(IMailingClient, MailingClient)

# Verify the container
container.verify()

# Resolve your service
order_service: IOrderService = container.resolve(IOrderService)
order_service.place_order("customer", {"custom_order": "custom_object"})
