
## linkSHU

ManuTus (Manuscript Status) 时刻监视投稿期刊的状态.

实现论文状态改变时，及时通过短信或电话通知作者.


## Table of Contents

   * [ManuTus](#manutus)
   * [Table of Contents](#table-of-contents)
   * [Progressing](#rocket-Progressing)
   * [For Windows](#for-windows)
      * [Step 1 Installation](#step-1-installation)
      * [Step 2 Token](#step-2-token)
   * [For Linux](#for-linux)
      * [Step 1 Dependency](#step-1-Dependency)
      * [Step 2 Python 3.7](#step-2-python-37)
      * [Step 3 Lib](#step-3-Lib)
      * [Step 4 Configure](#step-4-Configure)
      * [Q&A](#Q&A)
   * [Download](#building_construction-Download)

## :rocket: Progressing
欢迎对本项目提交“Issues”帮助我完善脚本;

目前支持**Elsevier**和**RSC**的投稿系统, 其它系统等有投稿再update哈...

## :pencil: For Windows (Win 10)

### Step 1 Installation
% Python 3.5 以上
% 安装必要库, 包括: pyppeteer, twilio, baidu-aip, *etc*.
% 参照 "Download" 配置 Chromium

### Step 2 Token
% 使用前提: 你已知晓如何申请[百度AI识别](https://login.bce.baidu.com/)和[Twilio](https://www.twilio.com/), 相关配置请Google.

% 调整程序中的网址和账号即可.

## :pushpin: For Linux (Centos 7)

### Step 1 Dependency

% 依赖库:
```
sudo yum install pango.x86_64 libXcomposite.x86_64 libXcursor.x86_64 libXdamage.x86_64 libXext.x86_64 libXi.x86_64 libXtst.x86_64 cups-libs.x86_64 libXScrnSaver.x86_64 libXrandr.x86_64 GConf2.x86_64 alsa-lib.x86_64 atk.x86_64 gtk3.x86_64 nss.x86_64 -y
```
% 字体
```
sudo yum install ipa-gothic-fonts xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc -y
```
% 去沙箱
```
await launch ("--no-sandbox")
```

### Step 2 Python 3.7

% Install yum-utils
```
sudo yum install yum-utils
```
% Install yum-builddep
```
sudo yum-builddep python
```
% Download Python 3.7
```
sudo yum install wget
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
```
% Compile Python 3.7
```
tar xf Python-3.7.0.tgz
cd Python-3.7.0
./configure
make && make install
```
% Update pip3
```
pip3 install --upgrade pip
```
### Step 3 Lib
% Install Lib
```
pip3 install pyppeteer
pip3 install twilio
pip3 install baidu-aip
```
% Correct connection.py
```
文件位置: /usr/local/lib/python3.7/site-packages/pyppeteer/connection.py
修改参考: https://github.com/miyakogi/pyppeteer/pull/160/files

修改内容: 44行
	原: self._url, max_size=None, loop=self._loop)
	后: self._url, max_size=None, loop=self._loop, ping_interval=None, ping_timeout=None)
```
### Step 4 Configure
% 按照 **“附件下载”** 部分执行 (GFW的Linux可忽略)
% 使用 SFTP 软件挂载上传至 /home/
% 建立screen 多窗口控制, 以防退出SSH时, 任务中止.

```
screen -S name 建立name任务
screen -x name 进入name任务
screen -ls     浏览当前所有任务
crtl + A + D   返回主窗口

crontab -l     浏览当前所有定时任务
crontab -e     建立定时任务

*/15 * * * * python /home/manuOCR.py
*/17 * * * * python /home/RSC_VPS.py
```


**Note:** 

Elsevier--> manuOCR.py

RSC --> RSC_VPS.py

使用前提: 你已知晓如何申请[百度AI识别](https://login.bce.baidu.com/)和[Twilio](https://www.twilio.com/), 相关配置请Google.



### Q&A
1. Python环境设置, 出现在./configure末. 提示代码: -zlib not available (zipimport.ZipImportError: can‘t decompress data; zlib not available)

解决办法: 安装依赖后, 重新 make && make install
```
sudo yum install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
```
2. 安装完 Python3 后, yum无法使用

解决方法: 修改yum的相关依赖,下述文件第一行改为 /usr/bin/python3.7
```
vi /usr/libexec/urlgrabber-ext-down
```


## :building_construction: Download
如果在GFW内，首次执行pyppeteer时，无法完成下载Chromium. 故提供下载所需Chromium文件, 并将其移动到下解压 (之后可删除压缩包).

**LInux (CentOS 7) 文件, /root/.local/share/...**

链接: https://pan.baidu.com/s/14yyKZfBsR_fPKGX5MLowVQ 提取码: qdap

**Windows 10 文件, C:\Users\你的用户名\AppData\Local\pyppeteer\pyppeteer\\local-chromium\575458\\...**

*<u>downloadLink 1</u>*

https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/575458/chrome-win32.zip

*<u>downloadLink 2</u>*

链接: https://pan.baidu.com/s/1QagNo8EE5IO0apYPJn80JQ 提取码: ek1n



**Note:** 如果不存放在指定文件夹内, 只要在launch里配置一下Chromium的路径即可 (注意Linux和Windows路径斜线不同). 示例: 

*<u>Win</u>*

```
'executablePath': 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', 
```

*<u>Linux</u>* 

```
'executablePath': '/root/home/chrome.exe',
```
