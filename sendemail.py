import smtplib
import datetime
#日本語メールのためのemailパッケージ
from email.mime.text import MIMEText
from email.header import Header

def send_email(tolist):
    
    now = datetime.datetime.now()
    tolist.append('poletowin1028@docomo.ne.jp')
    tolist.append('seino0702@gmail.com')
    tolist.append('rei2000826@gmail.com')
    tolist.append('hiro3mino3@yahoo.co.jp')
    tolist.append('ariermal@icloud.com')
    tolist.append('sunflower0719honobono@yahoo.co.jp')
    
    charset = 'utf_8'
    
    E_MAIL = 'seino0702@gmail.com'
    PASSWORD = 'uxcgkcgbwwgmovuz'

    maintext_file = open('./email.txt','r')

    msg = MIMEText(maintext_file.read(),'plain',charset)
    msg['Subject'] = Header(now.strftime('%m/%d(%a)').encode(charset),charset)


    smtp_obj = smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login(E_MAIL,PASSWORD)
    smtp_obj.sendmail('seino0702@gmail.com',tolist,msg.as_string())

    print('メールを以下のメールアドレスに送信します')
    print(tolist)
    maintext_file.close()
    smtp_obj.quit()

