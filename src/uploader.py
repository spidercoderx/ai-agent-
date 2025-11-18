import os
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from instabot import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeUploader:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def upload_video(self, video_path, title, description):
        try:
            request = self.youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "tags": ["trending", "viral"],
                        "categoryId": "22"  # People & Blogs
                    },
                    "status": {
                        "privacyStatus": "public"
                    }
                },
                media_body=MediaFileUpload(video_path)
            )
            response = request.execute()
            logger.info(f"Video uploaded to YouTube: {response['id']}")
            return response['id']
        except Exception as e:
            logger.error(f"Error uploading to YouTube: {e}")
            return None

class InstagramUploader:
    def __init__(self):
        self.bot = Bot()
        self.bot.login(username=os.getenv('INSTAGRAM_USERNAME'), password=os.getenv('INSTAGRAM_PASSWORD'))

    def upload_video(self, video_path, caption):
        try:
            self.bot.upload_video(video_path, caption=caption)
            logger.info("Video uploaded to Instagram")
            return True
        except Exception as e:
            logger.error(f"Error uploading to Instagram: {e}")
            return False

if __name__ == "__main__":
    # Example usage
    yt_uploader = YouTubeUploader()
    yt_uploader.upload_video("output.mp4", "Trending Topic", "Description")

    ig_uploader = InstagramUploader()
    ig_uploader.upload_video("output.mp4", "Trending Topic #viral")