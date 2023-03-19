import smtplib
import os

def email(
  send_to,
  subject,
  message
):
  
  sender_email = os.getenv("EMAIL_ADDRESS")
  sender_password = os.getenv("EMAIL_PASSWORD") 
  smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
  smtpObj.ehlo()
  smtpObj.starttls()
  smtpObj.login(sender_email, sender_password)
  smtpObj.sendmail(sender_email, send_to, f'Subject: {subject}\n\n {message}')
  smtpObj.quit()