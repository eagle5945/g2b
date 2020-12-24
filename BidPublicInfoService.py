#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import logging
import logging.handlers
import pandas as pd
from bs4 import BeautifulSoup
import urllib, pymysql, calendar, time, json
from datetime import datetime, timedelta
from threading import Timer
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote


#################################################
# Enable logging
#################################################
mylog = logging.getLogger('MYLOG')
mylog.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)-10s | %(filename)s: %(lineno)s\t\t] %(asctime)s > %(message)s')
file_max_bytes = 10 * 1024 * 1024     # file max size를 10MB로 설정
fileHandler = logging.handlers.RotatingFileHandler(filename='./log/getBidPblancListInfoServc.log', maxBytes=file_max_bytes, backupCount=10)
fileHandler.setFormatter(formatter)
mylog.addHandler(fileHandler)
mylog.info("프로세스 시작 : 입찰공고 - 용역 (WEB->XML)")


inqryEndDt = datetime.now().strftime('%Y%m%d%H%M')
inqryBgnDt = (datetime.now() - timedelta(days=3)).strftime('%Y%m%d%H%M')
numOfRows = 99
pageNo = 1

operation =  {"getBidPblancListInfoServc","getBidPblancListInfoThng","getBidPblancListInfoCnstwk"}

for oper in operation :

    while True : 
        url = "http://apis.data.go.kr/1230000/BidPublicInfoService/" + oper

        queryParams = '?' + urlencode({
            quote_plus('ServiceKey') : 'QtXQ4yL+TKbBh/9HrW7bGeE7rKBbYuXdy6+YMlJ9/WO/ENDL6FZyoGmmt39B3xxT9fTeNkeNOa9QTpN9s+mjRw==',
            quote_plus('numOfRows') : numOfRows,
            quote_plus('pageNo') : pageNo,
            quote_plus('inqryDiv') : 1,
            quote_plus('inqryBgnDt'): inqryBgnDt,
            quote_plus('inqryEndDt'): inqryEndDt,
            quote_plus('type'): 'json'
        })

        request = Request(url + queryParams)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read().decode('utf-8')

        res_dict = json.loads(response_body)
        item_list = res_dict['response']['body']['items']

        for item in item_list :
            # df = pd.DataFrame.from_dict(item)
            # print(type(item))
            # print(type(df))
            print (item['bidNtceNo'])
        

        res_numOfRows = res_dict['response']['body']['numOfRows']
        res_pageNo = res_dict['response']['body']['pageNo']
        res_totalCount = res_dict['response']['body']['totalCount']    

        print ("numOfRows = {}".format(numOfRows))
        # print ("pageNo = {}".format(pageNo))
        # print ("totalCount = {}".format(totalCount))

        if (numOfRows > res_numOfRows):
            pageNo += 1
        else:
            break


    




