import json
import os
import shutil
import unittest
from datetime import timedelta, datetime

from nscraper.core.models import NewsSource
from nscraper.core.scraper import NewsScraper


class TestNewsScraper(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = NewsScraper()
        self.dummy_sources = [
            NewsSource('example.com', os.path.join(os.path.dirname(__file__), 'rss.xml'))
        ]

    def tearDown(self) -> None:
        shutil.rmtree('cache')

    def test_articles(self) -> None:
        run = self.scraper.run(self.dummy_sources)
        articles = run.articles

        self.assertEqual(3, len(articles), 'Should have scraped 3 articles')
        self.assertEqual(3, run.urls_new)
        self.assertEqual(0, run.urls_fresh)
        self.assertEqual(0, run.urls_expired)

        article1, article2, article3 = articles[0], articles[1], articles[2]

        self.assertEqual(self.dummy_sources[0], article1.source)
        self.assertEqual('https://www.example.com/dummy-article1', article1.url)
        self.assertEqual('Article title 1', article1.title)
        self.assertEqual('Article description 1', article1.description)

        self.assertEqual(self.dummy_sources[0], article2.source)
        self.assertEqual('https://www.example.com/dummy-article2', article2.url)
        self.assertEqual('Article title 2', article2.title)
        self.assertIsNone(article2.description)

        self.assertEqual(self.dummy_sources[0], article3.source)
        self.assertEqual('https://www.example.com/dummy-article3', article3.url)
        self.assertEqual('Article title 3', article3.title)
        self.assertIsNone(article2.description)

    def test_articles_cached(self) -> None:
        run1 = self.scraper.run(self.dummy_sources)
        run2 = self.scraper.run(self.dummy_sources)
        run3 = self.scraper.run(self.dummy_sources)

        self.assertEqual(3, len(run1.articles), 'Should have scraped 3 articles initially')
        self.assertEqual(3, run1.urls_new)
        self.assertEqual(0, run1.urls_fresh)
        self.assertEqual(0, run1.urls_expired)

        self.assertEqual(0, len(run2.articles), 'Should have 0 new articles on second run due to caching')
        self.assertEqual(0, run2.urls_new)
        self.assertEqual(3, run2.urls_fresh)
        self.assertEqual(0, run2.urls_expired)

        self.assertEqual(0, len(run3.articles), 'Should have 0 new articles on third run due to caching')
        self.assertEqual(0, run3.urls_new)
        self.assertEqual(3, run3.urls_fresh)
        self.assertEqual(0, run3.urls_expired)

    def test_articles_cached_and_new(self) -> None:
        run1 = self.scraper.run(self.dummy_sources)
        run2 = self.scraper.run(self.dummy_sources)
        run3 = self.scraper.run([
            NewsSource('example.com', os.path.join(os.path.dirname(__file__), 'rss_alt.xml'))
        ])

        self.assertEqual(3, len(run1.articles), 'Should have scraped 3 articles initially')
        self.assertEqual(3, run1.urls_new)
        self.assertEqual(0, run1.urls_fresh)
        self.assertEqual(0, run1.urls_expired)

        self.assertEqual(0, len(run2.articles), 'Should have 0 new articles on second run due to caching')
        self.assertEqual(0, run2.urls_new)
        self.assertEqual(3, run2.urls_fresh)
        self.assertEqual(0, run2.urls_expired)

        self.assertEqual(1, len(run3.articles), 'Should have 1 new article on third run')
        self.assertEqual(1, run3.urls_new)
        self.assertEqual(3, run3.urls_fresh)
        self.assertEqual(0, run3.urls_expired)

    def test_articles_cache_expired(self) -> None:
        run1 = self.scraper.run(self.dummy_sources)

        time_2_days_ago = datetime.now() - timedelta(days=2, seconds=1)

        for url in self.scraper._url_cache:
            self.scraper._url_cache[url] = int(time_2_days_ago.timestamp())

        with open(self.scraper._url_cache_path, 'w', encoding='utf-8') as file:
            json.dump(self.scraper._url_cache, file, indent=2)

        run2 = self.scraper.run(self.dummy_sources)
        run3 = self.scraper.run(self.dummy_sources)

        self.assertEqual(3, len(run1.articles), 'Should have scraped 3 articles initially')
        self.assertEqual(3, run1.urls_new)
        self.assertEqual(0, run1.urls_fresh)
        self.assertEqual(0, run1.urls_expired)

        self.assertEqual(3, len(run2.articles), 'Should have scraped 3 articles again after cache expiration')
        self.assertEqual(3, run2.urls_new)
        self.assertEqual(0, run2.urls_fresh)
        self.assertEqual(3, run2.urls_expired)

        self.assertEqual(0, len(run3.articles), 'Should have 0 new articles on second run due to caching')
        self.assertEqual(0, run3.urls_new)
        self.assertEqual(3, run3.urls_fresh)
        self.assertEqual(0, run3.urls_expired)
