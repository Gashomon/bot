import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(receiver_email, passcode):
    sender_email = "novacarrier14@gmail.com"
    sender_password = "cvbwjtefkbujfobl"  # App password or regular password

    # Setting up the MIME
    subject = "Your 4-Digit Passcode"
    body = f"Your 4-digit passcode is: {passcode}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach body with the email
    msg.attach(MIMEText(body, 'plain'))

    # Connecting to Gmail's SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
        print(f"Passcode sent to {receiver_email}")
        return "Success"
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        if e == "[Errno 11001] getaddrinfo failed":
            # cant login. check net 
            # print("no net")
            return "nonet"
        elif e == "(535, b'5.7.8 Sorry.')":
            # print("server error")
            return "selferror"
        elif e == "(535, b'5.7.8 Username and Password not accepted. For more information, go to\n5.7.8  https://support.google.com/mail/?p=BadCredentials d9443c01a7336-2291f1f7dd8sm9884635ad.226 - gsmtp')":
            # print("login error")
            return "selferror"
        else:
            # cant find email. try checking if input is correct
            return "noemail"
        


