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

updated 30 Mar 2020

class CustomCVMatcher, matcher for cv2-based template matching with tiling option, new instance created with

    favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED,tiling=False)

padded_cv_matchTemplate() finds template/reference in padded image (current view) using given cv2 metric

padded_tiled_cv_matchTemplate() does the same but splits template into tiles with given overlap

for usage of functions, scroll to end of file

'''



import numpy as np

import cv2

class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init
        

    def __iadd__(self, second):
        self.shift(second.x, second.y)
        return self

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    def shift(self, x, y):
        self.x += x
        self.y += y


# Import statements necessary for class CustomCVMatcher

# from custom_matchers import padded_cv_matchTemplate, padded_tiled_cv_matchTemplate

#from autoscript_sdb_microscope_client.structures import *
#from src.Zeiss.CrossbeamDriver import DummyAdorned as AdornedImage
class Match():
    def __init__(self,match,score):
        self.score=score
        self.center=match
class binary_result():
    def __init__(self):
        self.pixel_size=(0.09615e-06,0.09615e-06)

class scan_field_of_view():
    def __init__(self):
        self.width=100e-06
class optics():
    def __init__(self):
        SFOV=scan_field_of_view()
        self.scan_field_of_view=SFOV
class metadata():
    def __init__(self):
        binary=binary_result()
        self.binary_result=binary
        opt=optics()
        self.optics=opt

class AdornedImage():
    def __init__(self):
        self.data=[]
        meta=metadata()
        self.metadata=meta
        self.bit_depth=8
        self.height=768
        #self.metadata.binary_result.pixel_size=1e-06
    def save(self,filepath):
        print("An Image should have been saved, to be implemented!!")

#from autoscript_toolkit.template_matchers import TemplateMatcher
import abc
class TemplateMatcher(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def match(self, image: AdornedImage, template: AdornedImage):
        raise Exception("Matching method is not implemented.")


# Find template in padded image by cross-correlation 

def padded_cv_matchTemplate(image_8bit,template_8bit,comparison_method):


    try:
        if image_8bit.shape[2]==3:
            image_8bit=image_8bit[:,:,2]
    
        if template_8bit.shape[2]==3:
            template_8bit=template_8bit[:,:,2]
    except IndexError:
        pass
    #print(image_8bit.shape)
    image_height, image_width = image_8bit.shape

    template_height, template_width = template_8bit.shape

    pad_height = int(template_height / 2)

    pad_width = int(template_width / 2)



    # Pad image

    image_8bit_pad = cv2.copyMakeBorder(image_8bit, pad_height, pad_height, pad_width, pad_width, cv2.BORDER_CONSTANT, value=np.mean(image_8bit)-np.std(image_8bit))

    print(image_8bit_pad)
    print(template_8bit)
    print(comparison_method)

    # Perform template matching

    res = cv2.matchTemplate(image_8bit_pad, template_8bit, comparison_method)

    min_value, max_value, min_location, max_location = cv2.minMaxLoc(res)



    # Take minimum when one of SQDIFF* methods is used, maximum otherwise

    if comparison_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:

        match_center_x = min_location[0] - pad_width + image_width / 2

        match_center_y = min_location[1] - pad_height + image_height / 2

        match_score = min_value

    else:

        match_center_x = max_location[0] - pad_width + image_width / 2

        match_center_y = max_location[1] - pad_height + image_height / 2

        match_score = max_value



    return match_center_x, match_center_y, match_score



# Find template in padded image by cross-correlation and splitting template in tiles with given overlap

# tile_overlap, fraction of overlap between tiles

# tile_scale, tile size is template dimensions divided by tile_scale

def padded_tiled_cv_matchTemplate(image_8bit,template_8bit,comparison_method,tile_overlap=0.5,tile_scale=2):



    image_height, image_width = image_8bit.shape

    template_height, template_width = template_8bit.shape



    tile_height = template_height // tile_scale

    tile_width = template_width // tile_scale

    step_y = int(tile_height * (1-tile_overlap))

    step_x = int(tile_width * (1-tile_overlap))



    tile_bounds_y = [np.array([0,tile_height]) + k * step_y for k in range((template_height-tile_height)//step_y+1)]

    if tile_bounds_y[-1][1] + tile_height / 2 < template_height:

        tile_bounds_y.append(np.array([template_height-tile_height,template_height]))



    tile_bounds_x = [np.array([0,tile_width]) + k * step_x for k in range((template_width-tile_width)//step_x+1)]

    if tile_bounds_x[-1][1] + tile_width / 2 < template_width:

        tile_bounds_x.append(np.array([template_width-tile_width,template_width]))

    

    pad_height = int(tile_height // 2)

    pad_width = int(tile_width // 2)



    # Pad image

    image_8bit_pad = cv2.copyMakeBorder(image_8bit, pad_height, pad_height, pad_width, pad_width, cv2.BORDER_CONSTANT, value=np.mean(image_8bit))



    num_tiles = len(tile_bounds_x) * len(tile_bounds_y)

    centers_x = [0.0] * num_tiles

    centers_y = [0.0] * num_tiles

    scores = [0.0] * num_tiles



    for i,y in enumerate(tile_bounds_y):



        for j,x in enumerate(tile_bounds_x):



            tile = template_8bit[y[0]:y[1],x[0]:x[1]]



            # Perform template matching

            res = cv2.matchTemplate(image_8bit_pad, tile, comparison_method)

            min_value, max_value, min_location, max_location = cv2.minMaxLoc(res)



            # Take minimum when one of SQDIFF* methods is used, maximum otherwise

            # Determine centre of (unsplit) template in input image (containing bottom bar)

            if comparison_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:

                centers_x[len(tile_bounds_x)*i+j] = min_location[0] - pad_width - x[0] + image_width/2

                centers_y[len(tile_bounds_x)*i+j] = min_location[1] - pad_height - y[0] + image_height/2

                scores[len(tile_bounds_x)*i+j] = min_value

            else:

                centers_x[len(tile_bounds_x)*i+j] = max_location[0] - pad_width - x[0] + image_width/2

                centers_y[len(tile_bounds_x)*i+j] = max_location[1] - pad_height - y[0] + image_height/2

                scores[len(tile_bounds_x)*i+j] = max_value



    # Report centers

    for k in range(num_tiles):

        print("tile %d: x=%d, y=%d, score=%.3f" % (k+1,centers_x[k],centers_y[k],scores[k]))



    # Reject outliers

    good_centers_x = [ind for ind, element in enumerate(centers_x) if abs(element - np.mean(centers_x)) <= np.std(centers_x)]

    good_centers_y = [ind for ind, element in enumerate(centers_y) if abs(element - np.mean(centers_y)) <= np.std(centers_y)]

    good_ind = np.intersect1d(good_centers_x, good_centers_y)



    # Take (unweighted) mean

    match_center_x = np.mean([centers_x[k] for k in good_ind])

    match_center_y = np.mean([centers_y[k] for k in good_ind])

    match_score = np.mean([scores[k] for k in good_ind])



    return match_center_x, match_center_y, match_score





# Matcher in Autoscript style using custom function

class CustomCVMatcher(TemplateMatcher):



    def __init__(self, comparison_method=cv2.TM_CCOEFF_NORMED, tiling=False):



        self.comparison_method = comparison_method

        self.tiling = tiling



    def match(self, image: AdornedImage, template: AdornedImage):



        # Convert to 8-bit and normalize

        image_8bit = self.normalized_uint8(image)

        template_8bit = self.normalized_uint8(template)

        print(image_8bit.shape)
        #print(template_8bit)

        # Remove Databar if present

        if template.height == 2188:

            template_8bit = template_8bit[:-140,:]

        elif template.height == 1094:

              template_8bit = template_8bit[:-70,:]


        tiling=False
        if tiling:

            match_center_x, match_center_y, match_score = padded_tiled_cv_matchTemplate(image_8bit,template_8bit,self.comparison_method,tile_overlap=0.5,tile_scale=2)

        else:

            match_center_x, match_center_y, match_score = padded_cv_matchTemplate(image_8bit,template_8bit,self.comparison_method)





        match_center = Point(match_center_x, match_center_y)

        print(match_center_x,match_center_y)

        # Create ImageMatch object

        #match = Match(center=match_center, score=match_score)
        match = Match(match_center, match_score)

        print(match_score)

        return match



    # Extract normalized, 8-bit image from AdornedImage instance

    def normalized_uint8(self, image: AdornedImage) -> np.ndarray:



        if image.bit_depth == 8 or image.bit_depth == 16:

            gray = image.data

        elif image.bit_depth == 24:

            gray = cv2.cvtColor(image.data, cv2.COLOR_BGR2GRAY)

        else:

            raise ValueError("Unsupproted bit depth of %d." % (image.bit_depth))



        lower_bound = np.min(gray)

        upper_bound = np.max(gray)

        lut = np.concatenate([

            np.zeros(lower_bound, dtype=np.uint16),

            np.linspace(0, 255, upper_bound - lower_bound).astype(np.uint16),

            np.ones(2 ** 16 - upper_bound, dtype=np.uint16) * 255

        ])



        return lut[gray].astype(np.uint8)





if __name__ == "__main__":



    image = cv2.cvtColor(cv2.imread('/Users/kf656/Desktop/Scripts/correlativeFIB/automation/GUI/2019-12-12_13_04_47_0_1.03e-11_first_move_0_copy.tif'),cv2.COLOR_BGR2GRAY)

    template = cv2.cvtColor(cv2.imread('/Users/kf656/Desktop/Scripts/correlativeFIB/automation/GUI/2019-12-12_13_04_47_0_1.03e-11_first_move_0.tif'),cv2.COLOR_BGR2GRAY)

    match_center_x, match_center_y, match_score = padded_cv_matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)

    print('Correlating with whole image')

    print(match_center_x, match_center_y, match_score)

    print('Correlating in tiles')

    match_center_x, match_center_y, match_score = padded_tiled_cv_matchTemplate(image,template,cv2.TM_CCOEFF_NORMED,tile_overlap=0.5,tile_scale=2)

    print(match_center_x, match_center_y, match_score)

