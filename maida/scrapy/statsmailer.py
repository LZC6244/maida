"""
StatsMailer extension sends an email when a spider finishes scraping.

Use STATSMAILER_RCPTS setting to enable and give the recipient mail address
"""

from scrapy import signals
from scrapy.mail import MailSender
from scrapy.exceptions import NotConfigured
from datetime import timedelta


class StatsMailer(object):

    def __init__(self, stats, recipients, mail, project_name):
        # 新增 project_name 字段，发送邮件时带上项目名，便于区分爬虫
        self.stats = stats
        self.recipients = recipients
        self.mail = mail
        self.project_name = project_name

    @classmethod
    def from_crawler(cls, crawler):
        recipients = crawler.settings.getlist("STATSMAILER_RCPTS")
        # 在 scrapy.settings 加上 PROJECT_NAME 字段,用于设定项目名
        project_name = crawler.settings.get('PROJECT_NAME')
        if not recipients:
            raise NotConfigured
        mail = MailSender.from_settings(crawler.settings)
        o = cls(crawler.stats, recipients, mail, project_name)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider):
        spider_stats = self.stats.get_stats(spider)
        # body = "Global stats\n\n"
        # body += "\n".join("%-50s : %s" % i for i in self.stats.get_stats().items())
        # # print(self.stats.get_stats().items())
        # body += "\n\n%s stats\n\n" % spider.name
        # body += "\n".join("%-50s : %s" % i for i in spider_stats.items())
        # 时区相差8小时，手动加上，还原真实时间
        body = "Global stats\n\n"
        g = dict(self.stats.get_stats().items())
        g['start_time'] = g['start_time'] + timedelta(hours=8)
        g['finish_time'] = g['finish_time'] + timedelta(hours=8)
        body += "\n".join("%-50s : %s" % i for i in g.items())
        # print(self.stats.get_stats().items())
        lo = dict(spider_stats.items())
        lo['start_time'] = lo['start_time'] + timedelta(hours=8)
        lo['finish_time'] = lo['finish_time'] + timedelta(hours=8)
        body += "\n\n%s stats\n\n" % spider.name
        body += "\n".join("%-50s : %s" % i for i in lo.items())
        return self.mail.send(self.recipients, "Scrapy stats for:\t[  %s  ]  %s" % (self.project_name, spider.name),
                              body)
