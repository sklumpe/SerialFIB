"""
A tiff file handler to read and write pixel size information.

Luyang Han
2020.05.13 First version
2020.05.19 read tiff info
"""

from PIL import Image
from io import BytesIO
import numpy as np

PIXEL_TAG_KEY = 36000
ZEISS_TAG_KEY = 34118

def write_tiff(fname, data, pixel_size):
    """function to write tiff data and include pixel_size in tiff tag"""
    with BytesIO() as f:
        im_data = Image.fromarray(data)
        im_data.save(f, format='TIFF')
        f.seek(0)
        im_back = Image.open(f)
        im_back.tag[PIXEL_TAG_KEY] = str(pixel_size)
        im_back.save(fname, format="TIFF", tiffinfo=im_back.tag)

def read_tiff(fname):
    """function to read tiff with additional pixel size info in meter.
    This function will understand the Zeiss TIFF pixel size as well as
    special pixel size defined here.

    Return value
    --------
    a tuple of image array and pixel size in meter. If no pixel size info
    can be found, it will return None.
    """
    with Image.open(fname) as img_data:
        img_array = np.array(img_data)
        if ZEISS_TAG_KEY in img_data.tag.keys():
            #zeiss tiff
            #print('hello')
            pixel_size = float(img_data.tag.tagdata[ZEISS_TAG_KEY][0:30].decode().split("\r\n")[3])
        elif PIXEL_TAG_KEY in img_data.tag.keys():
            #own tiff
            pixel_size = float(img_data.tag.tagdata[PIXEL_TAG_KEY].decode()[:-1])
        else:
            pixel_size = None
        return img_array, pixel_size

def get_tiff_info(fname):
    """
    Function to get the tiff parameter info as dict. 
    The dict keys are the true name of the parameter.
    The values are all returned as string, including units.
    """
    COUNT_LINE = 34
    START_LINE = 35
    with Image.open(fname) as img_data:
        try:
            data_list = img_data.tag.tagdata[ZEISS_TAG_KEY].decode("latin1").split("\r\n")
            total_count = int(data_list[COUNT_LINE])
            ext_dict = {}
            for i in range(total_count):
                key = data_list[START_LINE+i*2]
                value = data_list[START_LINE+i*2+1].split("=")[-1].strip()
                ext_dict[key] = value
            return ext_dict
        except:
            return None
