import smtplib

def sendEmail(code):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("donotreply.poe@gmail.com", "Velocity@093")
    text = """
    Your One Time Password to register for our poe.com is {}
    """.format(str(code))
    message = 'Subject: {}\n\n{}'.format("Welcome to poe.com", text)

    s.sendmail("donotreply.poe@gmail.com", "nkmajevadiya@gmail.com ", message)
    s.quit()
    pass

def Response(status,msg):
    dict_resp = {
        "status": status,
        "message": msg
    }
    return dict_resp



