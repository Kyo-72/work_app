ADDRESS_PATH = "email_programs/address/email_address.txt"

from email_programs import create_email
from email_programs import create_tolist
from email_programs import sendemail
from email_programs import get_schedule
import os

# from address import email_resister



# #TODO htmlからそのまま1,2,3,と受け取れるようにした方がいい
# def convert_into_num(date):
#     res = 0

#     if(date == "前日"):
#         res = 1
#     if(date == "二日前"):
#         res = 2
#     if(date == "三日前"):
#         res = 3

#     return res

def execute_email_jobs(days_later,email_address):

    gmail_address = os.getenv("ADMIN_GMAIL_ADDRESS")
    gmail_pass = os.getenv("ADMIN_GMAIL_KEY")

    #まいくらすから出勤コーチと授業数をスクレイピング.days_later日後の出勤コーチとコマ数のdictを返す
    dict = get_schedule.getSchedule(days_later)
    #メールをテキストファイルに出力
    create_email.Create_Mail(dict)
    list = create_tolist.Create_ToList(dict,email_address,gmail_address,gmail_pass)
    #メールを送信する
    sendemail.send_email(list,days_later,gmail_address,gmail_pass)







    

