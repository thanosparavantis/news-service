from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class NewsSource:
    name: str
    url: str
    etag: str = None
    modified: str = None


@dataclass
class NewsArticle:
    source: NewsSource
    title: str
    url: str
    description: str | None = None


@dataclass
class NewsSummary:
    headline: str
    id: str | None = None
    municipality: str | None = None
    timestamp: datetime = datetime.now(timezone.utc)
