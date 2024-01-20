import isodate
from googleapiclient.discovery import build
import os
import datetime


class PlayList:
    """Класс плейлиста ютуб-канала."""

    API_KEI: str = os.getenv('API_KEY')

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется по id плейлиста."""

        self.playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(id=self.playlist_id,
                                                            part='snippet',
                                                            ).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        # Во избежание дублирования кода в методах total_duration() и show_best_video()
        # отступил от ТЗ и добавил в конструктор поля:
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50,
                                                                       ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API"""

        return build('youtube', 'v3', developerKey=os.getenv('API_KEY'))

    @property
    def total_duration(self):
        """Приватный метод, возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""

        total_time = datetime.timedelta(0)
        # Выводим длительность видеороликов из плейлиста
        # docs: https://developers.google.com/youtube/v3/docs/videos/list
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)
                                                          ).execute()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        return total_time

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста по количеству лайков."""

        highest_like_count: int = 0
        best_video_url: str = ''
        for video_id in self.video_ids:
            video_response = self.get_service().videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id
            ).execute()
            like_count = video_response['items'][0]['statistics']['likeCount']
            if int(like_count) > highest_like_count:
                best_video_url = 'https://youtu.be/' + video_response['items'][0]['id']
        return best_video_url
