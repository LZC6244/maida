# author: lzc
# update: 2019.7.25
# email:  624486877@qq.com
import logging
import smtplib
from os import path
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def isContainChinese(string):
    # 判断字符串是否含有中文
    for s in string:
        if '\u4e00' <= s <= '\u9fa5':
            return True
    return False


class EmailSender(object):

    def __init__(self, email_host='smtphz.qiye.163.com', email_port=465, email_pass=''):
        # 初始化
        self.msg = MIMEMultipart()
        self.client = ''
        self.logger = logging.getLogger(__name__)
        self.email_host = email_host
        self.email_port = email_port
        if email_pass:
            self.email_pass = email_pass
        else:
            # 可以设置一个初始值，避免每次都输入授权码
            self.email_pass = 'xxxxxxxxxxx'
            # self.logger.error('Please Enter The  Password!')

    def init(self, from_addr, to_addrs, subject, x_priority='3', **kwargs):
        """
        初始化，填入以下信息
        :param from_addr:发件人
        :param to_addrs:收件人（收件人为字符串时，视其为一个仅含该字符串的列表）
        :param subject:邮件标题
        :param x_priority:邮件优先级 （ 等同于 email Message 的 X-Priority ）
                "1"	最高级别（重要性高）
                "2"	介于中间 （高）
                "3"	普通级别（不提示重要性）
                "4"	介于中间 （低）
                "5"	最低级别（重要性低）
                "其他" 普通级别（不提示重要性）
        :param kwargs:拓展字段，可以输入 email Message 支持的字段
        :return:
        """
        if isinstance(to_addrs, list):
            pass
        elif isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        else:
            self.logger.error('[ to_addrs ] must be a str or list.')
            return '[ to_addrs ] must be a str or list.'

        self.msg['From'] = from_addr
        # 需为用 ';' 连接的字符串
        self.msg['To'] = ';'.join(to_addrs)
        self.msg['Subject'] = subject
        self.msg['X-Priority'] = x_priority
        for k, v in kwargs.items():
            self.msg[k] = v

        try:
            # 在创建客户端对象的同时，使用SSL加密连接到邮箱服务器
            self.client = smtplib.SMTP_SSL(host=self.email_host, port=self.email_port)
            login_result = self.client.login(from_addr, self.email_pass)
            if login_result and login_result[0] == 235:
                print('[ EmailSender ] Login successful.')
            else:
                print('[ EmailSender ] Login failed: ', login_result[0], login_result[1])
        except Exception as e:
            self.logger.error('[ EmailSender ] Connection to mail server error: %s.' % e)

    def attach_text(self, text=''):
        # 添加邮件正文 （ 纯文本 ）
        msg_text = MIMEText(text, 'plain', 'utf8')
        self.msg.attach(msg_text)

    def attach_html(self, text=''):
        # 添加邮件正文 （ html ）
        # html 格式不固定，故请将 html 源码全部输入
        # 此处不通过 MIMEImage 定义图片ID，在 HTML 文本中引用 （ ... ）
        msg_text = MIMEText(text, 'html', 'utf8')
        self.msg.attach(msg_text)

    def attach_file(self, file=''):
        # 添加邮件附件
        if not file:
            self.logger.error('Please enter the filename that contains the full path.')
            return None
        with open(file, 'rb') as f:
            # 不使用这种，没有文件关闭操作
            # att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att = MIMEText(f.read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            # 获取文件名
            filename = path.split(file)[1]
            # 判断文件名是否含有中文
            if isContainChinese(filename):
                # 处理中文文件名 （ add_header的第三种写法 ）
                att.add_header("Content-Disposition", "attachment", filename=("gbk", "", filename))
            else:
                # 文件名不含中文 （ add_header的第一种写法 ）
                att.add_header('content-disposition', 'attachment', filename=filename)
                # 或者可以这样写
                # att['Content-Disposition'] = 'attachment;filename="%s"' % filename
            self.msg.attach(att)

    def send(self):
        if self.client:
            from_addr = self.msg['From']
            # 需为一个 list
            to_addrs = self.msg['To'].split(';')
            try:
                self.client.sendmail(from_addr, to_addrs, self.msg.as_string())
                print('[ EmailSender ] Email sent successfully.')
            except Exception as e:
                self.logger.error('[ EmailSender ] e-mail sending failed: %s.' % e)
        else:
            self.logger.error('[ EmailSender ] You must first connect to the mail server by using [ init ].')

    def close(self):
        # 关闭对邮件服务器的连接
        if self.client:
            self.client.close()
            print('[ EmailSender ] Closed.')
        else:
            self.logger.error('[ EmailSender ] You must first connect to the mail server by using [ init ].')


if __name__ == '__main__':
    email = EmailSender(email_host='smtp.qq.com', email_pass='xxx')
    content = '这是lzc发送过来的邮件。请注意查收！'
    email.init(from_addr='xxx@qq.com', to_addrs=['xxx@qq.com'], subject='测-试')
    email.attach_text(text=content)
    email.attach_file(r'C:\xxx\xx.jpg')
    email.attach_file(r'C:\xxx\xx.txt')
    email.send()
