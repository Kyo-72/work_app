import datetime
#日本語メールのためのemailパッケージ
import sendgrid
import os
from sendgrid.helpers.mail import *
from pathlib import Path

def send_email(tolist,days_later,gmail_address,gmail_pass,admin_emails):
    #admin_emailsに含まれるメールアドレスには毎日メールを送信する
    tolist += admin_emails
    #出勤メールの日時を取得
    execute_date = datetime.datetime.now() + datetime.timedelta(days = days_later)
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    list = ["seino0702@gmail.com"]
    from_email = From(gmail_address)
    to_email = [ To(email) for email in tolist]
    subject = execute_date.strftime('%m/%d(%a)')
    content = Content("text/html",Path('./email.txt').read_text())
    mail = Mail(from_email,to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

    #SendGridリクエストごとのX-idを返す
    return response.headers["X-Message-Id"]
   
