import sys
import os
import ctypes

from playsound import playsound
from time import sleep
from random import randint

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

ntdll = ctypes.windll.ntdll
SeShutdownPrivilege = 19

chamber = 0
location = randint(1,6)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(300, 200)
        MainWindow.setMinimumSize(QSize(300, 200))
        MainWindow.setMaximumSize(QSize(300, 200))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 9, 141, 151))
        self.pushButton.clicked.connect(self.spin)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(150, 9, 141, 151))
        self.pushButton_2.clicked.connect(self.shoot)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(13, 174, 281, 16))
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 159, 301, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)

        MainWindow.setWindowTitle("Bluescreen Roulette")
        self.pushButton.setText("Spin the chamber")
        self.pushButton_2.setText("Pull the trigger")
        self.label.setText("Press a button to play.")

        QMetaObject.connectSlotsByName(MainWindow)
    
    def get_error(err):
        return ntdll.RtlNtStatusToDosError(err)

    def its_bluescreen_time(stop_code):
        enabled = ctypes.c_bool()
        res = ntdll.RtlAdjustPrivilege(SeShutdownPrivilege, True, False, ctypes.pointer(enabled))

        if not res:
            print("We're in...")
        else:
            print("Alright we fucked up")
            raise ctypes.WinError(GetNtError(res))

        response = ctypes.c_ulong()
        res = ntdll.NtRaiseHardError(ctypes.c_ulong(0xDEADDEAD), 0, 0, 0, 6, ctypes.byref(response))

        if not res:
            print("Skill issue")
        else:
            print("Why dont you just fucking die already? (error)")
            raise ctypes.WinError(GetNtError(res))

    def buttons(self, onoff):
        self.pushButton.setEnabled(onoff)
        self.pushButton_2.setEnabled(onoff)

    def spin(self):
        global location
        location = randint(1,6)
        self.label.setText("You spin the chamber.")
        print("bullet is in:")
        print(location)
        playsound(resource_path("sfx/spin.wav"), False)

    def shoot(self):
        global chamber
        global location

        self.label.setText("You pull the trigger.")
        
        if chamber == location:
            print("you are dead")
            playsound(resource_path("sfx/gunshot.wav"), False)
            self.label.setText("You lose!")
            self.its_bluescreen_time()
        chamber = chamber+1
        if chamber == 7:
            chamber = 1
        print("you're on chamber:")
        print(chamber)
        self.buttons(False)
        playsound(resource_path("sfx/click.wav"), False)
        self.buttons(True)
        

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

playsound(resource_path("sfx/hammer.wav"), False)

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()