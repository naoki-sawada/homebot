import json
import urllib.request as urllib

class WeatherAPI:
    def __init__(self, cityid='130010'):
        self.url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + cityid

    def get(self):
        self.r = urllib.urlopen(self.url)
        root = json.loads(self.r.read().decode('utf8'))
        forecasts = root['forecasts']
        text = forecasts[0]['dateLabel'] + 'は' + forecasts[0]['telop'] + 'です'
        return text

    def close(self):
        self.r.close()
