from datetime import datetime

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

from nscraper.constants import sample_sources
from nscraper.core.consumer import NewsConsumer
from nscraper.core.scraper import NewsScraper
from nscraper.utils.logger import logger


def run_schedule():
    load_dotenv()

    cred = credentials.Certificate('firebase.json')
    firebase_admin.initialize_app(cred)

    scraper = NewsScraper()
    consumer = NewsConsumer()

    has_run = False

    while True:
        current_time = datetime.now()

        if not has_run and current_time.minute % 10 == 0 and current_time.second == 0:
            result = scraper.run(sample_sources)
            consumer.run(result.articles)
            has_run = True
        elif has_run:
            has_run = False


def main() -> None:
    logger.info("Program execution started")
    run_schedule()


if __name__ == '__main__':
    main()
