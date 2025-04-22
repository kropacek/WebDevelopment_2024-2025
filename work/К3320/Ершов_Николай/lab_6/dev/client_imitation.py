from logic.client import Client


def imitate():
    client = Client()
    client.send_hello()


if __name__ == '__main__':
    imitate()
