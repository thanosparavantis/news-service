import difflib
import time

from .dtos import ConsumerResult
from ..core.models import NewsArticle, NewsSummary
from ..utils.chatgpt import ChatGPT
from ..utils.discord import Discord
from ..utils.firestore import Firestore
from ..utils.logger import logger


class NewsConsumer:
    def run(self, articles: list[NewsArticle]) -> ConsumerResult:
        result = ConsumerResult()

        if len(articles) == 0:
            logger.info('No articles found for consumption.')
            return result

        logger.info('----------------- Consumer start -----------------')

        for index, article in enumerate(articles):
            if article.description:
                excerpt = f'{article.title} {article.description}'
            else:
                excerpt = f'{article.title}'

            municipality = ChatGPT.request_municipality(excerpt)

            if not municipality:
                result.articles_skipped += 1
                logger.info(f'SKIP> {article.source.name}: {article.title}')
                continue

            summary = ChatGPT.request_summary(municipality, excerpt)

            if not summary:
                result.articles_unprocessable += 1
                logger.info(f'UNPROCESSABLE> {article.source.name}: {article.title}')
                continue

            summaries_last_day = Firestore.get_summaries_last_day(municipality)
            summary_id = self._find_best_match(summary.headline, summaries_last_day)

            if summary_id:
                prev_summary = list(filter(lambda s: s.id == summary_id, summaries_last_day))[0]

                if len(prev_summary.headline) > len(summary.headline):
                    result.summaries_discarded += 1
                    logger.info(f'DISCARD> {municipality}: {summary.headline}')
                    continue

                Firestore.update_summary(summary_id, summary)
                result.summaries_updated += 1

                Discord.send_newsfeed(f'**[{municipality} (upd)]** {summary.headline}')
                logger.info(f'UPDATE> {municipality}: {summary.headline}')
            else:
                Firestore.add_summary(summary)
                result.summaries_created += 1

                Discord.send_newsfeed(f'**[{municipality}]** {summary.headline}\n{article.url}')
                logger.info(f'SUMMARY> {municipality}: {summary.headline}')

            if index < len(articles) - 1:
                time.sleep(1)

        logger.info('---------------- Consumer results ----------------')
        [logger.info(line) for line in str(result).split('\n')]
        logger.info('------------------ Consumer end ------------------')
        return result

    def _find_best_match(self, headline: str, summaries: list[NewsSummary], threshold: float = 0.6) -> str | None:
        best_match = None
        highest_score = 0

        for summary in summaries:
            score = difflib.SequenceMatcher(None, headline, summary.headline).ratio()

            if score > highest_score:
                highest_score = score
                best_match = summary.id

        if highest_score >= threshold:
            return best_match
        else:
            return None
