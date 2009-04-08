# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MemAnalyzer.ui'
#
# Created: Thu Nov 15 18:31:58 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os, sys

class Ui_MainWindow(object):
    def __init(self):
        self.dumpFile = ''
        self.mainWin = None
    
    def openFile(self):
        path = QtGui.QFileDialog.getOpenFileName(self.mainWin, "Open Memory Dump",  "..", "Dump Files (*.dmp)");

        if path.__len__() > 0:
            self.dumpFile = path
            self.textEdit.clear()
                    
    def saveFile(self):
        path = QtGui.QFileDialog.getSaveFileName(self.mainWin, "Save Memory Dump",  "..", "Text Files (*.txt)");

        if path.__len__() > 0:
            # Now I have to save the content of the text edit inside the file
             file = open(path,  'w')
             if not file is None:
                file.write(self.textEdit.plainText())
                file.close()
        else:
            errorDialog = QtGui.QErrorMessage(self.mainWin)
            errorDialog.showMessage('Error in opening file: ' + path + ' for saving')
            
    def comboChanged(self,  value):
        if value == 0: #mem-image
            self.lineEdit.setDisabled(False) #Cycle-1
            self.lineEdit_2.setDisabled(False) #Mem-Size
            self.lineEdit_3.setDisabled(True) #Address
            self.lineEdit_4.setDisabled(True) #Value
            self.lineEdit_5.setDisabled(True) #Cycle-2
            self.lineEdit_6.setDisabled(False) #Wordsize
        elif value == 1: #first-modification
            self.lineEdit.setDisabled(False) #Cycle-1
            self.lineEdit_2.setDisabled(False) #Mem-Size
            self.lineEdit_3.setDisabled(False) #Address
            self.lineEdit_4.setDisabled(True) #Value
            self.lineEdit_5.setDisabled(True) #Cycle-2
            self.lineEdit_6.setDisabled(False) #Wordsize
        elif value == 2: #last-modification
            self.lineEdit.setDisabled(True) #Cycle-1
            self.lineEdit_2.setDisabled(False) #Mem-Size
            self.lineEdit_3.setDisabled(False) #Address
            self.lineEdit_4.setDisabled(True) #Value
            self.lineEdit_5.setDisabled(True) #Cycle-2
            self.lineEdit_6.setDisabled(False) #Wordsize
        elif value == 3: #modifcations-time
            self.lineEdit.setDisabled(False) #Cycle-1
            self.lineEdit_2.setDisabled(False) #Mem-Size
            self.lineEdit_3.setDisabled(False) #Address
            self.lineEdit_4.setDisabled(True) #Value
            self.lineEdit_5.setDisabled(False) #Cycle-2
            self.lineEdit_6.setDisabled(False) #Wordsize
        elif value == 4: #all-modifications
            self.lineEdit.setDisabled(True) #Cycle-1
            self.lineEdit_2.setDisabled(False) #Mem-Size
            self.lineEdit_3.setDisabled(False) #Address
            self.lineEdit_4.setDisabled(True) #Value
            self.lineEdit_5.setDisabled(True) #Cycle-2
            self.lineEdit_6.setDisabled(False) #Wordsize
        elif value == 5: #value-writes
            self.lineEdit.setDisabled(True) #Cycle-1
            self.lineEdit_2.setDisabled(False) #Mem-Size
            self.lineEdit_3.setDisabled(True) #Address
            self.lineEdit_4.setDisabled(False) #Value
            self.lineEdit_5.setDisabled(True) #Cycle-2
            self.lineEdit_6.setDisabled(False) #Wordsize

    def executeMemoryQuery(self):
        value = self.comboBox.currentIndex()
        execPath = os.path.abspath(os.path.dirname(sys.modules['__main__'].__file__))
        if value == 0: #mem-image
            if int(self.lineEdit.text()) >= 0:
                retVal = os.popen(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -o tempOut.tmp -e ' + self.lineEdit.text() + ' -d 0 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' 2>&1'))
            else:
                retVal = os.popen(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -o tempOut.tmp -d 0 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' 2>&1'))
            #print(str('./memAnalyzer -f ' + self.dumpFile + ' -o tempOut.tmp -e ' + self.lineEdit.text() + ' -d 0 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' 2>&1'))
            if retVal.readline() != '':
                errorDialog = QtGui.QErrorMessage(self.mainWin)
                errorDialog.showMessage('Error in reading the memory dump: ' + retVal.readline())
            else:
                self.textEdit.clear()
                try:
                    self.textEdit.setPlainText('\n'.join(open('tempOut.tmp').readlines()))
                except Exception,  e:
                    errorDialog = QtGui.QErrorMessage(self.mainWin)
                    errorDialog.showMessage('Error in reading the memory dump: ' + str(e))
        elif value == 1: #first-modification
            retVal = os.popen(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -c ' + self.lineEdit.text() + ' -d 1 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' -a ' + self.lineEdit_3.text() + ' 2>&1'))
            print(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -c ' + self.lineEdit.text() + ' -d 1 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' 2>&1'))
            if retVal.readline() == '':
                errorDialog = QtGui.QErrorMessage(self.mainWin)
                errorDialog.showMessage('Error in reading the memory dump: ' + retVal.readline())
            else:
                self.textEdit.clear()
                try:
                    self.textEdit.setPlainText('\n'.join(retVal.readlines()))
                except Exception,  e:
                    errorDialog = QtGui.QErrorMessage(self.mainWin)
                    errorDialog.showMessage('Error in reading the memory dump: ' + str(e))
        elif value == 2: #last-modification
            retVal = os.popen(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -d 2 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' -a ' + self.lineEdit_2.text() + ' 2>&1'))
            print(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -d 2 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' 2>&1'))
            if retVal.readline() == '':
                errorDialog = QtGui.QErrorMessage(self.mainWin)
                errorDialog.showMessage('Error in reading the memory dump: ' + retVal.readline())
            else:
                self.textEdit.clear()
                try:
                    self.textEdit.setPlainText('\n'.join(retVal.readlines()))
                except Exception,  e:
                    errorDialog = QtGui.QErrorMessage(self.mainWin)
                    errorDialog.showMessage('Error in reading the memory dump: ' + str(e))
        elif value == 3: #modifcations-time
            retVal = os.popen(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -o tempOut.tmp -c ' + self.lineEdit.text() + ' -e ' + self.lineEdit_5.text() + ' -d 3 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' -a ' + self.lineEdit_3.text() + ' 2>&1'))
            print(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -c ' + self.lineEdit.text() + ' -e ' + self.lineEdit_5.text() + ' -d 3 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' 2>&1'))
            if retVal.readline() != '':
                errorDialog = QtGui.QErrorMessage(self.mainWin)
                errorDialog.showMessage('Error in reading the memory dump: ' + retVal.readline())
            else:
                self.textEdit.clear()
                try:
                    self.textEdit.setPlainText('\n'.join(open('tempOut.tmp').readlines()))
                except Exception,  e:
                    errorDialog = QtGui.QErrorMessage(self.mainWin)
                    errorDialog.showMessage('Error in reading the memory dump: ' + str(e))
        elif value == 4: #all-modifications
            retVal = os.popen(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -o tempOut.tmp -d 4 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' -a ' + self.lineEdit_3.text() + ' 2>&1'))
            print(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -o tempOut.tmp -d 4 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' 2>&1'))
            if retVal.readline() != '':
                errorDialog = QtGui.QErrorMessage(self.mainWin)
                errorDialog.showMessage('Error in reading the memory dump: ' + retVal.readline())
            else:
                self.textEdit.clear()
                try:
                    self.textEdit.setPlainText('\n'.join(open('tempOut.tmp').readlines()))
                except Exception,  e:
                    errorDialog = QtGui.QErrorMessage(self.mainWin)
                    errorDialog.showMessage('Error in reading the memory dump: ' + str(e))
        elif value == 5: #value-writes
            retVal = os.popen(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -o tempOut.tmp -d 5 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' -v ' + self.lineEdit_4.text() + ' 2>&1'))
            print(str(execPath + os.sep + 'memAnalyzer -f ' + self.dumpFile + ' -o tempOut.tmp -d 5 -m ' + self.lineEdit_2.text() + ' -w ' + self.lineEdit_6.text() + ' -v ' + self.lineEdit_4.text() + ' 2>&1'))
            if retVal.readline() != '':
                errorDialog = QtGui.QErrorMessage(self.mainWin)
                errorDialog.showMessage('Error in reading the memory dump: ' + retVal.readline())
            else:
                self.textEdit.clear()
                try:
                    self.textEdit.setPlainText('\n'.join(open('tempOut.tmp').readlines()))
                except Exception,  e:
                    errorDialog = QtGui.QErrorMessage(self.mainWin)
                    errorDialog.showMessage('Error in reading the memory dump: ' + str(e))

        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,824,590).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.hboxlayout = QtGui.QHBoxLayout(self.frame)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(self.frame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.comboBox = QtGui.QComboBox(self.frame)
        self.comboBox.setObjectName("comboBox")
        self.vboxlayout1.addWidget(self.comboBox)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.vboxlayout2.addWidget(self.label_4)

        self.lineEdit_3 = QtGui.QLineEdit(self.frame)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.vboxlayout2.addWidget(self.lineEdit_3)
        self.hboxlayout.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.label_7 = QtGui.QLabel(self.frame)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.vboxlayout3.addWidget(self.label_7)

        self.lineEdit_4 = QtGui.QLineEdit(self.frame)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.vboxlayout3.addWidget(self.lineEdit_4)
        self.hboxlayout.addLayout(self.vboxlayout3)

        self.vboxlayout4 = QtGui.QVBoxLayout()
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.vboxlayout4.addWidget(self.label_2)

        self.lineEdit = QtGui.QLineEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        self.vboxlayout4.addWidget(self.lineEdit)
        self.hboxlayout.addLayout(self.vboxlayout4)

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.vboxlayout5.addWidget(self.label_5)

        self.lineEdit_2 = QtGui.QLineEdit(self.frame)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.vboxlayout5.addWidget(self.lineEdit_2)
        self.hboxlayout.addLayout(self.vboxlayout5)

        self.vboxlayout6 = QtGui.QVBoxLayout()
        self.vboxlayout6.setObjectName("vboxlayout6")

        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.vboxlayout6.addWidget(self.label_3)

        self.lineEdit_5 = QtGui.QLineEdit(self.frame)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.vboxlayout6.addWidget(self.lineEdit_5)
        self.hboxlayout.addLayout(self.vboxlayout6)

        self.vboxlayout7 = QtGui.QVBoxLayout()
        self.vboxlayout7.setObjectName("vboxlayout7")

        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.vboxlayout7.addWidget(self.label_6)

        self.lineEdit_6 = QtGui.QLineEdit(self.frame)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.vboxlayout7.addWidget(self.lineEdit_6)
        self.hboxlayout.addLayout(self.vboxlayout7)

        self.pushButton = QtGui.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)
        self.vboxlayout.addWidget(self.frame)

        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.vboxlayout.addWidget(self.textEdit)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,824,30))
        self.menubar.setObjectName("menubar")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.menu_File.addAction("&Memory Image", self.openFile, QtGui.QKeySequence(MainWindow.tr("Ctrl+O", "File|Memory Image")))
        self.menu_File.addAction("&Save", self.saveFile, QtGui.QKeySequence(MainWindow.tr("Ctrl+R", "File|Save")))
        self.menu_File.addAction("&Close", MainWindow, QtCore.SLOT('close()'), QtGui.QKeySequence(MainWindow.tr("Ctrl+W", "File|Close")))
        MainWindow.connect(self.comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.comboChanged)
        MainWindow.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.executeMemoryQuery)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Memory Analyzer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Operation Type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Time - 1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Memory Size", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Time - 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Word Size", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_4.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("MainWindow", "-1", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_2.setText(QtGui.QApplication.translate("MainWindow", "1048576", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_5.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_3.setText(QtGui.QApplication.translate("MainWindow", "0x0", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_6.setText(QtGui.QApplication.translate("MainWindow", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItems(['mem-image',  'first-modification',  'last-modification',  'modifcations-time',  'all-modifications',  'value-writes'])
        self.lineEdit.setDisabled(False) #Cycle-1
        self.lineEdit_2.setDisabled(False) #Mem-Size
        self.lineEdit_3.setDisabled(True) #Address
        self.lineEdit_4.setDisabled(True) #Value
        self.lineEdit_5.setDisabled(True) #Cycle-2
        self.lineEdit_6.setDisabled(False) #Wordsize
        self.mainWin = MainWindow
