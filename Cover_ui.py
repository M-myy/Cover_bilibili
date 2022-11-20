from PySide2.QtWidgets import (QApplication,QMainWindow,
QPushButton,QPlainTextEdit,QMessageBox)
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from urllib.request import urlretrieve
from os import makedirs
from requests import get
from bs4 import BeautifulSoup
from threading import Thread

makedirs('./image/',exist_ok=True) #创建存储目录
# request_header http请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
}

class Window:
    def __init__(self):
        #从ui文件中加载UI定义
        qfile = QFile("UI/Cover.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)  # 可理解为 self.ui = QMainWindow()
        self.ui.button.clicked.connect(self.button_handle)

    def image_url(self,url):
        img_url_list = []
        video_url_list = url.split('\n')
        for tmp_url in video_url_list:
            response = get(tmp_url,headers=headers)
            response_all_page = BeautifulSoup(response.text,"lxml")
            response_img_div = response_all_page.find_all("meta",attrs={'itemprop':"image"})
            img_url = response_img_div[0].attrs.get("content")
            img_url_list.append(img_url)
        return img_url_list

    def load_img(self,url):
        try:
            for tmp_url in url:
                if tmp_url:
                    tmp_list = tmp_url.split('/')
                    urlretrieve(tmp_url,'./image/' + str(tmp_list[-1]))
        except:
            load_img(url)

    def button_handle(self):
        info = self.ui.text_edit.toPlainText()
        new_thread = Thread(target=self.button_entry,args=(info,))  #创建新线程,agrs=(info,)里面的逗号不能少代表info是一整个参数
        new_thread.start()

    def button_entry(self,info):
        if info:
            self.load_img(self.image_url(info))
            QMessageBox.about(self.ui,"提示","下载完成!")
        else:
            QMessageBox.about(self.ui,"提示","非法输入!")

app = QApplication([])
box = Window()
box.ui.show()
app.exec_()
