from psutil import net_if_addrs


def netHi():
    s = net_if_addrs()
    for key in s.keys():
        if '以太' in key:
            s = key
    return s
