# maida 

自己写的一些库，目前只有一个发送邮件的功能。

---

##  email
###  EmailSender
>基于 `smtplib` 的发送邮件脚本  
> 1. 可以发送文本
> 2. 可以发送图片
> 3. 可以发送附件（图片、文件等），`附件文件名可以包含中文` 
> 4. 可以群发邮件

### 安装
可以直接 `pip` 安装
>pip install maida

### demo
    email = EmailSender(email_host='smtp.qq.com', email_pass='xxx')
    content = '这是lzc发送过来的邮件。请注意查收！'
    email.init(from_addr='xxx@qq.com', to_addrs=['xxx@qq.com'], subject='测-试')
    email.attach_text(text=content)
    email.attach_file(r'C:\xxx\xx.jpg')
    email.attach_file(r'C:\xxx\xx.txt')
    email.send()

## 版本历程
详见 [history.md](https://github.com/LZC6244/maida/blob/master/history.md)

