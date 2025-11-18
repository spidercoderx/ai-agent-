import os
import time
import logging
from dotenv import load_dotenv
from trends import TrendDetector
from video_generator import VideoGenerator
from uploader import YouTubeUploader, InstagramUploader
import schedule

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_agent():
    logger.info("Starting trend video agent...")

    # Detect trends
    detector = TrendDetector()
    trends = detector.get_trending_topics()
    if not trends:
        logger.info("No trends found. Skipping.")
        return

    # Pick the top trend
    trend = trends[0]
    logger.info(f"Selected trend: {trend}")

    # Generate video prompt
    prompt = f"Create a short video about {trend}"

    # Generate video
    generator = VideoGenerator()
    video_path = generator.generate_video(prompt)

    # Upload to YouTube
    yt_uploader = YouTubeUploader()
    yt_id = yt_uploader.upload_video(video_path, f"Trending: {trend}", f"Latest trends: {trend}")

    # Upload to Instagram
    ig_uploader = InstagramUploader()
    ig_success = ig_uploader.upload_video(video_path, f"Trending: {trend} #viral")

    logger.info("Agent run complete.")

if __name__ == "__main__":
    # Run once for testing
    run_agent()

    # Schedule to run every hour
    schedule.every(1).hours.do(run_agent)

    while True:
        schedule.run_pending()
        time.sleep(60)