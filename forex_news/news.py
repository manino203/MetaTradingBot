import requests
from datetime import datetime

from forex_news.news_event import NewsEvent
from utils.singleton import singleton


@singleton
class ForexNews:

    def __init__(self, timezone):
        self.timezone = timezone
        self.url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        self.week_news = self.fetch_this_week_news()

    def fetch_this_week_news(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return [NewsEvent.from_json(event, self.timezone) for event in response.json()]
        else:
            print(f"Failed to fetch news. Status code: {response.status_code}")

    def get_todays_events(self):
        return list(filter(lambda x: x.is_today(), self.week_news))

    def get_todays_events_for_currency(self, currency):
        return list(filter(lambda x: x.is_today() and x.country == currency, self.week_news))


news = ForexNews("EET")
for i in news.get_todays_events_for_currency("USD"):
    print(i)
