import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

from nscraper.constants import sample_sources
from nscraper.core.consumer import NewsConsumer
from nscraper.core.scraper import NewsScraper


def main():
    load_dotenv()

    cred = credentials.Certificate('firebase.json')
    firebase_admin.initialize_app(cred)

    scraper = NewsScraper()
    consumer = NewsConsumer()

    result = scraper.run(sample_sources)
    consumer.run(result.articles)


if __name__ == '__main__':
    main()
