from typing import Callable, List


class HandlerManager:
    def __init__(self):
        self.message_handlers: List[Callable] = []
        self.callback_handlers: List[Callable] = []

    def add_message_handler(self, handler: Callable):
        self.message_handlers.append(handler)

    def add_callback_handler(self, handler: Callable):
        self.callback_handlers.append(handler)

    def handle_message(self, data):
        for handler in self.message_handlers:
            try:
                handler(data)
            except Exception as error:
                print(f"[HidMart] Handler error: {error}")

    def handle_callback(self, data):
        for handler in self.callback_handlers:
            try:
                handler(data)
            except Exception as error:
                print(f"[HidMart] Callback handler error: {error}")