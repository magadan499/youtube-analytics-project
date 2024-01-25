import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
print(moscowpython.get_service())