import websocket
import json

class BinanceClient:
    def __init__(self, logger, is_demo):
        self.spot_base_url = "wss://stream.binance.com:9443"
        self.um_base_url = "wss://fstream.binance.com"
        self.logger = logger
        self.is_demo = is_demo

    def handle_message(self, message):
        data = json.loads(message)
        # ztang-TODO: parse and compress data 

    def demo_message(self, message):
        data = json.loads(message)
        self.logger.info(data)

    def on_error(self, error):
        self.logger.error(error)

    def on_close(self):
        self.logger.info("Connection closed.")

    def on_open(self, streams):
        self.logger.info(f"Connection Opened. Streams: {streams}")

    def on_ping(self):
        pass

    def on_pong(self):
        pass
   
    def get_ws_url(self, streams, margin_type=None):
        """
		Raw streams: /ws/<streamName>
		Combined streams: /stream?streams=<streamName1>/<streamName2>/<streamName3>
		"""
        if margin_type is None: base_url = self.spot_base_url 
        else: base_url = self.um_base_url

        if len(streams) == 1:
            ws_url = base_url + '/ws/' + streams[0]
        else:
            ws_url = base_url + f"/stream?streams={'/'.join(streams)}"		
        return ws_url

    def run(self, streams, margin_type):
        ws_url = self.get_ws_url(streams, margin_type)
        if not self.is_demo:
            ws = websocket.WebSocketApp(ws_url,
                                            on_open=lambda ws: self.on_open(streams),
                                            on_message=lambda ws, msg: self.handle_message(msg),
                                            on_error=lambda ws, msg: self.on_error(msg),
                                            on_close=lambda ws: self.on_close()
                                            )
        else:
            ws = websocket.WebSocketApp(ws_url,
                                            on_open=lambda ws: self.on_open(streams),
                                            on_message=lambda ws, msg: self.demo_message(msg),
                                            on_error=lambda ws, msg: self.on_error(msg),
                                            on_close=lambda ws: self.on_close()
                                            )
        
        ws.run_forever()
