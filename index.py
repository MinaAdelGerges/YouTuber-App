from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import os
from os import path
import sys
import pafy
import humanize
import urllib.request



FROM_CLASS,_ =  loadUiType(path.join(path.dirname(__file__),'Downloader.ui'))

class Downloader(QMainWindow ,FROM_CLASS):
    def __init__(self,parent=None):
        super(Downloader,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Ui()
        self.Handel_Buttons()
    def Handel_Ui(self):
        self.setWindowTitle('PyDownloader')
        self.setFixedSize(640,480)
        # self.setWindowIcon(QIcon('Downloader.png'))
    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        self.pushButton_9.clicked.connect(self.Get_Youtube_Video)
        self.pushButton_3.clicked.connect(self.Download_Youtube_Video)
        self.pushButton_7.clicked.connect(self.Save_Browse)
        self.pushButton_5.clicked.connect(self.Playlist_Download)
        self.pushButton_8.clicked.connect(self.Save_Browse)
    def Handel_Browse(self):
        save_place = QFileDialog.getSaveFileName(self,caption='Save As',directory='.',filter='All Files (*.*)')
        text = str(save_place)
        name = text[2:].split(',')[0].replace("'",'')
        self.lineEdit_2.setText(name)
    def Handel_Progress(self,blocknum,blocksize,totalsize):
        read = blocknum * blocksize
        if totalsize > 0 :
            percent =  read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()
    def Download(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url,save_location,self.Handel_Progress)
        except Exception:
            QMessageBox.Warning(self,'Download error','The Download failed')
            return
        QMessageBox.information(self,'Download Completed','The Download Finished')
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
    def Save_Browse(self):
        save = QFileDialog.getExistingDirectory(self,'Select Download Directory')
        self.lineEdit_3.setText(save)
        self.lineEdit_5.setText(save)
    def Get_Youtube_Video(self):
        # print(Video.title)
        # print(Video.duration)
        # print(Video.rating)
        # print(Video.author)
        # print(Video.length)
        # print(Video.keywords)
        # print(Video.thumb)
        # print(Video.videoid)
        # print(Video.viewcount)
        Video_Url = self.lineEdit_4.text()
        Video = pafy.new(Video_Url)
        st = Video.allstreams
        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data ='{} {} {} {}' .format(s.mediatype , s.extension , s.quality , size)
            self.comboBox.addItem(data)
    def Download_Youtube_Video(self):
        try:
            Video_Url = self.lineEdit_4.text()
            save_location = self.lineEdit_3.text()
            Video = pafy.new(Video_Url)
            st = Video.allstreams
            quality = self.comboBox.currentIndex()
            download = st[quality].download(filepath=save_location)
        except Exception:
            QMessageBox.Warning(self, 'Download error', 'The Download failed')
            return
        QMessageBox.information(self, 'Download Completed', 'The Download Finished')
    def Playlist_Download(self):
        Playlist_Url = self.lineEdit_6.text()
        Save_Location = self.lineEdit_5.text()
        Playlist = pafy.get_playlist(Playlist_Url)
        Videos = Playlist['items']
        os.chdir(Save_Location)
        if os.path.exists(str(Playlist['title'])):
            os.chdir(str(Playlist['title']))
        else:
            os.mkdir(str(Playlist['title']))
            os.chdir(str(Playlist['title']))
        for video in Videos:
            p = video['pafy']
            best = p.getbest(preftype='mp4')
            best.download()
        """
        for video in videos:
            p = video['pavy'] 
            QApplication.processEvents()
            best = p.getbest(preftype='mp4')
            allstreams = p.allstreams
            for s in allstreams:
                size = humanise.naturalsize(s.get_filesize(), binary = True)
                data = '{} {} {} {}'.format(s.mediatype, s.extension, s.quality, size) 
                self.comboBox_2.addItem(data)
                down = allstreams[quality].download(filepath=Save_Location,quiet = False)   
        """

def main():
    app = QApplication(sys.argv)
    window = Downloader()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()

