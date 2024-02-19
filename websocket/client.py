import websocket
import json

class Client:
    def __init__(self, url):
        self.url = url
        self.ws = None

    def on_message(self, message):
        data = json.loads(message)
        print("Received Message:")
        print(data)

    def on_error(self, error):
        print("Error:", error)

    def on_close(self):
        print("### Connection Closed ###")

    def on_open(self):
        print("Connection Opened")

    def run(self):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=lambda ws, msg: self.on_message(msg),
                                         on_error=lambda ws, msg: self.on_error(msg),
                                         on_close=lambda ws: self.on_close())
        self.ws.on_open = lambda ws: self.on_open()
        self.ws.run_forever()
