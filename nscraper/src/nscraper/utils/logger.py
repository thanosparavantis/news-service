import logging
import os
from logging.handlers import RotatingFileHandler

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            filename=os.path.join(log_dir, 'nscraper.log'),
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
    ]
)

logger = logging.getLogger('nscraper')
