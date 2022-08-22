ADDRESS_PATH = "email_programs/address/email_address.txt"

from email_programs import create_email
from email_programs import create_tolist
from email_programs import sendemail
from email_programs import get_schedule
import os

# from address import email_resister


def execute_email_jobs(days_later,email_address):

    gmail_address = os.getenv("ADMIN_GMAIL_ADDRESS")
    gmail_pass = os.getenv("ADMIN_GMAIL_KEY")

    myclass_id = os.getenv("MYCLASS_ID")
    myclass_password = os.getenv("MYCLASS_PASSWORD")

    #まいくらすから出勤コーチと授業数をスクレイピング.days_later日後の出勤コーチとコマ数のdictを返す
    dict = get_schedule.getSchedule(days_later,myclass_id,myclass_password)
    #メールをテキストファイルに出力
    create_email.Create_Mail(dict)
    list = create_tolist.Create_ToList(dict,email_address,gmail_address,gmail_pass)
    #メールを送信する
    sendemail.send_email(list,days_later,gmail_address,gmail_pass)







    

