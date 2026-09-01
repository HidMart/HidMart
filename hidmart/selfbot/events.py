class NewMessage:
    def __init__(self, message):
        self.message = message

    @property
    def text(self):
        return self.message.text

    @property
    def chat_id(self):
        return self.message.chat.id if self.message.chat else None

    @property
    def sender_id(self):
        return (
            self.message.from_user.id
            if self.message.from_user
            else None
        )