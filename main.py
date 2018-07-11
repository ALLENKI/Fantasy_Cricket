from PyQt5 import QtGui, QtCore,QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox
from PyQt5.QtCore import pyqtSlot
from Fantasy_cricket import Ui_MainWindow
from evaluate import Ui_Form
import sqlite3
MySchool=sqlite3.connect('C:/Users/DELL/AppData/Local/VirtualStore/Program Files (x86)/sqlite-tools-win32-x86-3240000 (1)/sqlite-tools-win32-x86-3240000/fant_cric.db')
curschool=MySchool.cursor()
total_value=1000
BAT=BOW=WK=AR=0
batters=rounders=wicketers=bowlers=bat1=bow1=al1=wk1=[]

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    # Beware that all widgets are now available through the self.ui attribute
    # Getting the push button is written:
    #self.ui.pushButton.connect(about)
        self.ui.listWidget.itemDoubleClicked.connect(self.removelist1)
        self.ui.listWidget_2.itemDoubleClicked.connect(self.removelist2)
        self.ui.radioButton.toggled.connect(self.checkstate)
        self.ui.radioButton_4.toggled.connect(self.checkstate)
        self.ui.radioButton_3.toggled.connect(self.checkstate)
        self.ui.radioButton_2.toggled.connect(self.checkstate)
        self.ui.menuManage_Teams.triggered[QtWidgets.QAction].connect(self.menufunction)
        self.ui.radioButton.setDisabled(True)
        self.ui.radioButton_3.setDisabled(True)
        self.ui.radioButton_4.setDisabled(True)
        self.ui.radioButton_2.setDisabled(True)
        self.numbers()


    def numbers(self):
        global BAT,BOW,WK,AR,batters,bowlers,wicketers,rounders,bat1,bow1,al1,wk1
        curschool.execute('''select count(player) from stats where ctg="WK";''')
        WK=list(curschool.fetchone())
        curschool.execute('''select count(player) from stats where ctg="BAT";''')
        BAT=list(curschool.fetchone())
        curschool.execute('''select count(player) from stats where ctg="AR";''')
        AR=list(curschool.fetchone())
        curschool.execute('''select count(player) from stats where ctg="BWL";''')
        BOW=list(curschool.fetchone())
        curschool.execute('''select player from stats where ctg="BAT";''')
        batters=curschool.fetchall()
        curschool.execute('''select player from stats where ctg="BWL";''')
        bowlers=curschool.fetchall()
        curschool.execute('''select player from stats where ctg="AR";''')
        rounders=curschool.fetchall()
        curschool.execute('''select player from stats where ctg="WK";''')
        wicketers=curschool.fetchall()

        curschool.execute('''select player from stats where ctg="BAT";''')
        bat1=curschool.fetchall()
        curschool.execute('''select player from stats where ctg="BWL";''')
        bow1=curschool.fetchall()
        curschool.execute('''select player from stats where ctg="AR";''')
        al1=curschool.fetchall()
        curschool.execute('''select player from stats where ctg="WK";''')
        wk1=curschool.fetchall()



    def Window(self):
        self.window=QtWidgets.QWidget()
        self.ui=Ui_Form()
        self.ui.setupUi(self.window)
        myMainWindow.hide()
        self.window.show()


    def menufunction(self, action):
        txt= (action.text())
        if(txt=='NEW Team'):
            team_name=QtWidgets.QInputDialog.getText(self,"NEW TEAM","Enter the name of new team")
            if team_name[0] is '' :
                QtWidgets.QMessageBox.critical(self,"Error","Team Name cannot be empty")
            else:
                self.ui.lineEdit_7.setText(team_name[0])
                self.ui.radioButton.setDisabled(False)
                self.ui.radioButton_3.setDisabled(False)
                self.ui.radioButton_4.setDisabled(False)
                self.ui.radioButton_2.setDisabled(False)

        if(txt=='SAVE Team'):
            team1=[]
            curschool.execute('''insert into teams (name,players,value) values(?,?,?);''',(self.ui.lineEdit_7.text(),self.ui.listWidget_2.count(),self.ui.lineEdit_6.text()))
            MySchool.commit()


        if(txt=='EVALUATE Team'):
            self.Window()



    def checkstate(self):
        global batters
        state1='OFF'
        state2='OFF'
        state3='OFF'
        state4='OFF'
        if self.ui.radioButton.isChecked()==True:
           state1='ON'
           self.ui.listWidget.clear()
           curschool.execute('''select player from stats where ctg="BAT";''')
           for row in batters:
               self.ui.listWidget.addItem(row[0])
        else:
           state1='OFF'

        if self.ui.radioButton_4.isChecked()==True:
           state2='ON'
           self.ui.listWidget.clear()
           curschool.execute('''select player from stats where ctg="AR";''')
           for row in rounders:
               self.ui.listWidget.addItem(row[0])
        else:
           state2='OFF'

        if self.ui.radioButton_3.isChecked()==True:
           state3='ON'
           self.ui.listWidget.clear()
           curschool.execute('''select player from stats where ctg="BWL";''')
           for row in bowlers:
               self.ui.listWidget.addItem(row[0])
        else:
           state3='OFF'

        if self.ui.radioButton_2.isChecked()==True:
           state4='ON'
           self.ui.listWidget.clear()
           curschool.execute('''select player from stats where ctg="WK";''')
           for row in wicketers:
               self.ui.listWidget.addItem(row[0])
        else:
           state4='OFF'


    def x(self,ctg):
        global BAT,BOW,WK,AR
        if ctg=="BAT":
           BAT[0]=BAT[0]-1
           self.ui.lineEdit.setText(str(BAT[0]-self.ui.listWidget.count()))
        elif ctg=="BOW":
             BOW[0]=BOW[0]-1
             self.ui.lineEdit_2.setText(str(BOW[0]))
        elif ctg=="WK":
             WK[0]=WK[0]-1
             self.ui.lineEdit_4.setText(str(WK[0]))
        elif ctg=="AR":
             AR[0]=AR[0]-1
             self.ui.lineEdit_3.setText(str(AR[0]))

    def values(self,item,ctg):
        global total_value
        curschool.execute('''select value from stats where player="'''+item.text()+'''";''')
        value1=curschool.fetchone()
        total_value=total_value-value1[0]
        if total_value < 0 :
           QtWidgets.QMessageBox.critical(self,"Error","Cannot select this player")
           total_value=total_value+value1[0]
           self.ui.listWidget.addItem(item.text())
           y=0
        else:
           self.ui.listWidget_2.addItem(item.text())
           self.x(ctg)
           y=1
        self.ui.lineEdit_6.setText(str(1000-total_value))
        self.ui.lineEdit_5.setText(str(total_value))
        return y



    def removelist1(self, item):
        if self.ui.radioButton_2.isChecked()== True:
            if self.ui.lineEdit_4.text()=='1':
               QtWidgets.QMessageBox.critical(self,"error","cannot select more than one wicket keeper")
            else:
               self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
               y=self.values(item,self.ui.radioButton_2.text())
               if y==1:
                  wicketers.remove((item.text(),))

        if self.ui.radioButton.isChecked()==True:
            if self.ui.lineEdit.text()=='5':
               QtWidgets.QMessageBox.critical(self,"error","cannot select more than five batsmen")
            else:
               self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
               y=self.values(item,self.ui.radioButton.text())
               if y==1:
                  batters.remove((item.text(),))

        if self.ui.radioButton_3.isChecked()==True:
            if self.ui.lineEdit_2.text()=='3':
               QtWidgets.QMessageBox.critical(self,"error","cannot select more than three bowlers")
            else:
                self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
                y=self.values(item,self.ui.radioButton_3.text())
                if y==1:
                   bowlers.remove((item.text(),))

        if self.ui.radioButton_4.isChecked()==True:
            if self.ui.lineEdit_3.text()=='2':
               QtWidgets.QMessageBox.critical(self,"error","cannot select more than two Allrounders")
            else:
                self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
                y=self.values(item,self.ui.radioButton_4.text())
                if y==1:
                   rounders.remove((item.text(),))


    def removelist2(self, item):
        global total_value,bat1,bow1,al1,wk1,batters,bowlers,wicketers,rounders,BAT,BOW,AR,WK
        self.ui.listWidget_2.takeItem(self.ui.listWidget_2.row(item))

        if((item.text(),) in bat1):
            batters.append((item.text(),))
            BAT[0]=BAT[0]+1
            self.ui.lineEdit.setText(str(BAT[0]))

        if((item.text(),) in bow1):
            bowlers.append((item.text(),))
            BOW[0]=BOW[0]+1
            self.ui.lineEdit_2.setText(str(BOW[0]))

        if((item.text(),) in al1):
            rounders.append((item.text(),))
            AR[0]=AR[0]+1
            self.ui.lineEdit_3.setText(str(AR[0]))

        if((item.text(),) in wk1):
            wicketers.append((item.text(),))
            WK[0]=WK[0]+1
            self.ui.lineEdit_4.setText(str(WK[0]))

        curschool.execute('''select value from stats where player="'''+item.text()+'''";''')
        value2=curschool.fetchone()
        total_value=total_value+value2[0]
        self.ui.lineEdit_6.setText(str(1000-total_value))
        self.ui.lineEdit_5.setText(str(total_value))





if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  myMainWindow = MyMainWindow()
  myMainWindow.show()
  sys.exit(app.exec_())
