import json
import urllib.request as urllib
import requests

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

class WioNode:
    def __init__(self, token):
        self.token = token

    def relay(self, onoff):
        url = 'https://us.wio.seeed.io/v1/node/GroveRelayD1/onoff/' + onoff + '?access_token=' + self.token
        r = requests.post(url)
        if r.status_code == 200:
            return True
        else:
            return False
