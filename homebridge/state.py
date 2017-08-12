import sys
import redis

argvs = sys.argv
rdb = redis.StrictRedis(host='localhost', port=6379, db=0)
state = rdb.get(argvs[1])
print(state)
