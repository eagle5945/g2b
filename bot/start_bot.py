# coding=utf-8

import sys
import re
import traceback
import sys
import time
import logging
import logging.handlers
import pandas as pd
import urllib, pymysql, calendar, time, json
from datetime import datetime, timedelta
from threading import Timer
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import telegram


MAX_MSG_LENGTH = 3072

my_token = '291340689:AAG94M-vmn8W2Ca_dwVwRUcG2p-Nd6o5O1s'
bot = telegram.Bot(token = my_token)

mylog = logging.getLogger('MYLOG')
mylog.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)-10s | %(filename)s: %(lineno)s\t\t] %(asctime)s > %(message)s')
file_max_bytes = 10 * 1024 * 1024     # file max size를 10MB로 설정
fileHandler = logging.handlers.RotatingFileHandler(filename='../log/start_bot.log', maxBytes=file_max_bytes, backupCount=10)
fileHandler.setFormatter(formatter)
mylog.addHandler(fileHandler)


def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 텔레그램으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message    
    bot.sendMessage(chat_id='65311700', text=strbuf)

def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)



if __name__ == '__main__': 
    try:
        dbgout("start_bot start...")
    except Exception as ex:
        dbgout("start_bot error...")