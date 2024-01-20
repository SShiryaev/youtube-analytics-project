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
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.video_ids
                                                               ).execute()

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API"""

        return build('youtube', 'v3', developerKey=os.getenv('API_KEY'))

    @property
    def total_duration(self):
        """Приватный метод, возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""

        total_time = datetime.timedelta(0)

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        return total_time

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста по количеству лайков."""

        highest_like_count: int = 0
        best_video_url: str = ''
        for video in self.video_response['items']:
            like_count = video['statistics']['likeCount']
            video_id = video['id']
            if int(like_count) > int(highest_like_count):
                highest_like_count = like_count
                best_video_url = 'https://youtu.be/' + video_id
        return best_video_url
