import json

import requests

from .logger import logger


class Discord:
    @staticmethod
    def send_general(content: str) -> None:
        return Discord._send(
            'https://discord.com/api/webhooks/1112017330596216852/ucGqKC_G8vUZ-egn5bRg0ceRWHu1RXhqCk6KZkB5K_ZFREqcIEbAFU-WRfJtDrSsJlg4',
            content)

    @staticmethod
    def send_alerts(content: str) -> None:
        return Discord._send(
            'https://discord.com/api/webhooks/1223569344269910107/YZQaxEJKwy_RMkBRRJJRi6oTVbrHN5VlnpSPRxryl4x-NpL0-3aoaYeCCuuValWS4fz-',
            content)

    @staticmethod
    def send_newsfeed(content: str) -> None:
        return Discord._send(
            'https://discord.com/api/webhooks/1223566912211128400/yKn7Cyb1WJSfyGQa-btea-vhQpr7UMWfFApo6lVV8G2L-Wv8Yi7ne50CsXvrScxM42Qn',
            content)

    @staticmethod
    def _send(url: str, payload: str) -> None:
        try:
            response = requests.post(
                url=url,
                headers={
                    'Content-Type': 'application/json',
                },
                data=json.dumps({
                    'content': payload
                })
            )

            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logger.error(f'Failed to send Discord message: {error}')
