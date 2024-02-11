import os
from googleapiclient.discovery import build
import json


class PlayList:
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, playlist_id):
        """Класс инициализирует id плейлиста. Имеет публичные аттрибуты:
            название плейлиста и ссылку на плейлист"""
        self.playlist_id = playlist_id
        self.playlist_info = self.get_service().playlists().list(id=self.playlist_id, part='snippet,contentDetails').execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']

    def printj(self, dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        self.playlist_info = self.get_service().videos().list(id=self.playlist_id, part='snippet,contentDetails').execute()
        self.printj(self.playlist_info)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=PlayList.api_key)

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        pass

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        pass
