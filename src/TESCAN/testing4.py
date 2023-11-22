from src.TESCAN.TescanDriver import fibsem
from tescanautomation import Automation

fibsem=fibsem()

stagepos1={'label': '0', 'x': 0.263643, 'y': 9.802727, 'z': 28.812355, 't': 0.0, 'r': -60.0, 'patterns': '', 'image': ''}


fibsem.tescanScope.FIB.Optics.SetImageShift(0,0)
img1=fibsem.take_image_IB()
fibsem.tescanScope.FIB.Optics.SetImageShift(1e-03,0)
#img2=fibsem.take_image_IB()
fibsem.align(img1,'ION')

fibsem.align_current(1e-09,'ION',)

#fibsem.create_pattern(0,0,1e-06,1e-06)

#fibsem.session.FIB.Beam.Status.
#import matplotlib.pyplot as plt 



#fibsem.tescanScope.FIB.Optics.SetImageShift(0,0)
#img1=fibsem.take_image_IB()
#fibsem.tescanScope.FIB.Optics.SetImageShift(1e-03,0)
#img2=fibsem.take_image_IB()

#print(img1.data)

#print(img2.metadata.optics.scan_field_of_view.width)
#plt.imshow(img1.data)

#detectors = fibsem.tescanScope.FIB.Detector.Enum()
#SE=detectors[2]
#fibsem.tescanScope.FIB.Detector.AutoSignal(SE)
#plt.imshow(img2.data)


#print(fibsem.tescanScope.FIB.Centering.Enum())

#print(fibsem.tescanScope.FIB.Preset.Enum())

#table=fibsem.tescanScope.FIB.Preset.Enum()

#from src.TESCAN.tescan_client_utils import get_closest_preset

#preset=get_closest_preset(30,50e-12,table)

#fibsem.tescanScope.FIB.Preset.Activate(preset)


#print(fibsem.tescanScope.FIB.Optics.GetImageShift())

#fibsem.define_output_dir(r'D:/sklumpe/')
#image=fibsem.take_image_IB()
#fibsem.align(image,'ION')