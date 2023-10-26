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



from PyQt5 import QtCore, QtGui, QtWidgets

#############################################
#               Function Import             #
#############################################

vendor='TESCAN'
#### IMPORT AUTOSCRIPT STRUCTURES
if vendor=='Zeiss':
    from src.Zeiss.CrossbeamDriver import fibsem, DummyAdorned

if vendor=='TESCAN':
    from src.TESCAN.TescanDriver import fibsem, DummyAdorned

else:
    try:
        from autoscript_sdb_microscope_client.structures import *
    except:
        print("No Autoscript installed")
    
    from src.AquilosDriver import fibsem

### IMPROT DRIVERS AND TOOLS

from src.TESCAN.scripteditor import Ui_ScriptEditor
from src.PatternDesigner import Ui_PatternFileEditor
from src.LamellaDesigner import Ui_LamellaDesigner
from src.VolumeDesigner import Ui_VolumeDesigner
from src.Param3D import Param3D

### INITIALIZE MICROSCOPE FROM DRIVER
scope=fibsem()
###
print(scope)



### IMPORT EXTERNAL PACKAGES
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsScene
import numpy as np
import os
import src
import logging
import datetime
import cv2
import sys
import pickle

#Taken out for testing
#import src.project_3dct as project_3dct



import re
###

class Stream(QtCore.QObject):
    '''
    This class gets the output text such as error messages etc. and puts them in the GUI message
    box as well as the logfile.

    It does that by getting an update from the MainWindow function onUpdateText() as oyqtSignal
    '''
    newText = QtCore.pyqtSignal(str)
    sys.stdout = open(r'./SFIB.log', mode='a')
    def write(self, text):
        if str(text)==" ":
            print('test')
        else:
            self.newText.emit(str(text).split("\n")[0])




# TestImage load for developing
try:
    testimage=DummyAdorned.load('./DummyImages/testimage1.tif')
    testimage2=DummyAdorned.load('./DummyImages/testimage2.tif')
except:
    print('No testcase or "wrong" developer computer')






#############################################


class Ui_MainWindow(object):
    '''
    Definition of the GUI class
    '''
    def __init__(self):
        # Scene for the GraphicsView, SceneBuffer is a list of all the scenes that have been created
        self.scene=QtWidgets.QGraphicsScene()
        self.sceneBuffer=[]

        # Dictionary of all stage positions 
        self.StagePos={}

        # Dictionary of all patterns defined for the images in the Image Buffer. 
        self.pattern_dict={}
        # Image Buffer handle is a number that keeps track of which image is opened in the graphicsView
        # Image buffer images is a list of all images in the ImageBuffer
        self.ImageBufferHandle=0
        self.ImageBufferImages=[]

        # Output directory for outfiles
        import os
        path = r'%s' % os.getcwd().replace('\\', '/')
        self.output_dir=path
        scope.define_output_dir(self.output_dir)
        self.SAVparamsfile=r'./SAVparams.spf'
        self.roughmillprotocol=r'./roughmill.pro'
        self.finemillprotocol=r'./finemill.pro'
        self.custommillprotocol=r'./testprotocol.pro'
        self.custompatternfile=r'./patternfile.pf'
        self.settings=r'./standard.settings'
        self.number=0
        self.threads=[]

        # Logfile initialization
        self.sysout=open(self.output_dir + r'/'+r'/SFIB.log', mode='a')
        self.log_out=''

        # Initialization for correlation Images and associated tools, e.g. colors for displaying overlays
        self.load_image_pixel_size=1
        self.corrspots={}
        self.copy=[]
        self.pointer_projpixmap=None
        self.colordict={"green":[0,255,0], "magenta":[255,0,255], "cyan":[0,255,255], "yellow":[255,255,0], "red":[255,0,0], "white":[255,255,255]}
        self.CFproj=None

    def get_scene(self):
        '''
        A function that gets the current scene displayed in the GraphicsView

        Input: MainWindow class
        Output: QGraphicsScene
        '''
        scene=self.scene
        return(scene)
    def closeEvent(self):
        print('I Am closing')
        super(QtWidgets.QMainWindow,self).closeEvent()
        scope.disconnect()

        return()
    def get_scenebuffer(self):
        '''
        A function that gets the sceneBuffer

        Input: MainWindow class
        Output: List of QGraphicsScenes
        '''
        scenebuffer=self.sceneBuffer
        return(scenebuffer)
    def push_scene_to_buffer(self,scene,ImageBufferHandle):
        '''
        Function to overwrite the current scene given by the
        ImageBufferHandle with the given scene 

        Input: scene [QGraphicsScene], ImageBufferHandle [int]
        Output: None
        '''
        scenebuffer=self.sceneBuffer
        scenebuffer[ImageBufferHandle]=scene
        self.sceneBuffer=scenebuffer
        return()
    def get_pattern_dict(self):
        '''
        Function to get the pattern dictionnary for e.g. session file writing

        Input: MainWindow class
        Output: dictionary of patterns corresponding to the images in the ImageBuffer
        '''
        return(self.pattern_dict)

    def push_pattern_dict(self,pattern_dict_new):
        '''
        Function to overwrite the pattern_dictionary if session file is read

        Input: pattern_dictionary
        Output: None
        '''
        self.pattern_dict=pattern_dict_new
        return()
    def get_number_imageBuffer(self):
        '''
        Get imageBufferHandle

        Input: Ma
        '''
        return(self.ImageBufferHandle)
####
    def setupUi(self, MainWindow):
        '''
        GUI Setup as created by pyuic
        '''

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1070, 917)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 480, 201, 263))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Button_AddPosition = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_AddPosition.setObjectName("Button_AddPosition")
        self.verticalLayout.addWidget(self.Button_AddPosition)
        self.Button_SaveImageForAlignment = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_SaveImageForAlignment.setObjectName("Button_SaveImageForAlignment")
        self.verticalLayout.addWidget(self.Button_SaveImageForAlignment)
        self.Button_SavePatterns = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_SavePatterns.setObjectName("Button_SavePatterns")
        self.verticalLayout.addWidget(self.Button_SavePatterns)
        self.Button_UpdateZ = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_UpdateZ.setObjectName("Button_UpdateZ")
        self.verticalLayout.addWidget(self.Button_UpdateZ)
        self.Button_GoToXYZ = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_GoToXYZ.setObjectName("Button_GoToXYZ")
        self.verticalLayout.addWidget(self.Button_GoToXYZ)
        self.Button_GoToXY = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_GoToXY.setObjectName("Button_GoToXY")
        self.verticalLayout.addWidget(self.Button_GoToXY)
        self.Button_DeleteItem = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_DeleteItem.setObjectName("Button_DeleteItem")
        self.verticalLayout.addWidget(self.Button_DeleteItem)
        ####
        #self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        # Replacing the Standard QGraphicsView with the LamellaView Class
        self.graphicsView = LamellaView(self.centralwidget)
        #####
        self.graphicsView.setGeometry(QtCore.QRect(480, 30, 581, 461))
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 207, 396))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.Button_SetOutputDirectory = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Button_SetOutputDirectory.setObjectName("Button_SetOutputDirectory")
        self.verticalLayout_4.addWidget(self.Button_SetOutputDirectory)
        self.Button_TakeImageIB = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Button_TakeImageIB.setObjectName("Button_TakeImageIB")
        self.verticalLayout_4.addWidget(self.Button_TakeImageIB)
        self.Button_TakeImageEB = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Button_TakeImageEB.setObjectName("Button_TakeImageEB")
        self.verticalLayout_4.addWidget(self.Button_TakeImageEB)
        self.Button_RunRoughProtocol = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Button_RunRoughProtocol.setObjectName("Button_RunRoughProtocol")
        self.verticalLayout_4.addWidget(self.Button_RunRoughProtocol)
        self.Button_RunFineProtocol = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Button_RunFineProtocol.setObjectName("Button_RunFineProtocol")
        self.verticalLayout_4.addWidget(self.Button_RunFineProtocol)
        self.Button_RunTrenchMilling = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Button_RunTrenchMilling.setObjectName("Button_RunTrenchMilling")
        self.verticalLayout_4.addWidget(self.Button_RunTrenchMilling)
        #self.Button_RunRoughMilling = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        #self.Button_RunRoughMilling.setObjectName("Button_RunRoughMilling")
        #self.verticalLayout_4.addWidget(self.Button_RunRoughMilling)
        #self.Button_RunFineMilling = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        #self.Button_RunFineMilling.setObjectName("Button_RunFineMilling")
        #self.verticalLayout_4.addWidget(self.Button_RunFineMilling)
        self.Button_LoadCorrelationImages = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Button_LoadCorrelationImages.setObjectName("Button_LoadCorrelationImages")
        self.verticalLayout_4.addWidget(self.Button_LoadCorrelationImages)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(710, 10, 141, 16))
        self.label_3.setObjectName("label_3")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(230, 500, 831, 241))
        self.tableWidget.setMouseTracking(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 760, 1051, 111))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(490, 740, 60, 16))
        self.label_4.setObjectName("label_4")
        self.ImageBuffer = QtWidgets.QListWidget(self.centralwidget)
        self.ImageBuffer.setGeometry(QtCore.QRect(220, 30, 251, 201))
        self.ImageBuffer.setObjectName("ImageBuffer")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(300, 10, 91, 16))
        self.label_5.setObjectName("label_5")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(260, 430, 141, 26))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.checkBox_fluo = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_fluo.setGeometry(QtCore.QRect(260, 400, 171, 20))
        self.checkBox_fluo.setObjectName("checkBox_fluo")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(250, 470, 60, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(290, 240, 121, 16))
        self.label_7.setObjectName("label_7")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(240, 260, 211, 134))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Button_SetSAVparameters = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Button_SetSAVparameters.setObjectName("Button_SetSAVparameters")
        self.verticalLayout_2.addWidget(self.Button_SetSAVparameters)
        self.Button_RunVolumeImaging = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Button_RunVolumeImaging.setObjectName("Button_RunVolumeImaging")
        self.verticalLayout_2.addWidget(self.Button_RunVolumeImaging)
        self.Button_RunCustomProtocol = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Button_RunCustomProtocol.setObjectName("Button_RunCustomProtocol")
        self.verticalLayout_2.addWidget(self.Button_RunCustomProtocol)
        self.Button_RunCustomPatternfile = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Button_RunCustomPatternfile.setObjectName("Button_RunCustomPatternfile")
        self.verticalLayout_2.addWidget(self.Button_RunCustomPatternfile)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1070, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuCorrelation = QtWidgets.QMenu(self.menubar)
        self.menuCorrelation.setObjectName("menuCorrelation")
        self.menuTesting = QtWidgets.QMenu(self.menubar)
        self.menuTesting.setObjectName("menuTesting")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionSave_Session = QtWidgets.QAction(MainWindow)
        self.actionSave_Session.setObjectName("actionSave_Session")
        self.actionLoad_Session = QtWidgets.QAction(MainWindow)
        self.actionLoad_Session.setObjectName("actionLoad_Session")
        self.actionClose_2 = QtWidgets.QAction(MainWindow)
        self.actionClose_2.setObjectName("actionClose_2")
        self.actionOpen_Scripting = QtWidgets.QAction(MainWindow)
        self.actionOpen_Scripting.setObjectName("actionOpen_Scripting")
        self.actionScripting = QtWidgets.QAction(MainWindow)
        self.actionScripting.setObjectName("actionScripting")
        self.actionOpen_PatternDesigner = QtWidgets.QAction(MainWindow)
        self.actionOpen_PatternDesigner.setObjectName("actionOpen_PatternDesigner")
        self.actionCompute_FluoProjection = QtWidgets.QAction(MainWindow)
        self.actionCompute_FluoProjection.setObjectName("actionCompute_FluoProjection")
        self.actionLoad_Fluo_Projection = QtWidgets.QAction(MainWindow)
        self.actionLoad_Fluo_Projection.setObjectName("actionLoad_Fluo_Projection")
        self.actionLoad_Correlation_Images = QtWidgets.QAction(MainWindow)
        self.actionLoad_Correlation_Images.setObjectName("actionLoad_Correlation_Images")
        self.actionTestbutton1 = QtWidgets.QAction(MainWindow)
        self.actionTestbutton1.setObjectName("actionTestbutton1")
        self.actionTestbutton2 = QtWidgets.QAction(MainWindow)
        self.actionTestbutton2.setObjectName("actionTestbutton2")
        self.actionTestbutton3 = QtWidgets.QAction(MainWindow)
        self.actionTestbutton3.setObjectName("actionTestbutton3")
        self.actionTestbutton4 = QtWidgets.QAction(MainWindow)
        self.actionTestbutton4.setObjectName("actionTestbutton4")
        self.actionTestbutton5 = QtWidgets.QAction(MainWindow)
        self.actionTestbutton5.setObjectName("actionTestbutton5")
        self.actionSaveSettings = QtWidgets.QAction(MainWindow)
        self.actionSaveSettings.setObjectName("actionSaveSettings")
        self.actionLoadSettings = QtWidgets.QAction(MainWindow)
        self.actionLoadSettings.setObjectName("actionLoadSettings")
        self.actionVolumeDesigner = QtWidgets.QAction(MainWindow)
        self.actionVolumeDesigner.setObjectName("actionVolumeDesigner")
        self.actionLamellaDesigner = QtWidgets.QAction(MainWindow)
        self.actionLamellaDesigner.setObjectName("actionLamellaDesigner")
        self.actionSet_Output_Directory = QtWidgets.QAction(MainWindow)
        self.actionSet_Output_Directory.setObjectName("actionSet_Output_Directory")
        self.actionSet_SAV_parameters = QtWidgets.QAction(MainWindow)
        self.actionSet_SAV_parameters.setObjectName("actionSet_SAV_parameters")
        self.actionSet_Output_Directory_2 = QtWidgets.QAction(MainWindow)
        self.actionSet_Output_Directory_2.setObjectName("actionSet_Output_Directory_2")
        self.actionSet_Rough_Mill_protocol = QtWidgets.QAction(MainWindow)
        self.actionSet_Rough_Mill_protocol.setObjectName("actionSet_Rough_Mill_protocol")
        self.actionSet_Fine_Mill_protocol = QtWidgets.QAction(MainWindow)
        self.actionSet_Fine_Mill_protocol.setObjectName("actionSet_Fine_Mill_protocol")
        self.actionSet_Custom_Protocol = QtWidgets.QAction(MainWindow)
        self.actionSet_Custom_Protocol.setObjectName("actionSet_Custom_Protocol")
        self.actionSet_Custom_Milling = QtWidgets.QAction(MainWindow)
        self.actionSet_Custom_Milling.setObjectName("actionSet_Custom_Milling")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_Session)
        self.menuFile.addAction(self.actionLoad_Session)
        self.menuTools.addAction(self.actionLamellaDesigner)
        self.menuTools.addAction(self.actionVolumeDesigner)
        self.menuTools.addAction(self.actionOpen_PatternDesigner)
        self.menuTools.addAction(self.actionScripting)
        self.menuCorrelation.addAction(self.actionLoad_Correlation_Images)
        self.menuCorrelation.addAction(self.actionCompute_FluoProjection)
        self.menuCorrelation.addAction(self.actionLoad_Fluo_Projection)
        self.menuTesting.addAction(self.actionTestbutton1)
        self.menuTesting.addAction(self.actionTestbutton2)
        self.menuTesting.addAction(self.actionTestbutton3)
        self.menuTesting.addAction(self.actionTestbutton4)
        self.menuTesting.addAction(self.actionTestbutton5)
        self.menuSettings.addAction(self.actionSaveSettings)
        self.menuSettings.addAction(self.actionLoadSettings)
        self.menuSettings.addAction(self.actionSet_Output_Directory_2)
        self.menuSettings.addAction(self.actionSet_SAV_parameters)
        self.menuSettings.addAction(self.actionSet_Rough_Mill_protocol)
        self.menuSettings.addAction(self.actionSet_Fine_Mill_protocol)
        self.menuSettings.addAction(self.actionSet_Custom_Protocol)
        self.menuSettings.addAction(self.actionSet_Custom_Milling)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuCorrelation.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuTesting.menuAction())

        #self.actionTestbutton3.triggered.connect(self.roughprotocol)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        '''
        GUI Translate as created by pyuic5
        '''
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Serial FIB"))
        self.label.setText(_translate("MainWindow", "Lamellae"))
        self.Button_AddPosition.setText(_translate("MainWindow", "Add Position"))
        self.Button_SaveImageForAlignment.setText(_translate("MainWindow", "Save Image for Alignment"))
        self.Button_SavePatterns.setText(_translate("MainWindow", "Save Patterns"))
        self.Button_UpdateZ.setText(_translate("MainWindow", "Update Z"))
        self.Button_GoToXYZ.setText(_translate("MainWindow", "Go To XYZ"))
        self.Button_GoToXY.setText(_translate("MainWindow", "Go To XY"))
        self.Button_DeleteItem.setText(_translate("MainWindow", "Delete Item"))
        self.label_2.setText(_translate("MainWindow", "Main Functions"))
        self.Button_SetOutputDirectory.setText(_translate("MainWindow", "Set Output Directory"))
        self.Button_TakeImageIB.setText(_translate("MainWindow", "Take Image IB"))
        self.Button_TakeImageEB.setText(_translate("MainWindow", "Take Image EB"))
        self.Button_RunRoughProtocol.setText(_translate("MainWindow", "Run Rough Protocol"))
        self.Button_RunFineProtocol.setText(_translate("MainWindow", "Run Fine Protocol"))
        self.Button_RunTrenchMilling.setText(_translate("MainWindow", "Run Trench Milling"))
        #self.Button_RunRoughMilling.setText(_translate("MainWindow", "Run Rough Milling"))
        #self.Button_RunFineMilling.setText(_translate("MainWindow", "Run Fine Milling"))
        self.Button_LoadCorrelationImages.setText(_translate("MainWindow", "Load Correlation Images"))
        self.label_3.setText(_translate("MainWindow", "Alignment Image"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Label"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "X"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Y"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Z"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "R"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "T"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Alignment Image?"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Patterns?"))
        self.label_4.setText(_translate("MainWindow", "Error Log"))
        self.label_5.setText(_translate("MainWindow", "Image Buffer"))
        self.comboBox.setItemText(0, _translate("MainWindow", "green"))
        self.comboBox.setItemText(1, _translate("MainWindow", "magenta"))
        self.comboBox.setItemText(2, _translate("MainWindow", "cyan"))
        self.comboBox.setItemText(3, _translate("MainWindow", "yellow"))
        self.comboBox.setItemText(4, _translate("MainWindow", "red"))
        self.comboBox.setItemText(5, _translate("MainWindow", "white"))
        self.checkBox_fluo.setText(_translate("MainWindow", "Fluorescence Overlay"))
        self.label_6.setText(_translate("MainWindow", "Positions"))
        self.label_7.setText(_translate("MainWindow", "Custom Functions"))
        self.Button_SetSAVparameters.setText(_translate("MainWindow", "Set SAV parameters"))
        self.Button_RunVolumeImaging.setText(_translate("MainWindow", "Run Volume Imaging"))
        self.Button_RunCustomProtocol.setText(_translate("MainWindow", "Run Custom Protocol"))
        self.Button_RunCustomPatternfile.setText(_translate("MainWindow", "Run Custom Patternfile"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuCorrelation.setTitle(_translate("MainWindow", "Correlation"))
        self.menuTesting.setTitle(_translate("MainWindow", "Testing"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionOpen.setText(_translate("MainWindow", "Open New"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionSave_Session.setText(_translate("MainWindow", "Save Session"))
        self.actionLoad_Session.setText(_translate("MainWindow", "Load Session"))
        self.actionClose_2.setText(_translate("MainWindow", "Close"))
        self.actionOpen_Scripting.setText(_translate("MainWindow", "Open Scripting"))
        self.actionScripting.setText(_translate("MainWindow", "ScriptEditor"))
        self.actionOpen_PatternDesigner.setText(_translate("MainWindow", "PatternDesigner"))
        self.actionCompute_FluoProjection.setText(_translate("MainWindow", "Compute FluoProjection"))
        self.actionLoad_Fluo_Projection.setText(_translate("MainWindow", "Load Fluo Projection"))
        self.actionLoad_Correlation_Images.setText(_translate("MainWindow", "Load Correlation Images"))
        self.actionTestbutton1.setText(_translate("MainWindow", "Draw Corr Pattern"))
        self.actionTestbutton2.setText(_translate("MainWindow", "Align to Image Buffer"))
        self.actionTestbutton3.setText(_translate("MainWindow", "Change Alignment Current"))
        self.actionTestbutton4.setText(_translate("MainWindow", "Test Write Patterns"))
        self.actionTestbutton5.setText(_translate("MainWindow", "Testbutton5"))
        self.actionSaveSettings.setText(_translate("MainWindow", "SaveSettings"))
        self.actionLoadSettings.setText(_translate("MainWindow", "LoadSettings"))
        self.actionVolumeDesigner.setText(_translate("MainWindow", "VolumeDesigner"))
        self.actionLamellaDesigner.setText(_translate("MainWindow", "LamellaDesigner"))
        self.actionSet_Output_Directory.setText(_translate("MainWindow", "Set Output Directory"))
        self.actionSet_SAV_parameters.setText(_translate("MainWindow", "Set SAV parameters"))
        self.actionSet_Output_Directory_2.setText(_translate("MainWindow", "Set Output Directory"))
        self.actionSet_Rough_Mill_protocol.setText(_translate("MainWindow", "Set Rough Mill protocol"))
        self.actionSet_Fine_Mill_protocol.setText(_translate("MainWindow", "Set Fine Mill protocol"))
        self.actionSet_Custom_Protocol.setText(_translate("MainWindow", "Set Custom Protocol"))
        self.actionSet_Custom_Milling.setText(_translate("MainWindow", "Set Custom Milling"))


##################################
####  BUTTON DEFINITIONS #########
##################################





        # Testcase defintion
        self.testCase=False
        self.ktest=0
        

        # IMAGE BUFFER DEFINE
        self.ImageBufferImages=[]
        #self.ImageBufferHandle=0

        '''
        Whenever an image from the image buffer is loaded by double clicking
        saving of the patterns is triggered into the pattern_dict as well as 
        showInGraphview, which takes the current ImageBufferHandle as changed by 
        double clicking and load that image into the GraphView
        '''
        self.ImageBuffer.itemDoubleClicked.connect(self.savePatterns)
        self.ImageBuffer.itemDoubleClicked.connect(self.showInGraphview)

        self.pattern_root=""



        '''
        ShortCut definitions for deleting patterns and fullscreenmode
        '''
        #### Delete Option ####
        self.shortcut_backspace = QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), MainWindow)
        self.shortcut_backspace.activated.connect(self.pattern_delete)

        self.shortcut_delete = QtWidgets.QShortcut(QtGui.QKeySequence("Del"), MainWindow)
        self.shortcut_delete.activated.connect(self.pattern_delete)

        self.shortcut_fullscreen_graphview=QtWidgets.QShortcut(QtCore.Qt.Key_F5,MainWindow)
        self.shortcut_fullscreen_graphview.activated.connect(self.toggleFullScreen)

        self.shortcut_F6=QtWidgets.QShortcut(QtCore.Qt.Key_F6,MainWindow)
        self.shortcut_F6.activated.connect(self.key_F6)

        self.shortcut_copy=QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+c"),MainWindow)
        self.shortcut_copy.activated.connect(self.button_savePatterns)
        self.shortcut_copy.activated.connect(self.copy_patterns)

        self.shortcut_paste=QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+v"),MainWindow)
        self.shortcut_paste.activated.connect(self.paste_patterns)        


        #TextLogger
        sys.stdout = Stream(newText=self.onUpdateText)



        '''
        Button Definitions
        '''

        # Button_Add_Position
        self.Button_AddPosition.pressed.connect(self.AddPosition)
        self.Button_AddPosition.pressed.connect(self.addRow)

        # Button_DeleteItem
        self.Button_DeleteItem.pressed.connect(self.removeRow)

        # Button_GoToXYZ
        self.Button_GoToXYZ.pressed.connect(self.GoToXYZ)

        # Button_GoToXY
        self.Button_GoToXY.pressed.connect(self.GoToXY)

        # Button Take Image IB
        self.Button_TakeImageIB.pressed.connect(self.button_savePatterns)
        self.Button_TakeImageIB.pressed.connect(self.button_take_image_IB)
        

        # Button Take Image EB
        self.Button_TakeImageEB.pressed.connect(self.button_take_image_EB)

        # Button Save Image for Alignment
        self.Button_SaveImageForAlignment.pressed.connect(self.SaveImageForAlignment)


        # Button Save Patterns
        self.Button_SavePatterns.pressed.connect(self.button_savePatterns)
        

        # Button Load Correlated Image
        self.Button_LoadCorrelationImages.pressed.connect(self.load_correlated_image)


        # Button Set Output Directory
        self.Button_SetOutputDirectory.pressed.connect(self.define_directory)


        self.Button_UpdateZ.pressed.connect(self.UpdateZ)

        self.Button_SetSAVparameters.pressed.connect(self.define_SAVparams)

        # Thread based implementations Button definition
        self.Button_RunRoughProtocol.pressed.connect(self.roughprotocol)
        self.Button_RunFineProtocol.pressed.connect(self.fineprotocol)
        self.Button_RunVolumeImaging.pressed.connect(self.volumeimaging)
        self.Button_RunCustomProtocol.pressed.connect(self.customprotocol)
        self.Button_RunTrenchMilling.pressed.connect(self.trenchmill)
        self.Button_RunCustomPatternfile.pressed.connect(self.custompatternfilerun)


        '''
        File Tab
        '''
        # Button Save Session
        self.actionSave_Session.triggered.connect(self.save_session)

        # Button Load Session
        self.actionLoad_Session.triggered.connect(self.load_session)

        # Button New Session
        self.actionOpen.triggered.connect(self.new_session)


        '''
        Tools Tab
        '''

        # Button Open Scripting
        self.actionScripting.triggered.connect(self.open_scripting)

        # Button Open PatternEditor
        self.actionOpen_PatternDesigner.triggered.connect(self.open_patterneditor)

        self.actionVolumeDesigner.triggered.connect(self.open_volumedesigner)
        self.actionLamellaDesigner.triggered.connect(self.open_lamelladesigner)

        '''
        Fluorescence Tab
        '''
        self.actionLoad_Correlation_Images.triggered.connect(self.load_correlated_image)
        self.actionCompute_FluoProjection.triggered.connect(self.compute_fluo_proj)
        self.actionLoad_Fluo_Projection.triggered.connect(self.load_fluo_proj)

        self.checkBox_fluo.stateChanged.connect(self.overlay_fluo)
        self.comboBox.currentIndexChanged.connect(self.overlay_fluo)


        '''
        Settings Tab
        '''
        self.actionSet_Output_Directory.triggered.connect(self.define_directory)
        self.actionSet_Output_Directory_2.triggered.connect(self.define_directory)
        self.actionSet_SAV_parameters.triggered.connect(self.define_SAVparams)
        self.actionSet_Rough_Mill_protocol.triggered.connect(self.define_roughmillprotocol)
        self.actionSet_Fine_Mill_protocol.triggered.connect(self.define_finemillprotocol)
        self.actionSet_Custom_Protocol.triggered.connect(self.define_custommillprotocol)
        self.actionSet_Custom_Milling.triggered.connect(self.define_custompatternfile)

        self.actionSaveSettings.triggered.connect(self.save_settings)
        self.actionLoadSettings.triggered.connect(self.load_settings)


        


        '''
        TestButtons
        '''


        # Button for Testing

        self.actionTestbutton1.triggered.connect(self.draw_corr_pattern)
        self.actionTestbutton2.triggered.connect(self.align_to_item)
        self.actionTestbutton3.triggered.connect(self.set_alignment_current)
        self.actionTestbutton4.triggered.connect(self.write_patterns)
        self.actionTestbutton5.triggered.connect(self.testWidgets)




        #### Graphics Viewer
    
        self.graphicsView.aspectRatioMode = QtCore.Qt.KeepAspectRatio



##################################
# CODE:Button_take_image_IB      #
##################################

    def button_take_image_IB(self):
        '''
        Button to take an image at current mag etc. using the ion beam
        Uses the driver function take_image_IB()

        Input: None
        Output: None
        Action: Addition of image to ImageBuffer, showing Image in GraphicsView
        '''

        # ImageBufferHandle is set to the last image as given by the amount of images in the ImageBuffer
        self.ImageBufferHandle=self.ImageBuffer.count()

        # Image is taken using the Driver function and added as last element in the ImageBuffer
        img=scope.take_image_IB()
        numRows = self.ImageBuffer.count()
        self.ImageBuffer.addItem(str(numRows) + " (IB Image)")


        # Image Scene is grabed in order to set a new scene in the GraphicsView
        scene=self.get_scene()
        scene.clear()
        self.graphicsView.setScene(scene)



        # Check if image was taken, else add testimage
        if self.testCase==True:
            self.ktest=self.ktest+1
            if img==():
                if self.ktest%2==0:
                    array=testimage.data
                    self.ImageBufferImages.append(testimage)
                else:
                    array=testimage2.data
                    self.ImageBufferImages.append(testimage2) 
                #print("Bla")  
            else:
                array=img.data
                self.ImageBufferImages.append(img)
        else:
            if img==():
                print("No Microscope connected!")
                return()
            else:
                array=img.data
                self.ImageBufferImages.append(img)




        ### Convert 16 bit image to 8 bit to show it in the GraphicsView
        #array8u=cv2.convertScaleAbs(array, alpha=(255.0/65535.0))
        img_8bit=np.uint8(array)
        img_8bit = cv2.cvtColor(img_8bit,cv2.COLOR_BGR2GRAY)
        print(np.shape(img_8bit))

        
        ### Changed as colored picture comes from the Zeiss API
        #height,width=np.shape(img_8bit)
        height,width=np.shape(img_8bit)[0],np.shape(img_8bit)[1]
        qImg=QtGui.QImage(img_8bit, width, height, QtGui.QImage.Format_Grayscale8)
        pixmapImg=QtGui.QPixmap.fromImage(qImg)
        

        # Set scene size to image size.
        self.graphicsView.setSceneRect(QtCore.QRectF(pixmapImg.rect()))  
        self.graphicsView.fitInView(self.graphicsView.sceneRect(),self.graphicsView.aspectRatioMode)
        w2=self.graphicsView.sceneRect().width()
        h2=self.graphicsView.sceneRect().height()

        #Add Image as pixmap to scene
        scene.addPixmap(pixmapImg)


        # Update SceneBuffer
        self.scene=scene
        self.sceneBuffer.append(self.scene)

        # New Image cannot have fluorescence information, thus set checkBox to false
        self.checkBox_fluo.setChecked(False)
        
        # Adjust ImageBufferHandle to new Image
        self.ImageBufferHandle=self.ImageBuffer.count()+1
        return()
    
##################################
# /CODE:Button_take_image_IB     #
##################################

    def load_images(self,image):
        '''
        Same Setup as take_image_IB only that an image is loaded from a file

        Input: Image as .tif
        Output: None
        Action: Addition of image to ImageBuffer, showing Image in GraphicsView
        '''
        
        numRows = self.ImageBuffer.count()
        self.ImageBuffer.addItem(str(numRows) + " (IB Image)")
        scene=self.get_scene()
        scene.clear()
        self.graphicsView.setScene(scene)

        # Check if image was taken, else add testimage
        
        if image==():
            print("No Microscope connected!")
            return()
        else:
            array=image.data
            self.ImageBufferImages.append(image)


        ### Convert 16 bit image to 8 bit to show it in the GrahpicsView
        array8u=cv2.convertScaleAbs(array, alpha=(255.0/65535.0))
        img_8bit=np.uint8(array)
        img_8bit = cv2.cvtColor(img_8bit,cv2.COLOR_BGR2GRAY)

        ### Changed as colored picture comes from the Zeiss API
        #height,width=np.shape(img_8bit)
        height,width=np.shape(img_8bit)[0],np.shape(img_8bit)[1]
        qImg=QtGui.QImage(img_8bit, width, height, QtGui.QImage.Format_Grayscale8)
        pixmapImg=QtGui.QPixmap.fromImage(qImg)
        
        # Set scene size to image size.
        self.graphicsView.setSceneRect(QtCore.QRectF(pixmapImg.rect()))  
        self.graphicsView.fitInView(self.graphicsView.sceneRect(),self.graphicsView.aspectRatioMode)
        w2=self.graphicsView.sceneRect().width()
        h2=self.graphicsView.sceneRect().height()
        
        #Add Image as pixmap to scene
        scene.addPixmap(pixmapImg)

        # Update SceneBuffer
        self.scene=scene
        self.sceneBuffer.append(self.scene)


        # New Image cannot have fluorescence information, thus set checkBox to false
        self.checkBox_fluo.setChecked(False)


        return()




##################################
# CODE:Button_take_image_EB      #
##################################


    def button_take_image_EB(self):

        '''
        Button to take an image at current mag etc. using the electron beam
        Uses the driver function take_image_EB()

        Input: None
        Output: None
        Action: Addition of image to ImageBuffer, showing Image in GraphicsView
        '''

        img=scope.take_image_EB()
        numRows = self.ImageBuffer.count()
        self.ImageBuffer.addItem(str(numRows) + " (EB Image)")
        scene=self.get_scene()
        scene.clear()
        self.graphicsView.setScene(scene)
        self.ImageBufferHandle=numRows

        # Check if image was taken, else add testimage
        if self.testCase==True:
            self.ktest=self.ktest+1
            if img==():
                if self.ktest%2==0:
                    array=testimage.data
                    self.ImageBufferImages.append(testimage)
                else:
                    array=testimage2.data
                    self.ImageBufferImages.append(testimage2)    
            else:
                array=img.data
                self.ImageBufferImages.append(img)
        else:
            if img==():
                print("No Microscope connected!")
                return()
            else:
                array=img.data
                self.ImageBufferImages.append(img)


        ### Convert 16 bit image to 8 bit to show it in the GrahpicsView
        array8u=cv2.convertScaleAbs(array, alpha=(255.0/65535.0))
        img_8bit=np.uint8(array)
        img_8bit = cv2.cvtColor(img_8bit,cv2.COLOR_BGR2GRAY)
        height,width=np.shape(img_8bit)
        qImg=QtGui.QImage(img_8bit, width, height, QtGui.QImage.Format_Grayscale8)
        pixmapImg=QtGui.QPixmap.fromImage(qImg)
        
        # Set scene size to image size.
        self.graphicsView.setSceneRect(QtCore.QRectF(pixmapImg.rect()))  
        self.graphicsView.fitInView(self.graphicsView.sceneRect(),self.graphicsView.aspectRatioMode)
        
        #Add Image as pixmap to scene
        scene.addPixmap(pixmapImg)
        
        # Update SceneBuffer
        self.scene=scene
        self.sceneBuffer.append(self.scene)
        self.checkBox_fluo.setChecked(False)
        return()

##################################
# /CODE:Button_take_image_EB     #
##################################



##################################
# CODE:Button_run_rough_mill     #
##################################



    def Signal_Done(self,result):
        print("Result: "+result)

        self.progressDialog.close()
        return()

    




    


    def showInGraphview(self):
        #self.savePatterns()
        try:
            number=self.ImageBuffer.currentItem().text().split(" ")[0]
        except:

            number=0
        self.ImageBufferHandle=number

        scenes=self.get_scenebuffer()

        try:
            scene=scenes[int(number)]
        except:
            scene=self.get_scene()

        pattern_list=[]

        try:

            for i in self.pattern_dict[self.ImageBufferHandle]:
                #print(i.type())

                ### Check if item is Rectangle
                #if i.type()==3:
                #print(i)
                pattern_list.append(i)
            if self.checkBox_fluo.isChecked():
                if self.CFproj is not None:
                    height, width = np.shape(self.CFproj)
                    projColor = np.array(self.colordict[self.comboBox.currentText()],dtype=np.uint8)
                    fillImg = np.tile(projColor,[height,width,1])
                    rgbaImg = np.dstack((fillImg,self.CFproj))
                    qImg = QtGui.QImage(rgbaImg, width, height, QtGui.QImage.Format_RGBA8888)
                    pixmapImg = QtGui.QPixmap.fromImage(qImg)
                    self.pointer_projpixmap = scene.addPixmap(pixmapImg)
        except KeyError:
            #print(self.pattern_dict[self.get_number_imageBuffer()])
            print("Opening Image, No Patterns detected")
            
        scene.clear()
        self.graphicsView.setScene(scene)

        try:
            array=self.ImageBufferImages[int(number)].data

            array8u=cv2.convertScaleAbs(array, alpha=(255.0/65535.0))
        
            img_8bit=np.uint8(array)
            try:
                img_8bit = cv2.cvtColor(img_8bit,cv2.COLOR_BGR2GRAY)
            except:
                print("Couldn't convert colored image, probably already grayscale")
            ### Changed as colored picture comes from the Zeiss API
            #height,width=np.shape(img_8bit)
            height,width=np.shape(img_8bit)[0],np.shape(img_8bit)[1]

            qImg=QtGui.QImage(img_8bit, width, height, QtGui.QImage.Format_Grayscale8)
            pixmapImg=QtGui.QPixmap.fromImage(qImg)
        

            self.graphicsView.setSceneRect(QtCore.QRectF(pixmapImg.rect()))  # Set scene size to image size.
            self.graphicsView.fitInView(self.graphicsView.sceneRect(),self.graphicsView.aspectRatioMode)
            scene.addPixmap(pixmapImg)
            for i in pattern_list:

                scene.addItem(Rectangle(i.x,i.y,i.h,i.w))

            self.sceneBuffer[int(number)]=scene

        except:
            
            print("ERROR")

        if str(number) in self.corrspots:
            #print("Correlation spots already exist!")
            nonzeros=self.corrspots[str(number)]
            xx=nonzeros[1]
            yy=nonzeros[0]
            corr=np.zeros(np.shape(array))
            for i in range(len(xx)):
                x=int(xx[i])
                y=int(yy[i])
                corr[x,y]=255
                rad = 0.5
                scene.addEllipse(y-rad,x-rad,rad*2.0,rad*2.0,QtGui.QPen(QtCore.Qt.green, 5),QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.CrossPattern))
        else:
            print("No Correlation spots detected")


    
        

########################################
# /CODE:ImageBuffer Left Double Click  #
########################################




##################################
# CODE:TextLog                   #
##################################

    def onUpdateText(self, text):
        now = datetime.datetime.now()
        cursor = self.plainTextEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        if not bool(str(text)):
            pass
        else:
            cursor.insertText(now.strftime("%Y-%m-%d %H:%M ")+' : '+text+'\n')
            self.plainTextEdit.setTextCursor(cursor)
            self.sysout.write(now.strftime("%Y-%m-%d %H:%M ")+' : '+text+'\n')



##################################
# /CODE:TextLog                  #
##################################



##################################
# CODE:Button_AddPosition        #
##################################

    def AddPosition(self):
        #print(f)
        try:
            stagepos=scope.getStagePosition()
            print("Position Added")
            
            self.StagePos=stagepos
        except:
            print("Error, No Microscope Connected")
            stagepos=scope.getStagePosition()
            self.StagePos=stagepos

    def UpdateZ(self):
        try:
            numRows = self.tableWidget.rowCount()
            row_list=[index.row() for index in self.tableWidget.selectedIndexes()]
            stagepos = scope.getStagePosition()
            self.StagePos = stagepos
            if len(row_list)==1:
                row=row_list[0]
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.StagePos['z'])))
            else:
                printed("You selected more than 1 row")

        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())

        return()
    def addRow(self):
        try:
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(numRows)))
            self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.StagePos['x'])))
            self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(str(self.StagePos['y'])))
            self.tableWidget.setItem(numRows, 3, QtWidgets.QTableWidgetItem(str(self.StagePos['z'])))
            self.tableWidget.setItem(numRows, 4, QtWidgets.QTableWidgetItem(str(self.StagePos['r'])))
            self.tableWidget.setItem(numRows, 5, QtWidgets.QTableWidgetItem(str(self.StagePos['t'])))

        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
    def addRow_load(self,label,x,y,z,r,t,alignment_image="",patterns=""):
        try:
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(label))
            self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(x))
            self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(y))
            self.tableWidget.setItem(numRows, 3, QtWidgets.QTableWidgetItem(z))
            self.tableWidget.setItem(numRows, 4, QtWidgets.QTableWidgetItem(r))
            self.tableWidget.setItem(numRows, 5, QtWidgets.QTableWidgetItem(t))
            self.tableWidget.setItem(numRows, 6, QtWidgets.QTableWidgetItem(alignment_image))
            self.tableWidget.setItem(numRows, 7, QtWidgets.QTableWidgetItem(patterns))
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())

##################################
# /CODE:Button_AddPosition       #
##################################




##################################
# CODE:Button_DeleteItem         #
##################################
    def removeRow(self):
        try:
            row_list=[index.row() for index in self.tableWidget.selectedIndexes()]
            row_list = list(dict.fromkeys(row_list))
            for number in row_list[::-1]:
                self.tableWidget.removeRow(number)
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
            
##################################
# /CODE:Button_DeleteItem        #
##################################


##################################
# CODE:Button_GoToXY             #
##################################
    def GoToXY(self):
        try:
            row_list=[index.row() for index in self.tableWidget.selectedIndexes()]
            if len(row_list)==0:
                print("No Position selected")
            if len(row_list)>1:
                print("You selected multiple Stage Positions")
            if len(row_list)==1:
                row=row_list[0]
                print("Moving to Stage Position: "+self.tableWidget.item(row,0).text())
                label=self.tableWidget.item(row,0).text()
                x=float(self.tableWidget.item(row,1).text())
                y=float(self.tableWidget.item(row,2).text())
                stagepos={'label':label,'x':x,'y':y}
                try:
                    origin=scope.getStagePosition()
                    z=origin['z']
                    t=origin['t']
                    r=origin['r']
                    stagepos.update({'z':z,'t':t,'r':r})
                    if [x,y] == ['0','0']:
                        print("ERROR: Invalid Stage Position")
                    else:
                        try:
                            print("I tried to move the stage")
                            scope.moveStageAbsolute(stagepos)
                        except:
                            print("Error, No Microscope Connected")
                except:
                    print("No Microscope Connected")
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
            

##################################
# /CODE:Button_GoToXY            #
##################################

##################################
# CODE:Button_GoToXYZ            #
##################################
    def GoToXYZ(self):
        try:
            row_list=[index.row() for index in self.tableWidget.selectedIndexes()]
            if len(row_list)==0:
                print("No Position selected")
            if len(row_list)>1:
                print("You selected multiple Stage Positions")
            if len(row_list)==1:
                row=row_list[0]
                #print(row)
                #self.tableWidget.selectRow(row)
                print("Moving to Stage Position: "+self.tableWidget.item(row,0).text())
                label=self.tableWidget.item(row,0).text()
                x=float(self.tableWidget.item(row,1).text())
                y=float(self.tableWidget.item(row,2).text())
                z=float(self.tableWidget.item(row,3).text())
                r=float(self.tableWidget.item(row,4).text())
                t=float(self.tableWidget.item(row,5).text())
                stagepos={'label':label,'x':x,'y':y,'z':z,'t':t,'r':r}

                if [x,y,z,t,r] == ['0','0','0','0','0']:
                    print("ERROR: Invalid Stage Position")
                else:
                    try:
                        scope.moveStageAbsolute(stagepos)
                    except:
                        print("ERROR: No Microscope Connected")
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())

##################################
# /CODE:Button_GoToXYZ           #
##################################
        
####################################
# CODE:Button_SaveImageForAlignment#
####################################

    def SaveImageForAlignment(self):
        number=self.ImageBufferHandle
        try:
            alignment_image=self.ImageBufferImages[int(number)]
        except:
            print("No Images taken!")
            return()
        # Find Current selected and add to the Table
        row_list=[index.row() for index in self.tableWidget.selectedIndexes()]
        if len(row_list)==0:
            print("No Position selected")
        if len(row_list)>1:
            print("You selected multiple Stage Positions")
        if len(row_list)==1:
            row=row_list[0]
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(number))
        else:
            self.tableWidget.setItem(0, 6, QtWidgets.QTableWidgetItem(number))

        ### One needs to check whether the pic is IB or EB here! Only IB for alignment
        return()

####################################
#/CODE:Button_SaveImageForAlignment#
####################################


####################################
#CODE:Button_SavePatterns          #
####################################
    def savePatterns(self):
        print("Saving Patterns ...")

        number=self.ImageBufferHandle


        self.graphicsView.items()
        scene=self.graphicsView.scene
        rect_list=[]
        for i in self.graphicsView.items():
            #print(i)
            #print(i.type())
            ### Check if item is Rectangle
            if i.type()==3:

                pos=i.pos()
                x=pos.x()
                y=pos.y()

                shape=i.shape()
                boundingRect=shape.boundingRect()
                w=boundingRect.width()-2
                h=boundingRect.height()-2
                rect_list.append(Rectangle(x,y,h,w))
        self.pattern_dict.update({number : rect_list})
        return()

    def button_savePatterns(self):
        print("Saving Patterns ...")

        number=self.ImageBufferHandle
        if number==None:
            number=0


        # Find Current selected and add to the Table
        row_list=[index.row() for index in self.tableWidget.selectedIndexes()]
        if len(row_list)==0:
            print("No Position selected")
        if len(row_list)>1:
            print("You selected multiple Stage Positions")
        if len(row_list)==1:
            row=row_list[0]
            self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(number))
        self.graphicsView.items()
        scene=self.graphicsView.scene
        rect_list=[]
        for i in self.graphicsView.items():
            #print(i.type())
            ### Check if item is Rectangle
            if i.type()==3:
                pos=i.pos()
                x=pos.x()
                y=pos.y()
                shape=i.shape()
                boundingRect=shape.boundingRect()
                w=boundingRect.width()-2
                h=boundingRect.height()-2
                rect_list.append(Rectangle(x,y,h,w))
        self.pattern_dict.update({number : rect_list})
        return()
    
    def write_patterns(self):
        directory=self.output_dir+'/'
        for i in range(0,self.tableWidget.rowCount()):
            #print(i)
            label=self.tableWidget.item(i,0).text()
            lamella_dir=directory+label+'/'
            try:
                os.mkdir(lamella_dir)
            except:
                print("Directory "+label+" already exists")
            alignment_image_number=int(self.tableWidget.item(i,6).text())
            alignment_image=self.ImageBufferImages[alignment_image_number]
            pixel_size=alignment_image.metadata.binary_result.pixel_size.x
            image_shape=np.shape(alignment_image.data)

            pattern_number=int(self.tableWidget.item(i,7).text())
            #print(pattern_number)
            if i==None:
                continue
            else:
                #try:
                patterns=self.pattern_dict[str(pattern_number)]
                patterns=sorted(patterns, key=lambda pattern: pattern.y)
                name_list=['tp','lamella','bp']
                num=0
                print(patterns)
                for i in patterns:
                    
                    pattern_filename=str(label)+'_'+str(name_list[num])+".ptf"
                    num=num+1
                    pos=i.pos()
                    shape=i.shape()
                    boundingRect=shape.boundingRect()
                    w=boundingRect.width()
                    h=boundingRect.height()
                    #x=(pos.x()-image_shape[1]/2)+h/2
                    #y=-w/2-(pos.y()-image_shape[0]/2)
                    #try:
                    x=(pos.x()-image_shape[1]/2)
                    y=-(pos.y()-image_shape[0]/2)-w
                    pattern=scope.create_pattern(x*pixel_size,y*pixel_size,w*pixel_size,h*pixel_size)
                    print(pattern)
                    scope.save_pattern(lamella_dir,pattern_filename,pattern)
                        #except:
                            # print("Error in Pattern Writing: No Microscope connected?")
                            # #pattern=Pattern(0,0,0,0,0,'UP')
                            # from src.Zeiss.CrossbeamDriver import DummyPattern
                            # pattern=DummyPattern()
                            # scope.save_pattern(lamella_dir,pattern_filename,pattern)
                            
                #except KeyError:
                #    print('No Patterns were found')
                


####################################
#/CODE:Button_SavePatterns         #
####################################

####################################
# CODE: Alignment functions        #
####################################
    def align_to_item(self):

        try:
            img=self.ImageBufferImages[int(self.ImageBufferHandle)]
        except:
            print("No Image selected. Please select an image from the Image Buffer")

        try:
            scope.align(img,beam='ION',current=scope.get_current())
            #print(scope.get_current())
        except:
            print("Something went wrong in the alignment. Please let us know!")
            print(sys.exc_info())
        return()

    def set_alignment_current(self):

        #while not (isinstance(param.nX, float):
        ans, ok = QtWidgets.QInputDialog.getText(None, 'Missing Parameters', ''.join(
            ['Please specify the alignment current in pA']))
        if ok:
            try:
            #print(ans)
            #current = [float(a.strip()) for a in ans.split(',')]
                scope.alignment_current = float(ans)*1.0e-12
            except:
                pass
        else:
            #scope.alignment_current=float(10*1.0e-12)
            return()
        return()

####################################
#/CODE: Alignment functions        #
####################################

####################################
# CODE:Correlative mill functions  #
####################################
    def load_correlated_image(self):
        try:
            imgfile, _ = QtWidgets.QFileDialog.getOpenFileName(None, "IB image before correlation",self.output_dir,"Images (*.tif)")
            print(imgfile)
            self.checkBox_fluo.setChecked(False)
            img=DummyAdorned()
            img.load(imgfile)
            #img=DummyAdorned.load(imgfile)
            numRows = self.ImageBuffer.count()
            self.ImageBuffer.addItem(str(numRows) + " (IB Image)")
            scene=self.get_scene()
            scene.clear()
            self.graphicsView.setScene(scene)
            scene.clear()

            array=img.data

            img_8bit=np.uint8(array)
            #img_8bit = cv2.cvtColor(img_8bit,cv2.COLOR_BGR2GRAY)
            img_copy=img
            img_copy.data=img_8bit
            self.ImageBufferImages.append(img_copy)

            if img.bit_depth == 8:
                qImg=QtGui.QImage(img.data.copy(), img.width, img.height, img.width, QtGui.QImage.Format_Grayscale8)
            elif img.bit_depth == 16:
                #qImg=QtGui.QImage(img.data.copy(), img.width, img.height, img.width*2, QtGui.QImage.Format_Grayscale16)
                qImg=QtGui.QImage(img.data.copy(), img.width, img.height, img.width*1, QtGui.QImage.Format_Grayscale8)
                #img8=(img.data/256).astype('uint8')
                #qImg=QtGui.QImage(img8.data.copy(), img.width, img.height, img.width, QtGui.QImage.Format_Grayscale8)
            elif img.bit_depth == 24:
                qImg=QtGui.QImage(img.data.copy(), img.width, img.height, img.width*3, QtGui.QImage.Format_RGB888)
                #qImg=QtGui.QImage(img.data.copy(), img.width, img.height, img.width*3, QtGui.QImage.Format_Grayscale8)
            else:
                qImg=QtGui.QImage(img.data.copy(), img.width, img.height, img.width, QtGui.QImage.Format_Grayscale8)
            pixmapImg=QtGui.QPixmap.fromImage(qImg)
        
            self.graphicsView.setSceneRect(QtCore.QRectF(pixmapImg.rect()))  # Set scene size to image size.
            self.graphicsView.fitInView(self.graphicsView.sceneRect(),self.graphicsView.aspectRatioMode)
            w2=self.graphicsView.sceneRect().width()
            h2=self.graphicsView.sceneRect().height()
            #print("aspect ratio is",w2/width)
        
            scene.addPixmap(pixmapImg)

            #try:
            corrfile, _ = QtWidgets.QFileDialog.getOpenFileName(None, "3DCT text output", self.output_dir, "Text files(*.txt)")
            param = Param3D(corrfile)
            # corr=np.zeros(np.shape(array))
            print(param.xx)
            for i in range(len(param.xx)):
                x=int(param.xx[i])
                y=int(param.yy[i])
                # corr[y,x]=255
                #self.graphicsView.paintpoint(x,y)
                rad = 0.5
                scene.addEllipse(x-rad,y-rad,rad*2.0,rad*2.0,QtGui.QPen(QtCore.Qt.green, 5),QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.CrossPattern))
            if str(numRows) in self.corrspots:
                print("Correlation spots already exist!")
            else:
            #    self.corrspots.update({str(numRows):corr_list})
                nonzeros=[param.xx,param.yy]
                self.corrspots.update({str(numRows):nonzeros})
                #print(self.corrspots)
            #except:
            #    print("Incorrect or no text output specified")

            self.scene=scene
            self.sceneBuffer.append(self.scene)


            #except:
            #    print("No adequate Image selected")
        except Exception as inst:
            print("No correlated image file detected or one of the files is corrupt.")
            print(sys.exc_info())
            import traceback
            traceback.print_tb(inst.__traceback__)
        return
    
    def compute_fluo_proj(self):
        try:
            from skimage import io
            # parse 3DCT text output
            corrfile = QtWidgets.QFileDialog.getOpenFileNames(None, "3DCT text output", self.output_dir, "Text files(*.txt)")
            if corrfile == ('', ''):
                return
            param = Param3D(corrfile[0][0])
            # read resliced volume
            imgfile=QtWidgets.QFileDialog.getOpenFileNames(None, "Resliced fluorescence volume",self.output_dir,"Images (*.tif)")
            if imgfile == ('', ''):
                return
            CF = io.imread(imgfile[0][0])
            # calculate, store and write out projection
            self.CFproj = project_3dct.fluorescence_proj_mp(param,CF)
            if self.CFproj is not None:
                io.imsave(self.output_dir + '/' + imgfile[0][0].split('/')[-1].strip(".tif")+"_proj.tif",self.CFproj)
                print("Projection image saved as "+self.output_dir + '/' + imgfile[0][0].split('/')[-1].strip(".tif")+"_proj.tif")
        except:
            print("No file selected or file seems to be corrupt.")
        #   print(sys.exc_info())
        return

    def load_fluo_proj(self):
        from skimage import io
        projfile=QtWidgets.QFileDialog.getOpenFileNames(None, "Resliced fluorescence volume",self.output_dir,"Images (*.tif)")
        if projfile == ('', ''):
                return
        try:
            
            img = io.imread(projfile[0][0])
            if img.ndim==2 and img.dtype==np.dtype('uint8'):
                self.CFproj = img
            else:
                print("Please select an 8-bit 2D image")
        except:
            print("Incorrect file selected")
            print(sys.exc_info())
        return

    # need to uncheck box when showingraphview, load, etc.
    def overlay_fluo(self):
        scene = self.get_scene()
        self.graphicsView.setScene(scene)
        if self.pointer_projpixmap:
            self.showInGraphview()
            self.pointer_projpixmap = None
        if self.checkBox_fluo.isChecked():
            if self.CFproj is not None:
                height, width = np.shape(self.CFproj)
                projColor = np.array(self.colordict[self.comboBox.currentText()],dtype=np.uint8)
                fillImg = np.tile(projColor,[height,width,1])
                rgbaImg = np.dstack((fillImg,self.CFproj))
                qImg = QtGui.QImage(rgbaImg, width, height, QtGui.QImage.Format_RGBA8888)
                pixmapImg = QtGui.QPixmap.fromImage(qImg)
                if scene.items()==[]:
                    self.graphicsView.setSceneRect(QtCore.QRectF(pixmapImg.rect()))  # Set scene size to image size.
                    self.graphicsView.fitInView(self.graphicsView.sceneRect(),self.graphicsView.aspectRatioMode)
                self.pointer_projpixmap = scene.addPixmap(pixmapImg)
        self.scene = scene
        return


    def draw_corr_pattern(self):
        print("drawing_corrpattern")
        number=int(self.ImageBufferHandle)
        try:
            image=self.ImageBufferImages[number]
        except:
            return

        if str(number) in self.corrspots:
            try:
                print("CorrSpot detected")
                #pattern_filename=str(label)+'_'+str(name_list[num])+".ptf"
                image_shape=np.shape(image.data)
                nonzeros=self.corrspots[str(number)]
                xx=nonzeros[0]
                yy=nonzeros[1]
                pixel_size=image.metadata.binary_result.pixel_size[0]
                for i in range(len(xx)):
                    x_py=xx[i]

                    y_py=yy[i]

                    w=1
                    h=100
                    x=(x_py-image_shape[1]/2)+h/2
                    y=-w/2-(y_py-image_shape[0]/2)

                    try:
                        pattern=scope.create_pattern(x*pixel_size,y*pixel_size,w*pixel_size,h*pixel_size)

                    except:
                        print("Creating Pattern ended in error, probably outside FOV")
                        print(sys.exc_info())

            except:
                print("No Corrspots detected.")
                print(sys.exc_info())
        return

####################################
#/CODE:Correlative mill functions  #
####################################

####################################
# CODE:Define buttons              #
####################################

    def define_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Open a folder",self.output_dir)




        try:
            self.sysout = open(self.output_dir + '/' + 'SFIB.log', mode='a')


            scope.define_output_dir(self.output_dir)
            self.output_dir = directory
        except:
            print("Directory not valid!")
        return()

    def define_SAVparams(self):
        from os.path import expanduser
        filename = QtWidgets.QFileDialog.getOpenFileNames(None, "SAV paramsfile",self.output_dir,"SAV_paramsfile (*.spf)")
        try:
            self.SAVparamsfile=filename[0][0]
            scope.define_SAVparams_file(filename[0][0])
        except:
            print('No proper file selected.')
        return()
    
    def define_roughmillprotocol(self):
        from os.path import expanduser
        filename = QtWidgets.QFileDialog.getOpenFileNames(None, "Rough Mill Protocol File",self.output_dir,"Protocol file (*.pro)")
        try:
            self.roughmillprotocol=filename[0][0]
        except:
            print('No proper file selected.')
        return()

    def define_finemillprotocol(self):
        from os.path import expanduser
        filename = QtWidgets.QFileDialog.getOpenFileNames(None, "Fine Mill Protocol File",self.output_dir,"Protocol file (*.pro)")
        try:
            self.finemillprotocol=filename[0][0]
        except:
            print('No proper file selected.')
        return()

    def define_custommillprotocol(self):
        from os.path import expanduser
        filename = QtWidgets.QFileDialog.getOpenFileNames(None, "Fine Mill Protocol File",self.output_dir,"Protocol file (*.pro)")
        try:
            self.custommillprotocol=filename[0][0]
        except:
            print('No proper file selected.')
        return()

    def define_custompatternfile(self):
        from os.path import expanduser
        filename = QtWidgets.QFileDialog.getOpenFileNames(None, "Fine Mill Protocol File",self.output_dir,"Protocol file (*.pf)")
        try:
            self.custompatternfile=filename[0][0]
        except:
            print('No proper file selected.')
        return()


    def save_settings(self):

        try:
            settings_file, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Select SerialFIB Setting File",self.output_dir,"SerialFIB Settings (*.settings)")
            
            settingDict={}
            settingDict.update({'output_dir':self.output_dir,
                                'custommillprotocol':self.custommillprotocol,
                                'custompatternfile':self.custompatternfile,
                                'roughmillprotocol':self.roughmillprotocol,
                                'finemillprotocol':self.finemillprotocol,
                                'SAVparamsfile':self.SAVparamsfile})
        
            with open(settings_file,'w') as output_file:
                for i in settingDict:
                    output_file.write(str(i)+'='+str(settingDict[i])+'\n')

            self.settings = settings_file
        except:
            print(sys.exc_info())

        return()

    def save_settings_func(self,settings_file):

        try:
            #settings_file

            settingDict = {}
            settingDict.update({'output_dir': self.output_dir,
                                'custommillprotocol': self.custommillprotocol,
                                'custompatternfile': self.custompatternfile,
                                'roughmillprotocol': self.roughmillprotocol,
                                'finemillprotocol': self.finemillprotocol,
                                'SAVparamsfile': self.SAVparamsfile})

            with open(settings_file, 'w') as output_file:
                for i in settingDict:
                    output_file.write(str(i) + '=' + str(settingDict[i]) + '\n')

            self.settings = settings_file
        except:
            print(sys.exc_info())

        return ()

    def load_settings(self):
        try:
            settings_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select SerialFIB Setting File",self.output_dir,"SerialFIB Settings (*.settings)")

            with open(settings_file,'r') as input_file:
                lines=input_file.readlines()
                params={}
                for line in lines:
                    param=line.split('=')

                    params.update({param[0]:param[1].rstrip()})


            self.output_dir=params['output_dir']
            self.custommillprotocol=params['custommillprotocol']
            self.custompatternfile=params['custompatternfile']
            self.roughmillprotocol=params['roughmillprotocol']
            self.finemillprotocol=params['finemillprotocol']
            self.SAVparamsfile=params['SAVparamsfile']

            self.settings = settings_file
        except:
            print("Please choose a valid setting file")
            print(sys.exc_info())

        return()

    def load_settings_func(self,file):

        settings_file=file

        with open(settings_file,'r') as input_file:
            lines=input_file.readlines()
            params={}
            for line in lines:
                param=line.split('=')

                params.update({param[0]:param[1].rstrip()})


        self.output_dir=params['output_dir']
        #print(params)
        self.custommillprotocol=params['custommillprotocol']

        self.custompatternfile=params['custompatternfile']
        self.roughmillprotocol=params['roughmillprotocol']
        self.finemillprotocol=params['finemillprotocol']
        #print(self.output_dir)
        #print(self.finemillprotocol)
        self.SAVparamsfile=params['SAVparamsfile']
        scope.define_output_dir(self.output_dir)
        scope.define_SAVparams_file(self.SAVparamsfile)


        return()

####################################
# /CODE:Define buttons             #
####################################


####################################
# CODE: Diverse functions          #
####################################
    def pattern_delete(self):
        item=self.scene.selectedItems()
        number=self.ImageBufferHandle
        for i in item:
            self.scene.removeItem(i)
        return()

    
    def toggleFullScreen(self):
        #return()
        if self.graphicsView.isFullScreen():
            print('Full Screen')
            self.key_F6()

            self.graphicsView.showNormal()
            self.graphicsView.hide()


            
            self.graphicsView=LamellaView(self.centralwidget)
            self.shortcut_backspace = QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self.graphicsView)
            self.shortcut_backspace.activated.connect(self.pattern_delete)
            self.graphicsView.show()
            self.graphicsView.setGeometry(QtCore.QRect(480, 30, 581, 461))
            self.graphicsView.aspectRatioMode = QtCore.Qt.KeepAspectRatio

            self.showInGraphview()

            
            self.graphicsView.show()
            self.overlay_fluo()

        else:
            print("Not Full Screen")
            self.key_F6()

            
            self.graphicsView.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowType_Mask)


            self.graphicsView.showFullScreen()
            

            self.graphicsView.show()
            
            self.key_F6()
            self.overlay_fluo()

    
    def key_F6(self):
        def y_pos(element):
            return(element.y)
        self.savePatterns()
        self.showInGraphview()
        
        number=self.ImageBufferHandle
        image=self.ImageBufferImages[int(number)]
        #try:
        pixel_size=image.metadata.binary_result.pixel_size
        #except:
        #    pixel_size=self.load_image_pixel_size
        #    print("No Pixelsize detected, if image was loaded don't worry!")
        item=self.scene.items()
        patterns=[]

        for i in item:
            if i.type()==3:
                patterns.append(i)


        patterns.sort(key=y_pos)
        num=0
        for i in patterns:
            
            print("Pattern Number "+str(num)+str(" is ")+str(i.w*pixel_size.x*1000000)+" µm wide.")
            num=num+1
            #print(i)

    def save_session(self):
        try:
            if self.settings==r'./custom.settings':
                self.save_settings_func(str(self.output_dir+'/standard.settings'))
        except:
            print("Couldn't save settingsfile. Please let us know! ")
        try:
            session_file=QtWidgets.QFileDialog.getSaveFileName(None, "An IB image before correlation",self.output_dir,"SerialFIBSessions (*.sfs)")
            images=self.ImageBufferImages
            correlation_spots=self.corrspots
            num=int(self.tableWidget.rowCount())
            patterns=self.pattern_dict
            positions=[]
            for i in range(0,num):
                position=[]
                for j in range(0,8):
                    position.append(self.tableWidget.item(i,j).text())
                positions.append(position)

            print(positions)



            pickable_pattern_dict={}

            for i in range(0,len(images)):
                if str(i) in patterns:
                    pattern_list=patterns[str(i)]
                    entry=[]
                    for j in pattern_list:

                        entry.append([j.x,j.y,j.w,j.h])
                    pickable_pattern_dict.update({i:entry})
                else:
                    pickable_pattern_dict.update({i:[]})

            session_dict={'images':images,'corrspots':correlation_spots,'positions':positions,'patterns':pickable_pattern_dict,'settings':self.settings}
            
            with open(session_file[0],'wb') as pickle_out:
                pickle.dump(session_dict,pickle_out)
        except:
            print("No Session file saved!")
        return()
####################################
#/CODE: Diverse functions          #
####################################

####################################
# CODE:Define Run button Functions #
####################################

    def testWidgets(self):
        self.number
        self.threads.append(RoughProtocolThread())
        roughprotocol_thread=self.threads[self.number]
        self.number=self.number+1
        
        self.progressDialog = QtWidgets.QDialog()
        verticalLayout = QtWidgets.QVBoxLayout(self.progressDialog)
        label = QtWidgets.QLabel("Running Rough Protocol",self.progressDialog)
        verticalLayout.addWidget(label)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.progressDialog)
        buttonBox.rejected.connect(self.progressDialog.reject)
        verticalLayout.addWidget(buttonBox)
        roughprotocol_thread.__init__()
        roughprotocol_thread.start()
        if self.progressDialog.exec() == QtWidgets.QDialog.Rejected:
            scope.continuerun=False
            #scope.stop()
            roughprotocol_thread.continuerun=False
            self.progressDialog.close()

            #roughprotocol_thread.stop()
        return()

    def roughprotocol(self):
        self.number
        self.threads.append(RoughProtocolThread())
        roughprotocol_thread=self.threads[self.number]
        self.number=self.number+1
        
        ### COMMENTED OUT FOR DEV ###
        try:

            self.progressDialog = QtWidgets.QDialog()
            verticalLayout = QtWidgets.QVBoxLayout(self.progressDialog)
            label = QtWidgets.QLabel("Running Rough Protocol",self.progressDialog)
            verticalLayout.addWidget(label)
            buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.progressDialog)

            roughprotocol_thread.__init__()
            roughprotocol_thread.start()
            buttonBox.rejected.connect(self.progressDialog.reject)
            verticalLayout.addWidget(buttonBox)
            scope.continuerun = True
            while roughprotocol_thread.isRunning():
                if self.progressDialog.exec() == QtWidgets.QDialog.Rejected:


                    self.Signal_Done('Fine Milling stopped')
                    #scope.stop_patterning()
                    print("Fine Milling has been stopped")

                #
                    while roughprotocol_thread.isRunning():

                        #from autoscript_sdb_microscope_client.enumerations import PatterningState

                        if scope.is_idle():
                            continue
                        else:
                            scope.stop_patterning()

                            scope.stop()
                            scope.continuerun=False
                            roughprotocol_thread.continuerun=False
                            roughprotocol_thread.stop()
                            self.progressDialog.close()

                            print("Operation terminated")

            self.progressDialog.close()

            self.Signal_Done('Fine Mill stopped')
        except:
            print("Something went wrong with the setup.")
            print(sys.exc_info())
        self.progressDialog.close()
        return()

    def fineprotocol(self):
        self.number
        self.threads.append(FineProtocolThread())
        fineprotocol_thread=self.threads[self.number]
        self.number=self.number+1
        try:

            self.progressDialog = QtWidgets.QDialog()
            verticalLayout = QtWidgets.QVBoxLayout(self.progressDialog)
            label = QtWidgets.QLabel("Running Fine Milling",self.progressDialog)
            verticalLayout.addWidget(label)
            buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.progressDialog)

            fineprotocol_thread.__init__()
            fineprotocol_thread.start()
            buttonBox.rejected.connect(self.progressDialog.reject)
            verticalLayout.addWidget(buttonBox)
            scope.continuerun = True
            while fineprotocol_thread.isRunning():
                if self.progressDialog.exec() == QtWidgets.QDialog.Rejected:

                    self.Signal_Done('Fine Milling stopped')

                    print("Fine Milling has been stopped")


                    while fineprotocol_thread.isRunning():

                        from autoscript_sdb_microscope_client.enumerations import PatterningState

                        if scope.is_idle():
                            continue
                        else:
                            scope.stop_patterning()

                            scope.stop()
                            scope.continuerun=False
                            fineprotocol_thread.continuerun=False
                            fineprotocol_thread.stop()
                            self.progressDialog.close()

                            print("Operation terminated")

            self.progressDialog.close()

            self.Signal_Done('Fine Mill stopped')
        except:
            print("Something went wrong with the setup.")
            print(sys.exc_info())
        self.progressDialog.close()
        return()

    def trenchmill(self):
        self.number
        self.threads.append(TrenchMillThread())
        trenchmill_thread=self.threads[self.number]
        self.number=self.number+1
        try:

            self.progressDialog = QtWidgets.QDialog()
            verticalLayout = QtWidgets.QVBoxLayout(self.progressDialog)
            label = QtWidgets.QLabel("Running Trench Milling",self.progressDialog)
            verticalLayout.addWidget(label)
            buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.progressDialog)

            trenchmill_thread.__init__()
            trenchmill_thread.start()
            buttonBox.rejected.connect(self.progressDialog.reject)
            verticalLayout.addWidget(buttonBox)
            scope.continuerun = True
            while trenchmill_thread.isRunning():
                if self.progressDialog.exec() == QtWidgets.QDialog.Rejected:


                    self.Signal_Done('Trench Milling stopped')

                    print("Trench Milling has been stopped")


                    while trenchmill_thread.isRunning():

                        from autoscript_sdb_microscope_client.enumerations import PatterningState

                        if scope.is_idle():
                            continue
                        else:
                            scope.stop_patterning()

                            scope.stop()
                            scope.continuerun=False
                            trenchmill_thread.continuerun=False

                            self.progressDialog.close()

                            print("Operation terminated")

            self.progressDialog.close()

            self.Signal_Done('Trench Mill stopped')
        except:
            print("Something went wrong with the setup.")
            print(sys.exc_info())
        self.progressDialog.close()
        #self.runRoughMill2_Done('Rough Mill stopped')
        return()


    def customprotocol(self):
        self.number
        self.threads.append(CustomProtocolThread())
        customprotocol_thread=self.threads[self.number]
        self.number=self.number+1
        try:

            self.progressDialog = QtWidgets.QDialog()
            verticalLayout = QtWidgets.QVBoxLayout(self.progressDialog)
            label = QtWidgets.QLabel("Running Custom Protocol",self.progressDialog)
            verticalLayout.addWidget(label)
            buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.progressDialog)

            customprotocol_thread.__init__()
            customprotocol_thread.start()
            buttonBox.rejected.connect(self.progressDialog.reject)
            verticalLayout.addWidget(buttonBox)
            scope.continuerun = True
            while customprotocol_thread.isRunning():
                if self.progressDialog.exec() == QtWidgets.QDialog.Rejected:

                    self.Signal_Done('Custom Protocol stopped')

                    print("Custom Protocol has been stopped")


                    while customprotocol_thread.isRunning():

                        from autoscript_sdb_microscope_client.enumerations import PatterningState

                        if scope.is_idle():
                            continue
                        else:
                            scope.stop_patterning()

                            scope.stop()
                            scope.continuerun=False
                            customprotocol_thread.continuerun=False
                            customprotocol_thread.stop()

                            self.progressDialog.close()

                            print("Operation terminated")

            self.progressDialog.close()

            self.Signal_Done('Custom Protocol stopped')
        except:
            print("Something went wrong with the setup.")
            print(sys.exc_info())
        self.progressDialog.close()

        return()

    def volumeimaging(self):
        try:

            self.progressDialog = QtWidgets.QDialog()
            verticalLayout = QtWidgets.QVBoxLayout(self.progressDialog)
            label = QtWidgets.QLabel("Running Volume Imaging",self.progressDialog)
            verticalLayout.addWidget(label)
            buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.progressDialog)

            volumeimaging_thread=VolumeImagingThread()
            volumeimaging_thread.__init__()
            volumeimaging_thread.start()
            buttonBox.rejected.connect(self.progressDialog.reject)
            verticalLayout.addWidget(buttonBox)
            scope.continuerun = True
            while volumeimaging_thread.isRunning():
                if self.progressDialog.exec() == QtWidgets.QDialog.Rejected:


                    self.Signal_Done('Volume Imaging stopped')

                    print("Volume Imaging has been stopped")


                    while volumeimaging_thread.isRunning():

                        from autoscript_sdb_microscope_client.enumerations import PatterningState

                        if scope.is_idle():
                            continue
                        else:
                            scope.stop_patterning()

                            scope.stop()
                            scope.continuerun=False
                            volumeimaging_thread.continuerun=False
                            volumeimaging_thread.stop()

                            self.progressDialog.close()

                            print("Operation terminated")

            self.progressDialog.close()

            self.Signal_Done('Fine Mill stopped')
        except:
            print("Something went wrong with the setup.")
            print(sys.exc_info())
        self.progressDialog.close()

        return()


    def custompatternfilerun(self):
        try:

            self.progressDialog = QtWidgets.QDialog()
            verticalLayout = QtWidgets.QVBoxLayout(self.progressDialog)
            label = QtWidgets.QLabel("Running Custom Patternfile",self.progressDialog)
            verticalLayout.addWidget(label)
            buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.progressDialog)

            custompatternfile_thread=CustomPatternfileThread()
            custompatternfile_thread.__init__()
            custompatternfile_thread.start()
            buttonBox.rejected.connect(self.progressDialog.reject)
            verticalLayout.addWidget(buttonBox)
            scope.continuerun = True
            while custompatternfile_thread.isRunning():
                if self.progressDialog.exec() == QtWidgets.QDialog.Rejected:

                    #
                    self.Signal_Done('Custom Patternfile stopped')
                    print("Custom Patternfile has been stopped")


                    while custompatternfile_thread.isRunning():

                        from autoscript_sdb_microscope_client.enumerations import PatterningState

                        if scope.is_idle():
                            continue
                        else:
                            scope.stop_patterning()

                            scope.stop()
                            scope.continuerun=False
                            custompatternfile_thread.continuerun=False
                            custompatternfile_thread.stop()

                            self.progressDialog.close()

                            print("Operation terminated")

            self.progressDialog.close()

            self.Signal_Done('Rough Mill stopped')
        except:
            print("Something went wrong with the setup.")
            print(sys.exc_info())
        self.progressDialog.close()

        return()

####################################
#/CODE:Define Run button Functions #
####################################


####################################
# CODE:Session Functions           #
####################################

    def new_session(self):
        self.newSessionDialog = QtWidgets.QDialog()
        verticalLayout = QtWidgets.QHBoxLayout(self.newSessionDialog)
        label = QtWidgets.QLabel("Start new session?",self.newSessionDialog)
        verticalLayout.addWidget(label)

        buttonBox2 = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok,self.newSessionDialog)
        buttonBox2.accepted.connect(self.newSessionDialog.accept)
        verticalLayout.addWidget(buttonBox2)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.newSessionDialog)

        buttonBox.rejected.connect(self.newSessionDialog.reject)

        verticalLayout.addWidget(buttonBox)


        executed=self.newSessionDialog.exec()


        if  executed == QtWidgets.QDialog.Rejected:
            print("No new session")
            return None
        
        elif executed == QtWidgets.QDialog.Accepted:
            print("New session")
            self.pattern_dict={}

            scene=QtWidgets.QGraphicsScene()
            self.graphicsView.setScene(scene)
            self.StagePos={}
            self.pattern_dict={}
            self.ImageBufferHandle=0
            self.load_image_pixel_size=1
            self.corrspots={}
            self.ImageBufferImages=[]
            self.pointer_projpixmap=None
            self.colordict={"green":[0,255,0], "magenta":[255,0,255], "cyan":[0,255,255], "yellow":[255,255,0], "red":[255,0,0], "white":[255,255,255]}
            self.CFproj=None
            self.ImageBuffer.clear()
            #self.tableWidget.clear()
            for i in range(self.tableWidget.rowCount()):
                self.tableWidget.removeRow(i)
            return None
        
        
        return()
        

    def load_session(self):
        try:
            session_file=QtWidgets.QFileDialog.getOpenFileNames(None, "An IB image before correlation",self.output_dir,"SerialFIBSessions (*.sfs)")
            numRows = self.ImageBuffer.count()
            with open(session_file[0][0],'rb') as pickle_in:
                session_dict=pickle.load(pickle_in)



                ### Load Stage Positions
                for i in session_dict['positions']:
                    self.addRow_load(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])


                ### Load Images
                for i in session_dict['images']:

                    self.load_images(i)
                self.corrspots.update(session_dict['corrspots'])


                for i in session_dict['patterns']:
                    self.scene.clear()
                    for j in session_dict['patterns'][i]:
                        self.scene.addItem(Rectangle(j[0],j[1],j[3],j[2]))
                        self.graphicsView.setScene(self.scene)

                        try:
                            old_list=self.pattern_dict[str(numRows)]

                        except KeyError:
                            old_list=[]

                        self.pattern_dict.update({str(numRows) : old_list+[Rectangle(j[0],j[1],j[2],j[3])]})
                        

                    numRows=numRows+1

                #try:
                self.settings=session_dict['settings']
                self.load_settings_func(self.settings)

                #except:
                #    print("No settings file was saved, using standard settings")
                #    self.load_settings_func(self.settings)
                self.scene.clear()
                #print(self.pattern_dict)
                # Pickle cannot handle patterns. You need to save the entire x,y,w,h parameters here
                #self.patterns.update(session_dict['patterns'])
        except:
            print("No Session File loaded")

        

        
        return()

####################################
#/CODE:Session Functions           #
####################################


####################################
# CODE: "Tools" Functions          #
####################################
    def get_for_scripting(self):
        row_count = self.tableWidget.rowCount()
        stagepositions=[]
        for i in range(row_count):
            self.log_out=''
            #if self.tableWidget.item(i,7)==None:
            #    print("Skipping Position "+str(self.tableWidget.item(i,0).text()))
            #else:


            label=self.tableWidget.item(i,0).text()
            x=float(self.tableWidget.item(i,1).text())
            y=float(self.tableWidget.item(i,2).text())
            z=float(self.tableWidget.item(i,3).text())
            r=float(self.tableWidget.item(i,4).text())
            t=float(self.tableWidget.item(i,5).text())
            try:
                alignment_image=float(self.tableWidget.item(i,6).text())
                patterns=float(self.tableWidget.item(i,7).text())
                stagepos = {'label': label, 'x': x, 'y': y, 'z': z, 't': t, 'r': r, 'patterns':patterns, 'image':alignment_image}
            except:
                stagepos = {'label': label, 'x': x, 'y': y, 'z': z, 't': t, 'r': r, 'patterns':'', 'image':''}
            stagepositions.append(stagepos)

        images=self.ImageBufferImages
        
        patterns=self.pattern_dict
        pickable_pattern_dict={}
        #for i in patterns:
        for i in range(0,len(images)):
            if str(i) in patterns:
                pattern_list=patterns[str(i)]
                entry=[]
                for j in pattern_list:
                    #print(j.x,j.y,j.w,j.h)
                    entry.append([j.x,j.y,j.w,j.h])
                pickable_pattern_dict.update({i:entry})
            else:
                pickable_pattern_dict.update({i:[]})
        return (stagepositions,images,pickable_pattern_dict)
    
    def open_scripting(self):
        stagepositions,images,patterns=self.get_for_scripting()
        widget=QtWidgets.QDialog()
        ui=Ui_ScriptEditor()
        ui.setupUi(widget,stagepositions,images,patterns)
        widget.exec_()

        return()


    
    def open_patterneditor(self):

        widget=QtWidgets.QDialog()
        ui=Ui_PatternFileEditor()
        ui.setupUi(widget)
        widget.exec_()
        return()
    def open_volumedesigner(self):
        widget=QtWidgets.QDialog()
        ui=Ui_VolumeDesigner()
        ui.setupUi(widget)
        widget.exec_()
        return()

    def open_lamelladesigner(self):
        widget=QtWidgets.QDialog()
        ui=Ui_LamellaDesigner()
        ui.setupUi(widget)
        widget.exec_()
        return()

####################################
#/CODE: "Tools" Functions          #
####################################



####################################
# CODE:Pattern handling Functions  #
####################################
    def copy_patterns(self):
            print("Patterns copied")
            self.savePatterns()
            items=self.scene.items()
            item=self.scene.selectedItems()
            ids=[]
            for i in items:
                if i.type()==3:
                    if i in item:
                        ids.append(True)
                    else:
                        ids.append(False)
                
            self.showInGraphview()

            items2=self.scene.items()
            item=[]
            ids=ids[::-1]

            for i in range(len(ids)): 
                if items2[i].type()==3:
                    if ids[i]==True:

                        items2[i].setSelected(True)
                        item.append(items2[i])
            if item==[]:

                return()
            else:

                patterns=[]

                for i in item:
                    if i.type()==3:
                        patterns.append([i.x,i.y,i.w,i.h])

                self.copy=patterns


    def paste_patterns(self):
        print('paste_patterns')
        for i in self.copy:
            scene=self.graphicsView.scene.addItem(Rectangle(i[0],i[1],i[2],i[3]))

        return()
####################################
#/CODE:Pattern handling Functions  #
####################################

    


class LamellaView(QtWidgets.QGraphicsView):
    leftMouseButtonPressed = pyqtSignal(float, float)
    rightMouseButtonPressed = pyqtSignal(float, float)
    leftMouseButtonReleased = pyqtSignal(float, float)
    rightMouseButtonReleased = pyqtSignal(float, float)
    leftMouseButtonDoubleClicked = pyqtSignal(float, float)
    rightMouseButtonDoubleClicked = pyqtSignal(float, float)
    def __init__(self,parent=None):
        super(LamellaView,self).__init__(parent)
        self.left_begin=[]
        self.left_end=[]
        self.lamella_rect=QtCore.QRectF()
        global ui
        self.scene=ui.get_scene()
        self.sceneBuffer=ui.get_scenebuffer()
        self.number_imageBuffer=ui.get_number_imageBuffer()
        #self.number_imageBuffer=1
        self.pattern_dict=ui.get_pattern_dict()
        self.setAcceptDrops(True)

    def mouseDoubleClickEvent(self, event):
        """ Show entire image.
        """
        scenePos = self.mapToScene(event.pos())
        number=self.number_imageBuffer
        if event.button() == QtCore.Qt.LeftButton:
            self.leftMouseButtonDoubleClicked.emit(scenePos.x(), scenePos.y())
            #print("Left Double Clicked")
        elif event.button() == QtCore.Qt.RightButton:
            self.rightMouseButtonDoubleClicked.emit(scenePos.x(), scenePos.y())
            #print("Right Double Clicked",[scenePos.x(),scenePos.y()])
        QtWidgets.QGraphicsView.mouseDoubleClickEvent(self, event)
        self.scene.addItem(Rectangle(0,0,100,100))
        self.setScene(self.scene)
        #self.sceneBuffer[0]=self.scene
        self.number_imageBuffer=ui.get_number_imageBuffer()
        #print(self.number_imageBuffer)
        try:
            old_list=self.pattern_dict[self.number_imageBuffer]
            #new_list=old_list.append(Rectangle(0,0,100,100))
        except KeyError:
            old_list=[]
            #new_list=Rectangle(0,0,100,100)
        self.pattern_dict.update({self.number_imageBuffer : old_list+[Rectangle(0,0,100,100)]})
        
        ui.push_pattern_dict(self.pattern_dict)

    def keyPressEvent(self, e):
 
        if e.key() == QtCore.Qt.Key_F5:
            print("F5 pressed")
            #QtCore.Qt.FramelessWindowHint
            #print(self.parent())
            ui.toggleFullScreen()
            #self.showFullScreen()
            #self.show()
        if e.key() == QtCore.Qt.Key_F6:
            def y_pos(element):
                return(element.y)
            #print("Pattern size is:")
            ui.savePatterns()
            ui.showInGraphview()
            number=ui.ImageBufferHandle
            image=ui.ImageBufferImages[int(number)]
            pixel_size=image.metadata.binary_result.pixel_size
            item=self.scene.items()
            patterns=[]
            for i in item:
                if i.type()==3:
                    patterns.append(i)
                    #print(i.w)
                    #if i==item_id:

            patterns.sort(key=y_pos)
            num=0
            for i in patterns:
                
                print("Pattern Number "+str(num)+str(" is ")+str(i.w*pixel_size.x*1000000)+" µm wide.")
                num=num+1
                #print(i)
            #for i in patterns:
            #    print("Pattern Number "+str(patterns.index(i))+str(" is ")+str(i.w*pixel_size[0]*1000000)+" µm wide.")
        
    def paintpoint(self,x,y):
        #Painting Correlation Spots
        point=QtCore.QPointF(x,y)
        painter=QtGui.QPainter(self.viewport())
        painter.setPen(QtGui.QPen(QtCore.Qt.green, 3000))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.CrossPattern))
        self.scene.addPoint(point)

        

class CorrelationSpot(QtWidgets.QGraphicsPixmapItem):
    def __init__(self,x,y):
        super(CorrelationSpot, self).__init__()
        item=QtGui.QPixmap('../images/x.jpg')
        self.setPos(x,y)
        self.x=x
        self.y=y




class Rectangle(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super(Rectangle, self).__init__(0, 0, w, h)
        self.setPen(QtGui.QPen(QtCore.Qt.red, 2))
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable
            | QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemIsFocusable
            | QtWidgets.QGraphicsItem.ItemSendsGeometryChanges
            | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setPos(QtCore.QPointF(x, y))
        self.w=w
        self.h=h
        self.x=x
        self.y=y

    def mouseMoveEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            super(Rectangle, self).mouseMoveEvent(e)
        if e.buttons() & QtCore.Qt.RightButton:
            self.setRect(QtCore.QRectF(QtCore.QPoint(), e.pos()).normalized())



class Pattern():
    def __init__(self,center_x,center_y,depth,width,height,scan_direction):
        self.center_x=center_x
        self.center_y=center_y
        self.depth=depth
        self.width=width
        self.height=height
        self.scan_direction=scan_direction

####################################
# CODE:Threads for mill running    #
####################################
class RoughMillThread(QtCore.QThread):
    signal = pyqtSignal('PyQt_PyObject')
    global ui
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        ### COMMENTED OUT FOR DEV ###
        #try:

        ui.write_patterns()
        row_count=ui.tableWidget.rowCount()


        for i in range(row_count):
            ui.log_out=''
            if ui.tableWidget.item(i,7)==None:
                print("Skipping Position "+str(ui.tableWidget.item(i,0).text()))
            else:


                label=ui.tableWidget.item(i,0).text()
                x=float(ui.tableWidget.item(i,1).text())
                y=float(ui.tableWidget.item(i,2).text())
                z=float(ui.tableWidget.item(i,3).text())
                r=float(ui.tableWidget.item(i,4).text())
                t=float(ui.tableWidget.item(i,5).text())

                ui.sysout.write('---------------------------------------------------\n')
                ui.sysout.write(str(label))
                ui.sysout.write('\n---------------------------------------------------\n')

                stagepos={'label':label,'x':x,'y':y,'z':z,'t':t,'r':r}
                image_number=int(ui.tableWidget.item(i,6).text())
                alignment_image=ui.ImageBufferImages[image_number]

                pattern_dir=ui.output_dir+'/'+str(label)+'/'

                ### COMMENTED OUT FOR DEV ###
                log_out_new=scope.run_rough_milling(label,alignment_image,stagepos,pattern_dir)
                ui.log_out=ui.log_out+log_out_new

            ui.sysout.write(ui.log_out)

        self.signal.emit("Rough Mill done!")

        #except:
        #    print("Something went wrong. Most likely, your output directory is not valid!")
        #    print(sys.exc_info())

class TrenchMillThread(QtCore.QThread):
    signal = pyqtSignal('PyQt_PyObject')
    global ui

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        try:

            ui.write_patterns()
            row_count = ui.tableWidget.rowCount()


            for i in range(row_count):
                ui.log_out = ''
                if ui.tableWidget.item(i, 7) == None:
                    print("Skipping Position " + str(ui.tableWidget.item(i, 0).text()))
                else:

                    label = ui.tableWidget.item(i, 0).text()
                    x = float(ui.tableWidget.item(i, 1).text())
                    y = float(ui.tableWidget.item(i, 2).text())
                    z = float(ui.tableWidget.item(i, 3).text())
                    r = float(ui.tableWidget.item(i, 4).text())
                    t = float(ui.tableWidget.item(i, 5).text())

                    ui.sysout.write('---------------------------------------------------\n')
                    ui.sysout.write(str(label))
                    ui.sysout.write('\n---------------------------------------------------\n')

                    stagepos = {'label': label, 'x': x, 'y': y, 'z': z, 't': t, 'r': r}
                    image_number = int(ui.tableWidget.item(i, 6).text())
                    alignment_image = ui.ImageBufferImages[image_number]

                    pattern_dir = ui.output_dir + '/' + str(label) + '/'
                    log_out_new = scope.run_trench_milling(label, alignment_image, stagepos, pattern_dir)
                    ui.log_out = ui.log_out + log_out_new

                ui.sysout.write(ui.log_out)

            self.signal.emit("Rough Mill done!")

        except:
            print("Something went wrong. Most likely, your output directory is not valid!")
            print(sys.exc_info())




class RoughProtocolThread(QtCore.QThread):
    signal = pyqtSignal('PyQt_PyObject')
    global ui

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.continuerun = True
        QtCore.QThread.__init__(self)
    def run(self):
        try:

            ui.write_patterns()
            row_count = ui.tableWidget.rowCount()

            for i in range(row_count):
                if self.continuerun:
                    ui.log_out = ''
                    if ui.tableWidget.item(i, 7) == None:
                        print("Skipping Position " + str(ui.tableWidget.item(i, 0).text()))
                    else:

                        label = ui.tableWidget.item(i, 0).text()
                        x = float(ui.tableWidget.item(i, 1).text())
                        y = float(ui.tableWidget.item(i, 2).text())
                        z = float(ui.tableWidget.item(i, 3).text())
                        r = float(ui.tableWidget.item(i, 4).text())
                        t = float(ui.tableWidget.item(i, 5).text())

                        ui.sysout.write('---------------------------------------------------\n')
                        ui.sysout.write(str(label))
                        ui.sysout.write('\n---------------------------------------------------\n')

                        stagepos = {'label': label, 'x': x, 'y': y, 'z': z, 't': t, 'r': r}
                        image_number = int(ui.tableWidget.item(i, 6).text())
                        alignment_image = ui.ImageBufferImages[image_number]

                        pattern_dir = ui.output_dir + '/' + str(label) + '/'



                        protocolfile = ui.roughmillprotocol
                        log_out_new = scope.run_milling_protocol(label, alignment_image, stagepos, pattern_dir,
                                                                protocolfile,mode='rough')
                        ui.log_out = ui.log_out + log_out_new

                    ui.sysout.write(ui.log_out)

            self.signal.emit("Rough Protocol done!")

            ui.progressDialog.close()

        except:
            print("Something went wrong. Most likely, your output directory is not valid!")
            print(sys.exc_info())
        
            ui.progressDialog.close()



class FineProtocolThread(QtCore.QThread):
    signal = pyqtSignal('PyQt_PyObject')
    global ui

    def __init__(self):
        QtCore.QThread.__init__(self)

        QtCore.QThread.__init__(self)
        self.continuerun=True

    def run(self):
        try:

            ui.write_patterns()
            row_count = ui.tableWidget.rowCount()


            for i in range(row_count):
                if self.continuerun:
                    ui.log_out = ''
                    if ui.tableWidget.item(i, 7) == None:
                        print("Skipping Position " + str(ui.tableWidget.item(i, 0).text()))
                    else:

                        label = ui.tableWidget.item(i, 0).text()
                        x = float(ui.tableWidget.item(i, 1).text())
                        y = float(ui.tableWidget.item(i, 2).text())
                        z = float(ui.tableWidget.item(i, 3).text())
                        r = float(ui.tableWidget.item(i, 4).text())
                        t = float(ui.tableWidget.item(i, 5).text())

                        ui.sysout.write('---------------------------------------------------\n')
                        ui.sysout.write(str(label))
                        ui.sysout.write('\n---------------------------------------------------\n')

                        stagepos = {'label': label, 'x': x, 'y': y, 'z': z, 't': t, 'r': r}
                        image_number = int(ui.tableWidget.item(i, 6).text())
                        alignment_image = ui.ImageBufferImages[image_number]

                        pattern_dir = ui.output_dir + '/' + str(label) + '/'

                        protocolfile=ui.finemillprotocol
                        #protocolfile = ui.finemillprotocol
                        log_out_new = scope.run_milling_protocol(label, alignment_image, stagepos, pattern_dir,
                                                                 protocolfile)
                        ui.log_out = ui.log_out + log_out_new

                    ui.sysout.write(ui.log_out)


            self.signal.emit("Fine Protocol done!")
            self.quit()
            ui.progressDialog.close()
        except:
            print("Something went wrong. Most likely, your output directory is not valid!")
            print(sys.exc_info())
            self.quit()
            ui.progressDialog.close()

    def stop(self):
        self.continuerun=False
        return()

class VolumeImagingThread(QtCore.QThread):
    signal = pyqtSignal('PyQt_PyObject')
    global ui

    def __init__(self):
        QtCore.QThread.__init__(self)
        QtCore.QThread.__init__(self)
        self.continuerun = True

    def run(self):
        try:

            ui.write_patterns()
            row_count = ui.tableWidget.rowCount()


            for i in range(row_count):
                if self.continuerun:
                    ui.log_out = ''
                    if ui.tableWidget.item(i, 7) == None:
                        print("Skipping Position " + str(ui.tableWidget.item(i, 0).text()))
                    else:

                        label = ui.tableWidget.item(i, 0).text()
                        x = float(ui.tableWidget.item(i, 1).text())
                        y = float(ui.tableWidget.item(i, 2).text())
                        z = float(ui.tableWidget.item(i, 3).text())
                        r = float(ui.tableWidget.item(i, 4).text())
                        t = float(ui.tableWidget.item(i, 5).text())

                        ui.sysout.write('---------------------------------------------------\n')
                        ui.sysout.write(str(label))
                        ui.sysout.write('\n---------------------------------------------------\n')

                        stagepos = {'label': label, 'x': x, 'y': y, 'z': z, 't': t, 'r': r}
                        image_number = int(ui.tableWidget.item(i, 6).text())
                        alignment_image = ui.ImageBufferImages[image_number]

                        pattern_dir = ui.output_dir + '/' + str(label) + '/'



                        paramsfile = ui.SAVparamsfile
                        log_out_new = scope.run_SAV(label, alignment_image, stagepos, pattern_dir, paramsfile)
                        ui.log_out = ui.log_out + log_out_new

                    ui.sysout.write(ui.log_out)

            self.signal.emit("Fine Protocol done!")
            self.quit()
            ui.progressDialog.close()
        except:
            print("Something went wrong. Most likely, your output directory is not valid!")
            print(sys.exc_info())
            self.quit()
            ui.progressDialog.close()



class CustomPatternfileThread(QtCore.QThread):
    signal = pyqtSignal('PyQt_PyObject')
    global ui

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.continuerun = True
    def run(self):
        try:

            ui.write_patterns()
            row_count = ui.tableWidget.rowCount()


            for i in range(row_count):
                if self.continuerun:
                    ui.log_out = ''
                    if ui.tableWidget.item(i, 7) == None:
                        print("Skipping Position " + str(ui.tableWidget.item(i, 0).text()))
                    else:

                        label = ui.tableWidget.item(i, 0).text()
                        x = float(ui.tableWidget.item(i, 1).text())
                        y = float(ui.tableWidget.item(i, 2).text())
                        z = float(ui.tableWidget.item(i, 3).text())
                        r = float(ui.tableWidget.item(i, 4).text())
                        t = float(ui.tableWidget.item(i, 5).text())

                        ui.sysout.write('---------------------------------------------------\n')
                        ui.sysout.write(str(label))
                        ui.sysout.write('\n---------------------------------------------------\n')

                        stagepos = {'label': label, 'x': x, 'y': y, 'z': z, 't': t, 'r': r}
                        image_number = int(ui.tableWidget.item(i, 6).text())
                        alignment_image = ui.ImageBufferImages[image_number]

                        pattern_dir = ui.output_dir + '/' + str(label) + '/'


                        protocolfile = ui.custompatternfile
                        log_out_new = scope.run_milling_custom(label, alignment_image, stagepos, pattern_dir,
                                                               protocolfile)

                        ui.log_out = ui.log_out + log_out_new

                    ui.sysout.write(ui.log_out)

            self.signal.emit("Fine Protocol done!")
            #return True
            self.quit()
            ui.progressDialog.close()

        except:
            print("Something went wrong. Most likely, your output directory is not valid!")
            print(sys.exc_info())
            self.quit()
            ui.progressDialog.close()




class CustomProtocolThread(QtCore.QThread):
    signal = pyqtSignal('PyQt_PyObject')
    global ui

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.continuerun = True

    def run(self):
        try:

            ui.write_patterns()
            row_count = ui.tableWidget.rowCount()


            for i in range(row_count):
                if self.continuerun:
                    ui.log_out = ''
                    if ui.tableWidget.item(i, 7) == None:
                        print("Skipping Position " + str(ui.tableWidget.item(i, 0).text()))
                    else:

                        label = ui.tableWidget.item(i, 0).text()
                        x = float(ui.tableWidget.item(i, 1).text())
                        y = float(ui.tableWidget.item(i, 2).text())
                        z = float(ui.tableWidget.item(i, 3).text())
                        r = float(ui.tableWidget.item(i, 4).text())
                        t = float(ui.tableWidget.item(i, 5).text())

                        ui.sysout.write('---------------------------------------------------\n')
                        ui.sysout.write(str(label))
                        ui.sysout.write('\n---------------------------------------------------\n')

                        stagepos = {'label': label, 'x': x, 'y': y, 'z': z, 't': t, 'r': r}
                        image_number = int(ui.tableWidget.item(i, 6).text())
                        alignment_image = ui.ImageBufferImages[image_number]

                        pattern_dir = ui.output_dir + '/' + str(label) + '/'



                        protocolfile = ui.custommillprotocol
                        log_out_new = scope.run_milling_protocol(label, alignment_image, stagepos, pattern_dir,
                                                                 protocolfile)
                        ui.log_out = ui.log_out + log_out_new

                    ui.sysout.write(ui.log_out)

            self.signal.emit("Custom Protocol done!")

            ui.progressDialog.close()

        except:
            print("Something went wrong. Most likely, your output directory is not valid!")
            print(sys.exc_info())

            ui.progressDialog.close()
####################################
#/CODE:Threads for mill running    #
####################################



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.installEventFilter(MainWindow)


    MainWindow.show()
    #scope.disconnect()
    def myexcepthook(type,value,tb):
        scope.disconnect()

    sys.excepthook = myexcepthook
    sys.exit(app.exec_())
    
    



