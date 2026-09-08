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


class RPCError(HidMartError):
    def __init__(self, code=None, message="RPC request failed"):
        self.code = code
        self.message = message
        super().__init__(message)