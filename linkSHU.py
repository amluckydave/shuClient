# -*- coding: utf-8 -*-

import sys, \
    os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from sys import argv, exit
from shuClient import Ui_MainWindow
from wireConnect import wire_connect_status
from ruijie import shuConnect
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QSettings, Qt, QTimer
from PyQt5.QtGui import QIcon
from logo_png import img as logo
import base64
from linkSHUPath import shuPath


linkpath = shuPath()

sss = os.path.exists(linkpath + r'\logo.png')
if not sss:
    tmp = open(linkpath + r'\logo.png', 'wb')
    tmp.write(base64.b64decode(logo))
    tmp.close()
else:
    pass


class shuUi(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(shuUi, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle('linkSHU')
        self.setWindowIcon(QIcon(linkpath + r'\logo.png'))

        self.resize(391, 282)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.input_user.setPlaceholderText("请输入用户名")
        self.input_passwd.setPlaceholderText("请输入密码")
        self.updateLabel.setText("<A href='https://github.com/Holaplace/shuClient'>关于 & 更新</a>")
        self.updateLabel.setOpenExternalLinks(True)

        self.init_login_info()
        self.wireButton.clicked.connect(self.on_pushButton_enter_clicked)

        # 自动登录
        self.timer0 = QTimer(self)
        self.timer0.timeout.connect(self.goto_autologin)
        self.timer0.setSingleShot(True)
        self.timer0.start(1000)

    # 保存登录信息
    def save_login_info(self):
        settings = QSettings(linkpath + r"\config.ini", QSettings.IniFormat)
        settings.setValue("account", self.input_user.text())
        settings.setValue("password", self.input_passwd.text())
        settings.setValue("remeberpassword", self.passwdCB.isChecked())
        settings.setValue("autologin", self.auto_login.isChecked())

    # 初始化登录信息
    def init_login_info(self):
        settings = QSettings(linkpath + r"\config.ini", QSettings.IniFormat)
        the_account =settings.value("account")
        the_password = settings.value("password")
        the_remeberpassword = settings.value("remeberpassword")
        the_autologin = settings.value("autologin")

        self.input_user.setText(the_account)
        # 记住密码判断
        if the_remeberpassword == "true" or the_remeberpassword is True:
            self.passwdCB.setChecked(True)
            self.input_passwd.setText(the_password)

        # 自动登录判断
        if the_autologin == "true" or the_autologin is True:
            self.auto_login.setChecked(True)

    # 自动登录
    def goto_autologin(self):
        if self.auto_login.isChecked() is True:
           self.on_pushButton_enter_clicked()

    def on_pushButton_enter_clicked(self):
        # 账号密码NULL判断
        if self.input_user.text() == "" or self.input_passwd.text() == "":
            return

        self.auto_login.stateChanged.connect(self.cancel_autologin)

        # 保存登录信息
        self.save_login_info()

        self.wireConnect()

    def cancel_autologin(self):
        if not self.auto_login.isChecked():
            settings = QSettings(linkpath + r"\config.ini", QSettings.IniFormat)
            settings.setValue("autologin", False)

    def wireConnect(self):
        # 账号密码NULL判断
        if self.input_user.text() == "" or self.input_passwd.text() == "":
            return

        user = int(self.input_user.text())
        passwd = str(self.input_passwd.text())
        s = wire_connect_status(user, passwd)
        self.status.setText(s)

    def stopConnect(self):
        shu = shuConnect()
        s = shu.logOut()
        self.status.setText(s)


if __name__ == "__main__":
    app = QApplication(argv)
    ui = shuUi()

    ui.wireButton.clicked.connect(ui.wireConnect)
    ui.logout.clicked.connect(ui.stopConnect)

    ui.show()
    exit(app.exec_())
