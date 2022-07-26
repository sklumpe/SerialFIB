from src.Zeiss.crossbeam_client import Point



class FeatureLocation:
    def __init__(self):
        self.confidence=None
        self.center_in_pixels=None
        self.shift_in_meters=None
        self.shift_in_pixels=None

    
def locate_feature(image,feature_template,template_matcher,original_feature_center=None):
    image_pixel_size=image.metadata.binary_result.pixel_size
    match=template_matcher.match(image,feature_template)
    shape=image.data.shape
    #print('I made it to the locate feature')
    feature_location=FeatureLocation()
    feature_location.confidence=match.score
    
    
    new_center=Point(match.center.x-(shape[1]/2),match.center.y-(shape[0]/2))
    print(new_center)
    match.center=new_center
    feature_location.center_in_pixels=match.center


    ### Feature Location in Meters adjustment with image pixel size
    #print(match.center.x)
    feature_location.center_in_meters=Point(match.center.x*image_pixel_size.x,match.center.y*image_pixel_size.x)
    return(feature_location)
    