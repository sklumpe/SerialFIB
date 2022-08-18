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

# Form implementation generated from reading ui file 'PatternFileEditor3.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

####
import os
import sys
####

class Ui_PatternFileEditor(object):
    def setupUi(self, PatternFileEditor):
        PatternFileEditor.setObjectName("PatternFileEditor")
        PatternFileEditor.resize(774, 646)
        self.label = QtWidgets.QLabel(PatternFileEditor)
        self.label.setGeometry(QtCore.QRect(330, 10, 151, 16))
        self.label.setObjectName("label")
        self.Button_AddStep = QtWidgets.QPushButton(PatternFileEditor)
        self.Button_AddStep.setGeometry(QtCore.QRect(0, 10, 113, 32))
        self.Button_AddStep.setObjectName("Button_AddStep")
        self.Button_RemoveStep = QtWidgets.QPushButton(PatternFileEditor)
        self.Button_RemoveStep.setGeometry(QtCore.QRect(110, 10, 113, 32))
        self.Button_RemoveStep.setObjectName("Button_RemoveStep")
        self.graphicsView = QtWidgets.QGraphicsView(PatternFileEditor)
        self.graphicsView.setGeometry(QtCore.QRect(350, 50, 411, 301))
        self.graphicsView.setObjectName("graphicsView")
        self.Button_AddPattern = QtWidgets.QPushButton(PatternFileEditor)
        self.Button_AddPattern.setGeometry(QtCore.QRect(120, 80, 101, 32))
        self.Button_AddPattern.setObjectName("Button_AddPattern")
        self.Button_RemovePattern = QtWidgets.QPushButton(PatternFileEditor)
        self.Button_RemovePattern.setGeometry(QtCore.QRect(220, 80, 121, 32))
        self.Button_RemovePattern.setObjectName("Button_RemovePattern")
        self.label_10 = QtWidgets.QLabel(PatternFileEditor)
        self.label_10.setGeometry(QtCore.QRect(370, 530, 81, 41))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(PatternFileEditor)
        self.label_11.setGeometry(QtCore.QRect(130, 40, 81, 41))
        self.label_11.setObjectName("label_11")
        self.Value_IB_Current = QtWidgets.QDoubleSpinBox(PatternFileEditor)
        self.Value_IB_Current.setGeometry(QtCore.QRect(210, 50, 68, 24))
        self.Value_IB_Current.setObjectName("Value_IB_Current")
        self.label_12 = QtWidgets.QLabel(PatternFileEditor)
        self.label_12.setGeometry(QtCore.QRect(290, 40, 31, 41))
        self.label_12.setObjectName("label_12")
        self.PatternTypeBox = QtWidgets.QComboBox(PatternFileEditor)
        self.PatternTypeBox.setGeometry(QtCore.QRect(460, 540, 151, 26))
        self.PatternTypeBox.setObjectName("PatternTypeBox")
        self.PatternTypeBox.addItem("")
        self.PatternTypeBox.addItem("")
        self.PatternTypeBox.addItem("")
        self.listWidget_Steps = QtWidgets.QListWidget(PatternFileEditor)
        self.listWidget_Steps.setGeometry(QtCore.QRect(10, 60, 101, 511))
        self.listWidget_Steps.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_Steps.setObjectName("listWidget_Steps")
        self.listWidget_Patterns = QtWidgets.QListWidget(PatternFileEditor)
        self.listWidget_Patterns.setGeometry(QtCore.QRect(120, 120, 221, 451))
        self.listWidget_Patterns.setObjectName("listWidget_Patterns")
        self.Button_ZoomIn = QtWidgets.QPushButton(PatternFileEditor)
        self.Button_ZoomIn.setGeometry(QtCore.QRect(470, 10, 113, 32))
        self.Button_ZoomIn.setObjectName("Button_ZoomIn")
        self.Button_ZoomOut = QtWidgets.QPushButton(PatternFileEditor)
        self.Button_ZoomOut.setGeometry(QtCore.QRect(600, 10, 113, 32))
        self.Button_ZoomOut.setObjectName("Button_ZoomOut")
        self.Button_SavePatternFile = QtWidgets.QPushButton(PatternFileEditor)
        self.Button_SavePatternFile.setGeometry(QtCore.QRect(620, 600, 141, 32))
        self.Button_SavePatternFile.setObjectName("Button_SavePatternFile")
        self.pushButton = QtWidgets.QPushButton(PatternFileEditor)
        self.pushButton.setGeometry(QtCore.QRect(480, 600, 131, 32))
        self.pushButton.setObjectName("pushButton")
        self.label_13 = QtWidgets.QLabel(PatternFileEditor)
        self.label_13.setGeometry(QtCore.QRect(350, 560, 101, 41))
        self.label_13.setObjectName("label_13")
        self.PatternDirectionBox = QtWidgets.QComboBox(PatternFileEditor)
        self.PatternDirectionBox.setGeometry(QtCore.QRect(460, 570, 151, 26))
        self.PatternDirectionBox.setObjectName("PatternDirectionBox")
        self.PatternDirectionBox.addItem("")
        self.PatternDirectionBox.addItem("")
        self.PatternDirectionBox.addItem("")
        self.PatternDirectionBox.addItem("")
        #self.Checkbox_RTMonitor = QtWidgets.QCheckBox(PatternFileEditor)
        #self.Checkbox_RTMonitor.setGeometry(QtCore.QRect(550, 499, 150, 31))
        #self.Checkbox_RTMonitor.setObjectName("Checkbox_RTMonitor")
        self.widget = QtWidgets.QWidget(PatternFileEditor)
        self.widget.setGeometry(QtCore.QRect(440, 370, 70, 162))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Value_OffsetY = QtWidgets.QDoubleSpinBox(self.widget)
        self.Value_OffsetY.setObjectName("Value_OffsetY")
        self.gridLayout.addWidget(self.Value_OffsetY, 0, 0, 1, 1)
        self.Value_OffsetX = QtWidgets.QDoubleSpinBox(self.widget)
        self.Value_OffsetX.setObjectName("Value_OffsetX")
        self.gridLayout.addWidget(self.Value_OffsetX, 1, 0, 1, 1)
        self.Value_Height = QtWidgets.QDoubleSpinBox(self.widget)
        self.Value_Height.setObjectName("Value_Height")
        self.gridLayout.addWidget(self.Value_Height, 2, 0, 1, 1)
        self.Value_Width = QtWidgets.QDoubleSpinBox(self.widget)
        self.Value_Width.setObjectName("Value_Width")
        self.gridLayout.addWidget(self.Value_Width, 3, 0, 1, 1)
        self.Value_Time = QtWidgets.QSpinBox(self.widget)
        self.Value_Time.setObjectName("Value_Time")
        self.gridLayout.addWidget(self.Value_Time, 4, 0, 1, 1)
        self.widget1 = QtWidgets.QWidget(PatternFileEditor)
        self.widget1.setGeometry(QtCore.QRect(380, 370, 61, 161))
        self.widget1.setObjectName("widget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget1)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget1)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget1)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.widget1)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 4, 0, 1, 1)
        self.widget2 = QtWidgets.QWidget(PatternFileEditor)
        self.widget2.setGeometry(QtCore.QRect(510, 370, 41, 161))
        self.widget2.setObjectName("widget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.widget2)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 4, 0, 1, 1)
        self.widget3 = QtWidgets.QWidget(PatternFileEditor)
        self.widget3.setGeometry(QtCore.QRect(550, 370, 150, 61))
        self.widget3.setObjectName("widget3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget3)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        #self.Checkbox_LamellaHeight = QtWidgets.QCheckBox(self.widget3)
        #self.Checkbox_LamellaHeight.setObjectName("Checkbox_LamellaHeight")
        #self.gridLayout_4.addWidget(self.Checkbox_LamellaHeight, 0, 0, 1, 1)
        #self.Checkbox_LamellaWidth = QtWidgets.QCheckBox(self.widget3)
        #self.Checkbox_LamellaWidth.setObjectName("Checkbox_LamellaWidth")
        #self.gridLayout_4.addWidget(self.Checkbox_LamellaWidth, 1, 0, 1, 1)

        self.retranslateUi(PatternFileEditor)
        QtCore.QMetaObject.connectSlotsByName(PatternFileEditor)


        ###
        self.output_dir = '~/'
        ###
    def retranslateUi(self, PatternFileEditor):
        _translate = QtCore.QCoreApplication.translate
        PatternFileEditor.setWindowTitle(_translate("PatternFileEditor", "Form"))
        self.label.setText(_translate("PatternFileEditor", "Pattern Designer"))
        self.Button_AddStep.setText(_translate("PatternFileEditor", "Add Step"))
        self.Button_RemoveStep.setText(_translate("PatternFileEditor", "Remove Step"))
        self.Button_AddPattern.setText(_translate("PatternFileEditor", "Add Pattern"))
        self.Button_RemovePattern.setText(_translate("PatternFileEditor", "Remove Pattern"))
        self.label_10.setText(_translate("PatternFileEditor", "PatternType"))
        self.label_11.setText(_translate("PatternFileEditor", "IB Current"))
        self.label_12.setText(_translate("PatternFileEditor", "nA"))
        self.PatternTypeBox.setItemText(0, _translate("PatternFileEditor", "Cross-Section"))
        self.PatternTypeBox.setItemText(1, _translate("PatternFileEditor", "Cleaning Cross-Section"))
        self.PatternTypeBox.setItemText(2, _translate("PatternFileEditor", "Regular"))
        self.Button_ZoomIn.setText(_translate("PatternFileEditor", "Zoom In"))
        self.Button_ZoomOut.setText(_translate("PatternFileEditor", "Zoom Out"))
        self.Button_SavePatternFile.setText(_translate("PatternFileEditor", "Save Pattern File"))
        self.pushButton.setText(_translate("PatternFileEditor", "Load Pattern File"))
        self.label_13.setText(_translate("PatternFileEditor", "PatternDirection"))
        self.PatternDirectionBox.setItemText(0, _translate("PatternFileEditor", "TopToBottom"))
        self.PatternDirectionBox.setItemText(1, _translate("PatternFileEditor", "BottomToTop"))
        self.PatternDirectionBox.setItemText(2, _translate("PatternFileEditor", "LeftToRight"))
        self.PatternDirectionBox.setItemText(3, _translate("PatternFileEditor", "RightToLeft"))
        #self.Checkbox_RTMonitor.setText(_translate("PatternFileEditor", "Perform RT Monitor"))
        self.label_2.setText(_translate("PatternFileEditor", "Offset Y"))
        self.label_5.setText(_translate("PatternFileEditor", "Offset X"))
        self.label_6.setText(_translate("PatternFileEditor", "Height"))
        self.label_8.setText(_translate("PatternFileEditor", "Width"))
        self.label_14.setText(_translate("PatternFileEditor", "Time"))
        self.label_3.setText(_translate("PatternFileEditor", "µm"))
        self.label_4.setText(_translate("PatternFileEditor", "µm"))
        self.label_7.setText(_translate("PatternFileEditor", "µm"))
        self.label_9.setText(_translate("PatternFileEditor", "µm"))
        self.label_15.setText(_translate("PatternFileEditor", "s"))
        #self.Checkbox_LamellaHeight.setText(_translate("PatternFileEditor", "From Lamella Height"))
        #self.Checkbox_LamellaWidth.setText(_translate("PatternFileEditor", "From Lamella Width"))


##########################
        self.Button_AddStep.pressed.connect(self.AddStep)
        self.Button_AddPattern.pressed.connect(self.AddPattern)
        self.Button_RemoveStep.pressed.connect(self.RemoveStep)
        self.Button_RemovePattern.pressed.connect(self.RemovePattern)
        self.Button_ZoomIn.pressed.connect(self.zoomIn)
        self.Button_ZoomOut.pressed.connect(self.zoomOut)
        self.Button_SavePatternFile.pressed.connect(self.savePatternFile)
        self.pushButton.pressed.connect(self.loadPatternFile)


        self.listWidget_Steps.itemClicked.connect(self.showInStepView)
        
        
        self.listWidget_Steps.itemChanged.connect(self.ChangeStep)




        self.Value_IB_Current.valueChanged.connect(self.saveIB_Current)


        self.listWidget_Patterns.itemClicked.connect(self.showInPatternView)
        #self.listWidget_Patterns.itemClicked.connect(self.showPattern)
        self.Value_Height.valueChanged.connect(self.showPattern)
        self.Value_Width.valueChanged.connect(self.showPattern)
        self.Value_OffsetX.valueChanged.connect(self.showPattern)
        self.Value_OffsetY.valueChanged.connect(self.showPattern)
        #self.PatternDirectionBox.currentIndexChanged.connect(self.showPattern)
        #self.PatternTypeBox.currentIndexChanged.connect(self.showPattern)


        self.Value_Width.setMinimum(-1000)
        self.Value_Width.setMaximum(1000)
        self.Value_Height.setMinimum(-1000)
        self.Value_Height.setMaximum(1000)
        self.Value_OffsetX.setMinimum(-1000)
        self.Value_OffsetX.setMaximum(1000)
        self.Value_OffsetY.setMinimum(-1000)
        self.Value_OffsetY.setMaximum(1000)
        self.Value_Time.setMaximum(100000)


        self.step_list=[]
        self.step_dict={}
        self.pattern_handle=0
        self.step_handle="Step 0"
        self.previous_step_name="Step 0"

    
        #Here you can adjust the GraphView objects
        self.scene=QtWidgets.QGraphicsScene()
        self.scene.addLine(1,1,100,1)
        self.graphicsView.setScene(self.scene)
        self.zoom_factor=1

    def AddStep(self):
        try:
            numRows = self.listWidget_Steps.count()
            new_step_name="Step "+str(numRows)
            self.listWidget_Steps.addItem(new_step_name)
            item=self.listWidget_Steps.item(numRows)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            IB_Current=self.Value_IB_Current.value()
            new_step=Step(step_name=new_step_name,IB_Current=IB_Current)
            self.step_dict.update({new_step_name:new_step})
            self.step_list.append(new_step)
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
        return()
    
    def RemoveStep(self):
        try:
            item=self.listWidget_Steps.currentRow()
            text=self.listWidget_Steps.item(item).text()
            self.listWidget_Steps.takeItem(item)

            #del self.step_dict[text]
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
        return()
    
    def AddPattern(self):
        try:
            step_num=self.listWidget_Steps.currentRow()
            step_text=self.listWidget_Steps.item(step_num).text()
            numRows = self.listWidget_Patterns.count()
            pattern_name="Pattern "+str(numRows)
            self.listWidget_Patterns.addItem(pattern_name)
            item=self.listWidget_Patterns.item(numRows)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            #item=self.listWidget_Patterns.item(numRows)
            #print(item)
            #try:
            old_list=self.step_dict[step_text]
            #print(old_list.patterns)
            #print(old_list)


            value_IB_Current=self.Value_IB_Current.value()
            value_Height=self.Value_Height.value()
            value_OffsetX=self.Value_OffsetX.value()
            value_OffsetY=self.Value_OffsetY.value()
            value_Width=self.Value_Width.value()
            time=self.Value_Time.value()

            scan_direction=self.PatternDirectionBox.currentText()
            scan_type=self.PatternTypeBox.currentText()



            New_Pattern=VisPattern(pattern_name=pattern_name,
                                    offset_x=value_OffsetX,
                                    offset_y=value_OffsetY,
                                    height=value_Height,
                                    width=value_Width,
                                    scan_direction=scan_direction,
                                    scan_type=scan_type,
                                    time=time)

            new_list=old_list.patterns+[New_Pattern]
            old_list.patterns=new_list
            if step_num==-1:
                return()
            

                
            self.step_dict.update({step_text:old_list})


        except:
            print("No Step selected")
        return()
    def ChangeStep(self):
        try:
            item=self.listWidget_Steps.currentRow()
            new_name_list=[self.listWidget_Steps.item(i).text() for i in range(self.listWidget_Steps.count())]

            names=[step.step_name for step in self.step_list]
            difference=self.ListDiff(names,new_name_list)


            count=self.listWidget_Steps.count()
            for i in range(count):
                text=self.listWidget_Steps.item(i).text()

                if text in names:
                    continue
                else:

                    if not count==len(self.step_dict):

                        continue
                    else:

                        for renamed in difference:
                            entry=self.step_dict[renamed]
                            entry.step_name=text
                            self.step_dict.update({text:entry})


                            new_name_list=[]
                            for i in self.step_dict:
                                new_name_list.append(self.step_dict[i])
                            self.step_list=new_name_list
                            del self.step_dict[renamed]
                            self.step_handle=renamed

        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())

        return()




    def ListDiff(self,li1,li2):
        return (list(set(li1) - set(li2)))


    def RemovePattern(self):
        try:
            item=self.listWidget_Patterns.currentRow()
            self.listWidget_Patterns.takeItem(item)

            step_num=self.listWidget_Steps.currentRow()
            step_name=self.listWidget_Steps.item(step_num).text()
            pattern_num=self.listWidget_Patterns.currentRow()
            pattern_name=self.listWidget_Patterns.item(pattern_num).text()

            
            step=self.step_dict[step_name]
            print(item)
            pattern_list=step.patterns

            del pattern_list[item]
            step.patterns=pattern_list
        except:
            print("No Pattern selected.")
            print(sys.exc_info())
        return()
    
    def showInStepView(self):
        try:
            num=self.listWidget_Steps.currentRow()
            name=self.listWidget_Steps.item(num).text()

            step=self.step_dict[name]

            self.Value_IB_Current.setValue(step.IB_Current)
            self.listWidget_Patterns.clear()
            for i in step.patterns:

                try:
                    self.listWidget_Patterns.addItem(i.pattern_name)
                except:
                    print("Something went wrong")
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
        return()
    
    def saveIB_Current(self):
        try:
            step_num=self.listWidget_Steps.currentRow()
            step_name=self.listWidget_Steps.item(step_num).text()
            step=self.step_dict[step_name]
            step.IB_Current=self.Value_IB_Current.value()
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
        return()
        
    def showInPatternView(self):
        try:

            step_num=self.listWidget_Steps.currentRow()
            step_name=self.listWidget_Steps.item(step_num).text()
            pattern_num=self.listWidget_Patterns.currentRow()
            pattern_name=self.listWidget_Patterns.item(pattern_num).text()

            step=self.step_dict[step_name]

            try:

                #
                previous_step=self.step_dict[self.previous_step_name]
                previous_pattern=previous_step.patterns[self.pattern_handle]
                previous_pattern.width=self.Value_Width.value()
                previous_pattern.height=self.Value_Height.value()
                previous_pattern.offset_x=self.Value_OffsetX.value()
                previous_pattern.offset_y=self.Value_OffsetY.value()
                previous_pattern.time=self.Value_Time.value()
                previous_pattern.scan_direction=self.PatternDirectionBox.currentText()
                previous_pattern.scan_type=self.PatternTypeBox.currentText()



            except KeyError:
                print("Step has been changed")
            except IndexError:
                print("Step has been changed")




            pattern=step.patterns[pattern_num]

            self.Value_Width.setValue(pattern.width)
            self.Value_Height.setValue(pattern.height)
            self.Value_OffsetX.setValue(pattern.offset_x)
            self.Value_OffsetY.setValue(pattern.offset_y)
            self.Value_Time.setValue(pattern.time)
            self.step_handle=step_num
            self.pattern_handle=pattern_num
            self.previous_step_name=step_name

            ### Set QBoxes
            scan_direction=pattern.scan_direction
            index = self.PatternDirectionBox.findText(scan_direction, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.PatternDirectionBox.setCurrentIndex(index)

            scan_type=pattern.scan_type
            index = self.PatternTypeBox.findText(scan_type, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.PatternTypeBox.setCurrentIndex(index)


            scene=QtWidgets.QGraphicsScene()
            line=QtWidgets.QGraphicsLineItem(self.zoom_factor*125-(50*self.zoom_factor),self.zoom_factor*125,(self.zoom_factor*125)+(50*self.zoom_factor),self.zoom_factor*125)
            scene.addItem(line)
            self.graphicsView.centerOn(line)
            # 20 pixel = 1 um at zoom_factor=1
            coord_offset_x=-self.zoom_factor*20*self.Value_Width.value()/2+(125*self.zoom_factor)
            coord_offset_y=self.zoom_factor*20*self.Value_Height.value()/2-(125*self.zoom_factor)
            rect=QtWidgets.QGraphicsRectItem(QtCore.QRectF((self.zoom_factor*20*self.Value_OffsetX.value())+coord_offset_x,
                                                            (self.zoom_factor*20*self.Value_OffsetY.value())-coord_offset_y,
                                                            self.zoom_factor*(20*self.Value_Width.value()),
                                                            self.zoom_factor*(20*self.Value_Height.value())))
            scene.addItem(rect)
            scene.setSceneRect(0,0,self.zoom_factor*250,self.zoom_factor*250)
            self.graphicsView.setScene(scene)
            self.graphicsView.centerOn(line)
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())

        return()
    
    def showPattern(self):
        try:
            scene=QtWidgets.QGraphicsScene()

            line=QtWidgets.QGraphicsLineItem(self.zoom_factor*125-(50*self.zoom_factor),self.zoom_factor*125,(self.zoom_factor*125)+(50*self.zoom_factor),self.zoom_factor*125)
            scene.addItem(line)

            # 20 pixel = 1 um at zoom_factor=1
            coord_offset_x=-self.zoom_factor*20*self.Value_Width.value()/2+(125*self.zoom_factor)
            coord_offset_y=self.zoom_factor*20*self.Value_Height.value()/2-(125*self.zoom_factor)
            rect=QtWidgets.QGraphicsRectItem(QtCore.QRectF((self.zoom_factor*20*self.Value_OffsetX.value())+coord_offset_x,
                                                            (self.zoom_factor*20*self.Value_OffsetY.value())-coord_offset_y,
                                                            self.zoom_factor*(20*self.Value_Width.value()),
                                                            self.zoom_factor*(20*self.Value_Height.value())))
            scene.addItem(rect)

            scene.setSceneRect(0,0,self.zoom_factor*250,self.zoom_factor*250)
            self.graphicsView.setScene(scene)
            self.graphicsView.centerOn(line)
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())

        return()
    
    def zoomIn(self):
        try:
            if self.zoom_factor >= 1:
                self.zoom_factor+=1
            if self.zoom_factor<1:
                self.zoom_factor=self.zoom_factor*2

            self.showInPatternView()
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
        return()
    def zoomOut(self):
        try:
            if self.zoom_factor > 1:
                self.zoom_factor-=1
            if self.zoom_factor<=1:
                self.zoom_factor=self.zoom_factor/2

            self.showInPatternView()
        except:
            print("Something went wrong, please let us know!")
            print(sys.exc_info())
        return()

    


    def savePatternFile(self):
        
        try:
            pattern_file=session_file=QtWidgets.QFileDialog.getSaveFileName(None, "Saving Pattern File...",self.output_dir,"PatternFile (*.pf)")
            count=self.listWidget_Steps.count()
            with open(pattern_file[0],'w') as output_file:
                for i in range(count):
                    text=self.listWidget_Steps.item(i).text()
                    step=self.step_dict[text]
                    output_file.write("#    Step Name : " +str(self.listWidget_Steps.item(i).text())+'\n')
                    output_file.write('Step_Name=' +str(self.listWidget_Steps.item(i).text())+'\n')
                    output_file.write("Step=" +str(i)+'\n')
                    
                    output_file.write("IB_Current="+str(step.IB_Current)+'e-06\n')


                    patterns=step.patterns
                    output_file.write("Time=" + str(patterns[0].time) + '\n')
                    for j in range(len(patterns)):

                        output_file.write("Pattern="+str(j)+'\n')
                        pattern=patterns[j]

                        output_file.write("Offset_y="+str(pattern.offset_y)+'e-06\n')
                        output_file.write("Offset_x="+str(pattern.offset_x)+'e-06\n')
                        output_file.write("Height_y="+str(pattern.height)+'e-06\n')
                        output_file.write("Width_x="+str(pattern.width)+'e-06\n')
                        output_file.write("PatternType="+str(pattern.scan_type+'\n'))
                        output_file.write("ScanDirection="+str(pattern.scan_direction)+'\n')


                        output_file.write("/Pattern"+'\n')
                    output_file.write("/Step"+'\n')
        except:
            print("Please select a valid file for saving.")
            print(sys.exc_info())
        return()

    def loadPatternFile(self):
        try:
            pattern_file=QtWidgets.QFileDialog.getOpenFileNames(None, "Choose Pattern File to load",self.output_dir,"PatternFile (*.pf)")
            pattern_dict,steps_current,step_names=self.custom_file_parser(pattern_file[0][0])
            self.listWidget_Steps.clear()
            step_dict={}
            for i in range(len(steps_current)):
                #print(i)
                step=Step()
                step_list=[]
                step.step_name=step_names[i]
                step_list.append(step)
                
                
                self.listWidget_Steps.addItem(step.step_name)
                
                #for j in pattern_dict:
                pattern_list=[]
                #print(j)
                patterns=pattern_dict[i]
                print(patterns)
                num=0
                for k in range(len(patterns)):
                    if "IB_Current" in patterns[k]:
                        step.IB_Current=float(patterns[k]["IB_Current"].split('=')[1])
 
                    else:
                        pattern_param=patterns[k]

                        pattern_name="Pattern "+str(num)
                        num+=1
                        #try:
                        offset_y=pattern_param['Offset_y']
                        offset_x=pattern_param['Offset_x']
                        height=pattern_param['Height_y']
                        width=pattern_param['Width_x']
                        try:
                            time=float(pattern_param['Time'])
                        except:
                            ### Time already assigned ##
                            pass
                        #except:
                        #    print("Pattern not defined correctly")
                        try:
                            scan_type=pattern_param['PatternType']
                        except:
                            scan_type="Regular"
                        try:
                            scan_direction=pattern_param['ScanDirection']
                        except:
                            scan_direction="TopToBottom"

                        pattern=VisPattern(pattern_name=pattern_name,
                                            offset_x=float(offset_x)*1000000,
                                            offset_y=float(offset_y)*1000000,
                                            width=float(width)*1000000,
                                            height=float(height)*1000000,
                                            scan_direction=scan_direction,
                                            scan_type=scan_type,
                                            time=time)
                        pattern_list.append(pattern)
                #print(pattern_list)
                step.patterns=pattern_list
                step_list.append(step)
                step_dict.update({step.step_name:step})


            self.step_dict=step_dict
            self.step_list=step_list
            

            patterns=pattern_dict[0]
            #print(patterns)
            #print(self.step_list[0])
            #print(pattern_dict)
            #print(steps_current)
            #self.listWidget_Steps.setSelection(self.listWidget_Steps.item(0))
            self.listWidget_Steps.setCurrentRow(0)
            self.showInStepView()
            self.listWidget_Patterns.setCurrentRow(0)
            #print(float(patterns[1]['Height_y']))
            self.Value_Height.setValue(float(patterns[1]['Height_y'])*1e06)
            self.Value_Width.setValue(float(patterns[1]['Width_x'])*1e06)
            self.Value_OffsetX.setValue(float(patterns[1]['Offset_x'])*1e06)
            self.Value_OffsetY.setValue(float(patterns[1]['Offset_y'])*1e06)
            self.Value_Time.setValue(float(patterns[1]['Time']))
            #self.Value_OffsetY.setValue(float(patterns[1]['Offset_y'])*1e06)
            self.PatternDirectionBox.setCurrentText(patterns[1]['ScanDirection'])
            self.PatternTypeBox.setCurrentText(patterns[1]['PatternType'])
            #IB
            self.Value_IB_Current.setValue(float(steps_current[0])*1e09)
            
            self.showInPatternView()

            self.showInStepView()
            self.showInPatternView()
            #self.listWidget_Patterns.setSelection(0)
            #self.Value_Height.setValue(float(patterns[1]['Height_y'])*1e06)
            #self.showPattern()
        except:
            print("No patternfile selected or file seems to be corrupt.")
            print(sys.exc_info())

        return()
    


    def custom_file_parser(self,custom_filename):
        steps_current=[]
        steps=[]
        step=[]
        step_names=[]
        #step_times=[]
        with open(custom_filename,'r') as input_file:
            inRecordingMode = False
            for line in input_file.readlines():
                #print(line)
                if line.startswith('#'):
                    pass
                if line.startswith('IB_Current'):
                    steps_current.append(line.split('=')[1])
                if line.startswith("Step_Name="):
                    step_names.append(line.split('=')[1][:-1])
                #if line.startswith("Time"):
                #    step_times.append(line.split('=')[1][:-1])
                if not inRecordingMode:
                    if line.startswith('Step='):
                        inRecordingMode = True
                elif line.startswith('/Step'):
                    inRecordingMode = False
                    steps.append(step)
                    step=[]

                else:
                    step.append(line)
        #print(step)
        inRecordingMode = False
        pattern_dict={}
        num=0
        for i in steps:
            patterns=[]
            pattern={}
            for j in i:
                if j.startswith('#'):
                    pass
                if j.startswith('Time'):
                    pattern.update({j.split('=')[0]:j.split('=')[1][:-1]})
                if not inRecordingMode:
                    if j.startswith('Pattern'):
                        inRecordingMode = True

                elif j.startswith('/Pattern'):
                    inRecordingMode = False
                    patterns.append({'IB_Current':i[0][:-1]})
                    patterns.append(pattern)
                    pattern={}

                else:
                    try:
                        pattern.update({j.split('=')[0]:j.split('=')[1][:-1]})
                    except:
                        continue
            pattern_dict.update({num:patterns})
            num=num+1
        return(pattern_dict,steps_current,step_names)
        


    
    



    
    



class VisPattern():
    def __init__(self,pattern_name='Pattern 0',offset_x=0,offset_y=0,depth=10,width=10,height=10,scan_direction='TopToBottom',scan_type='Regular',time=120):
        self.pattern_name=pattern_name
        self.offset_x=offset_x
        self.offset_y=offset_y
        self.depth=depth
        self.width=width
        self.height=height
        self.scan_direction=scan_direction
        self.scan_type=scan_type
        self.time=time

class Step():
    def __init__(self,step_name='Step',IB_Current=10e-12,Patterns=[]):
        self.IB_Current=IB_Current
        self.patterns=Patterns
        self.step_name=step_name




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_PatternFileEditor()
    ui.setupUi(MainWindow)
    MainWindow.installEventFilter(MainWindow)


    MainWindow.show()
    sys.exit(app.exec_())


#########################





