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

'''
find_transform
prepare_8bit
corr_transform
    transformation matrices in homogeneous coordinates
    np.matmul(m,np.array([x,y,z,1])) to calculate points for overlay
limit_cpu
patch_zbounds
proj_patch
fluorescence_proj_mp
    optional parameters: repos_tx,repos_ty,repos_s
    image from take_image_IB may need to have same resolution
    5 min on 4 cpus with 8 GB RAM
'''

import numpy as np
from skimage import io
from scipy import ndimage
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count
import platform, psutil, os
from typing import Tuple
from PyQt5 import QtWidgets

from autoscript_sdb_microscope_client.structures import *

# Rescale high mag image to search within (padded) low mag image
# Point (x,y) in low mag image has coordinate ((x - trans_x)*scale_factor, (_y - trans_y)*scale_factor) in high mag image
# scale factor read from AdornedImage arguments, low mag HFW / high mag HFW > 0
def find_transform(low_mag: AdornedImage, high_mag: AdornedImage):

    # Convert to 8-bit and remove databar (useful for imported image)
    low_mag_8bit = prepare_8bit(low_mag)
    high_mag_8bit = prepare_8bit(high_mag)

    # Rescale high mag image   
    scale_factor = low_mag.metadata.optics.scan_field_of_view.width / high_mag.metadata.optics.scan_field_of_view.width
    high_mag_scaled = cv2.resize(high_mag_8bit,None,fx=1/scale_factor, fy=1/scale_factor, interpolation = cv2.INTER_AREA)

    # Pad low mag image
    pad_height = int(high_mag_scaled.shape[0] / 2)
    pad_width = int(high_mag_scaled.shape[1] / 2)
    low_mag_pad = cv2.copyMakeBorder(low_mag_8bit, pad_height, pad_height, pad_width, pad_width, cv2.BORDER_CONSTANT, value=np.mean(low_mag_8bit))

    # Perform template matching
    res = cv2.matchTemplate(low_mag_pad, high_mag_scaled, eval('cv2.TM_CCORR_NORMED'))
    min_value, max_value, min_location, max_location = cv2.minMaxLoc(res)

    if max_value < 0.8:
        print("Warning. Bad correlation.")

    # Calculate shift (in low mag pixel coordinates)
    trans_x = max_location[0] - pad_width
    trans_y = max_location[1] - pad_height

    return trans_x, trans_y, scale_factor


def prepare_8bit(image: AdornedImage) -> np.ndarray:

    if image.bit_depth == 16:
        lower_bound = np.min(image.data)
        upper_bound = np.max(image.data)
        lut = np.concatenate([
            np.zeros(lower_bound, dtype=np.uint16),
            np.linspace(0, 255, upper_bound - lower_bound).astype(np.uint16),
            np.ones(2 ** 16 - upper_bound, dtype=np.uint16) * 255
        ])
        image_8bit = lut[image.data].astype(np.uint8)
    elif image.bit_depth == 24:
        gray = np.matmul(image.data[...,:3], [0.2989, 0.5870, 0.1140])
        image_8bit = gray.astype(np.uint8)
    elif image.bit_depth != 8:
        raise ValueError("Unsupported bit depth. Please use 8-, 16- or 24-bit images.")
    else:
        image_8bit = image.data

    if image.height in [2188,1164,652]:
        image_8bit = image[0:image.height-140,:] # is databar always 140?

    return image_8bit


# Transformation matrices in homogenous coordinates
def corr_transform(s,tx,ty,tz,phi,psi,theta,repos_tx=0,repos_ty=0,repos_s=1) -> Tuple[np.ndarray, np.ndarray]:

    tr = np.array([ [1,0,0,tx],[0,1,0,ty],[0,0,1,tz],[0,0,0,1]], dtype='float64')
    tr_inv = np.array([ [1,0,0,-1*tx],[0,1,0,-1*ty],[0,0,1,-1*tz],[0,0,0,1]], dtype='float64')

    sca = np.array([ [s,0,0,0],[0,s,0,0],[0,0,s,0],[0,0,0,1]])
    sca_inv = np.array([ [1/s,0,0,0],[0,1/s,0,0],[0,0,1/s,0],[0,0,0,1]], dtype='float64')

    rot = np.array([[np.cos(psi)*np.cos(phi)-np.cos(theta)*np.sin(psi)*np.sin(phi), -np.cos(psi)*np.sin(phi)-np.cos(theta)*np.cos(phi)*np.sin(psi), np.sin(psi)*np.sin(theta), 0], \
                    [np.cos(phi)*np.sin(psi)+np.cos(psi)*np.cos(theta)*np.sin(phi), np.cos(psi)*np.cos(theta)*np.cos(phi)-np.sin(psi)*np.sin(phi), -np.cos(psi)*np.sin(theta), 0], \
                    [np.sin(theta)*np.sin(phi), np.cos(phi)*np.sin(theta), np.cos(theta), 0], \
                    [0,0,0,1]], dtype='float64')

    m = np.matmul( tr, np.matmul(sca,rot) )
    m_inv = np.matmul( np.transpose(rot), np.matmul(sca_inv,tr_inv) )

    # reposition based on registration to current image, overall function may be too slow for this
    repos_tr = np.array([ [1,0,0,-1*repos_tx],[0,1,0,-1*repos_ty],[0,0,1,0],[0,0,0,1]], dtype='float64')
    repos_tr_inv = np.array([ [1,0,0,repos_tx],[0,1,0,repos_ty],[0,0,1,0],[0,0,0,1]], dtype='float64')
    repos_sca = np.array([[repos_s,0,0,0],[0,repos_s,0,0],[0,0,1,0],[0,0,0,1]])
    repos_sca_inv = np.array([ [1/repos_s,0,0,0],[0,1/repos_s,0,0],[0,0,1,0],[0,0,0,1]])

    m = np.matmul(repos_sca, np.matmul(repos_tr,m) )
    m_inv = np.matmul(np.matmul(m_inv,repos_tr_inv),repos_sca_inv)

    return m, m_inv

# Find z range to evaluate in output space, saves cpu and memory
def patch_zbounds(coord, patch_size, m, m_inv, shape, cnrs):

    x = coord[0]
    y = coord[1]
    # intersection with edges, l and l0 to move outside of this function
    l = np.array([cnrs[1]-cnrs[0],cnrs[2]-cnrs[0],cnrs[4]-cnrs[0],cnrs[3]-cnrs[1],cnrs[5]-cnrs[1],cnrs[3]-cnrs[2],cnrs[6]-cnrs[2],cnrs[7]-cnrs[3],cnrs[5]-cnrs[4],cnrs[6]-cnrs[4],cnrs[7]-cnrs[5],cnrs[7]-cnrs[6]]).repeat(4,axis=0)
    l0 = np.array([cnrs[0],cnrs[0],cnrs[0],cnrs[1],cnrs[1],cnrs[2],cnrs[2],cnrs[3],cnrs[4],cnrs[4],cnrs[5],cnrs[6]]).repeat(4,axis=0)
    p0 = np.array([[x,y,0],[x,y,0],[x+patch_size,y+patch_size,0],[x+patch_size,y+patch_size,0]]).T.repeat(12,axis=0).reshape(3,-1).T
    n = np.array([[1,0,0],[0,1,0],[1,0,0],[0,1,0]]).T.repeat(12,axis=0).reshape(3,-1).T
    d = np.zeros([48])    
    for i in range(48):
        d[i] = np.dot(p0[i]-l0[i],n[i])/np.dot(l[i],n[i])
    pts = np.vstack([d.repeat(3).reshape(-1,3)*l+l0,cnrs]) # calculate points and add vertices
    within = np.logical_and.reduce([pts[:,0]>=x,pts[:,1]>=y,pts[:,0]<=(x+patch_size),pts[:,1]<=(y+patch_size)], dtype=bool)
    pts = np.compress(within,pts,axis=0)
    patch_cnrs = np.array(np.meshgrid([x,x+patch_size],[y,y+patch_size])).T.reshape(4,2)
    pts_xy = np.vstack([pts[:,[0,1]],patch_cnrs])

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
    pts_z = np.compress(zbounds[:,0]<=zbounds[:,1],zbounds,axis=0).ravel()
    if pts_z.size != 0:            
        return np.amin(pts_z), np.amax(pts_z)
    else:
        return None, None

# Determine projection for patch
def proj_patch(coord, patch_size, m, m_inv, CF_xyz, dest_cnrs) -> np.ndarray:
    z_lb, z_ub = patch_zbounds(coord,patch_size,m,m_inv,CF_xyz.shape, dest_cnrs)
    if z_lb is None:
        return np.zeros([patch_size,patch_size],dtype='float64')
    elif z_lb < 0:
        dest_zoffset = int(abs(z_lb)+1)
        dest_zmax = dest_zoffset + int(z_ub-z_lb+1)
    else:
        dest_zoffset = -1 * int(z_lb)
        dest_zmax = int(z_ub-z_lb+1)
    zoffset_inv = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,-1*dest_zoffset],[0,0,0,1]], dtype='float64')
    coord_shift_inv = np.array([[1,0,0,coord[0]],[0,1,0,coord[1]],[0,0,1,0],[0,0,0,1]], dtype='float64')
    complete_inv = np.matmul(np.matmul(m_inv,zoffset_inv),coord_shift_inv)
    patch = np.amax(ndimage.affine_transform(CF_xyz,complete_inv,output_shape=(patch_size,patch_size,dest_zmax),order=1),2)
    return patch

# Initialiser for worker during multiprocessing
def limit_cpu():
    p = psutil.Process(os.getpid())
    if platform.system()=='Windows':
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    else:
        p.nice(19)

# Find projection in patches, multiprocessing, single-processor routine available for debugging
# affine_transform performs spline filtering when order greater than 1, memory heavy

def fluorescence_proj_mp(param,CF,repos_tx=0,repos_ty=0,repos_s=1) -> np.ndarray:

    # 3DCT numbers
    nX = param.nX
    nY = param.nY
    phi = param.phi
    psi = param.psi
    theta = param.theta
    s =  param.s
    tx = param.tx
    ty = param.ty
    tz = param.tz
    phi = phi/180*np.pi
    psi = psi/180*np.pi
    theta = theta/180*np.pi

    # rearrange axes for affine transform
    CF_xyz = np.moveaxis(np.moveaxis(CF,0,2),0,1)

    # calculate transform matrices
    corrmat, corrmat_inv = corr_transform(s,tx,ty,tz,phi,psi,theta,repos_tx,repos_ty,repos_s)

    # calculate volume corners after transformation
    src_cnrs = np.vstack([np.array(np.meshgrid([0,CF_xyz.shape[2]], [0,CF_xyz.shape[1]], [0,CF_xyz.shape[0]])).reshape(3,-1), np.ones(8)])
    dest_cnrs = np.matmul(corrmat,src_cnrs)[0:3].T

     # cpu time and memory scales linearly at least up to 512, ~0.5 GB for 256
    ncpu = cpu_count()
    mem = psutil.virtual_memory()
    if mem.available > 2 * 1024 * 1024 * 1024 * ncpu:
        patch_size = 512
        # print('patch size: 512')
    else:
        patch_size = 256
        # print('patch size: 256')

    pixel_coords = np.array(np.mgrid[0:nX:patch_size,0:nY:patch_size]).T.reshape(-1,2)

    # find projection in patches, single process
    # CFproj = np.zeros([nX,nY])
    # for coord in pixel_coords:
    #     patch = proj_patch(coord,patch_size,corrmat,corrmat_inv,CF_xyz,dest_cnrs)
    #     CFproj[coord[0]:coord[0]+patch_size,coord[1]:coord[1]+patch_size] = patch
    # CFproj = np.transpose(np.ndarray.astype((CFproj-np.amin(CFproj))/(np.amax(CFproj)-np.amin(CFproj))*255,'uint8'))

    # find projection in patches, multiple cpus, no option to cancel
    # pool = Pool(ncpu,limit_cpu)
    # patches = pool.starmap(proj_patch, [(coord,patch_size,corrmat,corrmat_inv,CF_xyz,dest_cnrs) for coord in pixel_coords])
    # CFproj = np.transpose(np.hstack(np.vsplit(np.vstack(patches),int(nY/patch_size))))
    # CFproj = np.ndarray.astype((CFproj-np.amin(CFproj))/(np.amax(CFproj)-np.amin(CFproj))*255,'uint8')

    # find projection in patches, multiple cpus, option to cancel through dialog
    progressDialog = QtWidgets.QDialog()
    verticalLayout = QtWidgets.QVBoxLayout(progressDialog)
    label = QtWidgets.QLabel("Computing projection...",progressDialog)
    verticalLayout.addWidget(label)
    buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel,progressDialog)
    buttonBox.rejected.connect(progressDialog.reject)
    verticalLayout.addWidget(buttonBox)
    def dialogAccept(result):
        progressDialog.accept()
    pool = Pool(ncpu,limit_cpu)
    res = pool.starmap_async(proj_patch, [(coord,patch_size,corrmat,corrmat_inv,CF_xyz,dest_cnrs) for coord in pixel_coords], callback=dialogAccept)
    if progressDialog.exec() == QtWidgets.QDialog.Rejected:
        pool.close()
        pool.terminate()
        print("Action cancelled")
        return None
    patches = res.get()
    CFproj = np.transpose(np.hstack(np.vsplit(np.vstack(patches),int(nY/patch_size))))
    CFproj = np.ndarray.astype((CFproj-np.amin(CFproj))/(np.amax(CFproj)-np.amin(CFproj))*255,'uint8')


    return CFproj
