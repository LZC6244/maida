# -*- coding: utf-8 -*-
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def is_contain_chinese(string):
    # 判断字符串是否含有中文
    for s in string:
        if '\u4e00' <= s <= '\u9fa5':
            return True
    return False


class EmailSender(object):
    from_addr: str
    mail_log: bool
    msg = None

    def __init__(self, email_host, email_port, from_addr, need_auth=True, email_pass=None, mail_log: bool = True):
        """
        :param email_host: smtp 服务器地址，如 'smtp.163.com'
        :param email_port: smtp 服务器端口，如 465
        :param from_addr: 发件人
        :param need_auth: 发送邮件是否需要验证，默认为 Ture
        :param email_pass: 发件人授权码
        :param mail_log: 是否记录 mail 日志
        """
        self.email_host = email_host
        self.email_port = email_port
        self.from_addr = from_addr
        self.need_auth = need_auth
        self.email_pass = email_pass
        self.mail_log = mail_log
        self.msg = MIMEMultipart()
        self.from_addr = from_addr
        self.msg['From'] = self.from_addr

    def clear_attach(self):
        """还原为空白邮件"""
        # self.msg._payload.clear()
        self.msg = MIMEMultipart()
        self.msg['From'] = self.from_addr

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
            logger.error('Please enter the filename that contains the full path.')
            return None
        with open(file, 'rb') as f:
            # 不使用这种，没有文件关闭操作
            # att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att = MIMEText(f.read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            # 获取文件名
            filename = os.path.split(file)[1]
            # 判断文件名是否含有中文
            if is_contain_chinese(filename):
                # 处理中文文件名 （ add_header的第三种写法 ）
                att.add_header("Content-Disposition", "attachment", filename=("gbk", "", filename))
            else:
                # 文件名不含中文 （ add_header的第一种写法 ）
                att.add_header('content-disposition', 'attachment', filename=filename)
                # 或者可以这样写
                # att['Content-Disposition'] = 'attachment;filename="%s"' % filename
            self.msg.attach(att)

    def send(self, to_addrs, subject, cc_addrs=None, mail_ssl=True, mail_tls=True, x_priority='3', **kwargs):
        """
        :param to_addrs:收件人（收件人为字符串时，视其为一个仅含该字符串的列表）
        :param subject:邮件标题
        :param cc_addrs:抄送人
        :param mail_ssl:是否使用ssl加密连接
        :param mail_tls:是否使用tls加密连接
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
            logger.error('[ to_addrs ] must be a str or list.')
            return '[ to_addrs ] must be a str or list.'
        if cc_addrs:
            if isinstance(cc_addrs, list):
                pass
            elif isinstance(cc_addrs, str):
                cc_addrs = [cc_addrs]
            else:
                logger.error('[ cc_addrs ] must be a str or list or None.')
                return '[ cc_addrs ] must be a str or list or None.'
            self.msg['Cc'] = ','.join(cc_addrs)

        # 需为用 ';' 连接的字符串
        self.msg['To'] = ','.join(to_addrs)
        self.msg['Subject'] = subject
        self.msg['X-Priority'] = x_priority
        for k, v in kwargs.items():
            self.msg[k] = v

        if mail_ssl:
            # 在创建客户端对象的同时，使用SSL加密连接到邮箱服务器
            client = smtplib.SMTP_SSL(host=self.email_host, port=self.email_port)
        else:
            client = smtplib.SMTP(host=self.email_host, port=self.email_port)
            if mail_tls:
                client.starttls()
        if self.need_auth:
            login_result = client.login(self.from_addr, self.email_pass)
            if login_result and login_result[0] == 235:
                if self.mail_log:
                    logger.info(f'[ EmailSender ] Login successful: {subject}')
            else:
                raise UserWarning('[ EmailSender ] Login failed: ', login_result[0], login_result[1], f'--- {subject}')
        else:
            logger.info(f'[ EmailSender ] Not need auth: {subject}')

        from_addr = self.msg['From']
        # 需为一个 list
        to_addrs = self.msg['To'].split(',')
        if self.msg['Cc']:
            cc_addrs = self.msg['Cc'].split(',')
            to_addrs.extend(cc_addrs)
        try:
            client.sendmail(from_addr, to_addrs, self.msg.as_string())
            if self.mail_log:
                logger.info(f'[ EmailSender ] Email sent successful: {subject}')
        finally:
            client.close()


if __name__ == '__main__':
    email_sender = EmailSender(email_host='smtp.qq.com', email_port=465, from_addr='xxx@qq.com', email_pass='xxx')
    content = '这是 maida 发送过来的邮件。请注意查收！'
    email_sender.attach_text(text=content)
    email_sender.attach_file(r'C:\xxx\xx.jpg')
    email_sender.attach_file(r'C:\xxx\xx.txt')
    email_sender.send(to_addrs=['xxx@qq.com'], subject='测-试')
