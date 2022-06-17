import smtplib
import datetime
#日本語メールのためのemailパッケージ
from email.mime.text import MIMEText
from email.header import Header

def send_email(tolist,days_later):
    #出勤メールの日時を取得
    execute_date = datetime.datetime.now() + datetime.timedelta(days = days_later)
    
    
    charset = 'utf_8'
    
    E_MAIL = 'nagitsujisystems@gmail.com'
    PASSWORD = 'ywqjhdytbqoemomi'

    maintext_file = open('./email.txt','r')

    msg = MIMEText(maintext_file.read(),'plain',charset)
    msg['Subject'] = Header(execute_date.strftime('%m/%d(%a)').encode(charset),charset)


    smtp_obj = smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login(E_MAIL,PASSWORD)
    smtp_obj.sendmail('seino0702@gmail.com',"seino0702@gmail.com",msg.as_string())

    print('メールを以下のメールアドレスに送信します')
    print(tolist)
    maintext_file.close()
    smtp_obj.quit()

