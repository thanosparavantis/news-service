import json
import os
import threading
import time
from datetime import datetime, timedelta, timezone

import feedparser

from .dtos import ScraperResult
from .models import NewsArticle, NewsSource
from ..utils.logger import logger
from ..utils.preprocessor import Preprocessor


class NewsScraper:
    def __init__(self) -> None:
        self._result: ScraperResult | None = None
        self._lock: threading.Lock = threading.Lock()
        self._url_cache_path: str = os.path.join('cache', 'url_cache.json')
        self._url_cache: dict[str, int] = {}

    def _load_url_cache(self) -> None:
        if not os.path.exists(self._url_cache_path):
            return

        with open(self._url_cache_path, 'r', encoding='utf-8') as file:
            url_cache = dict(json.load(file))
            url_cache_fresh = {}

            for url in url_cache:
                url_age = datetime.now(timezone.utc) - datetime.fromtimestamp(url_cache[url], timezone.utc)

                if url_age <= timedelta(days=2):
                    url_cache_fresh[url] = url_cache[url]

            self._result.urls_fresh = len(url_cache_fresh)
            self._result.urls_expired = len(url_cache) - len(url_cache_fresh)
            self._url_cache = url_cache_fresh

    def _save_url_cache(self) -> None:
        os.makedirs(os.path.dirname(self._url_cache_path), exist_ok=True)

        self._result.urls_new = len(self._result.articles)

        with open(self._url_cache_path, 'w', encoding='utf-8') as file:
            json.dump(self._url_cache, file, indent=2)

    def run(self, sources: list[NewsSource]) -> ScraperResult:
        self._result = ScraperResult()

        logger.info('------------------ Scrape start ------------------')
        self._load_url_cache()

        threads = [threading.Thread(name=source.name, args=(source,), target=self._run_source) for source in sources]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self._save_url_cache()

        logger.info('----------------- Scrape results -----------------')
        [logger.info(line) for line in str(self._result).split('\n')]
        logger.info('------------------- Scrape end -------------------')
        return self._result

    def _run_source(self, source: NewsSource) -> None:
        start_time = time.time()
        feed = feedparser.parse(source.url, source.etag, source.modified)
        end_time = time.time()

        source.etag = feed.get('etag')
        source.modified = feed.get('modified')

        response_s = end_time - start_time
        entry_count = len(feed.entries)
        status_str = feed.get('status')
        error_str = feed.get('bozo_exception')

        logger.info(
            f'{f'{status_str} ' if status_str else ''}'
            f'{source.name:<20}'
            f'{response_s:>5.2f}s '
            f'{entry_count:>4} entries'
            f'{f' {error_str}' if error_str else ''}'
        )

        self._process_entries(source, feed.entries)

    def _process_entries(self, source: NewsSource, entries: list[feedparser.FeedParserDict]) -> None:
        for entry in entries:
            url = Preprocessor.clear_url(entry.link)

            with self._lock:
                if url in self._url_cache:
                    continue
                self._url_cache[url] = int(datetime.now(timezone.utc).timestamp())

            description = None

            if 'summary' in entry and len(entry.summary) > 0:
                description = Preprocessor.clear_text(entry.summary)

            article = NewsArticle(
                source=source,
                title=entry.title,
                description=description,
                url=url
            )

            self._result.articles.append(article)
