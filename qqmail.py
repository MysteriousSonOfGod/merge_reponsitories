# coding=utf-8

import requests
import re
import time


def print_instruction(fun, word='hello, this is a decorator.'):
    def wrapper(self):
        qq_ls = []
        input(word + '\n')
        while True:
            qq = input('')
            qq_ls.append(qq)
            if qq == '-1':
                break
            print(qq_ls)
        fun(self, qq_ls)
    return wrapper


def re_find(pattern, string):
    return re.findall(pattern, string)[0]


def file_read(file):
    with open(file, 'r', encoding='utf-8') as f:
        for friend in f:
            yield friend


class QQmailMixin:
    pass


class QQmail:
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.181 Safari/537.36',
        'origin': 'https://rl.mail.qq.com',
        'referer': 'https://rl.mail.qq.com/zh_CN/htmledition/ajax_proxy.html?mail.qq.com&v=130132',
    }

    def __init__(self, qqmail, sid, cookie):
        # self.cookie = {'cookie': 'pt2gguin=o0347761683; RK=/Ir1hRvwXg; '
        #                          'ptcz=50dc4224a1aaf038e754346f1b0fb3f841c248e99ab2849d5f8a424d596dc8d5; '
        #                          'edition=mail.qq.com; webp=1; pgv_pvid=2897244896; pgv_pvi=9966468096; '
        #                          'p_uin=o0347761683; wimrefreshrun=0&; qm_flag=0; qqmail_alias=347761683@qq.com; '
        #                          'qm_username=347761683; qm_domain=https://mail.qq.com; foxacc=347761683&0; '
        #                          'ssl_edition=sail.qq.com; username=347761683&347761683; CCSHOW=000001; ptisp=ctc; '
        #                          'pt4_token=kicV5PmPXV74ZfwXcmnNrGf29ZOG87GnzKIfZuRxAFw_; '
        #                          'p_skey=vW5vK24Lp2Y55xhdilGxlSKiXamzK6jWIGgeQa7cWb8_; '
        #                          'qm_antisky=347761683'
        #                          '&ae85957171cec788a15ba81e9e716097cdd85d5ee6f6536132fae044e945d959; '
        #                          'sid=347761683&108de223210b96f0750964c8b8fce321,'
        #                          'qdlc1dksyNExwMlk1NXhoZGlsR3hsU0tpWGFteks2aldJR2dlUWE3Y1diOF8.; '
        #                          'qm_ptsk=347761683&@rITroCgIV; qm_loginfrom=347761683&wsk; '
        #                          'new_mail_num=347761683&103; uin=o0347761683'
        #                }
        self.qqmail = qqmail
        self.sid = sid
        self.cookie = cookie
        # self.qqmail = '347761683@qq.com'
        # self.sid = 'gJN3st48O4FLFwNZ'
        # self.qqmail = str(input('输入你的qq邮箱\n'))
        # self.sid = str(input('输入sid\n'))
        # self.cookie = {'cookie': str(input('输入cookies\n'))}

        self.url = f'https://mail.qq.com/cgi-bin/compose_send?sid={self.sid}'

    @print_instruction
    def send_mes(self, qq_ls, file=None):
        if file:
            friend_addr = file_read(file)
        else:
            friend_addr = qq_ls
        # friend_addr = '3179621437@qq.com'
        topic = str(input('输入主题：\n'))
        message = str(input('输入内容：\n'))
        data = {
            'sid': 'gJN3st48O4FLFwNZ',
            'from_s': 'cnew',
            'to': friend_addr,
            'subject': topic,
            'content__html': f'<div>{message}</div>',
            'savesendbox': '1',
            'actiontype': 'send',
            's': 'comm',
            'cginame': 'compose_send',
            'ef': 'js',
            't': 'compose_send.json',
            'resp_charset': 'UTF8'
        }
        send = requests.post(self.url, headers=self.head, cookies=self.cookie, data=data)
        self.status_info(send.text)
        time.sleep(2)

    def status_info(self, info):
        status = re_find(r'errcode : "(\d+)"', info)
        sender = re_find(r'sAddr : "(.*?)"', info)
        if not int(status):
            print(f'successful  <{self.qqmail}> -> <{sender}>')


# if __name__ == '__main__':
    # fdl = QQmail()
    # fdl.send_mes()
    # f = fdl.file_read('qq.txt')
