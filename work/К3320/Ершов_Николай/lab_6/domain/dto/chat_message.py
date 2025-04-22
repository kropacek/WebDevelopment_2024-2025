
__all__ = (
    "ChatMessage",
)


class ChatMessage:
    """Сообщение из чата"""
    def __init__(self, author: str, text: str, timestamp: float):
        self.author = author
        self.text = text
        self.timestamp = timestamp
