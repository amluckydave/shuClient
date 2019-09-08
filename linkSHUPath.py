from os import path, makedirs


def shuPath():
    rootPath = path.expanduser('~')
    try:
        makedirs(rootPath + r'\linkSHU')
        addrSHU = rootPath + r'\linkSHU'
    except:
        addrSHU = rootPath + r'\linkSHU'

    return addrSHU
