import logging
import os

FILE_PATH = "./logs/"
FILE_NAME = "app.log"
LOG_FILE = os.path.join(FILE_PATH, FILE_NAME)

FORMAT = "%(asctime)s %(filename)s %(levelname)s:%(message)s"

os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

logging.basicConfig(level=logging.INFO, format=FORMAT, handlers=[logging.FileHandler(LOG_FILE)])

logger = logging.getLogger(__name__)
