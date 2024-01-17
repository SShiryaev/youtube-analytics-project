import os
from googleapiclient.discovery import build


class Video:
    """Класс видео с ютуб-канала"""
    api_key: str = os.getenv('API_KEY')

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется по id видео. Дальше все данные будут подтягиваться по API."""
        self.id = video_id
        self.video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                      id=video_id).execute()
        self.url = f'https://www.youtube.com/watch?v={self.video['items'][0]['id']}'
        self.video_title: str = self.video['items'][0]['snippet']['title']
        self.view_count: int = self.video['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Отображает название видео."""

        return f'{self.video_title}'

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=os.getenv('API_KEY'))


class PLVideo(Video):
    """Класс плейлиста видео с ютуб-канала"""

    def __init__(self, channel_id, playlist_id) -> None:
        """Экземпляр инициализируется по id канала и id плейлиста. Дальше все данные будут подтягиваться по API."""
        super().__init__(channel_id)
        self.playlist_id = playlist_id
