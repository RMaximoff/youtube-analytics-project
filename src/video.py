from src.channel import YouTubeConnector
from googleapiclient.errors import HttpError


class Video(YouTubeConnector):

    def __init__(self, id_video: str):
        try:
            super().__init__()
            self.id_video = id_video
            self.__video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.id_video
                                                               ).execute()
            self.title = self.__video_response['items'][0]['snippet']['title']
            self.link = f'https://youtu.be/{self.id_video}'
            self.view_count = self.__video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.__video_response['items'][0]['statistics']['likeCount']
            self.duration = self.__video_response['items'][0]['contentDetails']['duration']

        except IndexError:
            self.title = None
            self.link = None
            self.view_count = None
            self.like_count = None
            self.duration = None

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, id_video, playlist_id):
        super().__init__(id_video)
        self.playlist_id = playlist_id


