from dataclasses import dataclass, field

from nscraper.core.models import NewsArticle


@dataclass
class ScraperResult:
    articles: list[NewsArticle] = field(default_factory=list)
    urls_new: int = 0
    urls_fresh: int = 0
    urls_expired: int = 0

    def __str__(self):
        return (
            f'URLs new:               {self.urls_new}\n'
            f'URLs cache fresh:       {self.urls_fresh}\n'
            f'URLs cache expired:     {self.urls_expired}'
        )


@dataclass
class ConsumerResult:
    articles_skipped: int = 0
    articles_unprocessable: int = 0
    summaries_created: int = 0
    summaries_updated: int = 0
    summaries_discarded: int = 0

    def __str__(self):
        return (
            f'Articles skipped:       {self.articles_skipped}\n'
            f'Articles unprocessable: {self.articles_unprocessable}\n'
            f'Summaries created:      {self.summaries_created}\n'
            f'Summaries updated:      {self.summaries_updated}\n'
            f'Summaries discarded:    {self.summaries_discarded}'
        )
