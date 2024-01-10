import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.id = channel_id
        self.channel = self.get_service().channels().list(id=self.id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel['items'][0]['id']}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """Метод для отображения информации об объекте класса для пользователей."""

        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Метод, который позволяет складывать количество подписчиков на каналах."""

        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Метод для операции вычитания."""

        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        """Метод для операции сравнения «меньше»."""

        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Метод для операции сравнения «меньше или равно»."""

        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        """Метод для операции сравнения «больше»."""

        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Метод для операции сравнения «больше или равно»."""

        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        """Метод для проверки равенства."""

        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.get_service().channels().list(id=self.id, part='snippet,statistics')
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
