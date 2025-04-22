from typing import Union, List, Dict, Any

from domain.dto.chat_message import ChatMessage
from logic.utils.singleton_meta import SingletonMeta

__all__ = (
    "Repository",
)


class Repository(metaclass=SingletonMeta):
    def __init__(self):
        self.storage = {
            "chat_messages": [],
            "active_users": {},
        }

    async def add_message(self, message: ChatMessage):
        """Добавляет сообщение в историю чата"""
        self.storage["chat_messages"].append(message)

    async def get_last_messages(self, count=10) -> List[ChatMessage]:
        """Возвращает последние N сообщений"""
        return self.storage["chat_messages"][-count:]

    async def add_user(self, username: str, session):
        """Добавляет пользователя в чат"""
        self.storage["active_users"][username] = session

    async def remove_user(self, username: str):
        """Удаляет пользователя из чата"""
        del self.storage["active_users"][username]

    async def get_active_users(self) -> Dict[str, Any]:
        """Возвращает список активных пользователей"""
        return self.storage["active_users"]
