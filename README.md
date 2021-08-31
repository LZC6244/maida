# maida 

**目前：**
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

email_sender = EmailSender(email_host='smtp.qq.com', email_port=465, from_addr='xxx@qq.com', email_pass='xxx')
content = '这是lzc发送过来的邮件。请注意查收！'
email_sender.attach_text(text=content)
email_sender.attach_file(r'C:\xxx\xx.jpg')
email_sender.attach_file(r'C:\xxx\xx.txt')
email_sender.send(to_addrs=['xxx@qq.com'], subject='测-试')
```


## 版本历程
详见 [history.md](https://github.com/LZC6244/maida/blob/master/docs/history.md)

