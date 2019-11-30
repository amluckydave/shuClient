from pywifi import PyWiFi, Profile
from time import sleep
from ruijie import shuConnect
from psutil import net_if_stats
from netName import netHiWifi, netHiWire
from wireConnect import wire_connect_status
from PyQt5.QtCore import QThread, pyqtSignal

nameHiwire = netHiWire()
nameHiwifi = netHiWifi()


class wifiSHU():
    s1 = '无线连接前，请先断开网线\n'
    s2 = "无线网卡未打开，请打开 WLAN 开关\n"
    s3 = '未检测到无线网卡，或其他未知原因\n'

    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def wifi_connect_status(self):
        checkTag = wire_connect_status()

        if checkTag is None:
            try:
                if not net_if_stats()[nameHiwifi].isup:  # wifi未连接到 internet 或未打开WiFi开关
                    # s = "无线网卡未打开，请打开 WLAN 开关\n"
                    return 2

                else:  # wifi已连接到 Shu(ForAll)
                    return 4
            except:
                # s = '未检测到无线网卡，或其他未知原因: ' + str(e)
                return 3

        else:
            # s = '无线连接前，请先断开网线\n'
            return 1

    def wifi_connect(self):
        wifiTag = self.wifi_connect_status()
        if wifiTag == 1:
            return self.s1

        elif wifiTag == 2 or 4:
            try:
                shu = shuConnect(self.user, self.passwd)
                msg = shu.start_connect()
                if '暂时无法认证' in msg:

                    return

                else:  # wifi已连接到 Shu(ForAll)
                    s0 = "Shu(ForAll) 连接成功\n"
                    s = s0 + msg
                    return s
            except:
                return self.s3

        elif wifiTag == 3:
            return self.s3


class wifiCon(QThread):
    signalCon = pyqtSignal(str)

    def __init__(self, user, passwd, sender):
        super().__init__()
        self.user = user
        self.passwd = passwd
        self.signalCon.connect(sender.callback)

    def run(self):
        try:
            wifi = PyWiFi()  # 创建一个wifi对象
            iface = wifi.interfaces()[0]  # 取第一个无限网卡

            iface.disconnect()  # 断开网卡连接
            profile = Profile()  # 配置文件
            profile.ssid = "Shu(ForAll)"  # wifi名称

            iface.remove_all_network_profiles()  # 删除其他配置文件
            tmp_profile = iface.add_network_profile(profile)  # 加载配置文件

            iface.connect(tmp_profile)  # 连接
            sleep(1)  # 不延时，wifi反应不过来

            s0 = "Shu(ForAll) 连接成功\n"
            shu = shuConnect(self.user, self.passwd, chose=2)
            s = s0 + shu.start_connect()

        except:
            s = 'macError'

        self.signalCon.emit(s)
