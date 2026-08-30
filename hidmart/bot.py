import time
from typing import Callable, Optional

from .client import Client
from .handlers import HandlerManager


class Bot:
    def __init__(
        self,
        token: str,
        base_url: str,
        polling_interval: float = 1.0
    ):
        self.token = token
        self.polling_interval = polling_interval

        self.client = Client(
            token=token,
            base_url=base_url
        )

        self.handlers = HandlerManager()
        self.running = False

        self._offset: Optional[int] = None

    def on_message(self):
        def decorator(func: Callable):
            self.handlers.add_message_handler(func)
            return func

        return decorator

    def on_callback(self):
        def decorator(func: Callable):
            self.handlers.add_callback_handler(func)
            return func

        return decorator

    def send_message(
        self,
        chat_id,
        text,
        **kwargs
    ):
        data = {
            "chat_id": chat_id,
            "text": text,
            **kwargs
        }

        return self.client.request(
            "sendMessage",
            data
        )

    def get_updates(self):
        data = {}

        if self._offset is not None:
            data["offset"] = self._offset

        return self.client.request(
            "getUpdates",
            data
        )

    def run(self):
        self.running = True

        print("[HidMart] Bot is running...")

        while self.running:
            try:
                result = self.get_updates()

                updates = result.get("result", [])

                for update in updates:
                    update_id = update.get("update_id")

                    if update_id is not None:
                        self._offset = update_id + 1

                    self._process_update(update)

            except KeyboardInterrupt:
                self.off()
                break

            except Exception as error:
                print(f"[HidMart] Error: {error}")
                time.sleep(self.polling_interval)

    def _process_update(self, update):
        if "message" in update:
            self.handlers.handle_message(
                update["message"]
            )

        elif "callback_query" in update:
            self.handlers.handle_callback(
                update["callback_query"]
            )

    def off(self):
        self.running = False
        print("[HidMart] Bot stopped.")