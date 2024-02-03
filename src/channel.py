import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = int(channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """Вывод названия канала и ссылки на канал"""
        return f"{self.title} {self.url}"

    def __add__(self, other):
        """Сложение количества подписчиков"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Вычитание количества подписчиков"""
        if self.subscriber_count - other.subscriber_count:
            return self.subscriber_count - other.subscriber_count
        else:
            return other.subscriber_count - self.subscriber_count

    def __gt__(self, other):
        """Сравнение количества подписчиков (больше)"""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """Сравнение количества подписчиков (больше либо равно)"""
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """Сравнение количества подписчиков (меньше)"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """Сравнение количества подписчиков (меньше либо равно)"""
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """Сравнение количества подписчиков (равенство)"""
        return self.subscriber_count == other.subscriber_count

    def printj(self, dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.printj(channel)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=Channel.api_key)

    def to_json(self, file_name):
        """Сохраняет в Json файл значения атрибутов экземпляра - информацию о канале"""
        data = {'channel_id': self.__channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriber_count': self.subscriber_count,
                'video_count': self.video_count,
                'view_count': self.view_count
                }
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)

    @property
    def channel_id(self):
        return self.__channel_id
