from crossbeam_client import *
import matplotlib.pyplot as plt
import cv2
microscope = MicroscopeClient()
microscope.connect()
# microscope.specimen.stage.absolute_move((65e-3, 65e-3))
# microscope.specimen.stage.relative_move((-2e-3, -10e-3))
# # microscope.beams.electron_beam.beam_shift.value = Point(1,1)
# # microscope.beams.electron_beam.beam_shift.value += Point(1,1)
# microscope.beams.electron_beam.turn_on()
# microscope.beams.electron_beam.beam_current.value = 1e-9

# microscope.beams.electron_beam.beam_shift.value = Point(20,20)
# time.sleep(3)
# microscope.beams.electron_beam.beam_shift.value += Point(2,7)


# microscope.beams.ion_beam.turn_on()
# microscope.beams.ion_beam.beam_current.value = 1e-9

# microscope.beams.ion_beam.beam_shift.value = Point(20,20)
# time.sleep(3)
# microscope.beams.ion_beam.beam_shift.value += Point(2,7)


#stagepos=microscope.specimen.stage.current_position

#microscope.specimen.stage.absolute_move((65e-3, 65e-3,0.5e-3,0,0.1e-3))
# microscope.specimen.stage.relative_move((0.9e-3, 0.9e-3,0.1e-3,1,0.2e-3))

# microscope.disconnect()
# #print(stagepos)








### Grab Image ###
settings=GrabFrameSettings(dwell_time=10e-08,resolution='1024x768',line_integration=1)
microscope.imaging.grab_frame(settings)

microscope.disconnect()

img=cv2.imread(r'c:/Users/Sven/Pictures/test3.tif')
print(img.shape)

plt.imshow(img)
plt.show()

