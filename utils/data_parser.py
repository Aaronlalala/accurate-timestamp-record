import os
import json
import struct

class DataParser:
    def __init__(self, logger, path):
        self.logger = logger
        self.path = path

    def json_to_binary(self, message):
        data = json.loads(message)
        binary_format = 'dddd'
        binary_format += 'ff' * (len(data['b']) + len(data['a']))
        updates = [data['E'], data['U'], data['u'], data['pu']]

        for bid in data['b']:
            updates.extend([float(bid[0]), float(bid[1])])
        # ztang TODO: need an indicator to tell it's the end of bid.
        for ask in data['a']:
            updates.extend([float(ask[0]), float(ask[1])])
        binary_data = struct.pack(binary_format, *updates)
        return binary_data
    
    def read_binary_file(self, path=None):
        # ztang TODO: how do I know for each message, the number of bids and asks?
        pass

    def write(self, binary_data):
        # ztang TODO: there should be an indicator to separate each message
        with open(self.path, "ab") as file:
            file.write(binary_data)
        self.logger.info(f"Write binary data to file {self.path}.")
        