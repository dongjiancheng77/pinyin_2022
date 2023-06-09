# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(700, 1111)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(530, 180, 121, 181))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 30, 421, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 110, 421, 401))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setFocusPolicy(QtCore.Qt.TabFocus)
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(30, 540, 421, 221))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 30, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 670, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.cbBox_Mode = QtWidgets.QComboBox(self.centralwidget)
        self.cbBox_Mode.setGeometry(QtCore.QRect(480, 580, 191, 51))
        self.cbBox_Mode.setObjectName("cbBox_Mode")
        self.cbBox_Mode.addItem("")
        self.cbBox_Mode.addItem("")
        self.cbBox_Mode.addItem("")
        self.cbBox_Mode.addItem("")
        self.cbBox_Mode.setItemText(3, "")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 770, 661, 291))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionload = QtWidgets.QAction(mainWindow)
        self.actionload.setObjectName("actionload")

        self.retranslateUi(mainWindow)
        self.cbBox_Mode.activated['QString'].connect(mainWindow.cbBox_Mode_Callback)
        self.pushButton_2.clicked.connect(mainWindow.pbtPredict_Callback)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "暑期课程-智能输入法 by 董建承"))
        self.label_2.setText(_translate("mainWindow", "按下\n"
"数字\n"
"选择"))
        self.pushButton.setText(_translate("mainWindow", "拼音输入"))
        self.pushButton_2.setText(_translate("mainWindow", "自动预测"))
        self.cbBox_Mode.setItemText(0, _translate("mainWindow", "temperature=0.5"))
        self.cbBox_Mode.setItemText(1, _translate("mainWindow", "temperature=1.0"))
        self.cbBox_Mode.setItemText(2, _translate("mainWindow", "temperature=1.5"))
        self.label_3.setText(_translate("mainWindow", "在第一个框中输入拼音，可输入简写或错序\n"
"在第二个框中用键盘输入数字选择\n"
"在第三个框中得到结果，可以预测下一个词\n"
"可以调整lstm预测的temperature以得到不同结果\n"
"（ps：训练样本较小，结果不算理想）"))
        self.actionload.setText(_translate("mainWindow", "load"))
