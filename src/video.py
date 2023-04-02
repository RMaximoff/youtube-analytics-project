from src.channel import YouTubeConnector


class Video(YouTubeConnector):

    def __init__(self, id_video: str):
        super().__init__()
        self.id_video = id_video
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.id_video
                                       ).execute()
        self.tittle = self.video_response['items'][0]['snippet']['title']
        self.link = f'https://www.youtube.com/watch?v={self.id_video}'
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.tittle


class PLVideo(Video):

    def __init__(self, id_video, playlist_id):
        super().__init__(id_video)
        self.playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
