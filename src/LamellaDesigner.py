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

# Form implementation generated from reading ui file 'LamellaDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys

class Ui_LamellaDesigner(object):
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
        self.label_13.setGeometry(QtCore.QRect(370, 560, 101, 41))
        self.label_13.setObjectName("label_13")
        self.PatternDirectionBox = QtWidgets.QComboBox(PatternFileEditor)
        self.PatternDirectionBox.setGeometry(QtCore.QRect(460, 570, 151, 26))
        self.PatternDirectionBox.setObjectName("PatternDirectionBox")
        self.PatternDirectionBox.addItem("")
        self.PatternDirectionBox.addItem("")
        self.PatternDirectionBox.addItem("")
        #self.Checkbox_RTMonitor = QtWidgets.QCheckBox(PatternFileEditor)
        #self.Checkbox_RTMonitor.setGeometry(QtCore.QRect(620, 540, 150, 31))
        #self.Checkbox_RTMonitor.setObjectName("Checkbox_RTMonitor")
        self.layoutWidget = QtWidgets.QWidget(PatternFileEditor)
        self.layoutWidget.setGeometry(QtCore.QRect(490, 370, 70, 162))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Value_WidthRed = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.Value_WidthRed.setObjectName("Value_Width")
        self.gridLayout.addWidget(self.Value_WidthRed, 2, 0, 1, 1)
        self.Value_Pattern = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.Value_Pattern.setObjectName("Value_Pattern")
        self.gridLayout.addWidget(self.Value_Pattern, 1, 0, 1, 1)
        self.Value_Lamella = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.Value_Lamella.setObjectName("Value_Lamella")
        self.gridLayout.addWidget(self.Value_Lamella, 0, 0, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(PatternFileEditor)
        self.layoutWidget1.setGeometry(QtCore.QRect(370, 370, 114, 161))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(PatternFileEditor)
        self.layoutWidget2.setGeometry(QtCore.QRect(560, 370, 41, 161))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(PatternFileEditor)
        self.label_16.setGeometry(QtCore.QRect(610, 490, 131, 26))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(PatternFileEditor)
        self.label_17.setGeometry(QtCore.QRect(130, 70, 61, 34))
        self.label_17.setObjectName("label_17")
        self.Value_Time = QtWidgets.QSpinBox(PatternFileEditor)
        self.Value_Time.setGeometry(QtCore.QRect(210, 80, 68, 24))
        self.Value_Time.setObjectName("Value_Time_2")
        self.Value_Time.setValue(int(30))
        self.label_18 = QtWidgets.QLabel(PatternFileEditor)
        self.label_18.setGeometry(QtCore.QRect(280, 70, 39, 34))
        self.label_18.setObjectName("label_18")

        self.retranslateUi(PatternFileEditor)
        QtCore.QMetaObject.connectSlotsByName(PatternFileEditor)


        ###
        self.output_dir = '~/'
        ###
    def retranslateUi(self, PatternFileEditor):
        _translate = QtCore.QCoreApplication.translate
        PatternFileEditor.setWindowTitle(_translate("PatternFileEditor", "Form"))
        self.label.setText(_translate("PatternFileEditor", "Lamella Designer"))
        self.Button_AddStep.setText(_translate("PatternFileEditor", "Add Step"))
        self.Button_RemoveStep.setText(_translate("PatternFileEditor", "Remove Step"))
        self.label_10.setText(_translate("PatternFileEditor", "PatternType"))
        self.label_11.setText(_translate("PatternFileEditor", "IB Current"))
        self.label_12.setText(_translate("PatternFileEditor", "nA"))
        self.PatternTypeBox.setItemText(0, _translate("PatternFileEditor", "Cross-Section"))
        self.PatternTypeBox.setItemText(1, _translate("PatternFileEditor", "Cleaning Cross-Section"))
        self.PatternTypeBox.setItemText(2, _translate("PatternFileEditor", "Regular"))
        self.Button_ZoomIn.setText(_translate("PatternFileEditor", "Zoom In"))
        self.Button_ZoomOut.setText(_translate("PatternFileEditor", "Zoom Out"))
        self.Button_SavePatternFile.setText(_translate("PatternFileEditor", "Save Protocol"))
        self.pushButton.setText(_translate("PatternFileEditor", "Load Protocol"))
        self.label_13.setText(_translate("PatternFileEditor", "MillingSide"))
        self.PatternDirectionBox.setItemText(0, _translate("PatternFileEditor", "both"))
        self.PatternDirectionBox.setItemText(1, _translate("PatternFileEditor", "top"))
        self.PatternDirectionBox.setItemText(2, _translate("PatternFileEditor", "bottom"))
        #self.Checkbox_RTMonitor.setText(_translate("PatternFileEditor", "Perform RT Monitor"))
        self.label_5.setText(_translate("PatternFileEditor", "Pattern Thickness"))
        self.label_8.setText(_translate("PatternFileEditor", "Width Reduction"))
        self.label_2.setText(_translate("PatternFileEditor", "Lamella Thickness"))
        self.label_3.setText(_translate("PatternFileEditor", "µm"))
        self.label_4.setText(_translate("PatternFileEditor", "µm"))
        self.label_9.setText(_translate("PatternFileEditor", "%"))
        self.label_16.setText(_translate("PatternFileEditor", "not implemented yet"))
        self.label_17.setText(_translate("PatternFileEditor", "Time"))
        self.label_18.setText(_translate("PatternFileEditor", "s"))



##########################
        self.Button_AddStep.pressed.connect(self.AddStep)
        self.Button_AddStep.pressed.connect(self.AddPattern)
        self.Button_AddStep.pressed.connect(self.AddPattern)

        self.Button_RemoveStep.pressed.connect(self.RemoveStep)
        self.Button_RemoveStep.pressed.connect(self.RemovePattern)
        self.Button_RemoveStep.pressed.connect(self.RemovePattern)

        self.Button_ZoomIn.pressed.connect(self.zoomIn)
        self.Button_ZoomOut.pressed.connect(self.zoomOut)
        self.Button_SavePatternFile.pressed.connect(self.saveProtocolFile)
        self.pushButton.pressed.connect(self.loadPatternFile)


        self.listWidget_Steps.itemClicked.connect(self.showInStepView)
        self.listWidget_Steps.itemClicked.connect(self.showInPatternView)
        
        self.listWidget_Steps.itemChanged.connect(self.ChangeStep)


        self.Value_Height=1
        self.Value_Width=1

        self.Value_IB_Current.valueChanged.connect(self.saveIB_Current)



        self.Value_WidthRed.valueChanged.connect(self.showPattern)
        self.Value_Pattern.valueChanged.connect(self.showPattern)
        self.Value_Lamella.valueChanged.connect(self.showPattern)


        self.Value_WidthRed.setMinimum(-100)
        #self.Value_Height.setMinimum(-100)
        self.Value_Pattern.setMinimum(-100)
        self.Value_Lamella.setMinimum(-100)

        self.Value_WidthRed.setMaximum(1000)
        # self.Value_Height.setMinimum(-100)
        self.Value_Pattern.setMaximum(1000)
        self.Value_Lamella.setMaximum(1000)


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
        numRows = self.listWidget_Steps.count()
        new_step_name="Step "+str(numRows)
        self.listWidget_Steps.addItem(new_step_name)
        item=self.listWidget_Steps.item(numRows)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        IB_Current=self.Value_IB_Current.value()
        new_step=Step(step_name=new_step_name,IB_Current=IB_Current)
        self.step_dict.update({new_step_name:new_step})
        self.step_list.append(new_step)
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

        step_num=self.listWidget_Steps.count()
        step_text=self.listWidget_Steps.item(step_num-1).text()
        numRows = self.listWidget_Patterns.count()
        if numRows%2==0:
            pattern_name="Pattern "+str('top')
        else:
            pattern_name="Pattern "+str('bottom')
        self.listWidget_Patterns.addItem(pattern_name)
        item=self.listWidget_Patterns.item(numRows)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

        old_list=self.step_dict[step_text]



        value_IB_Current=self.Value_IB_Current.value()

        value_Height=0
        value_pattern=self.Value_Pattern.value()
        value_lamella=self.Value_Lamella.value()
        value_Width=self.Value_Width
        time=self.Value_Time.value()

        scan_direction=self.PatternDirectionBox.currentText()
        scan_type=self.PatternTypeBox.currentText()



        New_Pattern=VisPattern(pattern_name=pattern_name,
                                value_pattern=value_pattern,
                                value_lamella=value_lamella,
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


        return()
    def ChangeStep(self):
        item=self.listWidget_Steps.currentRow()
        new_name_list=[self.listWidget_Steps.item(i).text() for i in range(self.listWidget_Steps.count())]
        
        names=[step.step_name for step in self.step_list]
        difference=self.ListDiff(names,new_name_list)


        count=self.listWidget_Steps.count()
        for i in range(count):
            text=self.listWidget_Steps.item(i).text()
            #print(text)
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

        return()




    def ListDiff(self,li1,li2):
        return (list(set(li1) - set(li2)))


    def RemovePattern(self):
        try:

            item=self.listWidget_Patterns.count()
            self.listWidget_Patterns.takeItem(item-1)

            step_num=self.listWidget_Steps.currentRow()
            step_name=self.listWidget_Steps.item(step_num).text()
            pattern_num=self.listWidget_Patterns.currentRow()
            pattern_name=self.listWidget_Patterns.item(pattern_num).text()

            
            step=self.step_dict[step_name]

            pattern_list=step.patterns

            del pattern_list[item]
            step.patterns=pattern_list
        except:
            print("No Pattern selected.")
            print(sys.exc_info())
        return()
    
    def showInStepView(self):
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

            pattern_num=0
            pattern_name=self.listWidget_Patterns.item(pattern_num).text()

            step=self.step_dict[step_name]

            try:

                previous_step=self.step_dict[self.previous_step_name]
                previous_pattern=previous_step.patterns[self.pattern_handle]
                previous_pattern.width=self.Value_Width
                previous_pattern.height=self.Value_Pattern.value()
                previous_pattern.value_pattern=self.Value_Pattern.value()
                previous_pattern.value_lamella=self.Value_Lamella.value()

                previous_pattern.time=self.Value_Time.value()
                previous_pattern.scan_direction=self.PatternDirectionBox.currentText()
                previous_pattern.scan_type=self.PatternTypeBox.currentText()




            except KeyError:
                print("Step has been changed")
            except IndexError:
                print("Step has been changed")





            pattern=step.patterns[pattern_num]


            self.Value_Pattern.setValue(pattern.value_pattern)
            self.Value_Lamella.setValue(pattern.value_lamella)
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
            line_x1=self.zoom_factor*125-(50*self.zoom_factor)
            line_y1=self.zoom_factor*125
            line_x2=(self.zoom_factor*125)+(50*self.zoom_factor)
            line_y2=self.zoom_factor*125
            line=QtWidgets.QGraphicsLineItem(line_x1,line_y1,line_x2,line_y2)
            scene.addItem(line)
            self.graphicsView.centerOn(line)

            coord_offset_x=-self.zoom_factor*20*self.Value_Width/2+(125*self.zoom_factor)
            coord_offset_y=self.zoom_factor*20*self.Value_Height/2-(125*self.zoom_factor)

            x=self.zoom_factor*125/2
            y=self.zoom_factor*125+self.zoom_factor*20*(self.Value_Lamella.value()/2 )#+ self.Value_Pattern.value()/2)
            y2=self.zoom_factor*125-self.zoom_factor*20*(self.Value_Lamella.value()/2 )
            width=self.zoom_factor*125*self.Value_Width
            height=self.zoom_factor*20*self.Value_Pattern.value()
            rect=QtWidgets.QGraphicsRectItem(QtCore.QRectF(x,#+coord_offset_x,
                                                            y,#-coord_offset_y,
                                                            width,
                                                            height))
            scene.addItem(rect)

            rect2=QtWidgets.QGraphicsRectItem(QtCore.QRectF(x,#+coord_offset_x,
                                                            y2,#-coord_offset_y,
                                                            width,
                                                            -height))
            scene.addItem(rect2)
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
            #self.zoom_factor=2


            line=QtWidgets.QGraphicsLineItem(self.zoom_factor*125-(50*self.zoom_factor),self.zoom_factor*125,(self.zoom_factor*125)+(50*self.zoom_factor),self.zoom_factor*125)
            scene.addItem(line)

            # 20 pixel = 1 um at zoom_factor=1
            self.Value_Height=1

            coord_offset_y=self.zoom_factor*20*self.Value_Height/2-(250*self.zoom_factor)

            #x=self.zoom_factor*125
            x=self.zoom_factor*125/2
            y=self.zoom_factor*125+self.zoom_factor*20*(self.Value_Lamella.value()/2 )#+ self.Value_Pattern.value()/2)
            y2=self.zoom_factor*125-self.zoom_factor*20*(self.Value_Lamella.value()/2 )
            width=self.zoom_factor*125*self.Value_Width
            height=self.zoom_factor*20*self.Value_Pattern.value()
            rect=QtWidgets.QGraphicsRectItem(QtCore.QRectF(x,#+coord_offset_x,
                                                            y,#-coord_offset_y,
                                                            width,
                                                            height))
            rect2=QtWidgets.QGraphicsRectItem(QtCore.QRectF(x,#+coord_offset_x,
                                                            y2,#-coord_offset_y,
                                                            width,
                                                            -height))
            scene.addItem(rect)
            scene.addItem(rect2)



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

    


    def saveProtocolFile(self):
        import os
        try:
            pattern_file=session_file=QtWidgets.QFileDialog.getSaveFileName(None, "Saving Protocol File...",self.output_dir,"PatternFile (*.pro)")
            count=self.listWidget_Steps.count()
            with open(pattern_file[0],'w') as output_file:
                output_file.write('#    PROTOCOL FILE \n')
                for i in range(count):
                    text=self.listWidget_Steps.item(i).text()
                    step=self.step_dict[text]

                    output_file.write('#    Protocol Step Name :'+str(self.listWidget_Steps.item(i).text())+'\n')
                    output_file.write('Step_Name=' +str(self.listWidget_Steps.item(i).text())+'\n')
                    output_file.write('Step=' +str(i)+'\n')
                    
                    output_file.write('IB_Current='+str(step.IB_Current)+'e-09\n')
                    
                    #output_file.write("Side="+str(step.side))
                    pattern=step.patterns[0]
                    output_file.write('Time='+str(pattern.time)+'\n')
                    output_file.write('Side='+str(pattern.scan_direction)+'\n')
                    output_file.write('thickness_lamella='+str(pattern.value_lamella)+'e-06\n')
                    output_file.write('thickness_patterns='+str(pattern.value_pattern)+'e-06\n')
                    output_file.write('y_center=1e-06\n')
                    output_file.write('width=1e-06\n')
                    output_file.write('pattern_type='+str(pattern.scan_type)+'\n')
                    output_file.write('output_dir=./\n')




                    



                    output_file.write("/Step"+'\n')
        except:
            print("Please select a valid file for saving.")
            print(sys.exc_info())
        return()

    def loadPatternFile(self):
        try:
            protocol_file=QtWidgets.QFileDialog.getOpenFileNames(None, "Choose Pattern File to load",self.output_dir,"PatternFile (*.pro)")


            parameter_list=self.read_protocolfile(protocol_file[0][0])
            self.listWidget_Steps.clear()
            step_dict={}

            for i in parameter_list:

                step=Step()
                step_list=[]
                step.step_name="Step "+str(i['step'])
                step_list.append(step)


                self.listWidget_Steps.addItem(step.step_name)


                pattern_list=[]

                step.IB_Current=float(i["milling_current"]*1e09)
                for k in range(2):

                    names=['top', 'bottom']
                    pattern_name="Pattern "+names[k]

                    value_lamella=i['thickness_lamella']
                    value_pattern=i['thickness_patterns']

                    try:
                        scan_type=i['pattern_type']
                    except:
                        scan_type="Regular"


                    pattern=VisPattern(pattern_name=pattern_name,
                                        value_pattern=float(value_pattern)*1000000,
                                        value_lamella=float(value_lamella)*1000000,

                                        scan_type=scan_type)
                    pattern_list.append(pattern)


                step.patterns=pattern_list
                step_list.append(step)
                step_dict.update({step.step_name:step})


            self.step_dict=step_dict
            self.step_list=step_list


            #patterns=pattern_dict[0]
            #print(parameter_list[0])
            pattern=parameter_list[0]
            #print(pattern)

            print(step_list[0])
            #print(pattern['value_pattern'])
            #patterns=pattern_list
            #print(patterns[1])
            #print(self.step_list[0])
            #self.listWidget_Steps.setSelection(self.listWidget_Steps.item(0))
            self.listWidget_Steps.setCurrentRow(0)
            self.showInStepView()
            self.listWidget_Patterns.setCurrentRow(0)
            #print(float(patterns[1]['Height_y']))
            #self.Value_Height.setValue(float(patterns[0].height)*1e06)
            self.showInPatternView()

            #print(float(pattern['thickness_patterns'])*1e06)
            self.Value_Pattern.setValue(float(pattern['thickness_patterns'])*1e06)
            self.Value_Lamella.setValue(float(pattern['thickness_lamella'])*1e06)
            self.Value_Time.setValue(float(pattern['time']))
            self.PatternTypeBox.setCurrentText(str(pattern['pattern_type']))
            self.PatternDirectionBox.setCurrentText(str(pattern['side']))
            
            #self.Value_Time.setValue(pattern.time)
            


            #self.Value_Width.setValue(float(patterns[0]['Width_x'])*1e06)
            #self.Value_OffsetX.setValue(float(patterns[0]['Offset_x'])*1e06)
            #self.Value_OffsetY.setValue(float(patterns[0]['Offset_y'])*1e06)
            
            
        except:
            print("No patternfile selected or file seems to be corrupt.")
            print(sys.exc_info())

        return()
    


    def read_protocolfile(self,filename):
        parameter_list=[]

        with open(filename,'r') as input_file:
            inRecordingMode = False
            dictionary = {}
            for line in input_file.readlines():

                if line.startswith('#'):
                    pass
                elif line.startswith('Step'):
                    dictionary.update({'step':line.split('=')[1].rstrip('\n')})
                elif line.startswith('Side'):
                    dictionary.update({'side': line.split('=')[1].rstrip('\n')})
                elif line.startswith('thickness_lamella'):
                    dictionary.update({'thickness_lamella': float(line.split('=')[1].rstrip('\n'))})
                elif line.startswith('thickness_patterns'):
                    dictionary.update({'thickness_patterns': float(line.split('=')[1].rstrip('\n'))})
                elif line.startswith('y_center'):
                    dictionary.update({'y_center': float(line.split('=')[1].rstrip('\n'))})
                elif line.startswith('width'):
                    dictionary.update({'width': float(line.split('=')[1].rstrip('\n'))})
                elif line.startswith('pattern_type'):
                    dictionary.update({'pattern_type': line.split('=')[1].rstrip('\n')})
                elif line.startswith('IB_Current'):
                    dictionary.update({'milling_current': float(line.split('=')[1].rstrip('\n'))})
                elif line.startswith('Time'):
                    dictionary.update({'time': int(line.split('=')[1].rstrip('\n'))})
                elif line.startswith('output_dir'):
                    dictionary.update({'output_dir': line.split('=')[1].rstrip('\n')})


                if not inRecordingMode:
                    if line.startswith('Step='):
                        inRecordingMode = True
                elif line.startswith('/Step'):
                    inRecordingMode = False
                    parameter_list.append(dictionary)
                    dictionary = {}

                else:
                    pass

        return(parameter_list)

    def custom_file_parser(self,custom_filename):
        steps_current=[]
        steps=[]
        step=[]
        step_names=[]
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
                if not inRecordingMode:
                    if line.startswith('Step='):
                        inRecordingMode = True
                elif line.startswith('/Step'):
                    inRecordingMode = False
                    steps.append(step)
                    step=[]

                else:
                    step.append(line)

        inRecordingMode = False
        pattern_dict={}
        num=0
        for i in steps:
            patterns=[]
            pattern={}
            for j in i:
                if j.startswith('#'):
                    pass
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
    def __init__(self,pattern_name='Pattern 0',value_pattern=0,value_lamella=0,depth=10,width=10,height=10,scan_direction='both',scan_type='Regular',time=120):
        self.pattern_name=pattern_name
        self.value_pattern=value_pattern
        self.value_lamella=value_lamella
        self.depth=depth
        self.width=width
        self.height=height
        self.scan_direction=scan_direction
        self.scan_type=scan_type
        self.time=time
        #self.sides=sides

class Step():
    def __init__(self,step_name='Step',IB_Current=10e-12,Patterns=[]):
        self.IB_Current=IB_Current
        self.patterns=Patterns
        self.step_name=step_name




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LamellaDesigner()
    ui.setupUi(MainWindow)
    MainWindow.installEventFilter(MainWindow)


    MainWindow.show()
    sys.exit(app.exec_())


