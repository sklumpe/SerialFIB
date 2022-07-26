# -*- coding: utf-8 -*-

'''
################################################################
#                         SerialFIB                            #
#                                                              #
#            Sven Klumpe, Sara Goetz, Herman Fung              #
#                                                              #
#                  Julia Mahamid, Jürgen Plitzko               #
#                                                              #
#             Max-Planck-Institute for Biochemistry            #
#                    Martinsried, Germany                      #
#                                                              #
#             European Molecular Biology Laboratory            #
#                    Heidelberg, Germany                       #
#                                                              #
#                                                              #
#                                                              #
#          if you use SerialFIB in your work, please cite:     #
#                   DOI:                                       #
#                                                              #
#                                                              #
#          SerialFIB: A Developer’s Tool for Automated         #
#                 cryo-FIB Customized Workflows                #
#                                                              #
#     with bug reports, suggestions, etc. please contact:      #
#                   klumpe@biochem.mpg.de                      #
################################################################
'''

# Form implementation generated from reading ui file 'scripteditor3.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

#####
import pickle
import os
#####

class Ui_ScriptEditor(object):
    def setupUi(self, ScriptEditor,stagepostions=[],images=[],patterns=[]):
        ScriptEditor.setObjectName("ScriptEditor")
        ScriptEditor.resize(671, 568)
        self.Button_RunScript = QtWidgets.QPushButton(ScriptEditor)
        self.Button_RunScript.setGeometry(QtCore.QRect(520, 520, 113, 32))
        self.Button_RunScript.setObjectName("Button_RunScript")
        self.textEdit = QtWidgets.QTextEdit(ScriptEditor)
        self.textEdit.setGeometry(QtCore.QRect(20, 60, 621, 441))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(ScriptEditor)
        self.label.setGeometry(QtCore.QRect(280, 10, 101, 16))
        self.label.setObjectName("label")
        self.spinBox_chooseScript = QtWidgets.QSpinBox(ScriptEditor)
        self.spinBox_chooseScript.setGeometry(QtCore.QRect(340, 30, 48, 24))
        self.spinBox_chooseScript.setObjectName("spinBox_chooseScript")
        self.label_2 = QtWidgets.QLabel(ScriptEditor)
        self.label_2.setGeometry(QtCore.QRect(240, 30, 91, 20))
        self.label_2.setObjectName("label_2")
        self.Button_OpenScript = QtWidgets.QPushButton(ScriptEditor)
        self.Button_OpenScript.setGeometry(QtCore.QRect(10, 10, 113, 32))
        self.Button_OpenScript.setObjectName("Button_OpenScript")
        self.Button_OpenLibrary = QtWidgets.QPushButton(ScriptEditor)
        self.Button_OpenLibrary.setGeometry(QtCore.QRect(120, 10, 113, 32))
        self.Button_OpenLibrary.setObjectName("Button_OpenLibrary")
        self.Button_SaveScript = QtWidgets.QPushButton(ScriptEditor)
        self.Button_SaveScript.setGeometry(QtCore.QRect(400, 10, 113, 32))
        self.Button_SaveScript.setObjectName("Button_SaveScript")
        self.Button_SaveLibrary = QtWidgets.QPushButton(ScriptEditor)
        self.Button_SaveLibrary.setGeometry(QtCore.QRect(530, 10, 113, 32))
        self.Button_SaveLibrary.setObjectName("Button_SaveLibrary")

        self.retranslateUi(ScriptEditor)
        QtCore.QMetaObject.connectSlotsByName(ScriptEditor)
####
        self.stagepositions=stagepostions
        self.images=images
        self.patterns=patterns
        self.output_dir = '~/'
####

    def retranslateUi(self, ScriptEditor):
        _translate = QtCore.QCoreApplication.translate
        ScriptEditor.setWindowTitle(_translate("ScriptEditor", "Form"))
        self.Button_RunScript.setText(_translate("ScriptEditor", "Run Script"))
        self.label.setText(_translate("ScriptEditor", "Script Editor"))
        self.label_2.setText(_translate("ScriptEditor", "Choose script"))
        self.Button_OpenScript.setText(_translate("ScriptEditor", "Open Script"))
        self.Button_OpenLibrary.setText(_translate("ScriptEditor", "Open Library"))
        self.Button_SaveScript.setText(_translate("ScriptEditor", "Save Script"))
        self.Button_SaveLibrary.setText(_translate("ScriptEditor", "Save Library"))


###################

        self.spinBox_chooseScript.valueChanged.connect(self.changeScript)
        self.Button_RunScript.pressed.connect(self.runScript)
        self.Button_SaveLibrary.pressed.connect(self.saveLibrary)
        self.Button_OpenLibrary.pressed.connect(self.loadLibrary)

        self.Button_SaveScript.pressed.connect(self.saveScript)
        self.Button_OpenScript.pressed.connect(self.loadScript)


        self.scripts={}
        self.script_handle=0

        
    def changeScript(self):
        try:
            script_text=self.textEdit.toPlainText()
            self.scripts.update({self.script_handle:script_text})
            self.script_handle=self.spinBox_chooseScript.value()
            if self.script_handle in self.scripts:
                new_text=self.scripts[self.script_handle]
            else:
                new_text=''
            self.textEdit.setPlainText(new_text)
        except:
            print("Selection cancelled")
        return()
    



    

    def saveScript(self):
        self.changeScript()
        try:
            lib_file=session_file=QtWidgets.QFileDialog.getSaveFileName(None, "Saving Script File...",self.output_dir,"LibraryFile (*.lib)")
            #with open(lib_file[0],'wb') as pickle_out:
            #    pickle.dump(self.scripts,pickle_out)
            with open(lib_file[0],'w') as outfile:
                outfile.write(self.scripts[self.script_handle])
        except:
            print("No File selected!")
        return()
    
    def loadScript(self):
        try:
            lib_file=QtWidgets.QFileDialog.getOpenFileNames(None, "Choose Script File to load",self.output_dir,"LibraryFile (*.lib)")
            with open(lib_file[0][0],'r') as input_file:
                text=input_file.readlines()
                script_text=""
                for i in text:
                    script_text=script_text+i
                
            #print(self.scripts)
            #if self.script_handle in self.scripts:
                #new_text=self.scripts[self.script_handle]
            #else:
                #new_text=''
            self.textEdit.setPlainText(script_text)
        except:
            print("Please select a proper file.")

        return()



    def saveLibrary(self):
        self.changeScript()
        try:
            lib_file=session_file=QtWidgets.QFileDialog.getSaveFileName(None, "Saving Library File...",self.output_dir,"LibraryFile (*.lib)")
            with open(lib_file[0],'wb') as pickle_out:
                pickle.dump(self.scripts,pickle_out)
        except:
            print("No File selected!")
        return()

    def loadLibrary(self):
        try:
            lib_file=QtWidgets.QFileDialog.getOpenFileNames(None, "Choose Library File to load",self.output_dir,"LibraryFile (*.lib)")
            with open(lib_file[0][0],'rb') as pickle_in:
                self.scripts=pickle.load(pickle_in)
            print(self.scripts)
            if self.script_handle in self.scripts:
                new_text=self.scripts[self.script_handle]
            else:
                new_text=''
            self.textEdit.setPlainText(new_text)
        except: 
            print("Please Select a proper library file.")
        return()


    def runScript(self):#,stagepositions=self.stagepositions,images=self.images,patterns=None):
        script_num=self.script_handle
        stagepositions=self.stagepositions
        images=self.images
        patterns=self.patterns
        script_text=self.textEdit.toPlainText()
        self.scripts.update({self.script_handle:script_text})
        commands=self.scripts[script_num]

        import pickle

        with open('pickle.tmp','wb') as pickle_out:
            pickle.dump([stagepositions,images,patterns],pickle_out)
        with open('tmp.py','w') as outfile:
            outfile.write(
                '''
import pickle
with open('pickle.tmp','rb') as pickle_in:
    infile=pickle.load(pickle_in)
    stagepositions=infile[0]
    images=infile[1]
    patterns=infile[2]

from src.Zeiss.CrossbeamDriver import fibsem

import sys

def myexcepthook(type,value,tb):
    fibsem.disconnect()

sys.excepthook = myexcepthook

fibsem=fibsem()
'''
            )
            outfile.write(commands)
            outfile.write('\n')
            outfile.write('fibsem.disconnect()')

        ### Tries to do simultanoues update and writing into file... so far unsuccessful. 
        #cmd='python tmp.py >_ && type _ && type _ > ScriptEditor.log'
        #cmd='python tmp.py > ScriptEditor.log & type ScriptEditor.log'
        #cmd='python '+'tmp.py >> ScriptEditor.log'
        cmd='python tmp.py'

        #progressDialog = QtWidgets.QDialog()
        #verticalLayout = QtWidgets.QVBoxLayout(progressDialog)
        #label = QtWidgets.QLabel("Computing projection...", progressDialog)
        #verticalLayout.addWidget(label)
        #buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel, progressDialog)
        #buttonBox.rejected.connect(progressDialog.reject)
        #verticalLayout.addWidget(buttonBox)

        os.system(cmd)
        #if progressDialog.exec() == QtWidgets.QDialog.Rejected:
        #    pool.close()
        #    pool.terminate()
        #    print("Action cancelled")
        #    return None
        return()
###################
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ScriptEditor()
    ui.setupUi(MainWindow)
    MainWindow.installEventFilter(MainWindow)


    MainWindow.show()
    sys.exit(app.exec_())

