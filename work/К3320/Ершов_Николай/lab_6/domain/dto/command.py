from enum import Enum
from typing import Union, Optional

__all__ = (
    "Command",
    "CommandType",
    "CommandTypes",
)


class CommandType:
    """
    Тип операции и группа команды
    """
    type_num: str


class CommandTypes(CommandType, Enum):
    """
    Типы операций по группам команд
    """
    related_value: str

    GREETINGS = "1"
    """Команда приветствия пользователя"""
    MATHEMATICS = "2"
    """Команда обработки математической операции"""
    CHAT = "3"
    """Команда чата"""


class Command:
    """
    Команда для управления логикой сервера
    """
    def __init__(self, command_type: CommandTypes, kwargs=None):
        if kwargs is None:
            kwargs = {}

        self.command_type = command_type
        self.kwargs = kwargs

