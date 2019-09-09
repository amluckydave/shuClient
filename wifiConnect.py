from pywifi import PyWiFi, Profile
from time import sleep
from ruijie import shuConnect
from psutil import net_if_stats
from netName import netHiWifi, netHiWire


nameHiwire = netHiWire()
nameHiwifi = netHiWifi()


def wifi_connect_status(user, passwd):
    if not net_if_stats()[nameHiwifi].isup:  # wifi未连接到Shu(ForAll) 或未打开WiFi开关
        s = connect_wifi(user, passwd)
        return s

    else:  # wifi已连接到internet
        try:  # wifi已连接到 Shu(ForAll)
            s0 = "Shu(ForAll) 连接成功\n"
            shu = shuConnect(user, passwd)
            s = s0 + shu.start_connect()
            return s
        except:  # wifi未连接到 Shu(ForAll)，重连...
            s = connect_wifi(user, passwd)
            return s


def connect_wifi(user, passwd):
    if net_if_stats()[nameHiwire].isup:
        s = '无线连接前，请先断开网线\n'
        return s
    else:
        try:
            wifi = PyWiFi()  # 创建一个wifi对象
            iface = wifi.interfaces()[0]  # 取第一个无限网卡

            iface.disconnect()  # 断开网卡连接
            profile = Profile()  # 配置文件
            profile.ssid = "Shu(ForAll)"  # wifi名称

            iface.remove_all_network_profiles()  # 删除其他配置文件
            tmp_profile = iface.add_network_profile(profile)  # 加载配置文件

            iface.connect(tmp_profile)  # 连接
            sleep(0.5)  # 不延时，wifi反应不过来

            s0 = "Shu(ForAll) 连接成功\n"
            shu = shuConnect(user, passwd)
            s = s0 + shu.start_connect()

        except:
            s = "无线网卡未打开，请打开 WLAN 开关\n"

    return s
