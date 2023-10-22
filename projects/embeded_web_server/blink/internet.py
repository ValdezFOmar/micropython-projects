import socket

import network


def connect_wlan(ssid: str, password: str) -> network.WLAN:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    return wlan


class Server:
    def __init__(self, ip: str, port=80) -> None:
        self.ip = ip
        self.port = port
        self.html = ""

    def open_socket(self):
        address = (self.ip, self.port)
        self.connection = socket.socket()

        # Needed for reusing a bound address (OSError: [Errno 98] EADDRINUSE)
        # See: https://github.com/micropython/micropython/issues/3739#issuecomment-386191815
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.connection.bind(address)
        self.connection.listen(1)
        return self.connection

    def close_socket(self):
        self.connection.close()

    def load_html(self, path="index.html"):
        with open(path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def serve(self, callback=None, *args, **kwargs):
        """
        Takes a callback that receives a request as its
        first argument and passes all the arguments and
        keywords arguments to it.

        callback(request, *args, **kwargs)

        """
        print(f"Serving on {self.ip}")

        if callback is None:
            callback = lambda req: print("A request was made:", req)

        while True:
            client = self.connection.accept()[0]
            try:
                request = client.recv(1024)
                request = str(request)

                try:
                    request = request.split()[1]
                except IndexError:
                    pass

                callback(request, *args, **kwargs)
                client.send(self.html)
            finally:
                client.close()


def main():
    from env import getenv

    ssid = getenv("SSID")
    passwd = getenv("PASSWORD")

    wlan = connect_wlan(ssid, passwd)
    while True:
        if wlan.isconnected():
            break

    server = Server(wlan.ifconfig()[0])

    server.open_socket()
    try:
        server.serve()
    finally:
        server.close_socket()
        print("Closing connection...")


if __name__ == "__main__":
    main()
