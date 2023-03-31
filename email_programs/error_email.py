import smtplib
import datetime
#日本語メールのためのemailパッケージ
from email.mime.text import MIMEText
from email.header import Header

#エラー一覧
ADDRES_ERROR = 1 #shelveエラー

def CreateErrorMail(flag,list):
    email_file = open('./error.txt','w')
    email_file.write('不具合が生じた際に送信されます<br><br>')
    #メールアドレスが登録されていなかった時
    if(flag == ADDRES_ERROR):
        email_file.write('以下該当者のメールアドレスが登録されていないため、出勤メールを送信できていません。お手数ですがメールの転送お願いします<br><br>')
        for name in list:
        
            email_file.write(name + '<br>')

        email_file.write('<br>以下のサイトからメールアドレスの登録を行ってください<br>https://nagitsuji-systems.herokuapp.com/add_teachers_info')
        email_file.write('<br>※登録されているのに送信できていない場合は名前が間違えている可能性が高いです（空白が入ってる，漢字が間違えてるなど）')
        email_file.write('<br>※このメールはプログラムから自動で送信されています')
            

    email_file.close()

def SendError(gmail_address,gmail_pass,admin_emails,days_later):


    execute_date = datetime.datetime.now() + datetime.timedelta(days = days_later)

    charset = 'utf_8'

    maintext_file = open('./error.txt','r')

    msg = MIMEText(maintext_file.read(),'html',charset)
    msg['Subject'] = Header(execute_date.strftime('ERROR %m/%d(%a)').encode(charset),charset)

    
    smtp_obj = smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login(gmail_address,gmail_pass)
    smtp_obj.sendmail(gmail_address, admin_emails,msg.as_string())

    maintext_file.close()
    smtp_obj.quit()


def ErrorMail(flag,list,gmail_address,gmail_pass,admin_emails,days_later):
    #エラーのメールを作成
    CreateErrorMail(flag,list)
    #エラーメールを送信
    SendError(gmail_address,gmail_pass,admin_emails,days_later)
    
