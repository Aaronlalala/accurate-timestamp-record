import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_folder, log_prefix):
        self.log_folder = f"logs/{log_folder}"
        self.log_file_prefix = log_prefix
        os.makedirs(self.log_folder, exist_ok=True)
        self.configure_logger()

    def get_log_file_path(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_folder, f"{self.log_file_prefix}_{date_str}.log")

    def configure_logger(self):
        log_file_path = self.get_log_file_path()
        # Check if a handler exists and remove any existing handlers
        # This is necessary to avoid duplicate logs
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # Configure the new handler
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_file_path,
                            filemode='a')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def _log_wrapper(self, level, message):
        # Before logging, check if the log file needs to be updated (i.e., new day)
        current_log_file_path = self.get_log_file_path()
        if not any(handler.baseFilename == current_log_file_path for handler in self.logger.handlers):
            self.configure_logger()
        # Log the message
        getattr(self.logger, level.lower(), self.logger.error)(message)
        print(message)
    
    # Currenly we only need info and error.
    def info(self, message):
        self._log_wrapper("info", message)
    
    def error(self, message):
        self._log_wrapper("error", message)
         