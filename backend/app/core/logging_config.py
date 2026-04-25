import logging
import json
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        if record.exc_info:
            log_data["traceback"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

def init_logging(log_path: str = "logs/app.log", level: str = "INFO", max_bytes: int = 5242880, backups: int = 5):
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    file_handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backups, encoding="utf-8")
    file_handler.setFormatter(JSONFormatter())
    root.addHandler(file_handler)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(JSONFormatter())
    root.addHandler(stream_handler)
    return root