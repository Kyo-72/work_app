import smtplib
import datetime
#日本語メールのためのemailパッケージ
from email.mime.text import MIMEText
from email.header import Header

#エラー一覧
ADDRES_ERROR = 1 #shelveエラー

def CreateErrorMail(flag,list):
    email_file = open('./error.txt','w')
    email_file.write('不具合が生じた際に送信されます\n\n')
    #メールアドレスが登録されていなかった時
    if(flag == ADDRES_ERROR):
        email_file.write('以下該当者のメールアドレスが登録されていないため、出勤メールを送信できていません。お手数ですがメールの転送お願いします\n\n')
        for name in list:
        
            email_file.write(name + '\n')


        email_file.write('\n\n※このメールはプログラムから自動で送信されています')
            

    email_file.close()

def SendError(gmail_address,gmail_pass):

    admin_list = ['seino0702@gmail.com']

    now = datetime.datetime.now()

    charset = 'utf_8'

    maintext_file = open('./error.txt','r')

    msg = MIMEText(maintext_file.read(),'plain',charset)
    msg['Subject'] = Header(now.strftime('ERROR %m/%d(%a)').encode(charset),charset)


    smtp_obj = smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login(gmail_address,gmail_pass)
    smtp_obj.sendmail('seino0702@gmail.com', admin_list,msg.as_string())

    maintext_file.close()
    smtp_obj.quit()


def ErrorMail(flag,list,gmail_address,gmail_pass):
    #エラーのメールを作成
    CreateErrorMail(flag,list)
    #エラーメールを送信
    SendError(gmail_address,gmail_pass)
    
