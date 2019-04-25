#!/usr/bin/env python3

"""
Default Ports:                   Server:         Authentication:     Port:
=============                    ======          ==============      ====
SMTP Server (Outgoing Messages)  Non-Encrypted   AUTH                25 (or 587)
                                 Secure (TLS)    StartTLS            587
                                 Secure (SSL)    SSL                 465
                                    
POP3 Server (Incoming Messages)  Non-Encrypted   AUTH                110
                                 Secure (SSL)    SSL                 995
"""

import smtplib

# ------------------------------------------------------------ 
# Currently only text body message is supported.
# Future work:
#   - add attachment
#   - add image(s)
# ------------------------------------------------------------

class EmailGmail:
    def __init__(_s, fromaddr=None, username=None, password=None):
        _s.fromaddr = fromaddr
        _s.username = username
        _s.password = password
        _s.subject = ""
        _s.message = []

    def set_fromaddr(_s, text):
        _s.fromaddr = text

    def set_usename(_s, text):
        _s.username = text

    def set_password(_s, text):
        _s.password = text

    def set_subject(_s, text):
        _s.subject = text

    def set_body_message(_s, text_list):
        _s.message = text_list

    def send_email(_s, toaddr):
        print("[=] sending email...")
        if not _s.fromaddr or not _s.username or not _s.password or not _s.subject:
            print("[=] some required parameter is not set")
            return False
        if not _s.message:
            _s.message.append("[=] sending empty message")
            print(_s.message[0])

        _s.message.insert(0, "From: "+ _s.fromaddr)
        _s.message.insert(1, "To: "+ toaddr)
        _s.message.insert(2, "Subject: "+ _s.subject)
        _s.message.insert(3, " ")
        msg = "\r\n".join(_s.message)
        #
        # start sending email
        #
        server = smtplib.SMTP_SSL('smtp.gmail.com:465')
        server.ehlo()
        #
        # no server.starttls() as we are using
        # SMTP_SSL function
        #
        server.login(_s.username, _s.password)
        server.sendmail(_s.fromaddr, toaddr, msg)
        server.quit()
        print("[=] email sending done")
        return True

# -- end --        

