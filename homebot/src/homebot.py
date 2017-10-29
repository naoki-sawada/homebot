import time
import re
import json
import requests
from slackclient import SlackClient

from config_loader import *

class SlackRtmClient:
    def __init__(self, chname, token, botname):
        self.chname = chname
        self.token = token
        self.botname = botname
        self.sc = SlackClient(self.token)

    def connect(self):
        return self.sc.rtm_connect()

    def read(self):
        msg = self.sc.rtm_read()
        if len(msg) > 0:
            msg = msg[0]
            # user message
            try:
                if msg['user'] != self.botname:
                    if msg['channel'] == self.chname and msg['type'] == 'message':
                        return msg['text']
            except:
                pass

            try:
                if msg['username'] == 'IFTTT':
                    if msg['channel'] == self.chname:
                        return msg['attachments'][0]['pretext']
            except:
                pass

    def send(self, msg):
        sendmsg = msg
        self.sc.rtm_send_message(self.chname, sendmsg)

class NLP:
    def __init__(self, file):
        f = open(file, 'r')
        self.jsonData = json.load(f)

    def _multi_ctl(self, text):
        multiName = self.jsonData['multi']
        for name in multiName:
            #print(name)
            comp = re.compile(name, re.I)
            m = comp.search(text)
            if m != None:
                cmd = multiName[name]['control']
                res = multiName[name]['response']
                return cmd, res
        cmd = None
        res = None
        return cmd, res

    def _single_ctl(self, text):
        singleName = self.jsonData['single']
        ctrlName = singleName['control']
        listName = singleName['list']
        for name in listName:
            comp = re.compile(name, re.I)
            m = comp.search(text)
            if m != None:
                element = listName[name]
                electrl = element['control']
                if electrl != []:
                    for ctrl in electrl:
                        subctrl = ctrlName[ctrl]
                        for ctrlname in subctrl:
                            comp2 = re.compile(ctrlname, re.I)
                            m2 = comp2.search(text)
                            if m2 != None:
                                cmd = subctrl[ctrlname]
                                cmd = {listName[name]['func']: cmd}
                                return cmd

                elif electrl == []:
                    cmd = {listName[name]['func']: 'none'}
                    return cmd

    def search(self, text):
        multi_ctl, res = self._multi_ctl(text)
        if multi_ctl != None:
            return multi_ctl, res

        single_ctl = self._single_ctl(text)
        if single_ctl != None:
            res = None
            return single_ctl, res

        return None, None

class CtlReq:
    def __init__(self, url='http://localhost:8888'):
        self.url = url

    def send(self, cmd):
        res = requests.post(self.url, json=cmd)
        return res.text

if __name__ == '__main__':
    config = config_loader()
    nlp = NLP('cmd/default.json')
    ctlreq = CtlReq()
    sc = SlackRtmClient(
        chname=config['slack']['channel'],
        token=config['slack']['token'],
        botname=config['slack']['botname'],
    )

    failedcount = 0
    if sc.connect():
        connection = True
        print('Home Bot Start!')
        while connection:
            try:
                msg = sc.read()
                failedcount = 0
            except:
                failedcount += 1
                if failedcount > 30:
                    break
                    #connection = False

            if msg != None:
                print()
                print('usr_msg:', msg)
                # Analyze user's text
                ctlmessage, res = nlp.search(msg)
                print('ctl_msg:', ctlmessage)

                # control
                if ctlmessage != None:
                    if res != None:
                        ctlreq.send(ctlmessage)
                    else:
                        res = ctlreq.send(ctlmessage)

                    print('bot_msg:', res)
                    sc.send(res)

            time.sleep(1)

    else:
        print('Connection Failed, invalid token?')
        exit
