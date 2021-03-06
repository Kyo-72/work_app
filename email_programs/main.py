ADDRESS_PATH = "email_programs/address/email_address.txt"

import schedule
import create_email
import create_tolist
import sendemail
import get_schedule
import time
import subprocess
import os
import sys
from address import email_resister


args = sys.argv

print("args{}".format(len(args)) )

exe_date = args[1]
exe_time = args[2]
my_usr = args[3]
my_pass = args[4]
gmail_address = args[5]
gmail_pass = args[6]



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

    print(gmail_address)
    print(gmail_pass)

    #まいくらすから出勤コーチと授業数をスクレイピング.days_later日後の出勤コーチとコマ数のdictを返す
    dict = get_schedule.getSchedule(days_later)
    #メールをテキストファイルに出6力
    create_email.Create_Mail(dict)
    #登録済みコーチアドレス情報を取得
    address = email_resister.read_file(ADDRESS_PATH)
    #出勤コーチリストを返す
    print(gmail_address)
    print(gmail_pass)
    list = create_tolist.Create_ToList(dict,address,gmail_address,gmail_pass)
    #メールを送信する
    sendemail.send_email(list,days_later,gmail_address,gmail_pass)








#毎日0時に更新する
schedule.every().day.at(exe_time).do(task,days_later=convert_into_num(exe_date))

while True:
    schedule.run_pending()
    time.sleep(1)
    

