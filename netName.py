from psutil import net_if_addrs


def netHiWifi():
    for key in net_if_addrs().keys():
        if 'WLAN' in key:
            s = key
            return s


def netHiWire():
    for key in net_if_addrs().keys():
        if '以太' in key:
            s = key
            return s

