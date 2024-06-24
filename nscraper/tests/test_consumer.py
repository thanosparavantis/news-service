import unittest
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from typing import Generator
from unittest.mock import patch

from nscraper.core.consumer import NewsConsumer
from nscraper.core.models import NewsArticle, NewsSource, NewsSummary
from nscraper.utils.chatgpt import ChatGPT
from nscraper.utils.discord import Discord
from nscraper.utils.firestore import Firestore


class TestNewsConsumer(unittest.TestCase):
    def setUp(self) -> None:
        self.consumer = NewsConsumer()
        self.test_source = NewsSource('example.com', 'https://www.example.com')
        self.test_article = NewsArticle(
            source=self.test_source,
            title='Dummy article',
            description='Dummy description',
            url='https://www.example.com/dummy-article',
        )
        self.test_summary = NewsSummary(
            municipality='Δήμος Αθηναίων',
            headline='🚔 Μποτιλιάρισμα στο κέντρο της Αθήνας, κλειστή η λεωφόρος Αλεξάνδρας',
        )

    def test_article_no_municipality_matched(self) -> None:
        with self.mock_result():
            result = self.consumer.run([self.test_article])

        self.assertEqual(1, result.articles_skipped)
        self.assertEqual(0, result.articles_unprocessable)
        self.assertEqual(0, result.summaries_created)
        self.assertEqual(0, result.summaries_updated)
        self.assertEqual(0, result.summaries_discarded)

    def test_article_no_summary_generated(self) -> None:
        with self.mock_result('Δήμος Αθηναίων'):
            result = self.consumer.run([self.test_article])

        self.assertEqual(0, result.articles_skipped)
        self.assertEqual(1, result.articles_unprocessable)
        self.assertEqual(0, result.summaries_created)
        self.assertEqual(0, result.summaries_updated)
        self.assertEqual(0, result.summaries_discarded)

    def test_summary_created(self) -> None:
        with self.mock_result('Δήμος Αθηναίων', self.test_summary, []):
            result = self.consumer.run([self.test_article])

        self.assertEqual(0, result.articles_skipped)
        self.assertEqual(0, result.articles_unprocessable)
        self.assertEqual(1, result.summaries_created)
        self.assertEqual(0, result.summaries_updated)
        self.assertEqual(0, result.summaries_discarded)

    def test_summary_created_no_previous_match(self) -> None:
        last_summaries = [
            NewsSummary(
                id='5KHoqYQMfbrTj7sYmFCJ',
                municipality='Δήμος Αθηναίων',
                headline='🚲 Ποδηλατικός αγώνας την ερχόμενη Κυριακή',
                timestamp=datetime.now(timezone.utc) - timedelta(hours=8),
            )
        ]

        with self.mock_result('Δήμος Αθηναίων', self.test_summary, last_summaries):
            result = self.consumer.run([self.test_article])

        self.assertEqual(0, result.articles_skipped)
        self.assertEqual(0, result.articles_unprocessable)
        self.assertEqual(1, result.summaries_created)
        self.assertEqual(0, result.summaries_updated)
        self.assertEqual(0, result.summaries_discarded)

    def test_summary_updated(self) -> None:
        last_summaries = [
            NewsSummary(
                id='5KHoqYQMfbrTj7sYmFCJ',
                municipality='Δήμος Αθηναίων',
                headline='🚓 Μποτιλιάρισμα στο κέντρο της Αθήνας',
                timestamp=datetime.now(timezone.utc) - timedelta(hours=8),
            )
        ]

        with self.mock_result('Δήμος Αθηναίων', self.test_summary, last_summaries):
            result = self.consumer.run([self.test_article])

        self.assertEqual(0, result.articles_skipped)
        self.assertEqual(0, result.articles_unprocessable)
        self.assertEqual(0, result.summaries_created)
        self.assertEqual(1, result.summaries_updated)
        self.assertEqual(0, result.summaries_discarded)

    def test_summary_discarded(self) -> None:
        last_summaries = [
            NewsSummary(
                id='5KHoqYQMfbrTj7sYmFCJ',
                municipality='Δήμος Αθηναίων',
                headline='🚓 Μποτιλιάρισμα στο κέντρο της Αθήνας, κλειστή η λεωφόρος Αλεξάνδρας με εντολή της τροχαίας',
                timestamp=datetime.now(timezone.utc) - timedelta(hours=8),
            )
        ]

        with self.mock_result('Δήμος Αθηναίων', self.test_summary, last_summaries):
            result = self.consumer.run([self.test_article])

        self.assertEqual(0, result.articles_skipped)
        self.assertEqual(0, result.articles_unprocessable)
        self.assertEqual(0, result.summaries_created)
        self.assertEqual(0, result.summaries_updated)
        self.assertEqual(1, result.summaries_discarded)

    @contextmanager
    def mock_result(
            self,
            municipality_result: str | None = None,
            summary_result: NewsSummary | None = None,
            last_summaries_result: list[NewsSummary] | None = None
    ) -> Generator[None, None, None]:
        with (
            patch.object(ChatGPT, 'request_municipality', return_value=municipality_result),
            patch.object(ChatGPT, 'request_summary', return_value=summary_result),
            patch.object(Firestore, 'get_summaries_last_day', return_value=last_summaries_result),
            patch.object(Firestore, 'add_summary', return_value=None),
            patch.object(Firestore, 'update_summary', return_value=None),
            patch.object(Discord, 'send_newsfeed', return_value=None),
        ):
            yield
