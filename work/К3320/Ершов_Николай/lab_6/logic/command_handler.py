import time

from logic.repository import Repository
from domain.dto.command import Command
from domain.dto.chat_message import ChatMessage

__all__ = (
    "CommandHandler",
)


class CommandHandler:
    """
    Обработчик команд для работы с клиентом
    """

    @classmethod
    async def handle_say_hello(cls, command: Command):
        return f"Привет, {command.kwargs.get('name')}!\n"

    @classmethod
    async def handle_mathematics(cls, command: Command):
        try:
            result = command.kwargs.get('math_operation_function')(*command.kwargs.get('params'))
        except TypeError:
            result = "Неправильное количество параметров!"
        return result

    @classmethod
    async def handle_chat(cls, command: Command) -> str:
        """Обработчик чат-команд"""
        repository = Repository()

        async def __broadcast(message: ChatMessage):
            """Рассылает сообщение всем активным пользователям"""
            users = await repository.get_active_users()
            for username, session in users.items():
                try:
                    await session.send_chat_message(message)
                except (ConnectionError, OSError):
                    await repository.remove_user(username)

        if command.kwargs.get("action") == "join":
            await repository.add_user(command.kwargs["username"], command.kwargs.get("session"))
            return "Вы вошли в чат!\n"

        elif command.kwargs.get("action") == "send":
            message = ChatMessage(
                author=command.kwargs["username"],
                text=command.kwargs["message"],
                timestamp=time.time()
            )

            await repository.add_message(message)
            await __broadcast(message)
            return "Сообщение отправлено!\n"

        elif command.kwargs.get("action") == "exit":
            await repository.remove_user(command.kwargs.get("username"))
            return "Вы вышли из чата!\n"

        return "Неизвестная команда чата\n"
