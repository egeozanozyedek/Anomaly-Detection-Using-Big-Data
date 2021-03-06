import smtplib
from email.message import EmailMessage
from datetime import datetime


class Alert:
    def __init__(self):
        self.EMAIL_ADDRESS = 'anomaly.alert.system@gmail.com'
        self.EMAIL_PASSWORD = 'satdwujdpfkifarv'
        self.contacts = ['anomaly.alert.system@gmail.com', 'anomaly.alert.system@gmail.com']
        self.msg = EmailMessage()

        self.msg['Subject'] = 'Anomaly Detected'
        self.msg['From'] = self.EMAIL_ADDRESS
        self.msg['To'] = 'anomaly.alert.system@gmail.com'
        #self.msg.set_content('ANOMALY!!!')

        now = datetime.now()
        m = 'Anomalous behavior was detected in the system:' + str(now)
        self.msg.set_content(m)

        self.msg.add_alternative("""\
                    <!DOCTYPE html>
                    <html>
                        <body>
                            <h1 style="color:SlateGray;">An anomaly is detected!</h1>
                        </body>
                    </html>
                    """, subtype='html')

    def send_email(self):



        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)
            smtp.send_message(self.msg)


