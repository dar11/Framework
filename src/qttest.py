from PyQt4 import QtGui, QtCore
import sys, os

class MyClass(object):
    def __init__(self):
        super(MyClass, self).__init__()
        self.myAttr=None
    def getTime(self):
        import datetime
        return datetime.datetime.now() 

class Dialog_01(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow,self).__init__()

        myQWidget = QtGui.QWidget()
        myBoxLayout = QtGui.QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)

        self.ComboBox = QtGui.QComboBox() 
        self.ComboBox.setEditable(True)
        for i in range(12):
            name='Item '+str(i)
            myObject=MyClass()
            self.ComboBox.addItem( name, myObject )


        self.ComboBox.currentIndexChanged.connect(self.combobox_selected)
        myBoxLayout.addWidget(self.ComboBox)

    def combobox_selected(self, index):
        itemName=self.ComboBox.currentText()
        myObject=self.ComboBox.itemData(index).toPyObject()

        if not hasattr(myObject, 'getTime'):
            result=self.ComboBox.blockSignals(True)
            self.ComboBox.removeItem(index)
            myObject=MyClass()
            self.ComboBox.addItem( itemName, myObject )
            self.ComboBox.setCurrentIndex( index )
            self.ComboBox.blockSignals(False)

        print myObject.getTime()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())