from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton,QComboBox,QTableWidget ,QTableWidgetItem
from mainwindow import Ui_Form
import psutil
from sniffer import *
#import sys
from PyQt5.QtGui import QIcon
#from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QComboBox

class window(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        self.Ui=Ui_Form()
        self.setWindowTitle('Eagles packet sniffer')
        self.Ui.setupUi(self)
        self.setWindowIcon(QIcon('images.png'))
        self.combo()
        self.result=self.Ui.pushButton.clicked.connect(self.get_data)
        self.show()


    def combo(self):
        d = sniff.findInterfaces()
        for i in d:
           if "Loopback" not in i:
               self.Ui.comboBox.addItem(i[0])


    def get_data(self):
        if(sniff.run):
            self.Ui.pushButton.setText("Start  Sniffing")
            sniff.run =False
        else :
            d = sniff.findInterfaces()
            i=self.Ui.comboBox.currentIndex()
            interface = d[i][1]
            sniff.selectInterface(interface)
            filter_pkt=self.Ui.lineEdit.text()
            sniff.setFilter(filter_pkt)
            self.Ui.pushButton.setText("Stop  Sniffing")
            sniff.run = True
            sniff.start(self)
        return 0


        # self.setWindowIcon(QIcon('pic.png'))
sniff = sniffer()
app = QApplication(sys.argv)
Gui = window()
sys.exit(app.exec_())
