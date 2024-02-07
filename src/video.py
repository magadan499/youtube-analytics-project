import os
import json
from src.channel import Channel
from googleapiclient.discovery import build


class Video:
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, video_id: str) -> None:
        """Инициализирует id видео, название, ссылку на видео, количество просмотров и лайков."""
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(id=self.video_id, part='snippet,statistics,contentDetails,topicDetails').execute()
        self.title = self.video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/{self.video_id}"
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Вывод названия видео"""
        return self.title

    def printj(self, dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        self.video_response = self.get_service().videos().list(id=self.video_id, part='snippet,statistics,contentDetails,topicDetails').execute()
        self.printj(self.video_response)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=Channel.api_key)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """Инициализирует id видео, id плейлиста,
        наследует аттрибуты инициализации из класса Video"""
        super().__init__(video_id)
        self.playlist_id = playlist_id
