

from src.TESCAN.TescanDriver import fibsem


fibsem=fibsem()

stagepos1={'label': '0', 'x': 0.263643, 'y': 9.802727, 'z': 28.812355, 't': 0.0, 'r': -60.0, 'patterns': '', 'image': ''}


#fibsem.session.FIB.Beam.Status.
#import matplotlib.pyplot as plt 



fibsem.tescanScope.FIB.Optics.SetImageShift(0,0)
#img1=fibsem.take_image_IB()
fibsem.tescanScope.FIB.Optics.SetImageShift(1e-03,0)
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

fibsem.define_output_dir(r'D:/sklumpe/')
image=fibsem.take_image_IB()
fibsem.align(image,'ION')
#imageWidth = 512
#imageHeight = 512
# for simultaneous acquisition from multiple channels, we use this way of acquisition
#channel=0
#channel1=2
#channel2=

#images = fibsem.tescanScope.FIB.Scan.AcquireImagesFromChannels((channel,channel1), imageWidth, imageHeight, 320)
#print(images[0])
#fibsem.align(image,'ION')
#dictionary=)_

#layerSettings = automation.DrawBeam.LayerSettings.IEtching()
#fibsem.tescanScope.DrawBeam.LoadLayer('test_xml.xml')
#fibsem.tescanScope.DrawBeam.Start()
#fibsem.tescanScope.DrawBeam.GetStatus()
#fibsem.tescanScope.DrawBeam.UnloadLayer()

#[14:09] Martina Zánová
#image.Header['Common']['PixelsizeX']
#Header manipulat
#image.Header.write(sys.stdout)  # you can print header to output for debugging
#print('Detector {} was used\n\n'.format(image.Header['SEM']['Detector']))

