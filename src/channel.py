import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.id = channel_id
        self.api_key: str = os.getenv('API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.channel = self.youtube.channels().list(id=self.id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel['items'][0]['id']}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube.channels().list(id=self.id, part='snippet,statistics')
                         .execute(), indent=2))

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=os.getenv('API_KEY'))

    def to_json(self, json_file):
        """Метод сохраняющий в файл значения атрибутов экземпляра Channel"""
        attribute_dict = {'id': self.id,
                          'title': self.title,
                          'description': self.description,
                          'url': self.url,
                          'subscriber_count': self.subscriber_count,
                          'video_count': self.video_count,
                          'view_count': self.view_count}
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(attribute_dict, file, indent=2)
