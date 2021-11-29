import schedule
import create_email
import create_tolist
import sendemail
import get_schedule
import time

def task():

    #何日後の出勤をメールするか
    days_later = 3
    #まいくらすから出勤コーチと授業数をスクレイピング.days_later日後の出勤コーチとコマ数のdictを返す
    dict = get_schedule.getSchedule(days_later)
    #メールをテキストファイルに出6力
    create_email.Create_Mail(dict)
    #出勤コーチリストを返す
    list = create_tolist.Create_ToList(dict)
    #メールを送信する
    sendemail.send_email(list,days_later)

#毎日0時に更新する
#schedule.every().day.at("11:20").do(task)


"""
while True:
    schedule.run_pending()
    time.sleep(1)
    
"""

task()

