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

# -*- coding: utf-8 -*-

conn = pymysql.connect(host='localhost', user='root', password='kkc5945', db='g2b', charset='utf8')

""" Enable Logging """
mylog = logging.getLogger('MYLOG')
mylog.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)-10s | %(filename)s: %(lineno)s\t\t] %(asctime)s > %(message)s')
file_max_bytes = 10 * 1024 * 1024     # file max size를 10MB로 설정
fileHandler = logging.handlers.RotatingFileHandler(filename='./log/getBidPblancListInfoServc.log', maxBytes=file_max_bytes, backupCount=10)
fileHandler.setFormatter(formatter)
mylog.addHandler(fileHandler)
mylog.info("프로세스 시작 : 사전규격")

inqryEndDt = datetime.now().strftime('%Y%m%d%H%M') # 종료일
inqryBgnDt = (datetime.now() - timedelta(days=50)).strftime('%Y%m%d%H%M') # 시작일
numOfRows = 999

operation =  {"getPublicPrcureThngInfoThng","getPublicPrcureThngInfoServc","getPublicPrcureThngInfoCnstwk"}

for oper in operation :
    pageNo = 1
    print(f"============{oper}============")
    while True : 
        url = "http://apis.data.go.kr/1230000/HrcspSsstndrdInfoService/" + oper
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
        df = pd.DataFrame(item_list)

        with conn.cursor() as curs:
            for r in df.itertuples():              
                bidNtceDtlUrl = f"https://www.g2b.go.kr:8143/ep/preparation/prestd/preStdDtl.do?preStdRegNo={r.bfSpecRgstNo}"
                sql = f"REPLACE INTO HrcspSsstndrdInfoService VALUES ('{oper}', "\
                    f"'{r.bsnsDivNm}', '{r.refNo}', '{r.prdctClsfcNoNm}', '{r.orderInsttNm}', '{r.rlDminsttNm}','{r.asignBdgtAmt}',  "\
                    f"'{r.swBizObjYn}', '{r.rcptDt}', '{r.bfSpecRgstNo}', '{r.rgstDt}', '{r.bidNtceNoList}', '{bidNtceDtlUrl}' )"
                try:
                    curs.execute(sql)
                except Exception as e:
                    continue    # 특수문자 입력 오류가 발생해도 건너뛰고 입력

            conn.commit()
            

        res_numOfRows = res_dict['response']['body']['numOfRows']
        res_pageNo = res_dict['response']['body']['pageNo']
        res_totalCount = res_dict['response']['body']['totalCount']    

        print (f"numOfRows = {res_numOfRows}")
        print (f"len(item_list) = {len(item_list)}")
        print (f"pageNo = {res_pageNo}")
        print (f"totalCount = {res_totalCount}")

        if (len(item_list) < numOfRows):
            break
        else:
            pageNo += 1
            
conn.close()
    




