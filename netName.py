from psutil import net_if_addrs


def netHi():
    s = net_if_addrs()
    for key in s.keys():
        if 'WLAN' in key:
            s = key
    return s
