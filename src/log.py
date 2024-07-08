import logging

FORMAT = "%(asctime)s %(filename)s %(levelname)s:%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, handlers=[logging.FileHandler("./logs/app.log")]
)

logger = logging.getLogger(__name__)
