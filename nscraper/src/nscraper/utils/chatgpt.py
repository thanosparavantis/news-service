import difflib
import json
import os

import requests

from .logger import logger
from .preprocessor import Preprocessor
from ..constants import municipalities
from ..core.models import NewsSummary


class ChatGPT:
    @staticmethod
    def request_municipality(excerpt: str) -> str | None:
        prompt = (
            'Identify the Greek municipality that corresponds to the news excerpt. '
            'Provide only the official name of the municipality in Greek, starting with "Δήμος". '
            'If no municipality matches, respond with "none".'
        )

        response = ChatGPT._send(prompt, excerpt)

        if response is None:
            return None

        if 'none' in response.lower():
            return None

        value = response.replace(' - ', '-')
        value = Preprocessor.get_searchable(value)

        best_match = None
        highest_score = 0

        for municipality in municipalities:
            eligible = Preprocessor.get_searchable(municipality)
            score = difflib.SequenceMatcher(None, value, eligible).ratio()

            if score > highest_score:
                highest_score = score
                best_match = municipality

        return best_match

    @staticmethod
    def request_summary(municipality: str, excerpt: str) -> NewsSummary | None:
        prompt = (
            f'Write a short headline for {municipality} in Greek based on news excerpts. '
            'Ensure the content is truthful and factual, with slight paraphrasing from the original excerpts. '
            'Do not include links or cite sources. '
            f'The headline should infer the relation with {municipality}. '
            'The headline should begin with a single emoji that captures the mood of the news. '
            'Select an emoji that provides a strong contrast on a white background.'
        )

        response = ChatGPT._send(prompt, excerpt)

        if response is None:
            return None

        return NewsSummary(
            municipality=municipality,
            headline=response,
        )

    @staticmethod
    def _send(prompt: str, payload: str) -> str:
        try:
            response = requests.post(
                url='https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {os.getenv('OPENAI_API_KEY')}',
                    'Content-Type': 'application/json',
                },
                data=json.dumps({
                    'model': 'gpt-4o',
                    'messages': [
                        {
                            'role': 'system',
                            'content': prompt
                        },
                        {
                            'role': 'user',
                            'content': payload
                        }
                    ]
                })
            )

            response.raise_for_status()

            response_json = response.json()
            return response_json['choices'][0]['message']['content']
        except requests.exceptions.HTTPError as error:
            logger.error(f'ChatGPT request failed: {error}')

        return None
