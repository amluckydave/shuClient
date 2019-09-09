from ruijie import shuConnect
from psutil import net_if_addrs, net_if_stats
from IPy import IP
from eduIP import eduIPlist
from netName import netHiWire


def wire_connect_status(user, passwd):
    nameHi = netHiWire()

    if net_if_stats()[nameHi].isup:

        for i in range(len(net_if_addrs()[nameHi])):
            try:
                ip = net_if_addrs()[nameHi][i].address
                if IP(ip).version() == 4:
                    for eduip in eduIPlist:
                        if IP(ip) in IP(eduip):
                            s0 = '上海教育网 有线已连接\n'
                            shu = shuConnect(user, passwd)
                            s = s0 + shu.start_connect()
                            return s
            except:
                pass
    else:
        s = '请检查网线是否插入 或 是否已连接到 SHU有线\n'
        return s
