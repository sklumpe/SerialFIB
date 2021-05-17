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


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'volumedesigner2.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_VolumeDesigner(object):
    def setupUi(self, VolumeDesigner):
        VolumeDesigner.setObjectName("VolumeDesigner")
        VolumeDesigner.resize(806, 510)
        self.label_26 = QtWidgets.QLabel(VolumeDesigner)
        self.label_26.setGeometry(QtCore.QRect(70, 20, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_26.setFont(font)
        self.label_26.setFrameShape(QtWidgets.QFrame.Box)
        self.label_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_26.setLineWidth(2)
        self.label_26.setMidLineWidth(1)
        self.label_26.setTextFormat(QtCore.Qt.RichText)
        self.label_26.setScaledContents(False)
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(VolumeDesigner)
        self.label_27.setGeometry(QtCore.QRect(440, 20, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_27.setFont(font)
        self.label_27.setFrameShape(QtWidgets.QFrame.Box)
        self.label_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_27.setLineWidth(2)
        self.label_27.setMidLineWidth(1)
        self.label_27.setTextFormat(QtCore.Qt.RichText)
        self.label_27.setScaledContents(False)
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setObjectName("label_27")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(VolumeDesigner)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(480, 380, 281, 71))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_loadFile = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.button_loadFile.setObjectName("button_loadFile")
        self.horizontalLayout_2.addWidget(self.button_loadFile)
        self.button_saveFile = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.button_saveFile.setObjectName("button_saveFile")
        self.horizontalLayout_2.addWidget(self.button_saveFile)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(VolumeDesigner)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(70, 320, 341, 181))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_17 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 1, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 0, 2, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 2, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_19.setObjectName("label_19")
        self.gridLayout_3.addWidget(self.label_19, 0, 0, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_24.setObjectName("label_24")
        self.gridLayout_3.addWidget(self.label_24, 3, 0, 1, 1)
        self.comboBox_InitialAlignmentFIB = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.comboBox_InitialAlignmentFIB.setObjectName("comboBox_InitialAlignmentFIB")
        self.comboBox_InitialAlignmentFIB.addItem("")
        self.comboBox_InitialAlignmentFIB.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_InitialAlignmentFIB, 3, 1, 1, 1)
        self.comboBox_InitialFocusSEM = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.comboBox_InitialFocusSEM.setObjectName("comboBox_InitialFocusSEM")
        self.comboBox_InitialFocusSEM.addItem("")
        self.comboBox_InitialFocusSEM.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_InitialFocusSEM, 1, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 2, 0, 1, 1)
        self.int_FocusSEMevery = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.int_FocusSEMevery.setObjectName("int_FocusSEMevery")
        self.gridLayout_3.addWidget(self.int_FocusSEMevery, 0, 1, 1, 1)
        self.int_RealignSEMevery = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.int_RealignSEMevery.setObjectName("int_RealignSEMevery")
        self.gridLayout_3.addWidget(self.int_RealignSEMevery, 2, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 4, 0, 1, 1)
        self.int_RealignFIBevery = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.int_RealignFIBevery.setObjectName("int_RealignFIBevery")
        self.gridLayout_3.addWidget(self.int_RealignFIBevery, 4, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_28.setObjectName("label_28")
        self.gridLayout_3.addWidget(self.label_28, 4, 2, 1, 1)
        self.gridLayoutWidget = QtWidgets.QWidget(VolumeDesigner)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(70, 70, 341, 181))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.double_SliceThickness = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.double_SliceThickness.setObjectName("double_SliceThickness")
        self.gridLayout.addWidget(self.double_SliceThickness, 2, 1, 1, 1)
        self.double_IBcurrent = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.double_IBcurrent.setObjectName("double_IBcurrent")
        self.gridLayout.addWidget(self.double_IBcurrent, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.double_MillingTime = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.double_MillingTime.setObjectName("double_MillingTime")
        self.gridLayout.addWidget(self.double_MillingTime, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.comboBox_ScanDirection = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_ScanDirection.setObjectName("comboBox_ScanDirection")
        self.comboBox_ScanDirection.addItem("")
        self.comboBox_ScanDirection.addItem("")
        self.comboBox_ScanDirection.addItem("")
        self.comboBox_ScanDirection.addItem("")
        self.gridLayout.addWidget(self.comboBox_ScanDirection, 3, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(VolumeDesigner)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(440, 70, 341, 261))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_22 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_22.setObjectName("label_22")
        self.gridLayout_2.addWidget(self.label_22, 2, 2, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 2, 0, 1, 1)
        self.int_LineIntegration = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.int_LineIntegration.setObjectName("int_LineIntegration")
        self.gridLayout_2.addWidget(self.int_LineIntegration, 1, 1, 1, 1)
        self.comboBox_Resolution = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_Resolution.setObjectName("comboBox_Resolution")
        self.comboBox_Resolution.addItem("")
        self.comboBox_Resolution.addItem("")
        self.comboBox_Resolution.addItem("")
        self.comboBox_Resolution.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_Resolution, 2, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 1, 0, 1, 1)
        self.double_DwellTime = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.double_DwellTime.setObjectName("double_DwellTime")
        self.gridLayout_2.addWidget(self.double_DwellTime, 0, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 0, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_16.setText("")
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 1, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(VolumeDesigner)
        self.label_10.setGeometry(QtCore.QRect(70, 270, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_10.setFont(font)
        self.label_10.setFrameShape(QtWidgets.QFrame.Box)
        self.label_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_10.setLineWidth(2)
        self.label_10.setMidLineWidth(1)
        self.label_10.setTextFormat(QtCore.Qt.RichText)
        self.label_10.setScaledContents(False)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")

        self.retranslateUi(VolumeDesigner)
        QtCore.QMetaObject.connectSlotsByName(VolumeDesigner)


        ###
        self.output_dir='~/'
        ###
    def retranslateUi(self, VolumeDesigner):
        _translate = QtCore.QCoreApplication.translate
        VolumeDesigner.setWindowTitle(_translate("VolumeDesigner", "VolumeDesigner"))
        self.label_26.setText(_translate("VolumeDesigner", "Milling Parameters"))
        self.label_27.setText(_translate("VolumeDesigner", "SEM Imaging Parameters"))
        self.button_loadFile.setText(_translate("VolumeDesigner", "Load File"))
        self.button_saveFile.setText(_translate("VolumeDesigner", "Save File"))
        self.label_17.setText(_translate("VolumeDesigner", "Initial Focus SEM"))
        self.label_20.setText(_translate("VolumeDesigner", "steps"))
        self.label_23.setText(_translate("VolumeDesigner", "steps"))
        self.label_19.setText(_translate("VolumeDesigner", "Focus SEM every"))
        self.label_24.setText(_translate("VolumeDesigner", "Initial Alignment FIB"))
        self.comboBox_InitialAlignmentFIB.setItemText(0, _translate("VolumeDesigner", "no"))
        self.comboBox_InitialAlignmentFIB.setItemText(1, _translate("VolumeDesigner", "yes"))
        self.comboBox_InitialFocusSEM.setItemText(0, _translate("VolumeDesigner", "no"))
        self.comboBox_InitialFocusSEM.setItemText(1, _translate("VolumeDesigner", "yes"))
        self.label_21.setText(_translate("VolumeDesigner", "Realign SEM every"))
        self.label_25.setText(_translate("VolumeDesigner", "Realign FIB every"))
        self.label_28.setText(_translate("VolumeDesigner", "steps"))
        self.label_3.setText(_translate("VolumeDesigner", "Milling Time"))
        self.label_4.setText(_translate("VolumeDesigner", "s"))
        self.label.setText(_translate("VolumeDesigner", "Ion Beam current"))
        self.label_2.setText(_translate("VolumeDesigner", "nA"))
        self.label_5.setText(_translate("VolumeDesigner", "Slice Thickness"))
        self.label_6.setText(_translate("VolumeDesigner", "µm"))
        self.label_7.setText(_translate("VolumeDesigner", "Scan Direction"))
        self.comboBox_ScanDirection.setItemText(0, _translate("VolumeDesigner", "TopToBottom"))
        self.comboBox_ScanDirection.setItemText(1, _translate("VolumeDesigner", "BottomToTop"))
        self.comboBox_ScanDirection.setItemText(2, _translate("VolumeDesigner", "LeftToRight"))
        self.comboBox_ScanDirection.setItemText(3, _translate("VolumeDesigner", "RightToLeft"))
        self.label_22.setText(_translate("VolumeDesigner", "pixel"))
        self.label_18.setText(_translate("VolumeDesigner", "Resolution"))
        self.comboBox_Resolution.setItemText(0, _translate("VolumeDesigner", "1536x1024"))
        self.comboBox_Resolution.setItemText(1, _translate("VolumeDesigner", "756x512"))
        self.comboBox_Resolution.setItemText(2, _translate("VolumeDesigner", "3072x2048"))
        self.comboBox_Resolution.setItemText(3, _translate("VolumeDesigner", "6144x4096"))
        self.label_15.setText(_translate("VolumeDesigner", "Line Integration"))
        self.label_13.setText(_translate("VolumeDesigner", "Dwell Time"))
        self.label_14.setText(_translate("VolumeDesigner", "µs"))
        self.label_10.setText(_translate("VolumeDesigner", "Procedure Parameters"))


        self.button_loadFile.pressed.connect(self.read_SPF)
        self.button_saveFile.pressed.connect(self.write_SPF)





    def read_SPF(self):
        try:
            spffile, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Please provide a SPF file",self.output_dir,"SAV parameter file (*.spf)")
            #print(spffile)

            from src.read_SAV import read_SAV_params
            params=read_SAV_params(spffile)
            self.double_IBcurrent.setValue(float(params['IB_Current'])*1e09)
            self.double_MillingTime.setValue(float(params['MillingTime']))
            self.double_SliceThickness.setValue(float(params['SliceThickness'])*1e06)
            self.comboBox_ScanDirection.setCurrentText(str(params['ScanDirection']))
            self.comboBox_InitialAlignmentFIB.setCurrentIndex(int(params['AlignInitial']))
            self.int_RealignFIBevery.setValue(int(params['RealignEvery']))
            self.comboBox_InitialFocusSEM.setCurrentIndex(int(params['FocusInitial']))
            self.int_FocusSEMevery.setValue(int(params['FocusEvery']))
            self.double_DwellTime.setValue(float(params['DwellTime'])*1e06)
            self.comboBox_Resolution.setCurrentText(str(params['Resolution']))
            self.int_LineIntegration.setValue(int(params['LineIntegration']))
            self.int_RealignSEMevery.setValue(int(params['RealignSEMEvery']))
        except:
            #print('bla')
            import sys
            print(sys.exc_info())
        return()

    def write_SPF(self):
        try:
            spffile=QtWidgets.QFileDialog.getSaveFileName(None, "Please provide a SPF file",self.output_dir,"SAV parameter file (*.spf)")
            with open(spffile[0],'w') as output_file:
                output_file.write('IB_Current='+str(self.double_IBcurrent.value())+'e-09\n')
                output_file.write('MillingTime='+str(int(self.double_MillingTime.value()))+'\n')
                output_file.write('SliceThickness='+str(self.double_SliceThickness.value())+'e-06 \n')

                ### This one is currently kept out of the loop of changing since I don't see why you would want to change it. 
                ### If you do, you can do it directly in the textfile produced by this. Can be added at a later point if wanted
                output_file.write('PatternType='+str('Cross-Section')+'\n')
                ###
                output_file.write('ScanDirection='+str(self.comboBox_ScanDirection.currentText())+'\n')
                output_file.write('AlignInitial='+str(self.comboBox_InitialAlignmentFIB.currentIndex())+'\n')
                output_file.write('RealignEvery='+str(self.int_RealignFIBevery.value())+'\n')
                output_file.write('FocusInitial='+str(self.comboBox_InitialFocusSEM.currentIndex())+'\n')
                output_file.write('FocusEvery='+str(self.int_FocusSEMevery.value())+'\n')
                output_file.write('DwellTime='+str(self.double_DwellTime.value())+'e-06 \n')
                output_file.write('Resolution='+str(self.comboBox_Resolution.currentText())+'\n')
                output_file.write('LineIntegration='+str(self.int_LineIntegration.value())+'\n')
                output_file.write('RealignSEMEvery='+str(self.int_RealignSEMevery.value()))
        except:
            #print('bla')
            import sys
            print(sys.exc_info())
        return()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VolumeDesigner = QtWidgets.QWidget()
    ui = Ui_VolumeDesigner()
    ui.setupUi(VolumeDesigner)
    VolumeDesigner.show()
    sys.exit(app.exec_())

