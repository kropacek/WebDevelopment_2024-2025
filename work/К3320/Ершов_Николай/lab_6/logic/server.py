import asyncio
import socket

from logic.command_handler import CommandHandler
from logic.repository import Repository
from settings import HOST, PORT
from logic.client_session import ClientSession

__all__ = (
    "Server",
)


class Server:

    def __init__(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind((HOST, PORT))
        self.socket_server.listen()
        self.socket_server.setblocking(False)

        self.handler: CommandHandler = CommandHandler()

    async def handle_client(self, client_socket, addr):
        """Обработчик клиента"""
        print(f"Подключился клиент: {addr}")
        session = ClientSession(client_socket, addr, self.handler)
        await session.process()

    async def start_server(self):
        """Запуск сервера"""
        print(f"Сервер запущен на {HOST}:{PORT}")
        loop = asyncio.get_event_loop()

        while True:
            client_socket, addr = await loop.sock_accept(self.socket_server)
            asyncio.create_task(self.handle_client(client_socket, addr))
