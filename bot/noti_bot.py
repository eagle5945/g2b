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
from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler, Filters


MAX_MSG_LENGTH = 3072

# 텔레그램 봇을 생성한다.
# my_token = '291340689:AAG94M-vmn8W2Ca_dwVwRUcG2p-Nd6o5O1s'
my_token = '1370311379:AAE6oqEY53CA76XQuFa28pj3aSD53bNBEaE'
bot = telegram.Bot(token = my_token)

# 로그설정을 한다.
mylog = logging.getLogger('MYLOG')
mylog.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)-10s | %(filename)s: %(lineno)s\t\t] %(asctime)s > %(message)s')
file_max_bytes = 10 * 1024 * 1024     # file max size를 10MB로 설정
fileHandler = logging.handlers.RotatingFileHandler(filename='../log/noti_bot.log', maxBytes=file_max_bytes, backupCount=10)
fileHandler.setFormatter(formatter)
mylog.addHandler(fileHandler)

# DB 커넥션 획득
conn = pymysql.connect(host='localhost', user='root', password='kkc5945', db='g2b', charset='utf8')


def dbgout(message, user_id='65311700'):
    """인자로 받은 문자열을 파이썬 셸과 텔레그램으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message    
    bot.sendMessage(chat_id=user_id, text=strbuf)

def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)


def add_NotiHistoryBid(user_id, bidNtceNo, bidNtceOrd):
    sql = f"REPLACE INTO NotiHistoryBid VALUES('{user_id}','{bidNtceNo}','{bidNtceOrd}')"
    with conn.cursor() as curs:
        try:
            curs.execute(sql)
        except Exception as e:
            print(e)
        conn.commit()             

def add_NotiHistoryHrcsp(user_id, bfSpecRgstNo):
    sql = f"REPLACE INTO NotiHistoryHrcsp VALUES('{user_id}','{bfSpecRgstNo}')"
    with conn.cursor() as curs:
        try:
            curs.execute(sql)
        except Exception as e:
            print(e)
        conn.commit()             

def pushBidPublicInfoService(user_id, list_command):
    """본공고 검색정보를 텔레그램으로 보낸다."""
    
    strbuf = f"\U0001F536 {list_command[0]} {list_command[1]} {list_command[2]} \U0001F536 \n"

    if list_command[1] == "용역": 
        oper = "getBidPblancListInfoServc"
        infoBizYn = "A.infoBizYn ='Y'"
    elif list_command[1] == "물품": 
        oper = "getBidPblancListInfoThng"
        infoBizYn = "A.infoBizYn ='Y'"
    elif list_command[1] == "공사": 
        oper = "getBidPblancListInfoCnstwk"
        infoBizYn = "A.infoBizYn !='N'"
    else : return None

    sql = f"SELECT A.* FROM BidPublicInfoService A LEFT JOIN (SELECT * from NotiHistoryBid WHERE USER = '{user_id}') B "\
        f"ON A.bidNtceNo = B.bidNtceNo AND A.bidNtceOrd = B.bidNtceOrd " \
        f"WHERE B.bidNtceNo IS NULL AND B.bidNtceOrd IS NULL AND A.oper = '{oper}' AND {infoBizYn} "\
        f"AND ( A.bidNtceNm LIKE '%{list_command[2]}%' or A.bidNtceNm LIKE '%{list_command[2]}%' ) "\
        f"AND A.rgstDt BETWEEN date_format(now() -INTERVAL 30 DAY, '%Y-%m-%d %H:%i:%s') AND date_format(now(), '%Y-%m-%d %H:%i:%s') " \
        f"ORDER BY A.rgstDt DESC LIMIT 10 "

    df = pd.read_sql(sql, conn)
    if len(df) == 0:
        strbuf += f"      최신 등록정보가 없습니다. \n"
        bot.sendMessage(chat_id=user_id, text=strbuf, parse_mode='HTML')
    else:
        for idx in range(len(df)):
            if df['asignBdgtAmt'][idx] == "": df['asignBdgtAmt'][idx]="0"
            strbuf += f"입찰공고번호: {df['bidNtceNo'][idx]}-{df['bidNtceOrd'][idx]} \n"\
                f"입찰공고명: <a href ='{df['bidNtceDtlUrl'][idx]}'>{df['bidNtceNm'][idx]}</a>\n "\
                f"수요기관명: {df['dminsttNm'][idx]} \n" \
                f"배정예산금액: {int(df['asignBdgtAmt'][idx]):,d}원 \n"
            add_NotiHistoryBid(user_id, df['bidNtceNo'][idx], df['bidNtceOrd'][idx])
        bot.sendMessage(chat_id=user_id, text=strbuf, parse_mode='HTML')

def pushHrcspSsstndrdInfoService(user_id, list_command):
    """사전규격 검색정보를 텔레그램으로 보낸다."""  

    strbuf = f"\U0001F537 {list_command[0]} {list_command[1]} {list_command[2]} \U0001F537 \n"

    if list_command[1] == "용역": 
        oper = "getPublicPrcureThngInfoServc"
        swBizObjYn = "A.swBizObjYn ='Y'"
    elif list_command[1] == "물품": 
        oper = "getPublicPrcureThngInfoThng"
        swBizObjYn = "A.swBizObjYn ='Y'"
    elif list_command[1] == "공사": 
        oper = "getPublicPrcureThngInfoCnstwk"
        swBizObjYn = "A.swBizObjYn !='N'"
    else : return None

    sql = f"SELECT A.* FROM HrcspSsstndrdInfoService A LEFT JOIN (SELECT * from NotiHistoryHrcsp WHERE USER = '{user_id}') B "\
        f"ON A.bfSpecRgstNo = B.bfSpecRgstNo "\
        f"WHERE B.bfSpecRgstNo IS NULL AND B.user = '{user_id}' AND {swBizObjYn} "\
        f"and A.oper = '{oper}' and ( A.prdctClsfcNoNm LIKE '%{list_command[2]}%' or A.rlDminsttNm LIKE '%{list_command[2]}%' ) "\
        f"and A.rgstDt BETWEEN date_format(now() -INTERVAL 30 DAY, '%Y-%m-%d %H:%i:%s') AND date_format(now(), '%Y-%m-%d %H:%i:%s') "\
        f"ORDER BY A.rgstDt DESC LIMIT 10"

    df = pd.read_sql(sql, conn)
    if len(df) == 0:
        strbuf += f"      최신 검색정보가 없습니다. \n"
        bot.sendMessage(chat_id=user_id, text=strbuf, parse_mode='HTML')
    else:
        for idx in range(len(df)):
            if df['asignBdgtAmt'][idx] == "": df['asignBdgtAmt'][idx]="0"
            strbuf += f"사전규격등록번호: {df['bfSpecRgstNo'][idx]} \n"\
                f"품명(사업명): <a href ='{df['bidNtceDtlUrl'][idx]}'>{df['prdctClsfcNoNm'][idx]}</a>\n "\
                f"실수요기관명: {df['rlDminsttNm'][idx]} \n" \
                f"배정예산금액: {int(df['asignBdgtAmt'][idx]):,d}원 \n"
            add_NotiHistoryHrcsp(user_id, df['bfSpecRgstNo'][idx])                
        bot.sendMessage(chat_id=user_id, text=strbuf, parse_mode='HTML')

def push_search_info(df):
    for idx in range(len(df)):
        user_id = df['user'][idx]
        list_command = df['command'][idx].split()
        if list_command[0] == '사전규격': pushHrcspSsstndrdInfoService(user_id, list_command)
        elif list_command[0] == '본공고': pushBidPublicInfoService(user_id, list_command)
        else: return None

def get_search_word():
    sql = f"SELECT * FROM SearchWord"
    df = pd.read_sql(sql, conn)
    return df

if __name__ == '__main__': 
    df =  get_search_word()
    if len(df) !=0:
        push_search_info(df)
