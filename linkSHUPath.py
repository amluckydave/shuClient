from os import getenv, makedirs


def shuPath():
    rootPath = getenv('SYSTEMROOT')
    try:
        makedirs(rootPath + r'\linkSHU')
        addrSHU = rootPath + r'\linkSHU'
    except:
        addrSHU = rootPath + r'\linkSHU'

    return addrSHU
