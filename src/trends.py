import requests
from pytrends.request import TrendReq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrendDetector:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def get_trending_topics(self, geo='US', timeframe='now 1-d'):
        """
        Fetch trending topics using Google Trends.
        Returns a list of trending keywords.
        """
        try:
            self.pytrends.build_payload(kw_list=[''], geo=geo, timeframe=timeframe)
            trends_df = self.pytrends.trending_searches(pn='united_states')
            if not trends_df.empty:
                return trends_df[0].tolist()[:10]  # Top 10 trends
            else:
                logger.warning("No trending topics found.")
                return []
        except Exception as e:
            logger.error(f"Error fetching trends: {e}")
            return []

if __name__ == "__main__":
    detector = TrendDetector()
    trends = detector.get_trending_topics()
    print("Trending topics:", trends)