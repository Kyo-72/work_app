ADDRESS_PATH = "email_programs/address/email_address.txt"

from email_programs import create_email
from email_programs import create_tolist
from email_programs import sendemail
from email_programs import get_schedule
import os
import json
import pprint

# from address import email_resister


def execute_email_jobs(days_later,email_address):

    gmail_address = os.getenv("ADMIN_GMAIL_ADDRESS")
    gmail_pass = os.getenv("ADMIN_GMAIL_KEY")
    admin_emails_json = os.getenv("ADMIN_EMAILS_JSON")
    pprint.pprint(admin_emails_json)
    admin_emails = json.loads(admin_emails_json)

    myclass_id = os.getenv("MYCLASS_ID")
    myclass_password = os.getenv("MYCLASS_PASSWORD")

    #まいくらすから出勤コーチと授業数をスクレイピング.days_later日後の出勤コーチとコマ数のdictを返す
    dict = get_schedule.getSchedule(days_later,myclass_id,myclass_password)
    #メールをテキストファイルに出力
    create_email.Create_Mail(dict)
    list = create_tolist.Create_ToList(dict,email_address,gmail_address,gmail_pass,admin_emails,days_later)
    #誰も出勤しなければメールを送信しない
    if(len(list) == 0):
        res = None
    else:
        #メールを送信する
        res = sendemail.send_email(list,days_later,gmail_address,gmail_pass,admin_emails)
        #メール送信リクエスト毎のx_idと授業の日にち
    return res








    

