import os
import sys
from time import sleep
import paramiko
from PyQt5 import QtWidgets,  QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QDialog
from PyQt5.QtGui import QFont, QFontDatabase


class Load_Window(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setFixedSize(500, 250)
        fontId = QFontDatabase.addApplicationFont(
            "tgramer_source\\fs-gravity.ttf")
        self.fontName = QFontDatabase.applicationFontFamilies(fontId)[0]

        self.title = QLabel("TGRAMER", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(QFont(self.fontName, 30))
        self.title.resize(500, 30)
        self.title.move(0, 40)

        self.by_title = QLabel(self)
        self.by_title.setText("by THE INTERNET")
        self.by_title.setAlignment(QtCore.Qt.AlignCenter)
        self.by_title.setFont(QFont(self.fontName, 13))
        self.by_title.resize(500, 30)
        self.by_title.move(0, 70)

        self.info_title = QLabel("Обновляем программу...", self)
        self.info_title.setAlignment(QtCore.Qt.AlignCenter)
        self.info_title.setFont(QFont("Arial", 14))
        self.info_title.move(0, 140)
        self.info_title.setText("Проверяем обновления")
        self.info_title.resize(500, 30)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.show()

    def set_info_title(self, text):
        self.info_title.setText(text)

host = '185.246.66.186'
user = 'root'
secret = 'kD9aB4kT2ncH'
port = 22

app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('tgramer_source\\tg.ico'))
LoadWin = Load_Window()
app.processEvents()

def get_r_portable(sftp, remotedir, localdir):
    for entry in sftp.listdir_attr(remotedir):
        try:
            remotepath = remotedir + "/" + entry.filename
            localpath = os.path.join(localdir, entry.filename)
            sftp.get(remotepath, localpath)
            app.processEvents()
        except OSError:
            pass


try:
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=secret)
    sftp = paramiko.SFTPClient.from_transport(transport)
    remotepath = 'tgramer/version'
    localpath = 'tgramer_source\\update_log\\last version'
    sftp.get(remotepath, localpath)

    my_vers = open('tgramer_source\\update_log\\version', encoding='utf-8').read()
    last_vers = open('tgramer_source\\update_log\\last version',
                    encoding='utf-8').read()

    if my_vers != last_vers:
        print("Обновляем программу...")
        LoadWin.set_info_title("Обновляем программу...")
        app.processEvents()
        remotepath = 'tgramer/update text'
        localpath = 'tgramer_source\\update_log\\update text'
        sftp.get(remotepath, localpath)
        get_r_portable(sftp, "tgramer", "tgramer_source")
        with open('tgramer_source\\update_log\\version', "w", encoding='utf-8') as f:
            f.write(last_vers)
except:
    LoadWin.set_info_title("Ошибка обновления")
    sleep(2)

LoadWin.set_info_title("Запуск программы...")
app.processEvents()
sleep(1)
os.startfile('tgramer_source\\gui.exe')
# LoadWin.close()
# app.exec_()
# sys.exit()
