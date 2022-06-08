import sys
import asyncio
from time import sleep
from PyQt5 import QtWidgets,  QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout,QWidget, QScrollArea, QFileDialog, QMainWindow, QLabel, QPushButton, QListWidget, QLineEdit, QCheckBox, QComboBox, QTextEdit, QMessageBox, QDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QCursor

import parser_script
import inviter_script
import mailing_script
from license_script import auth

class EnterCodeDialog(QMainWindow):
    def __init__(self,) -> None:
        super().__init__()
        self.setFixedSize(600, 400)
        self.wrong_label = QLabel(self)
        self.wrong_label.setText("<b>Неверный ключ активации!</b>")
        self.wrong_label.setFont(QFont("Arial", 15))
        self.wrong_label.setAlignment(Qt.AlignCenter)
        self.wrong_label.move(135, 120)
        self.wrong_label.resize(350, 30)

        self.enter_label = QLabel(self)
        self.enter_label.setText("<b>Введите ключ активации</b>")
        self.enter_label.setFont(QFont("Arial", 15))
        self.enter_label.setAlignment(Qt.AlignCenter)
        self.enter_label.move(135, 160)
        self.enter_label.resize(350, 30)

        self.enter_key_label = QLineEdit(self)
        self.enter_key_label.resize(350, 30)
        self.enter_key_label.setFont(QFont("Arial", 11))
        self.enter_key_label.move(135, 200)

        self.enter_but = QPushButton(self)
        self.enter_but.setStyleSheet('''
        QPushButton {color: white;
                    background-color: #323232;
                    border: 1px solid rgb(40, 40, 40);
                    border-radius: 10px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 10px;
                                        }''')
        self.enter_but.setFont(QFont("Arial", 15))
        self.enter_but.setText("Enter")
        self.enter_but.resize(150, 40)
        self.enter_but.move(230, 250)
        self.enter_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                             blurRadius=100.0,
                                                                             color=QtGui.QColor(
                                                                                 40, 40, 40),
                                                                             offset=QtCore.QPointF(10.0, 10.0)))

        self.enter_but.clicked.connect(self.return_key)
        self.enter_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    
    def return_key(self):
        with open("key.txt", "w") as f:
            f.write(self.enter_key_label.text())
        self.close()

        


class ScrollLabel(QScrollArea):
 
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
 
        # making qwidget object
        self.setWidgetResizable(True)
 
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
 
        # vertical box layout
        lay = QVBoxLayout(content)
 
        # creating label
        self.label = QLabel(content)
        self.label.setFont(QFont("Arial", 14))
 
        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
 
        # making label multi-line
        self.label.setWordWrap(True)
 
        # adding label to the layout
        lay.addWidget(self.label)
 
    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)


class PicClick(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit()


class EnterCodeDialog_pars(QDialog):
    def __init__(self, client, window, phone):
        QDialog.__init__(self)
        self.client = client
        self.window = window
        self.phone = phone

        self.setFixedSize(500, 250)

        self.setWindowTitle("Enter code")

        self.title = QLabel("Введите отправленный код", self)
        self.title.setFont(QFont("Arial", 12))
        self.title.move(0, 40)
        self.title.resize(500, 30)
        self.title.setAlignment(Qt.AlignCenter)

        self.phone_title = QLabel(self.phone, self)
        self.phone_title.setFont(QFont("Arial", 13))
        self.phone_title.move(60, 100)

        self.code_zone = QLineEdit(self)
        self.code_zone.setFont(QFont("Arial", 13))
        self.code_zone.move(210, 100)
        self.code_zone.setStyleSheet('''
        QLineEdit {border: 2px solid #323232;
                                        }''')
        self.code_zone.resize(190, 25)

        self.enter_but = QPushButton(self)
        self.enter_but.setStyleSheet('''
        QPushButton {color: white;
                    background-color: #323232;
                    border: 1px solid rgb(40, 40, 40);
                    border-radius: 10px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 10px;
                                        }''')
        self.enter_but.setFont(QFont("Arial", 15))
        self.enter_but.setText("Enter")
        self.enter_but.resize(150, 40)
        self.enter_but.move(175, 160)
        self.enter_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                             blurRadius=100.0,
                                                                             color=QtGui.QColor(
                                                                                 40, 40, 40),
                                                                             offset=QtCore.QPointF(10.0, 10.0)))

        self.enter_but.clicked.connect(self.return_code)
        self.enter_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        print("here")

        self.exec_()

    def return_code(self):
        self.close()
        parser_script.client_sign_in(
            self.code_zone.text(), self.client, self.window, self.phone)


class EnterCodeDialog_inv(QDialog):
    def __init__(self, client, window, phone):
        QDialog.__init__(self)

        self.client = client
        self.window = window
        self.phone = phone

        self.setFixedSize(500, 250)

        self.setWindowTitle("Enter code")

        self.title = QLabel("Введите отправленный код", self)
        self.title.setFont(QFont("Arial", 12))
        self.title.move(0, 40)
        self.title.resize(500, 30)
        self.title.setAlignment(Qt.AlignCenter)

        self.phone_title = QLabel(self.phone, self)
        self.phone_title.setFont(QFont("Arial", 13))
        self.phone_title.move(60, 100)

        self.code_zone = QLineEdit(self)
        self.code_zone.setFont(QFont("Arial", 13))
        self.code_zone.move(210, 100)
        self.code_zone.setStyleSheet('''
        QLineEdit {border: 2px solid #323232;
                                        }''')
        self.code_zone.resize(190, 25)

        self.enter_but = QPushButton(self)
        self.enter_but.setStyleSheet('''
        QPushButton {color: white;
                    background-color: #323232;
                    border: 1px solid rgb(40, 40, 40);
                    border-radius: 10px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 10px;
                                        }''')
        self.enter_but.setFont(QFont("Arial", 15))
        self.enter_but.setText("Enter")
        self.enter_but.resize(150, 40)
        self.enter_but.move(175, 160)
        self.enter_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                             blurRadius=100.0,
                                                                             color=QtGui.QColor(
                                                                                 40, 40, 40),
                                                                             offset=QtCore.QPointF(10.0, 10.0)))

        self.enter_but.clicked.connect(self.return_code)
        self.enter_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        print("here")

        self.exec_()
        app.processEvents()

    def return_code(self):
        self.close()
        inviter_script.client_sign_in(
            self.code_zone.text(), self.client, self.window, self.phone)


class EnterCodeDialog_mail(QDialog):
    def __init__(self, client, window, phone):
        QDialog.__init__(self)

        self.client = client
        self.window = window
        self.phone = phone

        self.setFixedSize(500, 250)

        self.setWindowTitle("Enter code")

        self.title = QLabel("Введите отправленный код", self)
        self.title.setFont(QFont("Arial", 12))
        self.title.move(0, 40)
        self.title.resize(500, 30)
        self.title.setAlignment(Qt.AlignCenter)

        self.phone_title = QLabel(self.phone, self)
        self.phone_title.setFont(QFont("Arial", 13))
        self.phone_title.move(60, 100)

        self.code_zone = QLineEdit(self)
        self.code_zone.setFont(QFont("Arial", 13))
        self.code_zone.move(210, 100)
        self.code_zone.setStyleSheet('''
        QLineEdit {border: 2px solid #323232;
                                        }''')
        self.code_zone.resize(190, 25)

        self.enter_but = QPushButton(self)
        self.enter_but.setStyleSheet('''
        QPushButton {color: white;
                    background-color: #323232;
                    border: 1px solid rgb(40, 40, 40);
                    border-radius: 10px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 10px;
                                        }''')
        self.enter_but.setFont(QFont("Arial", 15))
        self.enter_but.setText("Enter")
        self.enter_but.resize(150, 40)
        self.enter_but.move(175, 160)
        self.enter_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                             blurRadius=100.0,
                                                                             color=QtGui.QColor(
                                                                                 40, 40, 40),
                                                                             offset=QtCore.QPointF(10.0, 10.0)))

        self.enter_but.clicked.connect(self.return_code)
        self.enter_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        print("here")

        self.exec_()
        app.processEvents()

    def return_code(self):
        self.close()
        mailing_script.client_sign_in(
            self.code_zone.text(), self.client, self.window, self.phone)


class MainWindow(QMainWindow):
    def __init__(self,) -> None:
        super().__init__()

        self.procpars = 1

        parser_script.signals.code_request.connect(
            lambda x: self.enter_code_dialog_pars(x[0], x[1], x[2]))

        inviter_script.signals.code_request.connect(
            lambda x: self.enter_code_dialog_inv(x[0], x[1], x[2]))

        mailing_script.signals.code_request.connect(
            lambda x: self.enter_code_dialog_mail(x[0], x[1], x[2]))

        fontId = QFontDatabase.addApplicationFont(
            "tgramer_source\\fs-gravity.ttf")
        self.fontName = QFontDatabase.applicationFontFamilies(fontId)[0]

        self.back_but = QPushButton(self)
        self.back_but.setStyleSheet('''
        QPushButton {color: white;
                    background-color: #323232;
                    border: 1px solid rgb(40, 40, 40);
                    border-radius: 10px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 10px;
                                        }''')
        self.back_but.setFont(QFont("Arial", 15))
        self.back_but.setText("Назад")
        self.back_but.resize(150, 40)
        self.back_but.move(20, 50)
        self.back_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                            blurRadius=100.0,
                                                                            color=QtGui.QColor(
                                                                                40, 40, 40),
                                                                            offset=QtCore.QPointF(10.0, 10.0)))

        self.back_but.clicked.connect(self.main_start)
        self.back_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.back_but.hide()

        self.setFixedSize(1152, 648)
        self.setWindowTitle("TGRAMER")

        self.setStyleSheet('''
        QMainWindow {background-color: #949494}
        '''
                           )

        self.main_title = QLabel(self)
        self.main_title.setText("TGRAMER")
        self.main_title.setStyleSheet('''
        QLabel {color: white;
                                        }''')
        self.main_title.setAlignment(Qt.AlignCenter)
        self.main_title.resize(400, 100)
        self.main_title.setFont(QFont(self.fontName, 45))
        self.main_title.move(370, 10)
        self.main_title.hide()

        self.by_title = QLabel(self)
        self.by_title.setText("by THE INTERNET")
        self.by_title.setStyleSheet('''
        QLabel {color: white;
                                        }''')
        self.by_title.setAlignment(Qt.AlignCenter)
        self.by_title.resize(400, 60)
        self.by_title.setFont(QFont(self.fontName, 20))
        self.by_title.move(370, 70)
        self.by_title.hide()

        self.pars_but = QPushButton(self)
        self.pars_but.setText("\n\n\n\nПарсинг")
        self.pars_but.resize(300, 300)
        self.pars_but.setFont(QFont("Arial", 21))
        self.pars_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                            blurRadius=100.0,
                                                                            color=QtGui.QColor(
                                                                                40, 40, 40),
                                                                            offset=QtCore.QPointF(10.0, 10.0)))

        self.pars_but.setStyleSheet('''
        QPushButton {background-color: #323232;
                    color: white;
                    text-align: bottom;
                    border-radius: 20px;
                                        }
        QPushButton:hover {background-color: #464646;
                    color: white;
                    text-align: bottom;
                    border-radius: 20px;
                                        }''')

        self.pars_but.move(70, 160)
        self.pars_but.clicked.connect(self.pars_window)
        self.pars_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pars_but.hide()

        self.pars_pic = PicClick(self)
        self.pars_pic.setPixmap(QPixmap('tgramer_source\\pars.png'))
        self.pars_pic.resize(110, 145)
        self.pars_pic.move(165, 199)
        self.pars_pic.clicked.connect(self.pars_window)
        self.pars_pic.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pars_pic.hide()

        self.inv_but = QPushButton(self)
        self.inv_but.setText("\n\n\n\nИнвайтинг")
        # self.pars_but.setAlignment(Qt.AlignCenter)
        self.inv_but.resize(300, 300)
        self.inv_but.setFont(QFont("Arial", 21))
        self.inv_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                           blurRadius=100.0,
                                                                           color=QtGui.QColor(
                                                                               40, 40, 40),
                                                                           offset=QtCore.QPointF(10.0, 10.0)))

        self.inv_but.setStyleSheet('''
        QPushButton {background-color: #323232;
                    color: white;
                    border-radius: 20px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 20px;
                                        }''')
        self.inv_but.move(420, 160)
        self.inv_but.clicked.connect(self.inv_window)
        self.inv_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.inv_but.hide()

        self.inv_pic = PicClick(self)
        self.inv_pic.setPixmap(QPixmap('tgramer_source\\inv.png'))
        self.inv_pic.resize(150, 150)
        self.inv_pic.move(500, 199)
        self.inv_pic.clicked.connect(self.inv_window)
        self.inv_pic.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.inv_pic.hide()

        self.mail_but = QPushButton(self)
        self.mail_but.setText("\n\n\n\nРассылка")
        self.mail_but.resize(300, 300)
        self.mail_but.setFont(QFont("Arial", 21))
        self.mail_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                            blurRadius=100.0,
                                                                            color=QtGui.QColor(
                                                                                40, 40, 40),
                                                                            offset=QtCore.QPointF(10.0, 10.0)))

        self.mail_but.setStyleSheet('''
        QPushButton {background-color: #323232;
                    color: white;
                    border-radius: 20px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 20px;
                                        }''')
        self.mail_but.move(770, 160)
        self.mail_but.clicked.connect(self.mail_window)
        self.mail_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.mail_but.hide()

        self.mail_pic = PicClick(self)
        self.mail_pic.setPixmap(QPixmap('tgramer_source\\mail.png'))
        self.mail_pic.clicked.connect(self.mail_window)
        self.mail_pic.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.mail_pic.resize(150, 150)
        self.mail_pic.move(845, 199)
        self.mail_pic.hide()

        self.instr_button = QPushButton(self)
        self.instr_button.setText("Инструкция")
        self.instr_button.resize(300, 90)
        self.instr_button.setFont(QFont("Arial", 20))
        self.instr_button.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                                blurRadius=100.0,
                                                                                color=QtGui.QColor(
                                                                                    40, 40, 40),
                                                                                offset=QtCore.QPointF(10.0, 10.0)))

        self.instr_button.setStyleSheet('''
        QPushButton {background-color: #323232;
                    color: white;
                    border-radius: 20px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 20px;
                                        }''')

        self.instr_button.move(20, 525)
        self.instr_button.clicked.connect(self.view_instruction)
        self.instr_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.instr_button.hide()

        self.channel_text = QLabel(self)
        self.channel_text.setText("Канал Telegram:")
        self.channel_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.channel_text.setAlignment(Qt.AlignCenter)
        self.channel_text.resize(400, 60)
        self.channel_text.setFont(QFont("Arial", 18))
        self.channel_text.move(750, 525)
        self.channel_text.hide()

        self.channel_link = QLabel(self)
        self.channel_link.setText(
            '<a href="https://t.me/the_internetgroup">@the_internetgroup</a>')
        self.channel_link.setOpenExternalLinks(True)
        # self.channel_link.setStyleSheet('''
        # a.text {text-decoration: none;
        # color: #323232;}''')
        self.channel_link.setAlignment(Qt.AlignCenter)
        self.channel_link.resize(400, 60)
        self.channel_link.setFont(QFont("Arial", 18))
        self.channel_link.move(750, 565)
        self.channel_link.hide()

        self.log_win = QListWidget(self)
        self.log_win.setFont(QFont("Arial", 10))
        self.log_win.resize(400, 300)
        self.log_win.setStyleSheet('''
        QListWidget {border: 2px solid #323232;
                                        }''')
        self.log_win.move(700, 175)
        self.log_win.hide()

        self.log_title = QLabel(self)
        self.log_title.setFont(QFont("Arial", 15))
        self.log_title.setStyleSheet('''
        QLabel {color: white;}''')
        self.log_title.resize(400, 20)
        self.log_title.setText("Логи")
        self.log_title.move(700, 145)
        self.log_title.hide()

        self.group_link_text = QLabel(self)
        self.group_link_text.setText("Ссылка на группу")
        self.group_link_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.group_link_text.resize(400, 40)
        self.group_link_text.setAlignment(Qt.AlignCenter)
        self.group_link_text.setFont(QFont("Arial", 15))
        self.group_link_text.move(370, 145)
        self.group_link_text.hide()

        self.group_link_zone = QLineEdit(self)
        self.group_link_zone.setFont(QFont("Arial", 13))
        self.group_link_zone.move(370, 175)
        self.group_link_zone.setStyleSheet('''
        QLineEdit {border: 2px solid #323232;
                                        }''')
        self.group_link_zone.resize(400, 30)
        self.group_link_zone.hide()

        self.group_add_text = QLabel(self)
        self.group_add_text.setText("Сколько добавить всего")
        self.group_add_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.group_add_text.resize(400, 40)
        self.group_add_text.setAlignment(Qt.AlignLeft)
        self.group_add_text.setFont(QFont("Arial", 15))
        self.group_add_text.move(180, 235)
        self.group_add_text.hide()

        self.group_add_zone = QLineEdit(self)
        self.group_add_zone.setFont(QFont("Arial", 13))
        self.group_add_zone.move(180, 265)
        self.group_add_zone.setStyleSheet('''
        QLineEdit {border: 2px solid #323232;
                                        }''')
        self.group_add_zone.resize(400, 30)
        self.group_add_zone.hide()

        self.group_each_text = QLabel(self)
        self.group_each_text.setText("Сколько добавить c каждого")
        self.group_each_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.group_each_text.resize(400, 40)
        self.group_each_text.setAlignment(Qt.AlignLeft)
        self.group_each_text.setFont(QFont("Arial", 15))
        self.group_each_text.move(180, 325)
        self.group_each_text.hide()

        self.group_each_zone = QLineEdit(self)
        self.group_each_zone.setFont(QFont("Arial", 13))
        self.group_each_zone.move(180, 355)
        self.group_each_zone.setStyleSheet('''
        QLineEdit {border: 2px solid #323232;
                                        }''')
        self.group_each_zone.resize(400, 30)
        self.group_each_zone.hide()

        self.group_pausemin_text = QLabel(self)
        self.group_pausemin_text.setText("Мин. пауза")
        self.group_pausemin_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.group_pausemin_text.resize(150, 40)
        self.group_pausemin_text.setAlignment(Qt.AlignLeft)
        self.group_pausemin_text.setFont(QFont("Arial", 15))
        self.group_pausemin_text.move(180, 415)
        self.group_pausemin_text.hide()

        self.group_pausemin_zone = QLineEdit(self)
        self.group_pausemin_zone.setFont(QFont("Arial", 13))
        self.group_pausemin_zone.move(180, 445)
        self.group_pausemin_zone.setStyleSheet('''
        QLineEdit {border: 2px solid #323232;
                                        }''')
        self.group_pausemin_zone.resize(150, 30)
        self.group_pausemin_zone.hide()

        self.group_pausemax_text = QLabel(self)
        self.group_pausemax_text.setText("Макс. пауза")
        self.group_pausemax_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.group_pausemax_text.resize(150, 40)
        self.group_pausemax_text.setAlignment(Qt.AlignLeft)
        self.group_pausemax_text.setFont(QFont("Arial", 15))
        self.group_pausemax_text.move(430, 415)
        self.group_pausemax_text.hide()

        self.group_pausemax_zone = QLineEdit(self)
        self.group_pausemax_zone.setFont(QFont("Arial", 13))
        self.group_pausemax_zone.move(430, 445)
        self.group_pausemax_zone.setStyleSheet('''
        QLineEdit {border: 2px solid #323232;
                                        }''')
        self.group_pausemax_zone.resize(150, 30)
        self.group_pausemax_zone.hide()

        self.start_but = QPushButton(self)
        self.start_but.setText("Запуск")
        self.start_but.resize(200, 60)
        self.start_but.setFont(QFont("Arial", 20))
        self.start_but.setStyleSheet('''
        QPushButton {background-color: #323232;
                    color: white;
                    border-radius: 10px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 10px;
                                        }''')
        self.procpars_title = QLabel(self)
        self.procpars_title.setText("Выполняется парсинг...")
        self.procpars_title.setStyleSheet('''
        QLabel {color: white;}''')
        self.procpars_title.resize(1152, 40)
        self.procpars_title.setAlignment(Qt.AlignCenter)
        self.procpars_title.setFont(QFont("Arial", 15))
        self.procpars_title.move(0, 470)
        self.procpars_title.hide()

        self.start_but.move(470, 550)
        self.start_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                             blurRadius=100.0,
                                                                             color=QtGui.QColor(
                                                                                 40, 40, 40),
                                                                             offset=QtCore.QPointF(10.0, 10.0)))

        self.start_but.clicked.connect(lambda: self.start_working("inv"))
        self.start_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.start_but.hide()

        self.check_memb = QCheckBox(self)
        self.check_memb.setChecked(True)
        self.check_memb.move(510, 240)
        self.check_memb.resize(28, 27)
        self.check_memb.setStyleSheet('''
            QCheckBox {
                                        }

            QCheckBox::indicator {
            width: 20px;
            height: 20px;}
        ''')
        self.check_memb.hide()

        self.check_memb_text = QLabel(self)
        self.check_memb_text.setText("Участники")
        self.check_memb_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.check_memb_text.resize(150, 40)
        self.check_memb_text.setFont(QFont("Arial", 15))
        self.check_memb_text.move(370, 230)
        self.check_memb_text.hide()

        self.check_amd = QCheckBox(self)
        self.check_amd.setChecked(True)
        self.check_amd.move(510, 290)
        self.check_amd.resize(28, 27)
        self.check_amd.setStyleSheet('''
            QCheckBox {
                                        }

            QCheckBox::indicator {
            width: 20px;
            height: 20px;}
        ''')
        self.check_amd.hide()

        self.check_adm_text = QLabel(self)
        self.check_adm_text.setText("Админы")
        self.check_adm_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.check_adm_text.resize(150, 40)
        self.check_adm_text.setFont(QFont("Arial", 15))
        self.check_adm_text.move(370, 280)
        self.check_adm_text.hide()

        self.check_photo = QCheckBox(self)
        self.check_photo.move(780, 240)
        self.check_photo.resize(28, 27)
        self.check_photo.setStyleSheet('''
            QCheckBox {
                                        }

            QCheckBox::indicator {
            width: 20px;
            height: 20px;}
        ''')
        self.check_photo.hide()

        self.check_photo_text = QLabel(self)
        self.check_photo_text.setText("С фото профиля")
        self.check_photo_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.check_photo_text.resize(210, 40)
        self.check_photo_text.setFont(QFont("Arial", 15))
        self.check_photo_text.move(560, 230)
        self.check_photo_text.hide()

        self.check_chatting = QCheckBox(self)
        self.check_chatting.move(780, 290)
        self.check_chatting.resize(28, 27)
        self.check_chatting.setStyleSheet('''
            QCheckBox {                 }

            QCheckBox::indicator {
            width: 20px;
            height: 20px;}
        ''')
        self.check_chatting.hide()

        self.check_chatting_text = QLabel(self)
        self.check_chatting_text.setText("Писали в чат")
        self.check_chatting_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.check_chatting_text.resize(190, 40)
        self.check_chatting_text.setFont(QFont("Arial", 15))
        self.check_chatting_text.move(560, 280)
        self.check_chatting_text.hide()

        self.active = QComboBox(self)
        self.active.resize(140, 30)
        self.active.setFont(QFont("Arial", 10))
        self.active.setStyleSheet('''
        QComboBox {border: 2px solid #323232;
                                        };
        ''')
        self.active.addItem("Все")
        self.active.addItem("1 час")
        self.active.addItem("3 часа")
        self.active.addItem("1 день")
        self.active.addItem("3 дня")
        self.active.addItem("1 неделя")
        self.active.addItem("Онлайн")
        self.active.move(500, 400)
        self.active.hide()

        self.active_text = QLabel(self)
        self.active_text.setText("Активность")
        self.active_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.active_text.setAlignment(Qt.AlignCenter)
        self.active_text.resize(400, 30)
        self.active_text.setFont(QFont("Arial", 15))
        self.active_text.move(370, 350)
        self.active_text.hide()

        self.mes_zone = QTextEdit(self)
        self.mes_zone.setStyleSheet(
            '''QTextEdit { border: 2px solid #323232; }''')
        self.mes_zone.move(50, 175)
        self.mes_zone.resize(480, 150)
        self.mes_zone.hide()

        self.mes_title = QLabel(self)
        self.mes_title.setText("Сообщение")
        self.mes_title.setStyleSheet('''
        QLabel {color: white;}''')
        self.mes_title.resize(200, 30)
        self.mes_title.setFont(QFont("Arial", 15))
        self.mes_title.move(50, 145)
        self.mes_title.hide()

        self.mes_total_text = QLabel(self)
        self.mes_total_text.setText("Сколько отправить всего")
        self.mes_total_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.mes_total_text.resize(300, 30)
        self.mes_total_text.setFont(QFont("Arial", 15))
        self.mes_total_text.move(50, 340)
        self.mes_total_text.hide()

        self.mes_total = QLineEdit(self)
        self.mes_total.setFont(QFont("Arial", 10))
        self.mes_total.move(50, 370)
        self.mes_total.setStyleSheet(
            '''QLineEdit { border: 2px solid #323232; }''')
        self.mes_total.resize(520, 30)
        self.mes_total.hide()

        self.mes_each_text = QLabel(self)
        self.mes_each_text.setText("Сколько отправить с каждого аккаунта")
        self.mes_each_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.mes_each_text.resize(500, 30)
        self.mes_each_text.setFont(QFont("Arial", 15))
        self.mes_each_text.move(50, 410)
        self.mes_each_text.hide()

        self.mes_each = QLineEdit(self)
        self.mes_each.setFont(QFont("Arial", 10))
        self.mes_each.setStyleSheet(
            '''QLineEdit { border: 2px solid #323232; }''')
        self.mes_each.move(50, 445)
        self.mes_each.resize(520, 30)
        self.mes_each.hide()

        self.mes_pause_text = QLabel(self)
        self.mes_pause_text.setText("Задержка")
        self.mes_pause_text.setStyleSheet('''
        QLabel {color: white;}''')
        self.mes_pause_text.resize(200, 30)
        self.mes_pause_text.setFont(QFont("Arial", 15))
        self.mes_pause_text.move(50, 485)
        self.mes_pause_text.hide()

        self.mes_pause = QLineEdit(self)
        self.mes_pause.setFont(QFont("Arial", 10))
        self.mes_pause.setStyleSheet(
            '''QLineEdit { border: 2px solid #323232; }''')
        self.mes_pause.move(50, 515)
        self.mes_pause.resize(200, 30)
        self.mes_pause.hide()

        self.file_but = QPushButton(self)
        self.file_but.setStyleSheet('''
        QPushButton {color: white;
                    background-color: #323232;
                    border-radius: 10px;}
        QPushButton:hover {background-color: #464646;
                    color: white;
                    border-radius: 10px;
                                        }''')
        self.file_but.setFont(QFont("Arial", 10))
        self.file_but.setText("Файл")
        self.file_but.resize(80, 40)
        self.file_but.move(535, 280)
        self.file_but.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,
                                                                            blurRadius=100.0,
                                                                            color=QtGui.QColor(
                                                                                40, 40, 40),
                                                                            offset=QtCore.QPointF(5.0, 5.0)))

        self.file_but.clicked.connect(self.get_file)
        self.file_but.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.file_but.hide()

        self.file_to_send = ""

        self.wind_title = QLabel(self)
        self.wind_title.setText("Парсинг")
        self.wind_title.setStyleSheet('''
        QLabel {color: white;}''')
        self.wind_title.setAlignment(Qt.AlignCenter)
        self.wind_title.resize(400, 60)
        self.wind_title.setFont(QFont("Arial", 25))
        self.wind_title.move(370, 50)
        self.wind_title.hide()

        with open("tgramer_source\\update_log\\update text", "r", encoding='utf-8') as f:
            i = 0
            self.update_text = ""
            self.fl_stop = False
            for line in f:
                if i == 0:
                    if not int(line):
                        self.fl_stop = True
                        break
                    i = 1
                    continue
                self.update_text += line
            self.now_version = open(
                "tgramer_source\\update_log\\last version").read()
        with open("tgramer_source\\update_log\\update text", "w", encoding='utf-8') as f:
            f.write("0\n"+self.update_text)

        self.main_start()

    def main_start(self):
        self.file_to_send = ""

        self.main_title.show()
        self.by_title.show()
        self.pars_but.show()
        self.pars_pic.show()
        self.inv_but.show()
        self.inv_pic.show()
        self.mail_but.show()
        self.mail_pic.show()
        self.instr_button.show()
        self.channel_text.show()
        self.channel_link.show()

        self.start_but.hide()
        self.back_but.hide()
        self.wind_title.hide()
        self.group_link_text.hide()
        self.group_link_zone.hide()
        self.check_memb_text.hide()
        self.check_memb.hide()
        self.check_amd.hide()
        self.check_adm_text.hide()
        self.check_photo.hide()
        self.check_photo_text.hide()
        self.check_chatting_text.hide()
        self.check_chatting.hide()
        self.active.hide()
        self.active_text.hide()

        self.group_add_zone.hide()
        self.group_add_text.hide()
        self.group_each_text.hide()
        self.group_each_zone.hide()
        self.group_pausemin_text.hide()
        self.group_pausemin_zone.hide()
        self.group_pausemax_text.hide()
        self.group_pausemax_zone.hide()

        self.log_win.hide()
        self.log_title.hide()

        self.mes_title.hide()
        self.mes_zone.hide()
        self.file_but.hide()
        self.mes_total.hide()
        self.mes_total_text.hide()
        self.mes_each.hide()
        self.mes_each_text.hide()
        self.mes_pause_text.hide()
        self.mes_pause.hide()

        if not self.fl_stop:
            QMessageBox.about(self, "Информация об обновлении",
                              f"Новое обновление! Версия {self.now_version}\n\n{self.update_text}")
            self.fl_stop = True

    def pars_window(self):
        self.pars_but.hide()
        self.pars_pic.hide()
        self.inv_but.hide()
        self.inv_pic.hide()
        self.mail_but.hide()
        self.mail_pic.hide()
        self.main_title.hide()
        self.by_title.hide()
        self.instr_button.hide()
        self.channel_text.hide()
        self.channel_link.hide()

        self.back_but.show()
        self.start_but.clicked.disconnect()
        self.start_but.clicked.connect(
            lambda: self.start_working("start parsing"))
        self.start_but.show()

        self.wind_title.setText("Парсинг")
        self.wind_title.show()

        self.group_link_text.setAlignment(Qt.AlignCenter)
        self.group_link_text.move(370, 135)
        self.group_link_text.show()

        self.group_link_zone.move(370, 175)
        self.group_link_zone.show()

        self.check_memb_text.show()
        self.check_memb.show()
        self.check_amd.show()
        self.check_adm_text.show()
        self.check_photo.show()
        self.check_photo_text.show()
        self.check_chatting_text.show()
        self.check_chatting.show()
        self.active.show()
        self.active_text.show()

    def inv_window(self):
        self.pars_but.hide()
        self.pars_pic.hide()
        self.inv_but.hide()
        self.inv_pic.hide()
        self.mail_but.hide()
        self.mail_pic.hide()
        self.main_title.hide()
        self.by_title.hide()
        self.instr_button.hide()
        self.channel_text.hide()
        self.channel_link.hide()

        self.back_but.show()
        self.start_but.clicked.disconnect()
        self.clear_logs()
        self.start_but.clicked.connect(
            lambda: self.start_working("start inviting"))
        self.start_but.show()

        self.wind_title.setText("Инвайтинг")
        self.wind_title.show()

        self.group_link_text.setAlignment(Qt.AlignLeft)
        self.group_link_text.move(180, 145)
        self.group_link_text.show()

        self.group_link_zone.move(180, 175)
        self.group_link_zone.show()

        self.group_add_text.show()
        self.group_add_zone.show()
        self.group_each_text.show()
        self.group_each_zone.show()
        self.group_pausemin_text.show()
        self.group_pausemin_zone.show()
        self.group_pausemax_text.show()
        self.group_pausemax_zone.show()

        self.log_win.show()
        self.log_title.show()

    def mail_window(self):
        self.pars_but.hide()
        self.pars_pic.hide()
        self.inv_but.hide()
        self.inv_pic.hide()
        self.mail_but.hide()
        self.mail_pic.hide()
        self.main_title.hide()
        self.by_title.hide()
        self.instr_button.hide()
        self.channel_text.hide()
        self.channel_link.hide()

        self.back_but.show()
        self.start_but.clicked.disconnect()
        self.clear_logs()
        self.start_but.clicked.connect(
            lambda: self.start_working("start mailing"))
        self.start_but.show()

        self.wind_title.setText("Рассылка")
        self.wind_title.show()

        self.mes_title.show()
        self.mes_zone.show()
        self.log_win.show()
        self.log_title.show()
        self.file_but.show()
        self.mes_total.show()
        self.mes_total_text.show()
        self.mes_each.show()
        self.mes_each_text.show()
        self.mes_pause_text.show()
        self.mes_pause.show()

    def start_working(self, param):
        print(param)
        self.add_log_inform(param)
        if param == "start parsing":
            parser_script.parsing(self)
        elif param == "start inviting":
            inviter_script.start_inviting(self)
        elif param == "start mailing":
            mailing_script.start_mailing(self)

    def add_log_inform(self, log: str):
        self.log_win.addItem(f"[+] {log}")
        self.log_win.scrollToBottom()
        app.processEvents()

    def add_log_warn(self, log: str):
        self.log_win.addItem(f"[!] {log}")
        self.log_win.scrollToBottom()
        app.processEvents()

    def clear_logs(self):
        self.log_win.clear()
        app.processEvents()

    def enter_code_dialog_pars(self, client, window, phone):
        code_dialog = EnterCodeDialog_pars(client, window, phone)

    def enter_code_dialog_inv(self, client, window, phone):
        code_dialog = EnterCodeDialog_inv(client, window, phone)
        if not code_dialog.code_zone.text():
            inviter_script.signals.next_client = True

    def enter_code_dialog_mail(self, client, window, phone):
        code_dialog = EnterCodeDialog_mail(client, window, phone)
        if not code_dialog.code_zone.text():
            mailing_script.signals.next_client = True

    def process_parsing(self):
        self.procpars_title.setText("Выполняется парсинг"+"."*self.procpars)
        self.procpars_title.show()
        app.processEvents()
        self.procpars = max((self.procpars + 1)%4, 1)

    def end_parsing(self):
        self.procpars_title.hide()

    def process_load_file(self):
        self.procpars_title.setText("Выгрузка данных...")
        self.procpars_title.show()
        app.processEvents()

    def get_file(self):
        self.file_to_send = QFileDialog.getOpenFileName(self, "Выберите картинку для отправки", ".\\")[0]
        print(self.file_to_send)

    def view_instruction(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Инструкция")

        txt = open("tgramer_source\\insrt.txt", encoding="utf-8").read()
        label = ScrollLabel(dialog)
 
        # setting text to the label
        label.setText(txt)
        label.setGeometry(100, 100, 800, 600) 
        # setting geometry
        dialog.setFixedSize(1000, 800)

        dialog.show()
        

if __name__ == "__main__":
    key = open('key.txt').read()
    approve = auth()
    if not approve and key:
        app2 = QtWidgets.QApplication(sys.argv)
        app2.setWindowIcon(QtGui.QIcon('tgramer_source\\tg.ico'))
        while not approve:
            dialog = EnterCodeDialog()
            dialog.setWindowIcon(QtGui.QIcon('tgramer_source\\tg.ico'))
            dialog.setWindowTitle("Активация программы")
            dialog.show()
            app2.exec_()
            key = open('key.txt').read()
            approve = auth()
    elif not approve and not key:
        app2 = QtWidgets.QApplication(sys.argv)
        app2.setWindowIcon(QtGui.QIcon('tgramer_source\\tg.ico'))
        while not approve:
            dialog = EnterCodeDialog()
            dialog.setWindowIcon(QtGui.QIcon('tgramer_source\\tg.ico'))
            dialog.setWindowTitle("Активация программы")
            dialog.wrong_label.hide()
            dialog.show()
            app2.exec_()
            key = open('key.txt').read()
            approve = auth()
    if approve:
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('tgramer_source\\tg.ico'))
        mw = MainWindow()
        mw.setWindowIcon(QtGui.QIcon('tgramer_source\\tg.ico'))
        mw.show()
        sys.exit(app.exec_())
