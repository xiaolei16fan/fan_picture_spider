# -*- coding: utf-8 -*-

import redis
import csv
import time

key = 'picture_url:'

# files = (
#     '../attraction_items.csv',#
#     '../restrant_items.csv',#
#     '../shopping_items.csv',
# )
file = 'restrant_items.csv'

r = redis.StrictRedis(host='localhost', port=6379, db=0)

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
count = 0

with open(file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print('[{}] [Restored]: {}'.format(current_time, row['pic_url']))
        try:
            added = r.sadd(key, row['pic_url'])
        except Exception as e:
            print('[Exception!] {}'.format(repr(e)))
        if added == 0:
            count += 1
            print('[{}] [Dupelicated URL]: {}'.format(current_time, row['pic_url']))
            
    print('[{}] [Done!] Count：{}'.format(current_time, count))
