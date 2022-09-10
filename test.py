import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("seino0702@gmail.com")
to_email = [ To("seino0702@gmail.com"),To("seino0702@icloud.com")]
subject = "テストしてるねｎ"
content = Content("text/html", "テストしてるんやけど")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)