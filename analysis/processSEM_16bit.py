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

import numpy as np
import pywt as pywt
import skimage as ski
import cv2 as cv2
import os
import skimage.morphology
import skimage.filters
import argparse

parser = argparse.ArgumentParser(description='Analysis for raw images from SAV data.')
parser.add_argument('-indir', metavar='--input_directory', type=str, nargs='+',
                    help='Input Directory with Raw Images',required=True)
parser.add_argument('-outdir', metavar='--output_directory', type=str, nargs='+',
                    help='Output Directory',required=True)
parser.add_argument('-l', metavar='--level', type=int, default=['8'], nargs='+',
                    help='Level of wavelet decomposition. Default is 8.',required=False)
parser.add_argument('-s', metavar='--sigma', type=int, default=['6'], nargs='+',
                    help='Sigma of gaussian for stripe dampening in wavelet decomposition. Default is 6.',required=False)                    
parser.add_argument('-wname', metavar='--wavelet_name', type=str, default=['coif3'], nargs='+',
                    help='Wavelet for decomposition. Default is coif3.',required=False)
parser.add_argument('-sb', metavar='--sigma_blur', type=int, default=['35'], nargs='+',
                    help='Sigma for blurred image to compensate charging. Default 35.',required=False)   
parser.add_argument('-offset', metavar='--offset_blur', type=int, default=['100'], nargs='+',
                    help='Offset for blurred image mask. Default 100.',required=False)
parser.add_argument('-iter', metavar='--iterations_erosion', type=int, default=['3'], nargs='+',
                    help='Number of iterations of image erosion for charge compensation. Default 3.',required=False)
                      


args = parser.parse_args()
#print(args.indir)

def removeStripesVertical(image,level,wname,sigma):
    coeffs2=pywt.wavedec2(image,wname,level=level)
    new_coeffs=[coeffs2[0]]
    for i in range(1,len(coeffs2)):
        Ch,Cv,Cd = coeffs2[i]
        fCv=np.fft.fft(Cv,axis=0)
        fCv2=np.fft.fftshift(fCv,axes=[0])
        [my,mx]=np.shape(fCv2)
        gauss1d = 1 - np.exp(-np.arange(-my // 2, my // 2)**2 / (2 * sigma**2))
        fCv3 = fCv2 * gauss1d[:, np.newaxis]
        Cv2=np.fft.ifftshift(fCv3, axes=[0])
        Cv3=np.fft.ifft(Cv2, axis=0)
        new_coeffs.append((Ch,Cv3.real,Cd))
    image2=pywt.waverec2(new_coeffs,wname)
    return(image2)
    
    

input_dir=args.indir[0]
output_dir=args.outdir[0]
level=int(args.l[0])
sigma=float(args.s[0])
wname=str(args.wname[0])
offset=float(args.offset[0])
sigma_blur=int(args.sb[0])
iter_erosions=int(args.iter[0])

try:
    os.mkdir(output_dir)
except:
    print("Directory already exists.")
for i in sorted(os.listdir(input_dir)):
    print(i)
    image=cv2.imread(input_dir+'/'+str(i),cv2.IMREAD_ANYDEPTH)
    #grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rimage=removeStripesVertical(image,level,wname,sigma)
    rimage_trim=rimage
    gaussian_blurred=ski.filters.gaussian(rimage_trim,sigma_blur)

    dilated2=gaussian_blurred-offset*255

    erosions=[]
    erosions.append(dilated2)
    for j in range(1,iter_erosions):
        dilated3=ski.morphology.erosion(erosions[-1])
        erosions.append(dilated3)


    image2=rimage_trim-erosions[-1].astype(float)

    print(output_dir+'/out_'+str(i))
    cv2.imwrite(output_dir+'/out_'+str(i), image2.astype(np.uint16))
