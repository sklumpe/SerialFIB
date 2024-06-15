
from tescanautomation import Automation
import time
# for easier usage
from tescanautomation.Common import Bpp

microscope_ip = 'localhost'
session = Automation(microscope_ip)  # default port 8300

if session.FIB.Beam.GetStatus() == Automation.FIB.Beam.Status.BeamOff:
    session.FIB.Beam.On()

# stop previous scanning (if any) - safe operation
session.FIB.Scan.Stop()

# Enumerate detectors present in the system
detectors = session.FIB.Detector.Enum()
for detector in detectors:
    print(detector.index, " ", detector.name)
print("")

# map detectors, set channels and enable them. We will set FIB to scan from detectors 0 and 1.
detector1 = detectors[0]
detector2 = detectors[1]
channel1 = 0
channel2 = 2
session.FIB.Detector.Set(channel1, detector1, Bpp.Grayscale_8_bit)
session.FIB.Detector.Set(channel2, detector2, Bpp.Grayscale_8_bit)
# check what is really selected
print("Channel ", channel1, ":", session.FIB.Detector.Get(channel1))
print("Channel ", channel2, ":", session.FIB.Detector.Get(channel2))
print("")

# find gain and black for first detector
print('Original Brightness, Contrast: ', session.FIB.Detector.GetGainBlack(detector1.index), '%')
# Performing Automatic brightness and contrast - the AutoSignal function
# adjust brightness and contrast, read back the result
print("Performing AutoSignal", end='')
session.FIB.Detector.StartAutoSignal(channel1)
while session.FIB.IsBusy():
    print('.', end='')
    time.sleep(0.1)
print('')
print('Brightness, Contrast: ', session.FIB.Detector.GetGainBlack(detector1.index), '%')
# set gain and black for second detector
session.FIB.Detector.SetGainBlack(detector2.index, 40.0, 50.0)


# Start scanning and store images to folder GeneratedFiles.
imageWidth = 512
imageHeight = 512
# for simultaneous acquisition from multiple channels, we use this way of acquisition
images = session.FIB.Scan.AcquireImagesFromChannels((channel1, channel2), imageWidth, imageHeight, 320)
#session.FIB.Scan.AcquireImagews
#if not os.path.isdir('GeneratedFiles'):
#    os.makedirs('GeneratedFiles')
#images[0].save('./fib_combi_1.png')
#images[1].save('GeneratedFiles/fib_combi_2.png')
print(images[0].Image)
import numpy as np

array=np.array(images[0].Image)
print(array)
print("images saved")

# disconnect is made automatically
session.Disconnect()