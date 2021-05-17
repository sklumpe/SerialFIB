#!/usr/bin/env python3

'''Calculate projection based on 3DCT parameters, multithreaded

Projector class to organise data in instances
QThreadPool for responsive GUI during long operation
'''

import numpy as np
import os, sys, traceback, psutil
import argparse

import tifffile
from scipy import ndimage

from typing import Tuple

from tools3dct.core import Param3D, corr_transform
from tools3dct import docs

from PyQt5 import QtGui, QtWidgets, QtCore

class Ui_MainWindow(object):
    def __init__(self,paramFiles,cfFiles,maskFile):
        self.paramFiles = paramFiles
        self.cfFiles = cfFiles
        self.maskFile = maskFile
        self.workdir = os.getcwd()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(674, 317)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_vol4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_vol4.setObjectName("lineEdit_vol4")
        self.gridLayout.addWidget(self.lineEdit_vol4, 4, 1, 1, 1)
        self.lineEdit_mask = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_mask.setObjectName("lineEdit_mask")
        self.gridLayout.addWidget(self.lineEdit_mask, 7, 1, 1, 1)
        self.lineEdit_param2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_param2.setObjectName("lineEdit_param2")
        self.gridLayout.addWidget(self.lineEdit_param2, 6, 1, 1, 1)
        self.lineEdit_param1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_param1.setObjectName("lineEdit_param1")
        self.gridLayout.addWidget(self.lineEdit_param1, 5, 1, 1, 1)
        self.toolButton_vol3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_vol3.setObjectName("toolButton_vol3")
        self.gridLayout.addWidget(self.toolButton_vol3, 3, 2, 1, 1)
        self.toolButton_param2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_param2.setObjectName("toolButton_param2")
        self.gridLayout.addWidget(self.toolButton_param2, 6, 2, 1, 1)
        self.toolButton_mask = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_mask.setObjectName("toolButton_mask")
        self.gridLayout.addWidget(self.toolButton_mask, 7, 2, 1, 1)
        self.toolButton_vol2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_vol2.setObjectName("toolButton_vol2")
        self.gridLayout.addWidget(self.toolButton_vol2, 2, 2, 1, 1)
        self.lineEdit_vol1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_vol1.setObjectName("lineEdit_vol1")
        self.gridLayout.addWidget(self.lineEdit_vol1, 1, 1, 1, 1)
        self.toolButton_vol1 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_vol1.setObjectName("toolButton_vol1")
        self.gridLayout.addWidget(self.toolButton_vol1, 1, 2, 1, 1)
        self.toolButton_param1 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_param1.setObjectName("toolButton_param1")
        self.gridLayout.addWidget(self.toolButton_param1, 5, 2, 1, 1)
        self.lineEdit_vol3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_vol3.setObjectName("lineEdit_vol3")
        self.gridLayout.addWidget(self.lineEdit_vol3, 3, 1, 1, 1)
        self.lineEdit_vol2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_vol2.setObjectName("lineEdit_vol2")
        self.gridLayout.addWidget(self.lineEdit_vol2, 2, 1, 1, 1)
        self.toolButton_vol4 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_vol4.setObjectName("toolButton_vol4")
        self.gridLayout.addWidget(self.toolButton_vol4, 4, 2, 1, 1)
        self.label_mask = QtWidgets.QLabel(self.centralwidget)
        self.label_mask.setObjectName("label_mask")
        self.gridLayout.addWidget(self.label_mask, 7, 0, 1, 1)
        self.label_param2 = QtWidgets.QLabel(self.centralwidget)
        self.label_param2.setObjectName("label_param2")
        self.gridLayout.addWidget(self.label_param2, 6, 0, 1, 1)
        self.label_param1 = QtWidgets.QLabel(self.centralwidget)
        self.label_param1.setObjectName("label_param1")
        self.gridLayout.addWidget(self.label_param1, 5, 0, 1, 1)
        self.label_vol4 = QtWidgets.QLabel(self.centralwidget)
        self.label_vol4.setObjectName("label_vol4")
        self.gridLayout.addWidget(self.label_vol4, 4, 0, 1, 1)
        self.label_vol3 = QtWidgets.QLabel(self.centralwidget)
        self.label_vol3.setObjectName("label_vol3")
        self.gridLayout.addWidget(self.label_vol3, 3, 0, 1, 1)
        self.label_vol2 = QtWidgets.QLabel(self.centralwidget)
        self.label_vol2.setObjectName("label_vol2")
        self.gridLayout.addWidget(self.label_vol2, 2, 0, 1, 1)
        self.label_vol1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_vol1.sizePolicy().hasHeightForWidth())
        self.label_vol1.setSizePolicy(sizePolicy)
        self.label_vol1.setObjectName("label_vol1")
        self.gridLayout.addWidget(self.label_vol1, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton_generateProjections = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_generateProjections.setObjectName("pushButton_generateProjections")
        self.verticalLayout.addWidget(self.pushButton_generateProjections)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setNativeMenuBar(False)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 674, 22))
        self.menuBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menuBar.setObjectName("menuBar")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.MainWindow = MainWindow
        self.helpdoc = docs.help(MainWindow)

        self.lineEdits_vol = [self.lineEdit_vol1, self.lineEdit_vol2, self.lineEdit_vol3, self.lineEdit_vol4]
        self.lineEdits_param = [self.lineEdit_param1, self.lineEdit_param2]
        self.dict_lineEdit = {
            'toolButton_vol1':self.lineEdit_vol1,
            'toolButton_vol2':self.lineEdit_vol2,
            'toolButton_vol3':self.lineEdit_vol3,
            'toolButton_vol4':self.lineEdit_vol4,
            'toolButton_param1':self.lineEdit_param1,
            'toolButton_param2':self.lineEdit_param2,
            'toolButton_mask':self.lineEdit_mask,
        }

        self.actionDocumentation.triggered.connect(self.helpdoc.fluoProject)        
        self.toolButton_vol1.clicked.connect(self.choose_volume)
        self.toolButton_vol2.clicked.connect(self.choose_volume)
        self.toolButton_vol3.clicked.connect(self.choose_volume)
        self.toolButton_vol4.clicked.connect(self.choose_volume)
        self.toolButton_param1.clicked.connect(self.choose_param)
        self.toolButton_param2.clicked.connect(self.choose_param)
        self.toolButton_mask.clicked.connect(self.choose_volume)
        self.pushButton_generateProjections.clicked.connect(self.generate_projections)

        if self.cfFiles is not None:
            count = 0
            for cfFile in self.cfFiles:
                if self.is_volume(cfFile) and count < 4:
                    self.lineEdits_vol[count].setText(cfFile)
                    self.lineEdits_vol[count].setStyleSheet("QLineEdit{background-color: rgba(0,255,0,80);}")
                    if count == 0:
                        self.workdir = os.path.dirname(cfFile)
                    count += 1

        if self.paramFiles is not None:
            count = 0
            for paramFile in self.paramFiles:
                if self.is_param(paramFile) and count < 2:
                    self.lineEdits_param[count].setText(paramFile)
                    self.lineEdits_param[count].setStyleSheet("QLineEdit{background-color: rgba(0,255,0,80);}")
                    count += 1

        if self.is_volume(self.maskFile):
            self.lineEdit_mask.setText(self.maskFile)
            self.lineEdit_mask.setStyleSheet("QLineEdit{background-color: rgba(0,255,0,80);}")


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fluorescence Projection"))
        self.toolButton_vol3.setText(_translate("MainWindow", "..."))
        self.toolButton_param2.setText(_translate("MainWindow", "..."))
        self.toolButton_mask.setText(_translate("MainWindow", "..."))
        self.toolButton_vol2.setText(_translate("MainWindow", "..."))
        self.toolButton_vol1.setText(_translate("MainWindow", "..."))
        self.toolButton_param1.setText(_translate("MainWindow", "..."))
        self.toolButton_vol4.setText(_translate("MainWindow", "..."))
        self.label_mask.setText(_translate("MainWindow", "Mask (optional)"))
        self.label_param2.setText(_translate("MainWindow", "3DCT Parameters"))
        self.label_param1.setText(_translate("MainWindow", "3DCT Parameters"))
        self.label_vol4.setText(_translate("MainWindow", "Fluorescence Volume"))
        self.label_vol3.setText(_translate("MainWindow", "Fluorescence Volume"))
        self.label_vol2.setText(_translate("MainWindow", "Fluorescence Volume"))
        self.label_vol1.setText(_translate("MainWindow", "Fluorescence Volume"))
        self.pushButton_generateProjections.setText(_translate("MainWindow", "Generate Projections"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))

    def choose_volume(self):
        cfFile = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow,'Select resliced fluorescence volume', self.workdir,'Image Files (*.tif *.tiff);; All (*.*)')[0]
        sender = self.MainWindow.sender().objectName()
        lineEdit = self.dict_lineEdit[sender]
        lineEdit.setText(cfFile)
        if self.is_volume(cfFile):
            lineEdit.setStyleSheet("QLineEdit{background-color: rgba(0,255,0,80);}")
            self.workdir = os.path.dirname(cfFile)
        elif cfFile != '':
            lineEdit.setStyleSheet("QLineEdit{background-color: rgba(255,0,0,80);}")
        else:
            lineEdit.setStyleSheet("QLineEdit{background-color: white;}")

    def is_volume(self,f):
        try:
            with tifffile.TiffFile(f) as tif:
                if len(tif.pages) > 1:
                    return True
                else:
                    return False
        except:
            return False

    def choose_param(self):
        paramFile = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow,'Select 3DCT text output', self.workdir,'Text Files (*.txt);; All (*.*)')[0]
        sender = self.MainWindow.sender().objectName()
        lineEdit = self.dict_lineEdit[sender]
        lineEdit.setText(paramFile)
        if self.is_param(paramFile):
            lineEdit.setStyleSheet("QLineEdit{background-color: rgba(0,255,0,80);}")
        elif paramFile != '':
            lineEdit.setStyleSheet("QLineEdit{background-color: rgba(255,0,0,80);}")
        else:
            lineEdit.setStyleSheet("QLineEdit{background-color: white;}")

    def is_param(self,f):
        try:
            param = Param3D(f)
            if param.bxx.size > 0:
                return True
            else:
                return False
        except:
            return False

    def generate_projections(self):
        cfFiles = []
        for lineEdit in self.lineEdits_vol:
            if lineEdit.styleSheet() == "QLineEdit{background-color: rgba(0,255,0,80);}":
                cfFiles.append(lineEdit.text())
        paramFiles = []
        for lineEdit in self.lineEdits_param:
            if lineEdit.styleSheet() == "QLineEdit{background-color: rgba(0,255,0,80);}":
                paramFiles.append(lineEdit.text())
        maskFile = None
        if self.lineEdit_mask.styleSheet() == "QLineEdit{background-color: rgba(0,255,0,80);}":
            maskFile = self.lineEdit_mask.text()
        self.fluo_project_multiple(paramFiles,cfFiles,maskFile,save=True)
        # self.statusbar.showMessage('Projections written to directory: '+self.workdir)

    def fluo_project_multiple(self,paramFiles=None,cfFiles=None,maskFile=None,save=False):
        mask = (tifffile.imread(maskFile)>0) if maskFile else None
        for paramFile in paramFiles:
            param = Param3D(paramFile)
            if param.nX is None:
                param = self.query_xydimensions(param,paramFile)
                if param.nX is None:
                    return
            for cfFile in cfFiles:
                CF = tifffile.imread(cfFile)
                if CF.dtype != np.uint8:
                    if CF.dtype in [np.uint16, np.uint32, np.uint64]:
                        CF = self.normalized_uint8(CF)
                    else:
                        print('Error: unsupported bit depth.')
                        return
                if maskFile:
                    if mask.shape == CF.shape:
                        CF = (CF * mask).astype('uint8')
                    else:
                        print('Error: mask and fluorescence volume have different dimensions.')
                        return
                CFproj = fluo_project_single(param,CF,self.MainWindow)
                if save and CFproj is not None:
                    prefix = '.'.join(os.path.basename(paramFile).split('.')[0:-1])
                    suffix = '.'.join(os.path.basename(cfFile).split('.')[0:-1])
                    if maskFile:
                        suffix += '_masked'
                    savepath = os.path.normpath(os.path.join(param.workdir,'_'.join([prefix,suffix,'proj.tif'])))
                    tifffile.imwrite(savepath,CFproj,photometric='minisblack',compress=0)
                    print('Projection image saved as: '+savepath)
    
    def query_xydimensions(self,param,paramFile):
        while not (isinstance(param.nX,int) and isinstance(param.nY,int) ):
            ans, ok = QtWidgets.QInputDialog.getText(self.MainWindow,'Missing Parameters',''.join(['Please specify output image dimensions for projection based on\n',os.path.basename(paramFile),' in the following format: X,Y']))
            if ok:
                try:
                    param.nX, param.nY = [int(a.strip()) for a in ans.split(',')]
                except:
                    pass
            else:
                param.nX, param.nY = [None, None]
                return param
        return param

    # Convert 3D image stack to 8-bit
    def normalized_uint8(self,image):
        lower_bound = np.min(image)
        upper_bound = np.max(image)
        lut = np.concatenate([
            np.zeros(lower_bound, dtype=image.dtype),
            np.linspace(0, 255, upper_bound - lower_bound).astype(image.dtype),
            np.ones(2 ** (8*image.dtype.itemsize) - upper_bound, dtype=image.dtype) * 255
        ])
        return lut[image].astype(np.uint8)


class QMainWindowCustom(QtWidgets.QMainWindow):
    def __init__(self,parent=None,paramFiles=None,cfFiles=None,maskFile=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow(paramFiles,cfFiles,maskFile)
        self.ui.setupUi(self)


### Base code ###

class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)

class Worker(QtCore.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # return result of processing
        finally:
            self.signals.finished.emit()  # done

# Class for multi-threaded calculation
class Projector:

    def __init__(self,param,CF,parentWidget=None):
        self.param = param
        self.CF = CF
        self.parentWidget = parentWidget
        self.threadpool = QtCore.QThreadPool()
        ncpu = os.cpu_count()
        self.threadpool.setMaxThreadCount(ncpu)
        mem = psutil.virtual_memory()
        if mem.available > 2 * 1024 * 1024 * 1024 * ncpu:
            self.patch_size = 512
        else:
            self.patch_size = 256
        self.npatch = int( np.ceil(self.param.nX/self.patch_size) * np.ceil(self.param.nY/self.patch_size) )
        self.start_coords = []
        self.end_coords = []
        self.patches = []
        self.counter = 0
    
    def store_result(self, result):
        self.start_coords.append(result[0])
        self.end_coords.append(result[1])
        self.patches.append(result[2])
        
    def thread_complete(self):
        self.counter += 1
        if self.counter == self.npatch:
            self.progressDialog.accept()

    # Find z range to evaluate in output space, saves cpu and memory
    def patch_zbounds(self, start_coord, end_coord, m, m_inv, shape, cnrs):

        x1, y1 = start_coord
        x2, y2 = end_coord

        # intersection of confocal volume boundaries with patch edges
        l = np.array([cnrs[1]-cnrs[0],cnrs[2]-cnrs[0],cnrs[4]-cnrs[0],cnrs[3]-cnrs[1],cnrs[5]-cnrs[1],cnrs[3]-cnrs[2],cnrs[6]-cnrs[2],cnrs[7]-cnrs[3],cnrs[5]-cnrs[4],cnrs[6]-cnrs[4],cnrs[7]-cnrs[5],cnrs[7]-cnrs[6]]).repeat(4,axis=0)
        l0 = np.array([cnrs[0],cnrs[0],cnrs[0],cnrs[1],cnrs[1],cnrs[2],cnrs[2],cnrs[3],cnrs[4],cnrs[4],cnrs[5],cnrs[6]]).repeat(4,axis=0)
        p0 = np.array([[x1,y1,0],[x1,y1,0],[x2,y2,0],[x2,y2,0]]).T.repeat(12,axis=0).reshape(3,-1).T
        n = np.array([[1,0,0],[0,1,0],[1,0,0],[0,1,0]]).T.repeat(12,axis=0).reshape(3,-1).T
        d = np.zeros([48])    
        for i in range(48):
            d[i] = np.dot(p0[i]-l0[i],n[i])/np.dot(l[i],n[i])
        pts = np.vstack([d.repeat(3).reshape(-1,3)*l+l0,cnrs]) # calculate points and add vertices
        within = np.logical_and.reduce([pts[:,0]>=x1,pts[:,1]>=y1,pts[:,0]<=(x2),pts[:,1]<=(y2)], dtype=bool)
        pts = np.compress(within,pts,axis=0)
        patch_cnrs = np.array(np.meshgrid([x1,x2],[y1,y2])).T.reshape(4,2) # append corners of patch
        pts_xy = np.vstack([pts[:,[0,1]],patch_cnrs])

        # solve inequality for each corner or xy-position where there is an intersection
        zbounds = np.zeros([pts_xy.shape[0],2])
        for i, pcnr in enumerate(pts_xy):
            u = pcnr[0]
            v = pcnr[1]
            a = np.array([(-1*m_inv[0,0]*u-m_inv[0,1]*v-m_inv[0,3])/m_inv[0,2], \
                        (-1*m_inv[1,0]*u-m_inv[1,1]*v-m_inv[1,3])/m_inv[1,2], \
                        (-1*m_inv[2,0]*u-m_inv[2,1]*v-m_inv[2,3])/m_inv[2,2]])
            b = np.array([(shape[0]-m_inv[0,0]*u-m_inv[0,1]*v-m_inv[0,3])/m_inv[0,2], \
                        (shape[1]-m_inv[1,0]*u-m_inv[1,1]*v-m_inv[1,3])/m_inv[1,2], \
                        (shape[2]-m_inv[2,0]*u-m_inv[2,1]*v-m_inv[2,3])/m_inv[2,2]])
            c = np.array([a,b])
            if m_inv[0,2]<0:
                c[:,0]=np.flip(c[:,0])
            if m_inv[1,2]<0:
                c[:,1]=np.flip(c[:,1])
            if m_inv[2,2]<0:
                c[:,2]=np.flip(c[:,2])
            zbounds[i] = [np.amax(c[0]), np.amin(c[1])]    
        pts_z = np.ravel(np.compress(zbounds[:,0]<=zbounds[:,1],zbounds,axis=0))
        pts_z = np.append(pts_z,np.ravel(np.compress(np.logical_and.reduce([cnrs[:,0]>=x1,cnrs[:,0]<=x2,cnrs[:,1]>=y1,cnrs[:,1]<=y2], dtype=bool),cnrs,axis=0)[:,2])) # append corner of confocal volume if wihtin range
        if pts_z.size != 0:            
            return int(np.floor(np.amin(pts_z))), int(np.ceil(np.amax(pts_z)))
        else:
            return None, None

    # Determine projection for patch
    def proj_patch(self, start_coord, end_coord, m, m_inv, CF_xyz, dest_cnrs) -> Tuple[np.ndarray, np.ndarray]:
        patch_shape = end_coord - start_coord
        z_lb, z_ub = self.patch_zbounds(start_coord,end_coord,m,m_inv,CF_xyz.shape,dest_cnrs)
        if z_lb is None:
            return start_coord, end_coord, np.zeros(patch_shape,dtype='float64')
        else:
            dest_zoffset = -1 * z_lb
            dest_zmax = z_ub - z_lb
        zoffset_inv = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,-1*dest_zoffset],[0,0,0,1]], dtype='float64')
        coord_shift_inv = np.array([[1,0,0,start_coord[0]],[0,1,0,start_coord[1]],[0,0,1,0],[0,0,0,1]], dtype='float64')
        complete_inv = np.matmul(np.matmul(m_inv,zoffset_inv),coord_shift_inv)
        patch = np.amax(ndimage.affine_transform(CF_xyz,complete_inv,output_shape=(patch_shape[0],patch_shape[1],dest_zmax),order=1),2)
        return start_coord, end_coord, patch

    # Find projection in patches, multithreading
    # affine_transform performs spline filtering when order greater than 1, memory heavy
    def fluorescence_proj_mt(self,repos_tx=0,repos_ty=0,repos_s=1) -> np.ndarray:

        # 3DCT numbers
        nX = self.param.nX
        nY = self.param.nY
        phi = self.param.phi
        psi = self.param.psi
        theta = self.param.theta
        s =  self.param.s
        tx = self.param.tx
        ty = self.param.ty
        tz = self.param.tz
        
        # rearrange axes for affine transform
        CF_xyz = np.moveaxis(np.moveaxis(self.CF,0,2),0,1)

        # calculate transform matrices
        corrmat, corrmat_inv = corr_transform(s,tx,ty,tz,phi,theta,psi,repos_tx,repos_ty,repos_s)

        # calculate volume corners after transformation
        src_cnrs = np.vstack([np.array(np.meshgrid([0,CF_xyz.shape[0]], [0,CF_xyz.shape[1]], [0,CF_xyz.shape[2]])).reshape(3,-1), np.ones(8)])
        dest_cnrs = np.matmul(corrmat,src_cnrs)[0:3].T

        start_pixel_coords = np.array(np.mgrid[0:nX:self.patch_size,0:nY:self.patch_size]).T.reshape(-1,2).astype(int)
        end_pixel_coords = start_pixel_coords + self.patch_size
        end_pixel_coords[end_pixel_coords[:,0]>nX,0] = nX
        end_pixel_coords[end_pixel_coords[:,1]>nY,1] = nY

        # find projection in patches, option to cancel
        self.progressDialog = QtWidgets.QDialog(self.parentWidget)
        verticalLayout = QtWidgets.QVBoxLayout(self.progressDialog)
        label = QtWidgets.QLabel("Computing projection...",self.progressDialog)
        verticalLayout.addWidget(label)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,self.progressDialog)
        buttonBox.rejected.connect(self.progressDialog.reject)
        verticalLayout.addWidget(buttonBox)

        for start_coord, end_coord in zip(start_pixel_coords,end_pixel_coords):
            worker = Worker(self.proj_patch,start_coord,end_coord,corrmat,corrmat_inv,CF_xyz,dest_cnrs) # fn, args, kwargs
            worker.signals.result.connect(self.store_result) # return coord, patch in a tuple
            worker.signals.finished.connect(self.thread_complete)
            self.threadpool.start(worker)
        if self.progressDialog.exec() == QtWidgets.QDialog.Rejected:
            print("Aborting calculation...")
            self.threadpool.clear()
            return None

        CFproj = np.zeros([nX,nY])
        for start_coord, end_coord, patch in zip(self.start_coords,self.end_coords,self.patches):
            CFproj[start_coord[0]:end_coord[0],start_coord[1]:end_coord[1]] = patch
        CFproj = np.transpose(np.ndarray.astype((CFproj-np.amin(CFproj))/(np.amax(CFproj)-np.amin(CFproj))*255,'uint8'))

        return CFproj


### Wrapper functions ###

# Compute, save and return projection
def fluo_project_single(param,CF,parentWidget=None):
    fluoprojector = Projector(param,CF,parentWidget)
    CFproj = fluoprojector.fluorescence_proj_mt()
    return CFproj

def fluo_project_GUI(paramFiles=None,cfFiles=None,maskFile=None,parentWidget=None):
    MainWindow = QMainWindowCustom(parentWidget,paramFiles,cfFiles,maskFile)
    MainWindow.show()
    return MainWindow


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Project resliced fluorescence volum(s) based on correlation')
    parser.add_argument('--corr', dest='paramFiles', nargs='+', metavar='FILE', help='3DCT text output for the correlated image')
    parser.add_argument('--fluo', dest='cfFiles', nargs='+', metavar='FILE', help='resliced fluorescence volume(s)')
    parser.add_argument('--mask', dest='maskFile', metavar='FILE', help='(optional) fluorescence volume mask')
    args = parser.parse_args()

    if args.paramFiles is not None:
        for i, paramFile in enumerate(args.paramFiles):
            args.paramFiles[i] = os.path.abspath(paramFile)
    if args.cfFiles is not None:
        for i, cfFile in enumerate(args.cfFiles):
            args.cfFiles[i] = os.path.abspath(cfFile)
    if args.maskFile is not None:
        args.maskFile = os.path.abspath(args.maskFile)
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = fluo_project_GUI(args.paramFiles,args.cfFiles,args.maskFile)
    sys.exit(app.exec_())
