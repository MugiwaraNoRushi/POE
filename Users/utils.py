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

    message = 'Subject: {}\n\n{}'.format("Welcome to poe.com",otp_text.format(username,str(code)))

    s.sendmail(email_id, user_email, message)
    s.quit()
    pass

def sendEmail_faculty(username,user_email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_id,password)
    
    message = 'Subject: {}\n\n{}'.format("Welcome to poe.com", faculty_text.format(username))

    s.sendmail(email_id, user_email, message)
    s.quit()
    pass
