class HidMartError(Exception):
    pass


class AuthenticationError(HidMartError):
    pass


class ConnectionError(HidMartError):
    pass


class ProtocolError(HidMartError):
    pass


class SessionError(HidMartError):
    pass