from os import path, makedirs


def shuPath():
    rootPath = path.expanduser('~')
    try:
        makedirs(rootPath + r'\linkSHUwifi')
        addrSHU = rootPath + r'\linkSHUwifi'
    except:
        addrSHU = rootPath + r'\linkSHUwifi'

    return addrSHU
