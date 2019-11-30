# -*- coding: utf-8 -*-

import os
import sys

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from sys import argv, exit
from linkUI import Ui_MainWindow
from wireConnect import wire_connect
from wifiConnect import wifiSHU, wifiCon
from ruijie import shuConnect
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QSettings, Qt, QTimer
from PyQt5.QtGui import QIcon
from logo_png import img as logo
from base64 import b64decode
from linkSHUPath import shuPath

linkpath = shuPath()

sss = os.path.exists(linkpath + r'\logo.png')
if not sss:
    tmp = open(linkpath + r'\logo.png', 'wb')
    tmp.write(b64decode(logo))
    tmp.close()
else:
    pass


class shuUi(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(shuUi, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle('linkSHU')
        self.setWindowIcon(QIcon(linkpath + r'\logo.png'))

        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.input_user.setPlaceholderText("请输入用户名")
        self.input_passwd.setPlaceholderText("请输入密码")
        self.updateLabel.setText("<A href='https://github.com/Holaplace/shuClient'>关于 & 更新</a>")
        self.updateLabel.setOpenExternalLinks(True)

        self.init_login_info()
        self.passwdCB.clicked.connect(self.monitor_passwdCB)
        self.auto_login.clicked.connect(self.monitor_auto_login)
        self.comboBox.currentIndexChanged.connect(self.monitor_comboBox)

        # 自动登录
        self.timer0 = QTimer(self)
        self.timer0.timeout.connect(self.goto_autologin)
        self.timer0.setSingleShot(True)
        self.timer0.start(1000)

        self.myo = None

    def monitor_passwdCB(self):
        if self.passwdCB.isChecked():
            self.auto_login.setEnabled(True)
        else:
            self.auto_login.setChecked(False)
            self.auto_login.setEnabled(False)

        self.save_login_info()
        self.status.setText("登录信息已更新\n")

    def monitor_auto_login(self):
        if self.auto_login.isChecked():
            self.status.setText("请在连接方式的下拉菜单中选择连接方式")

        else:
            self.status.setText("登录信息已更新")
            self.save_login_info()

    def monitor_comboBox(self):
        if self.auto_login.isChecked():
            if self.comboBox.currentIndex() != 0:
                self.status.setText("登录信息已更新")
                self.save_login_info()

    # 保存登录信息
    def save_login_info(self):
        settings = QSettings(linkpath + r"\config.ini", QSettings.IniFormat)

        if not self.passwdCB.isChecked():
            settings.setValue("password", '')
        if self.passwdCB.isChecked():
            settings.setValue("password", self.input_passwd.text())

        if not self.auto_login.isChecked():
            settings.setValue("loginStyle", '')
        if self.auto_login.isChecked():
            settings.setValue("loginStyle", self.comboBox.currentIndex())

        settings.setValue("account", self.input_user.text())
        settings.setValue("remeberpassword", self.passwdCB.isChecked())
        settings.setValue("autologin", self.auto_login.isChecked())

    # 初始化登录信息
    def init_login_info(self):
        settings = QSettings(linkpath + r"\config.ini", QSettings.IniFormat)
        the_account = settings.value("account")
        the_password = settings.value("password")
        the_remeberpassword = settings.value("remeberpassword")
        the_autologin = settings.value("autologin")
        the_loginStyle = settings.value("loginStyle")

        self.input_user.setText(the_account)

        # 记住密码判断
        if the_remeberpassword == "true":
            self.passwdCB.setChecked(True)
            self.input_passwd.setText(the_password)

        if the_remeberpassword == "false":
            self.passwdCB.setChecked(False)
            self.auto_login.setEnabled(False)
            self.input_passwd.setText(the_password)

        # 自动登录判断
        if the_autologin == "true":
            self.auto_login.setChecked(True)

            # 登录方式判断
            if the_loginStyle is None:
                s = '首次登录，请注意选择连接方式'
                self.status.setText(s)
            else:
                self.comboBox.setCurrentIndex(int(the_loginStyle))

    def connectStyle(self):
        try:
            if self.comboBox.currentIndex() is int(1):
                self.wireConnect()
                return

            elif self.comboBox.currentIndex() is int(2):
                self.wifiConnect()
                return

            elif self.comboBox.currentIndex() is int(0):
                return True

        except Exception as e:
            self.status.setText(e)

    # 自动登录
    def goto_autologin(self):
        if self.auto_login.isChecked() is True:
            self.on_pushButton_enter_clicked()

    def on_pushButton_enter_clicked(self):
        # 账号密码NULL判断
        if self.input_user.text() == "" or self.input_passwd.text() == "":
            self.status.setText("请完整输入 用户名 或 密码")

        self.auto_login.stateChanged.connect(self.cancel_autologin)

        tag = self.connectStyle()
        if tag:  # 如果点击login按钮之前选择的连接方式未空
            s = '未选择连接方式，无法登录'
            self.status.setText(s)
        else:
            # 保存登录信息
            self.save_login_info()

    def cancel_autologin(self):
        if not self.auto_login.isChecked():
            settings = QSettings(linkpath + r"\config.ini", QSettings.IniFormat)
            settings.setValue("autologin", False)

    def wireConnect(self):
        # 账号密码NULL判断
        if self.input_user.text() == "" or self.input_passwd.text() == "":
            self.status.setText("请完整输入 用户名 或 密码")

        else:
            user = int(self.input_user.text())
            passwd = str(self.input_passwd.text())
            s = wire_connect(user, passwd)
            self.status.setText(s)

            self.save_login_info()

            # if '有线已连接' or '连接成功' in s:
            #     QTimer.singleShot(500, self.close)

    def wifiConnect(self):
        # 账号密码NULL判断
        if self.input_user.text() == "" or self.input_passwd.text() == "":
            self.status.setText("请完整输入 用户名 或 密码")

        else:
            user = int(self.input_user.text())
            passwd = str(self.input_passwd.text())

            wifiInstance = wifiSHU(user, passwd)
            s = wifiInstance.wifi_connect()

            if s is None:
                self.myo = wifiCon(user, passwd, sender=self)
                self.myo.start()
            else:
                self.status.setText(s)
                self.save_login_info()

    def callback(self, s):
        if '用户' in s:
            pass
        elif s == 'macError':
            s = wifiSHU.s3
        else:
            s = wifiSHU.s2

        self.status.setText(s)
        self.save_login_info()

    def stopConnect(self):
        shu = shuConnect()
        s = shu.logOut()
        self.status.setText(s)


if __name__ == "__main__":
    app = QApplication(argv)
    ui = shuUi()

    ui.login.clicked.connect(ui.connectStyle)
    ui.logout.clicked.connect(ui.stopConnect)

    ui.show()
    exit(app.exec_())
