import os
from typing import Optional
import asyncio
from datetime import datetime

from domain.dto.command import Command, CommandTypes
from domain.dto.chat_message import ChatMessage
from logic.command_handler import CommandHandler
from logic.repository import Repository
from const import command_handlers_mapping, math_operations_mapping
from settings import STATIC_URL

__all__ = (
    "ClientSession"
)


class ClientSession:
    def __init__(self, client_socket, addr, handler: CommandHandler):
        self.client_socket = client_socket
        self.addr = addr
        self.handler = handler
        self.name: Optional[str] = None
        self.repository: Repository = Repository()

    async def __send(self, message: str) -> None:
        """Отправляет сообщение клиенту"""
        await asyncio.get_event_loop().sock_sendall(
            self.client_socket,
            message.encode("utf-8")
        )

    async def __receive(self) -> str:
        """Принимает сообщение от клиента"""
        data = await asyncio.get_event_loop().sock_recv(
            self.client_socket,
            1024
        )
        return data.decode("utf-8", errors="replace").strip()

    # noinspection PyMethodMayBeStatic
    async def _is_http_request(self, data: str) -> bool:
        """Проверяет, является ли запрос HTTP (от браузера)."""
        return data.startswith(("GET /", "POST /", "HEAD /"))

    async def _send_http_response(self, html_content: str) -> None:
        """Отправляет HTTP-ответ с HTML"""
        encoded_content = html_content.encode('utf-8')
        response = (
                   "HTTP/1.1 200 OK\r\n"
                   "Content-Type: text/html; charset=utf-8\r\n"
                   f"Content-Length: {len(encoded_content)}\r\n"
                   "\r\n"
        ) + encoded_content.decode("utf-8")
        await self.__send(response)

    # noinspection PyMethodMayBeStatic
    async def _load_html_template(self) -> str:
        """Загружает HTML из файла index.html"""
        try:
            file_path = os.path.join(STATIC_URL + "index.html")
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                print(content)
                return content
        except FileNotFoundError:
            return "<h1>Ошибка: файл index.html не найден!</h1>"

    async def _greet_client(self) -> None:
        """Приветствие и запрос имени"""
        await self.__send("Привет, как мне тебя называть?\n")
        self.name = await self.__receive()
        print(f"Клиент {self.addr} представился как {self.name}")
        await self.__send(
            f"Приятно познакомиться, {self.name}!\n"
            "Ты можешь следующее:\n"
            "1. Поздороваться с сервером\n"
            "2. Решить математическую задачу\n"
            "3. Войти в чат\n"
            "4. Завершить сессию\n"
        )

    async def _handle_greeting(self) -> str:
        """Обработка команды приветствия"""
        command = Command(
            command_type=CommandTypes.GREETINGS,
            kwargs={"name": self.name}
        )
        return await command_handlers_mapping[CommandTypes.GREETINGS](command)

    async def _handle_math_operation(self) -> str:
        """Обработка математической команды"""
        await self.__send(
            "Отлично! Какую математическую задачу хочешь решить:\n"
            "1. Нахождение гипотенузы треугольника по теореме Пифагора\n"
            "2. Решение квадратного уравнения\n"
            "3. Поиск площади трапеции\n"
            "4. Поиск площади параллелограмма\n"
            "Твой вариант: "
        )
        math_operation = await self.__receive()

        if math_operation not in math_operations_mapping:
            return "Некорректный номер задачи ;(\n"

        await self.__send(
            "Введите требуемые параметры через пробел.\n"
            "1. a, b\n"
            "2. a, b, c\n"
            "3. a, b, h\n"
            "4. a, h\n"
            "Твои параметры: "
        )
        params = await self.__receive()

        try:
            params = tuple(map(float, params.split()))
            command = Command(
                command_type=CommandTypes.MATHEMATICS,
                kwargs={
                    "params": params,
                    "math_operation_function": math_operations_mapping[math_operation],
                }
            )
            return await command_handlers_mapping[CommandTypes.MATHEMATICS](command)
        except ValueError:
            return "Некорректный тип у введенных параметров\n"

    async def _print_chat_header(self):
        """Красивое оформление заголовка чата"""
        await self.__send("\n" + "═" * 50)
        await self.__send("📢 ЧАТ 📢")
        await self.__send("═" * 50 + "\n")

    async def _print_message(self, message: ChatMessage):
        """Форматированный вывод сообщения"""
        time_str = datetime.fromtimestamp(message.timestamp).strftime("%H:%M:%S")
        msg = (
            f"[{time_str}] {message.author}: "
            f"\033[1;34m{message.text}\033[0m\n"
        )
        await self.__send(msg)

    async def _handle_chat(self):
        """Основной цикл чата"""
        await self._print_chat_header()

        command = Command(
            command_type=CommandTypes.CHAT,
            kwargs={
                "action": "join",
                "username": self.name,
                "session": self,
            }
        )
        await self.handler.handle_chat(command)

        # Показываем последние 10 сообщений
        for msg in await self.repository.get_last_messages(10):
            await self._print_message(msg)

        # Основной цикл чата
        while True:
            message = await self.__receive()

            if message.lower() == "exit":
                command = Command(
                    command_type=CommandTypes.CHAT,
                    kwargs={
                        "action": "exit",
                        "username": self.name
                    }
                )
                response = await self.handler.handle_chat(command)
                return response

            # Отправляем сообщение
            command = Command(
                command_type=CommandTypes.CHAT,
                kwargs={
                    "action": "send",
                    "username": self.name,
                    "message": message
                }
            )
            await self.handler.handle_chat(command)

    async def process(self) -> None:
        """Основной цикл обработки команд клиента"""
        try:
            initial_data = await self.__receive()

            if await self._is_http_request(initial_data):
                html = await self._load_html_template()
                await self._send_http_response(html)
                return

            await self._greet_client()

            while True:
                await self.__send("Твой выбор действия: ")
                choice = await self.__receive()

                if choice == "1":
                    response = await self._handle_greeting()
                elif choice == "2":
                    response = await self._handle_math_operation()
                elif choice == "3":
                    response = await self._handle_chat()
                elif choice == "4":
                    break
                else:
                    response = "Я не умею обрабатывать такое сообщение ;("

                await self.__send(response + "\n")

        except (ConnectionResetError, BrokenPipeError):
            print(f"Клиент {self.addr} отключился (ошибка соединения)")
        finally:
            self.client_socket.close()
            print(f"Соединение с {self.addr} закрыто")

    async def send_chat_message(self, message: ChatMessage) -> None:
        """Отсылает сообщение в чат всем пользователям"""
        # Сохраняем позицию курсора
        await self.__send("\033[s")

        if message.author == self.name:
            await self.__send("\033[1A")  # Вверх на одну строку

        # Вставляем новую строку
        await self.__send("\033[L")

        await self._print_message(message)

        # Восстанавливаем позицию курсора
        await self.__send("\033[u")
        await self.__send("\033[2K")


