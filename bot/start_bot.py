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

# 텔레그램 updater 
updater = Updater(token=my_token, use_context=True)
dispatcher = updater.dispatcher

global Hrcsp_list, Bid_list, search_list
Hrcsp_list = ['최신 사전규격 용역', '최신 사전규격 물품', '최신 사전규격 공사']
Bid_list = ['최신 본공고 용역', '최신 본공고 물품', '최신 본공고 공사']
search_list = ['검색어 등록', '검색어 삭제', '등록 검색어 조회']

# 로그설정을 한다.
mylog = logging.getLogger('MYLOG')
mylog.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)-10s | %(filename)s: %(lineno)s\t\t] %(asctime)s > %(message)s')
file_max_bytes = 10 * 1024 * 1024     # file max size를 10MB로 설정
fileHandler = logging.handlers.RotatingFileHandler(filename='../log/start_bot.log', maxBytes=file_max_bytes, backupCount=10)
fileHandler.setFormatter(formatter)
mylog.addHandler(fileHandler)


def dbgout(message, user_id='65311700'):
    """인자로 받은 문자열을 파이썬 셸과 텔레그램으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message    
    bot.sendMessage(chat_id=user_id, text=strbuf)

def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)


def putBidPublicInfoService(user_id, command):
    """본공고 검색정보를 텔레그램으로 보낸다."""

def putHrcspSsstndrdInfoService(user_id, command):
    """사전규격 검색정보를 텔레그램으로 보낸다."""    



# command hander
def start(update, context):

    custom_keyboard = [['/start', '/help'], Hrcsp_list, Bid_list ,search_list]
    message =  """ \U0001F518 나라장터 조달정보 봇 v0.2 \U0001F518 
조달정보봇은 나라장터 공공데이터를 가공하여 정보를 제공합니다. 
최신정보는 최근 10일간 조달에 등록된 정보 중 최신 10건을 보여줍니다.
검색어를 등록하시면 매일 9,12,15,17시에 신규등록정보를 수신하실수 있습니다.
한번 수신한 정보는 다음 정보 수신 시 최신정보에서 제외됩니다. """                   

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(message, reply_markup=telegram.ReplyKeyboardRemove())    
    bot.send_message(chat_id=update.effective_chat.id, text="원하시는 버튼을 클릭하세요.", reply_markup=reply_markup )

def help(update, context):
    update.message.reply_text("무엇을 도와드릴까요?")    

def add_search_word(update, context):
    update.message.reply_text("add_search_word?")    

def del_search_word(update, context):
    update.message.reply_text("del_search_word?")            

def list_search_word(update, context):
    update.message.reply_text("list_search_word?")                

def info_search_word(update, context):
    if update.message.text == "검색어 등록":
        msg = "검색어 등록시 다음과 같이 /add 명령어를 입력해주세요. \n /add 본공고 용역 홈페이지"
        update.message.reply_text(msg, reply_markup=telegram.ReplyKeyboardRemove())
    elif update.message.text == "검색어 삭제":
        msg = "검색어 삭제시 다음과 같이 /del 명령어를 입력해주세요. \n /del 본공고 용역 홈페이지"
        update.message.reply_text(msg, reply_markup=telegram.ReplyKeyboardRemove())
    elif update.message.text == "등록 검색어 조회":
        list_search_word(update, context)

# message handler
def echo(update, context):
    user_id = update.effective_chat.id
    user_text = update.message.text

    if user_text in Hrcsp_list: putHrcspSsstndrdInfoService(update, context)
    elif user_text in Bid_list: putBidPublicInfoService(update, context)
    elif user_text in search_list: info_search_word(update, context)
    else: start(update, context)
    
    # context.bot.send_message(chat_id=user_id, text=user_text)



if __name__ == '__main__': 
    try:
        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(CommandHandler('add', add_search_word))
        dispatcher.add_handler(CommandHandler('del', del_search_word))

        # on noncommand i.e message - echo the message on Telegram
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

        # Start the Bot
        updater.start_polling(timeout=3, clean=True)
        dbgout("start_bot start...")

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()        

    except Exception as ex:
        dbgout("start_bot error...")