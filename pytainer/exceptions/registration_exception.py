class RegistrationException(Exception):
    def __init__(self, service: type, reason: str) -> None:
        super().__init__(f'Registration failed for "{service}". {reason}')
        self.service = service
        self.reason = reason
