import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(module)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler()],
)
DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "data.json"
)
