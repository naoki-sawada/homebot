from homebot import *

#soc = UdpSocket('192.168.100.104', 1192)
soc = UdpSocket('raspberrypib2.local', 1192)
#soc.send('clean'.encode())
#soc.send('dock'.encode())
soc.send('safe'.encode())
#soc.send('power'.encode())
