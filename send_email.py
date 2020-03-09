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
    def __init__(self, fromaddr=None, username=None, password=None):
        self.fromaddr = fromaddr
        self.username = username
        self.password = password
        self.subject = ""
        self.message = []

    def set_fromaddr(self, text):
        self.fromaddr = text

    def set_usename(self, text):
        self.username = text

    def set_password(self, text):
        self.password = text

    def setselfubject(self, text):
        self.subject = text

    def set_body_message(self, text_list):
        self.message = text_list

    def send_email(self, toaddr):
        print("[=] sending email...")
        if not self.fromaddr or not self.username or not self.password or not self.subject:
            print("[=] some required parameter is not set")
            return False
        if not self.message:
            self.message.append("[=] sending empty message")
            print(self.message[0])

        self.message.insert(0, "From: "+ self.fromaddr)
        self.message.insert(1, "To: "+ toaddr)
        self.message.insert(2, "Subject: "+ self.subject)
        self.message.insert(3, " ")
        msg = "\r\n".join(self.message)
        #
        # start sending email
        #
        server = smtplib.SMTPselfSL('smtp.gmail.com:465')
        server.ehlo()
        #
        # no server.starttls() as we are using
        # SMTPselfSL function
        #
        server.login(self.username, self.password)
        server.sendmail(self.fromaddr, toaddr, msg)
        server.quit()
        print("[=] email sending done")
        return True

# -- end --        

