from datetime import datetime

import pytz


class NewsEvent:

    def __init__(self, title, country, date, impact, forecast, previous, timezone):
        self.timezone = pytz.timezone(timezone)
        self.title = title
        self.country = country
        self.date = datetime.fromisoformat(date).astimezone(self.timezone)
        self.impact = impact
        self.forecast = forecast
        self.previous = previous

    @staticmethod
    def from_json(json, tz):
        return NewsEvent(json['title'],
                         json['country'],
                         json['date'],
                         json['impact'],
                         json['forecast'],
                         json['previous'],
                         tz)

    def is_today(self):
        return self.date.day == datetime.now(self.timezone).day

    def is_impactful(self):
        return self.impact == "High"

    def __str__(self):
        return (f"""title = {self.title}
            country = {self.country}
            date = {self.date}
            impact = {self.impact}
            forecast = {self.forecast}
            previous = {self.previous}
        """.strip())
