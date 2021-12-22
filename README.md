# maida 

**目前：**
1. 用于发送邮件  
2. 小说图片转文字

---
## 安装
可以直接 `pip` 安装
> pip install maida

##  mail
###  EmailSender
基于 `smtplib` 的发送邮件脚本  
```text
1. 可以发送文本
2. 可以发送图片
3. 可以发送附件（图片、文件等），`附件文件名可以包含中文` 
4. 可以群发邮件
5. 可以设置邮件优先级（如标红）
```

### demo
```text
from maida import EmailSender

email_sender = EmailSender(email_host='smtp.qq.com', email_port=465, from_addr='xxx@qq.com', email_pass='xxx')
content = '这是 maida 发送过来的邮件。请注意查收！'
email_sender.attach_text(text=content)
email_sender.attach_file(r'C:\xxx\xx.jpg')
email_sender.attach_file(r'C:\xxx\xx.txt')
email_sender.send(to_addrs=['xxx@qq.com'], subject='测-试')
```

## ocr
### img_2_cn
基于 [cnocr](https://github.com/breezedeus/cnocr) 的小说图片转中文文字脚本  

这里提供了一个[来源于网上的小说图片样例](https://github.com/LZC6244/maida/blob/master/test_files/test_img_2_cn.gif)  

可以看出识别效果还是不错的

### demo
```text
from maida import img_2_cn

print(img_2_cn('xxx.gif'))
```

## 版本历程
详见 [history.md](https://github.com/LZC6244/maida/blob/master/docs/history.md)

