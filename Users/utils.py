import smtplib
from Users.email_files import *


def Response(status,msg):
    dict_resp = {
        "status": status,
        "message": msg
    }
    return dict_resp

def sendEmail_reg_code(username,code,user_email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_id,password)

    message = 'Subject: {}\n\n{}'.format("Welcome for Online Exam",otp_text.format(username,str(code)))

    s.sendmail(email_id, user_email, message)
    s.quit()
    pass

def sendEmail_faculty(username,user_email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_id,password)
    
    message = 'Subject: {}\n\n{}'.format("Welcome to Online Exam", faculty_text.format(username))

    s.sendmail(email_id, user_email, message)
    s.quit()
    pass

def sendEmail_forgot_password(username,user_email,random_password):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_id,password)

    message = 'Subject: {}\n\n{}'.format("Online Exam - Forgot Password Request", forgot_password.format(username,random_password))

    s.sendmail(email_id, user_email, message)
    s.quit()
    pass
