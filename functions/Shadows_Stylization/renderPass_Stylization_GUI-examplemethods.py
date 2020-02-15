from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys



def main():
    # Passing system os informations to the application
    app = QApplication(sys.argv)

    # Set up the window
    win = MainWindow()

    #Showing the window
    win.show()
    #Exit when clicking on the X button
    sys.exit(app.exec_())

# Creating instance of QMainWindow
class MainWindow(QMainWindow):
    # Making sure we're calling parent constructor to set up main window properly
    # use the self and self. in order to be able to access them from inside the class
    def __init__(self):
        super(MainWindow, self).__init__()
        # Size of the window
        xpos = 480
        ypos = 270
        width = 960
        height = 540
        self.setGeometry(xpos, ypos, width, height)
        self.setWindowTitle("Python EXR stylization - v.ALPHA.00.00.1")
        # init window UI
        self.initUI()

    # Put what's going in the window here
    # use the self and self. in order to be able to access them from inside the class
    def initUI(self):

        
        width = 960
        height = 540

        #### Button Open EXR Dialog
        self.bOpenEXR = QtWidgets.QPushButton(self)
        self.bOpenEXR.setText("Open original EXR image")
        self.bOpenEXR.move(5, 20)
        self.bOpenEXR.adjustSize()
        self.bOpenEXR.clicked.connect(self.openExrDialog)

        #### Path to EXR label
        self.exrLabel = QtWidgets.QLabel(self)
        self.exrLabel.setText("You need to select an EXR image")
        self.exrLabel.move(5,40)
        self.exrLabel.adjustSize()

        #### Button to open Brush Dialog
        self.bOpenBrush = QtWidgets.QPushButton(self)
        self.bOpenBrush.setText("Open your brush EXR")
        self.bOpenBrush.move(5, 60)
        self.bOpenBrush.adjustSize()
        self.bOpenBrush.clicked.connect(self.openBrushDialog)

        #### Path to brush label
        self.brushLabel = QtWidgets.QLabel(self)
        self.brushLabel.setText("You need to select a brush EXR")
        self.brushLabel.move(5,80)
        self.brushLabel.adjustSize()

    # Click event
    def clicked(self):
        self.label1.setText("ButtonPressed!")   

    # Picking file dialog
    def openExrDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.updateExrFile(fileName)
            return(fileName)
    
    # Updating Exr File name display
    def updateExrFile(self, fileName):
        self.exrLabel.setText(fileName)
        self.exrLabel.adjustSize()

    # Picking brush dialog
    def openBrushDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.updateBrushFile(fileName)
            return(fileName)
    
    # updating Brush file name display
    def updateBrushFile(self, fileName):
        self.brushLabel.setText(fileName)
        self.brushLabel.adjustSize()

if __name__ == "__main__":
    main()