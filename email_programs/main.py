ADDRESS_PATH = "email_programs/address/email_address.txt"

import schedule
import create_email
import create_tolist
import sendemail
import get_schedule
import time
import sys
from address import email_resister


#TODO htmlからそのまま1,2,3,と受け取れるようにした方がいい
def convert_into_num(date):
    res = 0

    if(date == "前日"):
        res = 1
    if(date == "二日前"):
        res = 2
    if(date == "三日前"):
        res = 3

    return res

def execute_email_jobs(days_later):

    gmail_address = "GMAIL_ADRESS"
    gmail_pass = "ADMIN_GMAIL_ADRESS"

    #まいくらすから出勤コーチと授業数をスクレイピング.days_later日後の出勤コーチとコマ数のdictを返す
    dict = get_schedule.getSchedule(days_later)
    #メールをテキストファイルに出力
    create_email.Create_Mail(dict)
    #登録済みコーチアドレス情報を取得
    address = email_resister.read_file(ADDRESS_PATH)
    #出勤コーチリストを返す
    print(gmail_address)
    print(gmail_pass)
    list = create_tolist.Create_ToList(dict,address,gmail_address,gmail_pass)
    #メールを送信する
    sendemail.send_email(list,days_later,gmail_address,gmail_pass)







    

