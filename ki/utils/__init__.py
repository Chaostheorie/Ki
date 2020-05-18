import smtplib
from email.mime.text import MIMEText


class Emails:
    def __init__(self, app, auth=True):
        self.config = app.config
        self.auth()

    def auth(self):
        self.smtp = smtplib.SMTP(self.config["EMAIL_ADDRESS"],
                                 self.config["EMAIL_PORT"])
        self.e_mail = self.config["EMAIL_FROM"]
        return

    def send(self, message, recpt, subject):
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.e_mail
        msg["To"] = recpt
        self.smtp.sendmail(self.e_mail, [recpt], msg.as_string())
        return


class TreeGroup:
    def __init__(self, trees):
        self.trees = trees
        self.count = len(trees)

    def jsonify(self):
        return [tree.jsonify() for tree in self.trees]
