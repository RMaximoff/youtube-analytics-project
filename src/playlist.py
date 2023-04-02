from src.channel import YouTubeConnector
from src.video import PLVideo
import isodate
from datetime import datetime, timedelta
import json


class PlayList(YouTubeConnector):
    def __init__(self, playlist_id: str):
        super().__init__()
        self.playlist_id = playlist_id
        self.playlist = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.videos = self.__get_videos()

    def __get_videos(self):
        """
        Получает список видео в плейлисте
        """
        videos = []
        pl_response = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                        part='snippet',
                                                        maxResults=50
                                                        ).execute()
        for pl_item in pl_response['items']:
            video_id = pl_item['snippet']['resourceId']['videoId']
            videos.append(PLVideo(video_id, self.playlist_id))

        return videos

    @property
    def total_duration(self):
        """
        Возвращает суммарную длительность плейлиста в формате timedelta
        """
        duration = 0
        for video in self.videos:
            time_in_sec = isodate.parse_duration(video.duration).total_seconds()
            duration += time_in_sec

        return timedelta(seconds=duration)

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        best_video = max(self.videos, key=lambda video: int(video.like_count))
        return best_video.link

