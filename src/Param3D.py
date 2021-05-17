import numpy as np
import re
import os
from typing import Tuple
from PyQt5 import QtCore, QtGui, QtWidgets
# import matplotlib.pyplot as plt

# Parser for 3DCT text output
class Param3D:
    def __init__(self,txtfile):
        self.workdir = os.path.dirname(os.path.abspath(txtfile))
        self.nX = None
        self.nY = None
        with open(txtfile) as f:
            for line in f:
                line = line.rstrip()
                if "Euler" in line:
                    foo = re.split("[\[\],\s]+",line)
                    self.phi = float(foo[-4])/180*np.pi
                    self.psi = float(foo[-3])/180*np.pi
                    self.theta = float(foo[-2])/180*np.pi
                elif "rotation around [0,0,0]" in line:
                    foo = re.split("[\[\],\s]+",line)
                    self.tx = float(foo[-4])
                    self.ty = float(foo[-3])
                    self.tz = float(foo[-2])
                elif "scale" in line:
                    self.s = float(re.split("[\s=]+",line)[-1])
                elif "This center is at x/y" in line:
                    foo = re.search("\d+\.?\d*/\d+\.?\d*",line)
                    foo2 = re.split("/",foo.group())
                    self.nX = int(float(foo2[0]))*2  # image dimensions
                    self.nY = int(float(foo2[1]))*2
            foo = f.seek(0)
            bxx, byy, bzz, xx, yy, zz = [],[],[],[],[],[]
            for line in f:
                if "Initial (3D) markers" in line:
                    line = next(f).rstrip()
                    while "#" not in line:
                        while line == '':
                            line = next(f,'#').rstrip()
                        foo = re.split("\s+", line)
                        if len(foo) > 1:
                            bxx.append(float(foo[-7]))
                            byy.append(float(foo[-6]))
                            bzz.append(float(foo[-5]))
                        line = next(f,'#').rstrip()
                        while line == '':
                            line = next(f,'#').rstrip()
                if "Correlated spots" in line:
                    line = next(f).rstrip()
                    while "#" not in line:
                        while line == '':
                            line = next(f,'#').rstrip()
                        foo = re.split("\s+", line)
                        if len(foo) > 1:
                            xx.append(float(foo[-3]))
                            yy.append(float(foo[-2]))
                            zz.append(float(foo[-1]))
                        line = next(f,'#').rstrip()
                        while line == '':
                            line = next(f,'#').rstrip()
                    break
            self.bxx = np.array(bxx)
            self.byy = np.array(byy)
            self.bzz = np.array(bzz)
            self.xx = np.array(xx)
            self.yy = np.array(yy)
            self.zz = np.array(zz)

# Custom QGraphicsScene subclass
class QGraphicsSceneCustom(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        if event.delta() > 0:
            scalingFactor = 1.15
        else:
            scalingFactor = 1 / 1.15
        mouse_position = event.scenePos()
        view_center = self.parent().mapToScene(QtCore.QPoint(self.parent().width()//2,self.parent().height()//2))
        new_center = mouse_position+(view_center-mouse_position)/scalingFactor
        self.parent().scale(scalingFactor, scalingFactor)
        self.parent().centerOn(new_center)
        event.accept()

    def mouseReleaseEvent(self, event):
        super(QGraphicsSceneCustom,self).mouseReleaseEvent(event)
        self.parent().setDragMode(QtWidgets.QGraphicsView.NoDrag)

# Homogeneous translation matrix
def translate(tx,ty,tz):
    tr = np.array([ [1,0,0,tx],[0,1,0,ty],[0,0,1,tz],[0,0,0,1]], dtype='float64')
    return tr

# Homogeneous rotation matrix in the ZXZ convention, angles in radians
def rotate(phi,theta,psi):
    rot = np.array([[np.cos(psi)*np.cos(phi)-np.cos(theta)*np.sin(psi)*np.sin(phi), -np.cos(psi)*np.sin(phi)-np.cos(theta)*np.cos(phi)*np.sin(psi), np.sin(psi)*np.sin(theta), 0], \
                    [np.cos(phi)*np.sin(psi)+np.cos(psi)*np.cos(theta)*np.sin(phi), np.cos(psi)*np.cos(theta)*np.cos(phi)-np.sin(psi)*np.sin(phi), -np.cos(psi)*np.sin(theta), 0], \
                    [np.sin(theta)*np.sin(phi), np.cos(phi)*np.sin(theta), np.cos(theta), 0], \
                    [0,0,0,1]], dtype='float64')
    return rot

# Homogeneous scaling matrix
def scale(s):
    sca = np.array([ [s,0,0,0],[0,s,0,0],[0,0,s,0],[0,0,0,1]])
    return sca

# Full 3D transform required for projection, accounting for additional translation and scaling of view, and its inverse
def corr_transform(s,tx,ty,tz,phi,theta,psi,repos_tx=0,repos_ty=0,repos_s=1) -> Tuple[np.ndarray, np.ndarray]:

    tr = translate(tx,ty,tz)
    tr_inv = translate(-1*tx,-1*ty,-1*tz)

    sca = scale(s)
    sca_inv = scale(1/s)

    rot = rotate(phi,theta,psi)
    rot_inv = rot.T

    m = tr @ sca @ rot
    m_inv = rot_inv @ sca_inv @ tr_inv

    repos_tr = translate(-1*repos_tx,-1*repos_ty,0)
    repos_tr_inv = translate(repos_tx,repos_ty,0)

    repos_sca = scale(repos_s)
    repos_sca_inv = scale(1/repos_s)

    m = repos_sca @ repos_tr @ m
    m_inv = m_inv @ repos_tr_inv @ repos_sca_inv

    return m, m_inv

### Matplotlib functions ###

# # Callback to scroll-zoom in matplotlib figure
# def scroll_zoom(event,scale_factor=1.5):
#     ax = event.inaxes
#     x = event.xdata
#     y = event.ydata
#     xlim = ax.get_xbound()
#     ylim = ax.get_ybound()
#     x_range = xlim[1] - xlim[0]
#     y_range = ylim[1] - ylim[0]
#     x_rel = (x-xlim[0])/x_range
#     y_rel = (y-ylim[0])/y_range
#     if event.button == 'down':
#         scale_factor = 1/scale_factor
#     ax.set_xbound(x-x_range/scale_factor*x_rel,x+x_range/scale_factor*(1-x_rel))
#     ax.set_ybound(y-y_range/scale_factor*y_rel,y+y_range/scale_factor*(1-y_rel))
#     plt.draw()

# # Select an umlimited or set number of points on image
# def point_select(img,nPts,msg1=None,msg2=None):
#     pts = []
#     h = plt.figure()
#     cid = h.canvas.mpl_connect('scroll_event', scroll_zoom)
#     if nPts < 0:
#         plt.imshow(img.data)
#         if msg1 != None:
#             plt.figtext(0.5, 0.94, msg1, wrap=True, horizontalalignment='center', fontsize='large')
#         if msg2 != None:
#             plt.figtext(0.5, 0.893, msg2, wrap=True, horizontalalignment='center', fontsize='small')
#         pts = np.array(plt.ginput(-1, timeout=-1))
#     else:
#         while len(pts) != nPts:
#             plt.imshow(img.data)
#             if msg1 != None:
#                 plt.figtext(0.5, 0.94, msg1, wrap=True, horizontalalignment='center', fontsize='large')
#             if msg2 != None:
#                 plt.figtext(0.5, 0.893, msg2, wrap=True, horizontalalignment='center', fontsize='small')
#             pts = np.array(plt.ginput(-1, timeout=-1))
#             if len(pts) != nPts:
#                 print("Too few or too many points selected. Please try again.")  # Left-click to add points. Right-click or backspace to remove points. Enter to finish.
#     plt.close(h)
#     return pts
