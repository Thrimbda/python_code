#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-02-14 10:34:46
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-02-17 10:40:35
# Just a dynamic test program for learning.
from PyQt5.QtWidgets import (QToolTip, QMessageBox, QAction, QDesktopWidget, QApplication, QMainWindow)
from PyQt5.QtGui import QFont, QIcon
import sys


class Test(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('Myriad Set'))
        self.setToolTip('This is a <b>QWidget</b> widget')
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QApplication.quit)
        self.statusBar().showMessage('Ready')
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        self.resize(250, 150)
        self.center()
        self.setWindowTitle('Tooltips')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            'Are you sure want to quit?', QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())
