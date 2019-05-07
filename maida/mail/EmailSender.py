# author: lzc
# update: 2019.5.5
import logging
import smtplib
from email.mime.text import MIMEText


class EmailSend(object):
    def __init__(self, email_host='smtphz.qiye.163.com', email_port=465, email_pass=''):
        self.logger = logging.getLogger(__name__)
        self.email_host = email_host
        self.email_port = email_port
        if email_pass:
            self.email_pass = email_pass
        else:
            # 设置一个初始值，避免每次都输入授权码
            self.email_pass = '4faNFstCz5jMUyU7'
            # self.logger.error('Please Enter The  Password!')

    def send(self, from_addr, to_addrs, subject, content):
        to_addrs_s = ''
        if not isinstance(to_addrs, str):
            for i in list(to_addrs):
                to_addrs_s += i + ','
            to_addrs_s = to_addrs_s.strip(',')
        else:
            to_addrs_s = to_addrs

        message_text = MIMEText(content, 'plain', 'utf8')
        message_text['From'] = from_addr
        message_text['To'] = to_addrs_s
        message_text['Subject'] = subject
        try:
            # 在创建客户端对象的同时，连接到邮箱服务器。
            client = smtplib.SMTP_SSL(host=self.email_host, port=self.email_port)
            login_result = client.login(from_addr, self.email_pass)
            if login_result and login_result[0] == 235:
                print('[ EmailSend ] Login successful.')
                # print(login_result)
                client.sendmail(from_addr, to_addrs, message_text.as_string())
                print('[ EmailSend ] Email sent successfully.')
            else:
                print('[ EmailSend ] Login failed: ', login_result[0], login_result[1])
        except Exception as e:
            self.logger.error('[ EmailSend ] Connection to mail server error: %s.' % e)


if __name__ == '__main__':
    email = EmailSend()
    content = '这是lzc发送过来的邮件。请注意查收！'
    email.send(from_addr='xxx@xxx.com', to_addrs=['xxx@xxx.com', 'xxx@xxx.com'], subject='测-试',
               content=content)
