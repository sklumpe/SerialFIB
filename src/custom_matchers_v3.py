'''
updated 09 Aug 2020
class CustomMatcher, matcher based on phase correlation or cv2.matchTemplate() metrics
  option to split template into overlapping tiles for cv2.matchTemplate(), off by default
  new instance created with
    favourite_matcher = CustomMatcher('phase')
    favourite_matcher = CustomMatcher(cv2.TM_CCOEFF_NORMED)
    favourite_matcher = CustomMatcher(cv2.TM_CCOEFF_NORMED,tiling=True)
phase_correlate() finds template in image by phase correation with skimage (preferred) or cv2 implementation
padded_cv_matchTemplate() finds template/reference in padded image (current view) using given cv2 metric
padded_tiled_cv_matchTemplate() does the same but splits template into tiles with given overlap
for usage of functions, scroll to end of file
'''

import numpy as np
import cv2

try:
    from skimage.feature import register_translation
except ModuleNotFoundError:
    pass


# Import statements necessary for class CustomCVMatcher
# from custom_matchers import padded_cv_matchTemplate, padded_tiled_cv_matchTemplate
from autoscript_sdb_microscope_client.structures import *
from autoscript_toolkit.template_matchers import TemplateMatcher

# Find template in image by phase correlation, skimage implementation
#  cv2 implementation executed if skimage not available
def phase_correlate(image_8bit, template_8bit, upsample_factor=25):

    # Determine image sizes
    image_height, image_width = image_8bit.shape
    template_height, template_width = template_8bit.shape
    target_height = max(image_height,template_height)
    target_width = max(image_width,template_width)

    # Pad to largest dimensions
    image_8bit_pad = np.zeros([target_height,target_width],dtype=np.uint8)
    image_8bit_pad[0:image_height,0:image_width] = image_8bit
    template_8bit_pad = np.zeros([target_height,target_width],dtype=np.uint8)
    template_8bit_pad[0:template_height,0:template_width] = template_8bit

    try:
        # Phase correlation with upsampled matrix-multiplication DFT
        shift, error, diffphase = register_translation(template_8bit_pad, image_8bit_pad, upsample_factor)
        match_center_x = template_width / 2 - shift[1]
        match_center_y = template_height / 2 - shift[0]
        transform = np.float32([ [1,0,shift[1]], [0,1,shift[0]] ])
    except NameError:
        # Phase correlation with Hanning window function and 5x5-weighted centroid around peak
        retval, response = cv2.phaseCorrelate(np.float32(template_8bit_pad), np.float32(image_8bit_pad))
        match_center_x = template_width / 2 + retval[0]
        match_center_y = template_height / 2 + retval[1]
        transform = np.float32([ [1,0,-retval[0]], [0,1,-retval[1]] ])
    image_8bit_pad_shifted = cv2.warpAffine(image_8bit_pad, transform, (target_width,target_height) )
    match_score = float(cv2.matchTemplate(template_8bit_pad, image_8bit_pad_shifted, cv2.TM_CCOEFF_NORMED)[0][0])

    return match_center_x, match_center_y, match_score

# Find template in padded image by cross-correlation 
def padded_cv_matchTemplate(image_8bit,template_8bit,comparison_method):

    image_height, image_width = image_8bit.shape
    template_height, template_width = template_8bit.shape
    pad_height = int(template_height / 2)
    pad_width = int(template_width / 2)

    # Pad image
    image_8bit_pad = cv2.copyMakeBorder(image_8bit, pad_height, pad_height, pad_width, pad_width, cv2.BORDER_CONSTANT, value=np.mean(image_8bit)-np.std(image_8bit))

    # Perform template matching
    res = cv2.matchTemplate(image_8bit_pad, template_8bit, comparison_method)
    min_value, max_value, min_location, max_location = cv2.minMaxLoc(res)

    # Take minimum when one of SQDIFF* methods is used, maximum otherwise
    if comparison_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        match_center_x = min_location[0] - pad_width + template_width / 2
        match_center_y = min_location[1] - pad_height + template_height / 2
        match_score = min_value
    else:
        match_center_x = max_location[0] - pad_width + template_width / 2
        match_center_y = max_location[1] - pad_height + template_height / 2
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
                centers_x[len(tile_bounds_x)*i+j] = min_location[0] - pad_width - x[0] + template_width/2
                centers_y[len(tile_bounds_x)*i+j] = min_location[1] - pad_height - y[0] + template_height/2
                scores[len(tile_bounds_x)*i+j] = min_value
            else:
                centers_x[len(tile_bounds_x)*i+j] = max_location[0] - pad_width - x[0] + template_width/2
                centers_y[len(tile_bounds_x)*i+j] = max_location[1] - pad_height - y[0] + template_height/2
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

        # Rescale if pixel size available
        try:
            scale_factor = template.metadata.binary_result.pixel_size.x / image.metadata.binary_result.pixel_size.x
            if scale_factor != 1:
                template_8bit = cv2.resize(template_8bit,None,fx=scale_factor, fy=scale_factor, interpolation = cv2.INTER_LINEAR)
        except AttributeError:
            pass

        if self.comparison_method == 'phase':
            match_center_x, match_center_y, match_score = phase_correlate(image_8bit,template_8bit)
        elif self.comparison_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF,cv2.TM_CCOEFF_NORMED]:
            if self.tiling:
                match_center_x, match_center_y, match_score = padded_tiled_cv_matchTemplate(image_8bit,template_8bit,self.comparison_method,tile_overlap=0.5,tile_scale=2)
            else:
                match_center_x, match_center_y, match_score = padded_cv_matchTemplate(image_8bit,template_8bit,self.comparison_method)

        match_center = Point(match_center_x, match_center_y)

        # Create ImageMatch object
        match = ImageMatch(center=match_center, score=match_score)

        return match

    # Extract normalized, 8-bit image from AdornedImage instance
    def normalized_uint8(self, image: AdornedImage) -> np.ndarray:

        # Detect bit depth and convert to grayscale
        if isinstance(image, AdornedImage):
            if image.bit_depth == 8 or image.bit_depth == 16:
                gray = image.data
            elif image.bit_depth == 24:
                gray = cv2.cvtColor(image.data, cv2.COLOR_BGR2GRAY)
            else:
                raise ValueError("Unsupproted bit depth of %d." % (image.bit_depth))
        elif isinstance(image, np.ndarray):
            if image.dtype == 'uint8' and image.ndim == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            elif image.dtype == 'uint8' or image.dtype == 'uint16':
                gray = image

        # Remove Aquilos Databar
        if gray.shape[0] == 2188:
            gray = gray[:-140,:]
        elif gray.shape[0] == 1094:
              gray = gray[:-70,:]

        lower_bound = np.min(gray)
        upper_bound = np.max(gray)
        lut = np.concatenate([
            np.zeros(lower_bound, dtype=np.uint16),
            np.linspace(0, 255, upper_bound - lower_bound).astype(np.uint16),
            np.ones(2 ** 16 - upper_bound, dtype=np.uint16) * 255
        ])

        return lut[gray].astype(np.uint8)

if __name__ == "__main__":

    image = AdornedImage.load('/Users/kf656/Desktop/Scripts/correlativeFIB/automation/GUI/2019-12-12_13_33_30_0_1.03e-11_first_move_0.tif')
    template = AdornedImage.load('/Users/kf656/Desktop/Scripts/correlativeFIB/automation/GUI/2019-12-12_13_28_59_0_1.03e-11_first_move_2.tif')
    favourite_matcher = CustomCVMatcher('phase')
    match = favourite_matcher.match(image,template)
    print(match.center, match.score)
    
    # scale_factor = template.metadata.binary_result.pixel_size.x / image.metadata.binary_result.pixel_size.x
    # image = favourite_matcher.normalized_uint8(image)
    # template = favourite_matcher.normalized_uint8(template)
    # template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor, interpolation = cv2.INTER_LINEAR)
    # print('Correlating with whole image')
    # match_center_x, match_center_y, match_score = padded_cv_matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)
    # print(match_center_x, match_center_y, match_score)
    # print('Correlating in tiles')
    # match_center_x, match_center_y, match_score = padded_tiled_cv_matchTemplate(image,template,cv2.TM_CCOEFF_NORMED,tile_overlap=0.5,tile_scale=2)
    # print(match_center_x, match_center_y, match_score)
    # print('Correlating by phase correlation')
    # match_center_x, match_center_y, match_score = phase_correlate(image,template)
    # print(match_center_x, match_center_y, match_score)


