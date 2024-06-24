import datetime

from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

from .preprocessor import Preprocessor
from ..core.models import NewsSummary


class Firestore:
    @staticmethod
    def get_summaries_last_day(municipality: str) -> list[NewsSummary] | None:
        client = firestore.client()
        slug = Preprocessor.slugify_greek(municipality)

        municipality_ref = client.collection('municipalities').document(slug)
        summaries_ref = municipality_ref.collection('summaries')

        now = datetime.datetime.now(datetime.timezone.utc)
        yesterday = now - datetime.timedelta(days=1)

        summaries = []
        summaries_stream = summaries_ref.where(filter=FieldFilter('timestamp', '>=', yesterday)).stream()

        for summary_doc in summaries_stream:
            data = summary_doc.to_dict()
            summaries.append(NewsSummary(
                id=summary_doc.id,
                headline=data['headline'],
                timestamp=data['timestamp'],
            ))

        return summaries

    @staticmethod
    def add_summary(summary: NewsSummary) -> str:
        client = firestore.client()
        slug = Preprocessor.slugify_greek(summary.municipality)

        municipalities_ref = client.collection('municipalities')
        municipality_ref = municipalities_ref.document(slug)
        municipality_ref.set({
            'headline': summary.headline,
            'timestamp': firestore.SERVER_TIMESTAMP,
        }, merge=True)

        summaries_ref = municipality_ref.collection('summaries')
        result = summaries_ref.add({
            'headline': summary.headline,
            'timestamp': firestore.SERVER_TIMESTAMP,
        })
        return result[1].id

    @staticmethod
    def update_summary(summary_id, summary: NewsSummary) -> None:
        client = firestore.client()
        slug = Preprocessor.slugify_greek(summary.municipality)

        municipalities_ref = client.collection('municipalities')
        municipality_ref = municipalities_ref.document(slug)
        municipality_ref.set({
            'headline': summary.headline,
            'timestamp': firestore.SERVER_TIMESTAMP,
        }, merge=True)

        summaries_ref = municipality_ref.collection('summaries')
        summary_ref = summaries_ref.document(summary_id)
        summary_ref.set({
            'headline': summary.headline,
            'timestamp': firestore.SERVER_TIMESTAMP,
        }, merge=True)
