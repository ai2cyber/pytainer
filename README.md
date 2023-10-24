
# pytainer: Python Dependency Injection Container

`pytainer` is a dependency injection container for Python. The main goal of this library is to improve development experience while also improving the overall performance of the application and drastically reducing boilerplate code. Internally, advanced type checking techniques are utilized to ensure that even if a mistake happens during development time, wrong implementation, missing dependencies, etc., it will be caught and reported to the developer at runtime.

- [pytainer: Python Dependency Injection Container](#pytainer-python-dependency-injection-container)
  - [Philosophy \& Terms](#philosophy--terms)
    - [Client \& Services](#client--services)
    - [Interfaces](#interfaces)
    - [Injectors](#injectors)
    - [Injection Types](#injection-types)
      - [Constructor Injection](#constructor-injection)
      - [Property Injection](#property-injection)
      - [Method Injection](#method-injection)
    - [Dependency Injection Containers](#dependency-injection-containers)
  - [About `pytainer`](#about-pytainer)
    - [Registration Providers](#registration-providers)
    - [Services Lifecycle Management](#services-lifecycle-management)
      - [Singleton](#singleton)
      - [Transient](#transient)
    - [Container Safety](#container-safety)
  - [Usage](#usage)
    - [Examples](#examples)
  - [API Reference](#api-reference)
    - [Container](#container)
      - [Properties](#properties)
      - [Methods](#methods)
        - [Registration Methods](#registration-methods)
        - [Resolution Methods](#resolution-methods)
        - [Verification Methods](#verification-methods)

## Philosophy & Terms

For starters, dependency injection (DI) in general is an Object Oriented Programming (OOP) design pattern. It can be applied to procedural or functional programming using argument injection but it's not that common of a pattern. Now that's done, let's begin by defining the participating entities in DI.

By convention, we recognize four different entities in the dependency injection pattern: _interfaces_, _clients_, _services_ and _injectors_.

### Client & Services

Any class that defines useful functionality is a _service_ in dependency injection, and any class that needs a service is a _client_. The services that a client requires are called _dependencies_. Those terms are not concrete, meaning that a class can be both a service AND a client, meaning it can have dependencies and be a dependency itself.

### Interfaces

A basic need that dependency injection covers is _decoupling_. Decoupling means that clients should not know nor care how their dependencies do their work, just the contract on how to interact with them. Those contracts are called _interfaces_.

### Injectors

Any object that manages to construct and connect complex object graphs, where objects may be both clients and services, is called an _injector_.Because dependency injection separates how objects are constructed from how they are used, it often diminishes the importance of the new keyword found in most object-oriented languages. Because the framework handles creating services, the programmer tends to only directly construct value objects which represents entities in the program's domain.

### Injection Types

There are three types of dependency injection — _constructor injection_, _method injection_, and _property injection_. Mind you, this library only supports constructor injection, the other registration types are more of an honorable mention.

#### Constructor Injection

Constructor injection is a type of dependency injection where dependencies are provided to a class through its constructor. This design pattern promotes loose coupling and makes it easier to manage and test dependencies. In Python, you can implement constructor injection to inject dependencies into a class's constructor.

Let's create an example of an order service that depends on a mailing service to send an email when an order is received. We'll use constructor injection to inject the mailing service into the order service.

```python
class MailingService:
    def send_email(self, recipient, subject, message):
        # Simulate sending an email
        print(f"Email sent to {recipient} with subject '{subject}': {message}")


class OrderService:
    def __init__(self, mailing_service):
        self.mailing_service = mailing_service

    def receive_order(self, order_details):
        # Process the order
        # ...

        # Send an email confirmation using the mailing service
        recipient = order_details['email']
        subject = "Order Confirmation"
        message = f"Thank you for your order! Your order ID is {order_details['order_id']}."
        self.mailing_service.send_email(recipient, subject, message)


# Create instances of the MailingService and OrderService
mailing_service = MailingService()
order_service = OrderService(mailing_service)

# Simulate receiving an order
order_details = {
    'order_id': 12345,
    'email': 'customer@example.com',
    # Other order details...
}
order_service.receive_order(order_details)
```

In this example:

1. We have a `MailingService` class responsible for sending emails, with a `send_email` method.
2. The `OrderService` class is designed to receive orders and send email confirmations. It takes an instance of `MailingService` as a parameter in its constructor, making it dependent on the mailing service.
3. When an order is received using the `receive_order` method of `OrderService`, it processes the order and then uses the injected `MailingService` to send an email confirmation.

By injecting the `MailingService` through the constructor, we allow for flexibility and easy testing. You can easily replace the mailing service with a different implementation or a mock object during testing without modifying the `OrderService` class itself. This promotes a clean separation of concerns and makes your code more maintainable and testable.

#### Property Injection

Property injection is another form of dependency injection where dependencies are set through properties or setter methods of a class rather than through the constructor. In Python, you can implement property injection by defining setter methods for your dependencies. Let's modify the previous example to use property injection:

```python
class MailingService:
    def send_email(self, recipient, subject, message):
        # Simulate sending an email
        print(f"Email sent to {recipient} with subject '{subject}': {message}")


class OrderService:
    def set_mailing_service(self, mailing_service):
        self.mailing_service = mailing_service

    def receive_order(self, order_details):
        # Process the order
        # ...

        # Send an email confirmation using the mailing service
        recipient = order_details['email']
        subject = "Order Confirmation"
        message = f"Thank you for your order! Your order ID is {order_details['order_id']}."
        self.mailing_service.send_email(recipient, subject, message)


# Create instances of the MailingService and OrderService
mailing_service = MailingService()
order_service = OrderService()

# Inject the mailing service using property injection
order_service.set_mailing_service(mailing_service)

# Simulate receiving an order
order_details = {
    'order_id': 12345,
    'email': 'customer@example.com',
    # Other order details...
}
order_service.receive_order(order_details)
```

In this modified example:

1. We still have the `MailingService` class responsible for sending emails with a `send_email` method.

2. The `OrderService` class no longer takes the `MailingService` as a constructor parameter. Instead, it has a `set_mailing_service` method that allows you to set the mailing service as a property.

3. After creating instances of both classes, we inject the `MailingService` into the `OrderService` by calling `set_mailing_service(mailing_service)`.

4. The `receive_order` method of `OrderService` remains the same and continues to use the injected `MailingService` to send email confirmations.

Property injection can be useful when you want to allow flexibility in setting dependencies after an object's creation or if you need to change the dependency at runtime. However, it can make it less obvious which dependencies a class requires compared to constructor injection, which clearly specifies them in the constructor's parameter list.

#### Method Injection

Method injection involves passing dependencies to a method when it is called, rather than injecting them into a class's constructor or setting them as properties. Let's adapt the previous example to use method injection:

```python
class MailingService:
    def send_email(self, recipient, subject, message):
        # Simulate sending an email
        print(f"Email sent to {recipient} with subject '{subject}': {message}")


class OrderService:
    def receive_order(self, order_details, mailing_service):
        # Process the order
        # ...

        # Send an email confirmation using the provided mailing service
        recipient = order_details['email']
        subject = "Order Confirmation"
        message = f"Thank you for your order! Your order ID is {order_details['order_id']}."
        mailing_service.send_email(recipient, subject, message)


# Create an instance of the MailingService
mailing_service = MailingService()

# Create an instance of the OrderService
order_service = OrderService()

# Simulate receiving an order and inject the mailing service
order_details = {
    'order_id': 12345,
    'email': 'customer@example.com',
    # Other order details...
}
order_service.receive_order(order_details, mailing_service)
```

In this updated example:

1. The `MailingService` class remains the same, responsible for sending emails.
2. The `OrderService` class no longer requires the `MailingService` to be injected through the constructor or properties. Instead, the `receive_order` method accepts the `mailing_service` as an argument.
3. We create instances of both the `MailingService` and `OrderService`.
4. When we call the `receive_order` method of the `OrderService`, we pass the `mailing_service` instance as an argument. This allows us to inject the dependency directly when calling the method.

Method injection can be useful when you want to inject dependencies only when they are needed for specific method calls, providing more flexibility in controlling the dependencies at runtime. However, it may require more effort to ensure that the correct dependencies are provided to the methods when called.

### Dependency Injection Containers

A Dependency Injection Container (also known as a DI Container or IoC Container) is a software framework or container that manages the creation and resolution of dependencies in an application. It centralizes the configuration and handling of object creation and dependency injection, making it easier to manage dependencies, promote code reusability, and maintain the flexibility and testability of your code.

Using a dependency injection container simplifies the management of dependencies, allows for centralized configuration, and promotes the separation of concerns in your code. It also makes it easier to swap out implementations or configurations without modifying the client code, making your application more flexible and maintainable. Dependency injection containers are commonly used in larger-scale applications to manage complex dependency graphs.

## About `pytainer`

The container, much like the concept it represents, it is designed with inversion of control (IoC) in mind. This means that the container itself is completely agnostic of how it registers, validates and resolves dependencies. By removing this logic from the container, the process of adding new registration types or debugging existing ones is simplified and focused on the modules that handle it, instead of a monolithic container that does everything. This functionality is migrated to an entity internally called _Provider_, and are analyzed in depth in the [Registration Providers](#registration-providers) section.

Moreover, the container is responsible of managing the lifecycle of the services registered to it. _Service lifecycle management_ refers to the idea of managing both the quantity of instances a configured service will possess and the timeframe during which those instances will exist. This functionality is of course migrated to the providers. To read more about lifecycle management check the [Services Lifecycle Management](#services-lifecycle-management) section.

Finally, it is of the utmost importance that the end user (developer in this case) can trust the container he uses to be safe. Safety in this context means that the registrations made are of the correct type and can be all its dependencies are also registered to the container. If either of those conditions are not met, the application might exhibit unexpected behavior, runtime errors or failure to even begin its execution. As Python's infamous for its indifference for type safety, custom typechecking techniques were devised to satisfy the aforementioned conditions, and you can learn more about them in the [Container Safety](#container-safety) section.

### Registration Providers

Providers as mentioned above handle the execution logic of the container. When you call the container to register a service, it internally creates the appropriate provider and registers _it_ instead of the service itself. In a similar manner, when you attempt to resolve a service for the container, it will try to find the provider that corresponds to this service and use _it_ for the resolution. The providers, then, essentially provide (no pun intended) any and all functionality the container has to offer.

`pytainer` offers three different providers: _Implementation_, _Instance_ and _Factory_. As their names suggest, each one of those providers handle the validation, registration and resolution of an _Implementation_ of the service, an _instance_ of the service and the _dependency factory_ of the service respectively. (We define as a _dependency factory_ any function that takes the container as its only argument and returns an instance of the service).

### Services Lifecycle Management

As mentioned before, _service lifecycle management_ is the containers responsibility to manage how many instances of a service are created and how long they exist. In simpler terms, it enables you to specify how instances are stored when they are returned. Many dependency injection libraries include advanced features for handling lifecycle management, and `pytainer` is no different, as it comes with built-in support for the most commonly used lifecycles: _transient_ and _singleton_.

#### Singleton

_Singleton_ is a design pattern that ensures a single instance of a particular class is created and shared across the entire application. When you configure a component as a singleton in a dependency injection container, it means that the container will create an instance of that component once and then reuse that same instance whenever it is requested throughout the lifetime of the application.

However, it's essential to use singletons with care, as they can introduce tight coupling between components and potentially lead to issues like hidden dependencies and difficulty in unit testing. Not every component should be a singleton; you should reserve this pattern for cases where it makes sense to share a single instance across the application's lifetime.

#### Transient

Unlike singletons, which provide a single shared instance throughout the application's lifetime, _transient_ objects are created anew each time they are requested from the dependency injection container.

While transient components have their advantages, it's essential to be mindful of their usage. Creating new instances for every request can be resource-intensive for objects with heavy initialization or high overhead. It can also lead to increased memory usage if not managed carefully.

### Container Safety

As mentioned above, for the container to function successfully and be considered "safe", it must meet the conditions of  _typesafety_ and _resolvability_. Typesafety in this context means that the registered implementation, instance of factory actually implements the registered service which is typically an abstract class, while resolvability means that the dependencies each registration needs to resolve are also registered in the container.

It is known that Python does not handle typing well and while there are some libraries and tools that improve type checking in Python, this information is lost or ignored during the runtime of an application. For this reason, with additional help from those aforementioned libraries, advanced type checking techniques were devised as a solution to this problem. Those methods were exhaustively tested to find and correct errors in them, and they now offer complete runtime validation that a class implements another one and therefore can be assigned to it, supporting generics, inheritance and polymorphism.

While the methods devised are functional, the computation for each _parent - child_ class pairs is expensive and actually slowed down the performance of the application significantly when called every time a registration was made. So an architectural change was made for the verification process to only occur once and disabling further registrations once it had completed. This change means that the lifecycle of the container is split in three phases: the _registration phase_, the _verification phase_ and the _resolution phase_, all of which are implemented in the providers as said before.

When in the **registration phase**, the developer can freely register any service and provider type he wishes freely, relying on the typesafety provided by static analysis tools like [`pyright`](https://microsoft.github.io/pyright/#/) or [`mypy`](https://mypy-lang.org/), with the container offering little to no validation during this time. The developer must then call the `validate` method (see the [API Reference](#verification-methods)) which transitions the container in its **validation phase**. The container then, relying on the implementation of each provider registered, checks that every registration can be assigned to its corresponding service and that the resolution method can be called and return an instance. If this process completes successfully, the container is now frozen, meaning no more registrations can be made, and the container transitions to its **resolution phase**. Otherwise it will raise a `VerificationException` describing which service is incorrectly registered and why.

## Usage

```python
from pytainer import Container, Lifecyle

from application.interfaces import IServiceA, IServiceB, IServiceC
from application.services import ServiceA, ServiceB, ServiceC

container = Container()
container.register(service=IServiceA, implementation=ServiceA)  # You can register the implementation
container.register(service=IServiceB, instance=ServiceB())  # You can register an instance
container.register(service=IServiceC, factory=lambda c: ServiceC())  # You can register a factory
container.verify()

service_a: IServiceA = container.resolve(IServiceA)
service_b: IServiceB = container.resolve(IServiceB)
service_c: IServiceC = container.resolve(IServiceC)
```

### Examples

Check the `<root>/examples` folder for examples.

## API Reference

### Container

The container class that handles the registration, validation and resolution of dependencies.

```python
class Container:
    verified: bool
```

#### Properties

- `verified: bool`: A boolean flag that specifies wether the container is validated or not.

#### Methods

##### Registration Methods

```python
def register_factory(self, service: Type[_T], factory: DependencyFactory[_T]) -> None: ...
```

- **Description**: Registers a factory provider to the container.
- **Arguments**
  - `service: Type[_T]`: The service to register.
  - `factory: DependencyFactory[_T]`: The factory that resolves the service.
- **Raises**
  - `RegistrationException`: An exception is raised if called from a verified container.

```python
def register_instance(self, service: Type[_T], instance: _T) -> None: ...
```

- **Description**: Registers an instance provide to the container.
- **Arguments**
  - `service: Type[_T]`: The service to register.
  - `instance: _T`: An instance of the service to be resolved.
- **Raises**
  - `RegistrationException`: An exception is raised if called from a verified container.

```python
def register_implementation(self, service: Type[_T], implementation: Type[_T], lifecycle: Lifecycle = Lifecycle.Singleton) -> None: ...
```

- **Description**: Registers an implementation provider to the container.
- **Arguments**
  - `service: Type[_T]`: The service to register.
  - `implementation: Type[_T]`: An implementation of the service to be resolved.
  - `lifecycle: Lifecyle`: The lifecycle configuration of the registration. Defaults to `Lifecycle.Singleton`.
- **Raises**
  - `RegistrationException`: An exception is raised if called from a verified container.

##### Resolution Methods

```python
def resolve(self, service: Type[_T]) -> _T: ...
```

- **Description**: Resolves a service from the container.
- **Arguments**
  - `service: Type[_T]`: The service to be resolved.
- **Returns** `_T`: The resolved instance of the service.
- **Raises**
  - `ResolutionException`: An exception is raised when called from an unverified container or when the requested service is not registered.

```python
def resolve_all(self, service: Type[_T]) -> List[_T]: ...
```

- **Description**: Resolves a all registered providers for a service from the container.
- **Arguments**
  - `service: Type[_T]`: The service to be resolved.
- **Returns** `List[_T]`: The resolved instances of the service.
- **Raises**
  - `ResolutionException`: An exception is raised when called from an unverified container or when the requested service is not registered.

##### Verification Methods

```python
def is_registered(self, service: type) -> bool: ...
```

- **Description**: Determines whether the specified service is registered or not.
- **Arguments**
  - `service: type`: The service to check if registered in the container.
- **Returns** `bool`: `True` if the service is registered and `False` otherwise.

```python
def verify(self) -> None: ...
```

- **Description**: Verifies the container.
- **Raises**
  - `VerificationException`: An exception is raised when a provider fails to pass verification.
