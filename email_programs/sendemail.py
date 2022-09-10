import datetime
#日本語メールのためのemailパッケージ
from email.mime.text import MIMEText
from email.header import Header

def send_email(tolist,days_later,gmail_address,gmail_pass,admin_emails):
    #出勤メールの日時を取得
    execute_date = datetime.datetime.now() + datetime.timedelta(days = days_later)
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    list = ["seino0702@gmail.com","is0462fx@ed.ritsumei.ac.jp"]
    
    from_email = Email(gmail_address)
    to_email = [ To(email) for email in list]
    subject = execute_date.strftime('%m/%d(%a)')
    content = Content("text/html",Path('./email.txt').read_text())
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

    print('メールを以下のメールアドレスに送信します')
    print(tolist)
   
