import schedule
import create_email
import create_tolist
import sendemail
import get_schedule
import time
import subprocess
import os
import sys

def convert_into_num(date):
    res = 0

    if(date == "前日"):
        res = 1
    if(date == "二日前"):
        res = 2
    if(date == "三日前"):
        res = 3

    return res

def task(days_later):

    #まいくらすから出勤コーチと授業数をスクレイピング.days_later日後の出勤コーチとコマ数のdictを返す
    dict = get_schedule.getSchedule(days_later)
    #メールをテキストファイルに出6力
    create_email.Create_Mail(dict)
    #出勤コーチリストを返す
    list = create_tolist.Create_ToList(dict)
    #メールを送信する
    sendemail.send_email(list,days_later)



args = sys.argv

exe_date = args[1]
exe_time = args[2]


#毎日0時に更新する
schedule.every().day.at(exe_time).do(task,days_later=convert_into_num(exe_date))

while True:
    schedule.run_pending()
    time.sleep(1)
    

