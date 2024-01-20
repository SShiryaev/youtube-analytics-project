import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    API_KEY: str = os.getenv('API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel['items'][0]['id']}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """Отображает информацию об объекте класса для пользователей."""

        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Складывает количество подписчиков на каналах."""

        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Вычитает количество подписчиков на каналах."""

        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        """Сравнивает со значением «меньше» количество подписчиков на каналах."""

        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Сравнивает со значением «меньше или равно» количество подписчиков на каналах."""

        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        """Сравнивает со значением «больше» количество подписчиков на каналах."""

        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Сравнивает со значением «больше или равно» количество подписчиков на каналах."""

        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        """Проверяет равенство количества подписчиков на каналах."""

        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.get_service().channels().list(id=self.channel_id, part='snippet,statistics')
                         .execute(), indent=2))

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API"""

        return build('youtube', 'v3', developerKey=os.getenv('API_KEY'))

    def to_json(self, json_file):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""

        attribute_dict = {'id': self.channel_id,
                          'title': self.title,
                          'description': self.description,
                          'url': self.url,
                          'subscriber_count': self.subscriber_count,
                          'video_count': self.video_count,
                          'view_count': self.view_count}
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(attribute_dict, file, indent=2)
