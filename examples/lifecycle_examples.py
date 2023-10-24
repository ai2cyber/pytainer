from pytainer import Container
from pytainer.lifecycle import Lifecycle

from .application.interfaces import IMailingClient, IOrderRepository, IOrderService
from .application.services import MailingClient, OrderRepository, OrderService

# Singleton Registration (Default)
container = Container()
# Registration order does not affect functionality
container.register_implementation(IOrderService, OrderService)
container.register_implementation(IOrderRepository, implementation=OrderRepository)
container.register_implementation(IMailingClient, MailingClient, Lifecycle.Singleton)

# Verify the container
container.verify()

# Resolve your service
order_service_one: IOrderService = container.resolve(IOrderService)
order_service_two: IOrderService = container.resolve(IOrderService)
print(order_service_one, order_service_two)
assert order_service_one == order_service_two

# Transient Registration (Default)
container = Container()
# Registration order does not affect functionality
container.register_implementation(IOrderService, OrderService)
container.register_implementation(IOrderRepository, implementation=OrderRepository)
container.register_implementation(IMailingClient, MailingClient, Lifecycle.Transient)

# Verify the container
container.verify()

# Resolve your service
order_service_one: IOrderService = container.resolve(IOrderService)
order_service_two: IOrderService = container.resolve(IOrderService)
print(order_service_one, order_service_two)
assert order_service_one != order_service_two
