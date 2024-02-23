from websocket_client.binance_client import BinanceClient
from utils.logger import Logger

"""
Docs: https://binance-docs.github.io/apidocs/futures/en/#websocket-market-streams
"""
streams = ["btcusdt@depth@100ms"]
logger = Logger("ws_log", "binance_depth")
client = BinanceClient(logger, False)
client.run(streams, "um")
