#-*- encoding:utf-8 -*-
#coding=utf-8

import sys
import starter
import time
import ctypes
import webS
from PIL import Image
from PyQt4 import QtGui, QtCore, QtSql

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle(u'Start')
        self.setWindowIcon(QtGui.QIcon('icons/bomb.png'))

        refresh = QtGui.QAction(QtGui.QIcon('icons/arrow_refresh.png'), 'Refresh', self)
        refresh.setShortcut('Ctrl+R')
        refresh.setStatusTip('Refresh')
        self.connect(refresh, QtCore.SIGNAL('triggered()'), self.refreshData)
        
        exit = QtGui.QAction(QtGui.QIcon('icons/cross.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        #菜单
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(refresh)
        file.addAction(exit)

        toolbar = self.addToolBar('ToolBar')
        toolbar.addAction(refresh)
        toolbar.addAction(exit)

        #状态栏
        self.statusBar().showMessage('Ready')

        #连接数据库
        #self.db = dbUtil.DBUtil('lib.db')
        
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)
    
        self.mainLayout = QtGui.QVBoxLayout()
        widget.setLayout(self.mainLayout)

        self.createTable()
        self.refreshData()

        funcWidget = QtGui.QWidget()
        self.mainLayout.addWidget(funcWidget)
        self.funcLayout = QtGui.QHBoxLayout()
        funcWidget.setLayout(self.funcLayout)

        #添加按钮
        add = QtGui.QPushButton(u'添加', self)
        self.connect(add, QtCore.SIGNAL('clicked()'), self.addRow)
        self.funcLayout.addWidget(add)

        #保存按钮
        save = QtGui.QPushButton(u'保存', self)
        self.connect(save, QtCore.SIGNAL('clicked()'), self.saveRows)
        self.funcLayout.addWidget(save)
        
        #删除按钮
        delete = QtGui.QPushButton(u'删除一行', self)
        self.connect(delete, QtCore.SIGNAL('clicked()'), self.deleteRow)
        self.funcLayout.addWidget(delete)
        
        #退出按钮
        refresh = QtGui.QPushButton(u'刷新', self)
        self.connect(refresh, QtCore.SIGNAL('clicked()'), self.refreshData)
        self.funcLayout.addWidget(refresh)
        
        #执行
        self.startButton = QtGui.QPushButton(u'接受控制', self)
        self.connect(self.startButton, QtCore.SIGNAL('clicked()'), self.start)
        self.funcLayout.addWidget(self.startButton)
        
        self.running = False

    #创建表控件
    def createTable(self):
        self.table = QtGui.QTableWidget(2, 5)
        self.mainLayout.addWidget(self.table)
        self.table.hideColumn(0)
        self.table.clear()
        self.table.setHorizontalHeaderLabels([u'ID', u'名字', u'执行命令', u'执行时间', u'是否启用'])
        self.table.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.table.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        selected = None
        
    #刷新数据
    def refreshData(self):
        #self.db.execute("create table if not exists exes(id integer primary key autoincrement, name text, cmd text, time text, enabled text)")
        #ret = self.db.select("select * from exes")
        ret = webS.getAllExe()
        self.table.setRowCount(len(ret))
        row = 0
        for line in ret:
            self.table.setItem(row, 0, QtGui.QTableWidgetItem(unicode(line['id'])))
            self.table.setItem(row, 1, QtGui.QTableWidgetItem(unicode(line['name'])))
            self.table.setItem(row, 2, QtGui.QTableWidgetItem(unicode(line['cmd'])))
            self.table.setItem(row, 3, QtGui.QTableWidgetItem(unicode(line['time'])))
            self.table.setItem(row, 4, QtGui.QTableWidgetItem(unicode(line['enabled'])))
            row += 1

    #添加行
    def addRow(self):
        rowCount = self.table.rowCount()
        if self.getTextFromCell(rowCount - 1, 0) != '' or rowCount == 0:
            self.table.insertRow(rowCount)
            #self.db.execute("insert into exes(name, cmd, time, enabled) values ('', '', '', '')")
            #maxId = self.db.selectOne("select max(id) from exes")
            maxId = webS.addExe('', '', '', '')
            self.table.setItem(rowCount, 0, QtGui.QTableWidgetItem(unicode(maxId)))

    #保存
    def saveRows(self):
        for row in range(self.table.rowCount()):
            id = self.getTextFromCell(row, 0)
            name = self.getTextFromCell(row, 1)
            cmd = self.getTextFromCell(row, 2)
            time = self.getTextFromCell(row, 3)
            enabled = self.getTextFromCell(row, 4)
            #self.db.execute("update exes set name = ?, cmd = ?, time = ?, enabled = ? where id = ?", (name, cmd, time, enabled, id))
            print id, name, cmd, time, enabled
            webS.updateExe(id, name, cmd, time, enabled)

    #删除行
    def deleteRow(self):
        selected = self.table.selectedItems()
        if selected != []:
            name = self.getTextFromItem(selected[0])
            #self.db.execute('delete from exes where name = ?', (name,))
            webS.deleteExe(name)
            self.refreshData()

    #开始执行
    def start(self):
        if not self.running:
            self.startButton.setText(u'正在接受控制')
            self.startButton.setFlat(True)
            tableScanner = TableScanner(self.table)
            tableScanner.start()
            screenShoter = ScreenShoter()
            screenShoter.start()
            self.running = True
                
    #居中功能函数
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/ 2, (screen.height() - size.height()) / 2)
        self.statusBar().showMessage('Centered')

    #关闭事件处理
    def closeEvent(self, event):
        #reply = QtGui.QMessageBox.question(self, 'Message', 'Are you sure to quit?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        #if reply == QtGui.QMessageBox.Yes:
            event.accept()
        #else:
        #    event.ignore()

    def getTextFromCell(self, row, column):
        item = self.table.item(row, column)
        if item is None:
            return ''
        else:
            return unicode(item.text().toUtf8(), 'utf-8')
        
    def getTextFromItem(self, item):
        if item is None:
            return ''
        else:
            return unicode(item.text().toUtf8(), 'utf-8')

import threading
class TableScanner(threading.Thread):
    def __init__(self, table):
        threading.Thread.__init__(self)
        self.__table = table
         #启动工具对象
        self.starter = starter.Starter()
        self.startedNames = []

    def run(self):
        while 1:
            #刷新数据
            ret = webS.getAllExe()
            print 'running'
            print ret
            self.__table.setRowCount(len(ret))
            row = 0
            for line in ret:
                self.__table.setItem(row, 0, QtGui.QTableWidgetItem(unicode(line['id'])))
                self.__table.setItem(row, 1, QtGui.QTableWidgetItem(unicode(line['name'])))
                self.__table.setItem(row, 2, QtGui.QTableWidgetItem(unicode(line['cmd'])))
                self.__table.setItem(row, 3, QtGui.QTableWidgetItem(unicode(line['time'])))
                self.__table.setItem(row, 4, QtGui.QTableWidgetItem(unicode(line['enabled'])))
                row += 1
            for row in range(self.__table.rowCount()):
                name = getTextFromCell(self.__table, row, 1)
                cmd = getTextFromCell(self.__table, row, 2)
                t = getTextFromCell(self.__table, row, 3)
                enabled = getTextFromCell(self.__table, row, 4)
                
                if cmd != '' and enabled == 'y' and not name in self.startedNames:
                    if t == '':
                        self.starter.start(name, cmd)
                    else:
                        self.starter.start(name, cmd, t)
                    self.startedNames.append(name)
                if enabled == 'n' and name in self.startedNames:
                    ps = self.starter.getPS()
                    print name
                    for p in ps:
                        if p['name'] == name:
                            ctypes.windll.kernel32.TerminateProcess(int(p['process']._handle), -1)
                            self.startedNames.remove(name)
            time.sleep(8)

def getTextFromCell(table, row, column):
    item = table.item(row, column)
    if item is None:
        return ''
    else:
        return unicode(item.text().toUtf8(), 'utf-8')

def getTextFromItem(item):
    if item is None:
        return ''
    else:
        return unicode(item.text().toUtf8(), 'utf-8')


class ScreenShoter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.originalPixmap = None

    def run(self):
        while 1:
            #截取屏幕
            self.shootScreen()
            self.saveScreenshot()
            time.sleep(5)
    def saveScreenshot(self):
        format = 'png'
        initialPath = QtCore.QDir.currentPath() + "/untitled." + format
        self.originalPixmap.save(initialPath, format)
        img = Image.open('untitled.png')
        img = img.convert('P')
        img.save('untitled.png')
        webS.uploadImage(open('untitled.png', 'rb'))

    def shootScreen(self):
        # Garbage collect any existing image first.
        self.originalPixmap = None
        self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())
