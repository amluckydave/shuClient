from pywifi import PyWiFi, Profile, const
from time import sleep
from ruijie import shuConnect
import psutil
from netName import netHi

nameHi = netHi()


def wifi_connect_status(user, passwd):
    if not psutil.net_if_stats()[nameHi].isup:  # wifi未连接到wifi或未打开WiFi开关
        try:
            s = connect_wifi(user, passwd)
        except Exception as e:
            s = e
        return s

    else:  # wifi已连接到internet
        try:  # wifi已连接到 Shu(ForAll)
            s0 = "Shu(ForAll) 连接成功\n"
            shu = shuConnect(user, passwd)
            s = s0 + shu.start_connect()
            return s
        except:  # wifi未连接到 Shu(ForAll)，重连...
            try:
                s = connect_wifi(user, passwd)
            except Exception as e:
                s = e
            return s


def connect_wifi(user, passwd):
    wifi = PyWiFi()  # 创建一个wifi对象
    iface = wifi.interfaces()[0]  # 取第一个无限网卡
    iface.disconnect()  # 断开网卡连接

    profile = Profile()  # 配置文件
    profile.ssid = "Shu(ForAll)"  # wifi名称

    iface.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = iface.add_network_profile(profile)  # 加载配置文件

    iface.connect(tmp_profile)  # 连接
    sleep(1.5)  # 不延时，状态码来不及改变

    if iface.status() == const.IFACE_CONNECTED:
        s0 = "Shu(ForAll) 连接成功\n"
        shu = shuConnect(user, passwd)
        s = s0 + shu.start_connect()

    else:
        s = "无线网卡未打开，请打开 WLAN 开关\n"

    return s
