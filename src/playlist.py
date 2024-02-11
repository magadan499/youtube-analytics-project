import os
from googleapiclient.discovery import build
import json
import datetime
import isodate


class PlayList:
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, playlist_id):
        """Класс инициализирует id плейлиста. Имеет публичные аттрибуты:
            название плейлиста и ссылку на плейлист"""
        self.playlist_id = playlist_id
        self.playlist_info = self.get_service().playlists().list(id=playlist_id, part='contentDetails, snippet').execute()
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails, snippet', maxResults=50,).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

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
        max_like = 0
        max_video = ''
        for video in self.video_response['items']:
            count_like = video['statistics']['likeCount']
            count_video = video['id']
            if int(count_like) > int(max_like):
                max_video = count_video
        return f"https://youtu.be/{max_video}"

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration
