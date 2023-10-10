import socket
from time import sleep

import network

_template = """<!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pico W Server</title>
  <style>
    :root {
      font: sans-serif;
      font-size: 10px;
    }

    body {
      margin: 0 auto;
      max-width: 600px;
    }

    h1 {
      font-size: 3rem;
      margin: 0 0 1rem;
      padding-top: 1rem;
      text-align: center;
    }

    main {
      font-size: 2rem;
    }

    form {
      display: flex;
      align-content: center;
      margin-top: 1rem;
    }

    input {
      font-size: inherit;
      margin: auto;
    }
  </style>
</head>

<body>
  <main>
    <h1>Pico W Example Template</h1>
    <p>This is a html template example for a simple embeded server on a raspberry pi pico w.</p>
    <form action="./action-1">
      <input type="submit" value="Action 1" />
    </form>
    <form action="./action-2">
      <input type="submit" value="Action 2" />
    </form>
    <form action="./action-3">
      <input type="submit" value="Action 3" />
    </form>
  </main>
</body>

</html>"""


class Server:
    def __init__(self, port=80) -> None:
        self.ssid = None
        self.wlan = None
        self.ip = None
        self.port = port
        self.html = _template

    def connect_wlan(self, ssid: str, password: str) -> str:
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)  # IP

        while not self.wlan.isconnected():
            print("Waiting for connection...")
            sleep(1)

        self.ip = self.wlan.ifconfig()[0]
        self.ssid = ssid

        return self.ip

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

    server = Server()
    server.connect_wlan(ssid, passwd)

    server.open_socket()
    try:
        server.serve()
    finally:
        server.close_socket()
        print("Closing connection...")


if __name__ == "__main__":
    main()
