# -*- coding: utf-8 -*-

from requests import get, post
from json import dump, load
from linkSHUPath import shuPath
import socket
from time import sleep


linkpath = shuPath()


class shuConnect:
    def __init__(self, user=0, passwd='shu'):
        self.user = user
        self.passwd = passwd

    def precheck_connect(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect(("10.10.9.9", 8080))
            return True
        except socket.error:
            return False
        finally:
            sock.close()

    def check_connect(self):
        pre_status = self.precheck_connect()
        if pre_status:
            r = get("http://10.10.9.9:8080")
            if "success.jsp" in r.url:
                return 1
            else:
                return 2
        else:
            return 3

    def catch_data(self):
        try:
            r = get("http://123.123.123.123/")
            query_string = r.text
            st = query_string.find("index.jsp?") + 10
            end = query_string.find("'</script>")
            query_string = query_string[st:end]

            data = {"userId": self.user,
                    "password": self.passwd,
                    "passwordEncrypt": "false",
                    "queryString": query_string,
                    "service": "shu",
                    "operatorPwd": "",
                    "operatorUserId": "",
                    "validcode": ""}

            with open(linkpath + r'\catch_data.json', 'w') as data_file:
                dump(data, data_file)

            return data
        except:
            s = '频繁登录下线操作，可能该无线网卡MAC地址已被锐捷封禁. \n\n 补救方法：点击下方“关于&更新”'
            return s

    def connect(self):
        r = post("http://10.10.9.9:8080/eportal/InterFace.do?method=login", data=self.catch_data())
        r.encoding = "utf-8"
        resp = r.json()

        if resp["result"] == "success":
            return True, ""
        else:
            return False, resp["message"]

    def start_connect(self):
        sleep(1)  # 不延时，precheck 中 sock.connect 反应不过来
        status = self.check_connect()
        if status == 1:
            s = '已认证 & 用户已在线 \n'

        elif status == 2:
            r, msg = self.connect()
            if r:
                s = '认证成功 & 用户上线\n'

            else:
                s = '认证失败\n' + msg
        else:
            s = '暂时无法认证\n'

        return s

    def logOut(self):
        try:
            with open(linkpath + r'\catch_data.json', 'r') as data_file:
                logoutData = load(data_file)

            r = post("http://10.10.9.9:8080/eportal/InterFace.do?method=logout", data=logoutData)
            r.encoding = "utf-8"
            resp = r.json()

            s = resp["message"] + '\n'
            return s
        except IOError:
            s = '提示：首次使用，请打开浏览器转到 http://10.10.9.9:8080 网络认证下线后，再使用客户端登录'
            return s
