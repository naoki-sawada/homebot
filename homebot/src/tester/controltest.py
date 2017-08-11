from homebot import *

ctl = Control()

dic = {'aircon': 'off'}
for key, val in dic.items():
    print(key)
    print(val)
ctl.module(dic)
