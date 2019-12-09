# maida 

可以看成自定义拓展 scrapy 的库。目前：
1. 用于发送邮件

---
## 安装
可以直接 `pip` 安装
> pip install maida

##  mail
###  EmailSender
> 基于 `smtplib` 的发送邮件脚本  
> 1. 可以发送文本
> 2. 可以发送图片
> 3. 可以发送附件（图片、文件等），`附件文件名可以包含中文` 
> 4. 可以群发邮件
> 5. 可以设置邮件优先级（如标红）

### demo
```text
from maida import EmailSender

email = EmailSender(email_host='smtp.qq.com', email_pass='xxx')
content = '这是lzc发送过来的邮件。请注意查收！'
email.init(from_addr='xxx@qq.com', to_addrs=['xxx@qq.com'], subject='测-试', x_priority='1')
email.attach_text(text=content)
email.attach_file(r'C:\xxx\xx.jpg')
email.attach_file(r'C:\xxx\xx.txt')
email.send()
email.close()
```

    
## scrapy
整合了 [scrapy_mail](https://github.com/LZC6244/scrapy_mail) 中的拓展，详情请到原始页面查看  
`scrapy` 使用此拓展时可以直接引用，不用手动复制至 **scrapy 同级目录**
即
```text
EXTENSIONS = {
    'lzc.extensions.closespider.CloseSpider': 200,
}
```
变更为
```text
EXTENSIONS = {
    'maida.scrapy.extensions.closespider.CloseSpider': 200,
}
```
其他地方保持不变
## 版本历程
详见 [history.md](https://github.com/LZC6244/maida/blob/master/history.md)

