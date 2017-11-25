import json
import socket
import datetime
import subprocess
import RPi.GPIO as GPIO
import redis
import requests
import time

from config_loader import *
from temphudi import *
from api import *

class Control:
    def __init__(self):
        config = config_loader()
        self.temphudi = Temphudi()
        self.wapi = WeatherAPI(cityid=config['api']['weather']['cityid'])
        self.wio = WioNode(token=config['api']['wio']['token'])
        self.espr = ESPr(url=config['api']['espr']['url'])
        self.rdb = redis.StrictRedis(host='localhost', port=6379, db=0)
        # GPIO setting
        GPIO.setmode(GPIO.BOARD)
        self.gpiono = {'roomba': 38, 'table_light': 40}
        for var in self.gpiono:
            GPIO.setup(int(self.gpiono[var]), GPIO.OUT)

    def light(self, ctlcmd):
        light_state = self.rdb.get('light')
        if light_state != None:
            light_state = light_state.decode('utf-8')
        if ctlcmd == 'on':
            subprocess.call('irsend SEND_ONCE led.conf on', shell=True)
            GPIO.output(self.gpiono['table_light'], True)
            self.rdb.set('light', 'on')
            return '電気をonにします'
        elif ctlcmd == 'off':
            if light_state == 'orange':
                subprocess.call('irsend SEND_ONCE led.conf orange', shell=True)
            elif light_state == 'off':
                pass
            else:
                subprocess.call('irsend SEND_ONCE led.conf off', shell=True)
            GPIO.output(self.gpiono['table_light'], False)
            self.rdb.set('light', 'off')
            return '電気をoffにします'
        elif ctlcmd == 'orange':
            if light_state == 'orange':
                pass
            else:
                subprocess.call('irsend SEND_ONCE led.conf orange', shell=True)
                GPIO.output(self.gpiono['table_light'], True)
            self.rdb.set('light', 'orange')
            return '電気をorangeにします'

    def aircon(self, ctlcmd):
        if ctlcmd == 'on':
            today = datetime.date.today()
            if today.month in [1, 2, 3, 4, 11, 12]:
                subprocess.call('irsend SEND_ONCE aircon heater_on', shell=True)
            else:
                subprocess.call('irsend SEND_ONCE aircon cooler_on', shell=True)
            self.rdb.set('aircon', 'on')
            return 'エアコンをonにします'
        elif ctlcmd == 'off':
            subprocess.call('irsend SEND_ONCE aircon off', shell=True)
            self.rdb.set('aircon', 'off')
            return 'エアコンをoffにします'

    def fan(self, ctlcmd):
        if ctlcmd == 'on':
            self.espr.relay(1)
            self.rdb.set('fan', 'on')
            return '扇風機をonにします'
        elif ctlcmd == 'off':
            self.espr.relay(0)
            self.rdb.set('fan', 'off')
            return '扇風機をoffにします'

    def roomba(self, ctlcmd):
        # TODO: Roomba control will be available in the future version...
        
        GPIO.output(self.gpiono['roomba'], True)
        time.sleep(3)
        GPIO.output(self.gpiono['roomba'], False)
        return '掃除を開始します'

    def temp(self, ctlcmd):
        tmp, hum = self.temphudi.get()
        ret =  '室温' + str(tmp) + '°, 湿度' + str(hum) + '%'
        return '室温' + str(tmp) + '°, 湿度' + str(hum) + '%'

    def weather(self, ctlcmd):
        ret = self.wapi.get()
        return ret

    def none(self, ctlcmd):
        return 'dummy'

    def music(self, ctlcmd):
        # TODO: Music control will be fixed in the future version...
        playname = 'xxxx'
        url = 'http://xxx.xxx.xxx.xxx:30002'
        payload = {'type': ctlcmd, 'name': playname}
        try:
            ret = requests.post(url, data=json.dumps(payload))
            ret_json = json.loads(ret.text)
            if ctlcmd == 'play':
                ret_str = ret_json['name'] + 'を再生します'
            elif ctlcmd == 'stop':
                ret_str = '停止します'
            elif ctlcmd == 'pause':
                ret_str = '一時停止します'
        except:
            ret_str = 'iTunes server error.'
        return ret_str

    def module(self, dic):
        for key, val in dic.items():
            funcname = 'self.' + key
            ret = eval(funcname)(val)
            if ret != None and len(dic) == 1:
                return ret
