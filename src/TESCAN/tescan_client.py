import sys
import time
import shutil

#sys.coinit_flags = 0  # type: ignore
#import pythoncom  # isort:skip  # noqa: E402, F401


# ###
# import sys
# import warnings
# warnings.simplefilter("ignore", UserWarning)
# sys.coinit_flags = 2
# #import pywinauto
# ###

from time import sleep
from typing import List, Pattern, Tuple

import numpy as np
#from SEM_API import SEM_API

import math

#global probe_table_path

#image_output=r'C:/Users/Sven/Pictures/test.tif'



SI_METERS = [   (1/1000000000000,"fm"),
                (1/1000000000,"pm"),
                (1/1000000000,   "nm"),
                (1/1000000,      "µm"),
                (1/1000,         "mm"),
                (1/100,          "cm"),
                (1,          "m")]


SI_VOLTS = [   (1/1000000000000,"fV"),
                (1/1000000000,"pV"),
                (1/1000000000,   "nV"),
                (1/1000000,      "µV"),
                (1/1000,         "mV"),
                (1/100,          "cV"),
                (1,          "V"),
               (1000,          "kV")]

SI_AMPERES = [   (1/1000000000000,"fA"),
                (1e-12,"pA"),
                (1e-09,   "nA"),
                (1e-06,      "µA"),
                (1e-03,         "mA"),
                (1e-02,          "cA"),
                (1,          "A"),
                (1e03,          "kA")]

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


class DwellTime():
    def __init__(self) -> None:
        self._value = 100e-9

    @property
    def value(self) -> float:
        """Get the current dwelltime value"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value


# TODO:
class Resolution():
    def __init__(self) -> None:
        self._value = "1024 * 768"

    @property
    def value(self) -> str:
        """Get the current resolution"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value


# TODO:
class Rotation():
    def __init__(self) -> None:
        self._value = 0.0

    @property
    def value(self) -> float:
        """Get the set scan rotation angle"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value


# TODO:
class Scanning():
    def __init__(self) -> None:
        self._dwell_time = DwellTime()
        self._resolution = Resolution()
        self._rotation = Rotation()

    @property
    def dwell_time(self) -> DwellTime:
        """Get the current DwellTime"""
        return self._dwell_time

    @property
    def resolution(self) -> Resolution:
        """Get the current scan resolution"""
        return self._resolution

    @property
    def rotation(self) -> Rotation:
        """Get the current scan rotation"""
        return self._rotation


# TODO:
class BeamShift():
    def __init__(self, sem) -> None:
        self._value = Point(0, 0)
        self._sem = sem

    @property
    def value(self) -> Point:
        """Get the current beam shift angle"""
        return self._value

    @value.setter
    def value(self, value: Point,beam='ION') -> None:
        

        if beam=='ION':
            if self._sem is not None:
                #self._sem.SetValue("AP_FIB_BEAM_SHIFT_X", value.x)
                #self._sem.SetValue("AP_FIB_BEAM_SHIFT_Y", value.y)
                print(f"Setting beamshift x to {value.x} and y to {value.y}")

        else:
            if self._sem is not None:
                #self._sem.SetValue("AP_BEAMSHIFT_X", value.x)
                #self._sem.SetValue("AP_BEAMSHIFT_Y", value.y)
                print(f"Setting beamshift x to {value.x} and y to {value.y}")
        self._value = value


# TODO:
class BeamCurrent():
    def __init__(self, sem) -> None:
        self._source = "Ion"
        self._value = 0.0e-9
        self._sem = sem
        #self.probe_table = readProbeTable(probe_table_path)
        #self.probe_table = readProbeTable(r"D:/Images/RoSa/GitHub/SerialFIB/src/Zeiss/ExampleFiles/ProbeTable.xml")
        self.probe_table = r"C:/ProgramData/Carl Zeiss/SmartSEM/Config/ProbeTable.xml"
    @property
    def source(self) -> str:
        """Get the set beam current"""
        return self._source

    @source.setter
    def source(self, source) -> None:
        self._source = "Ion"

    @property
    def value(self) -> float:
        """Get the set beam current"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        """set the available beam current that is closest to the required one"""
        # print(getProbe(value, self.probe_table))
        # probeDict=getProbe(value, self.probe_table)
        # print(probeDict['name'])
        #if self._sem is not None:
            #if self._source == "Ion": 
            #    probeDict=getProbe(value, self.probe_table)
            
                #self._sem.SetState("DP_FIB_IMAGE_PROBE", probeDict['name'])
            #else: self._sem.SetValue("AP_IPROBE", value)
            #TODO distinguish between Gemini 1 and 2
        #self._value = value
        #print(getProbe(self._value, self.probe_table))
        print('Not implemented')
# TODO:
class FieldOfView():
    def __init__(self) -> None:
        self._value = 0

    @property
    def value(self) -> float:
        """Get the set scan rotation angle"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value


# TODO: do not implement
class IonBeam():
    def __init__(self, sem) -> None:
        self._is_blanked = True
        self._horizontal_field_width = FieldOfView()
        self.scanning = Scanning()
        self._beam_shift = BeamShift(sem)
        self._beam_current = BeamCurrent(sem)

        self.scanning.resolution.value = "1024 * 768"
        self.scanning.dwell_time.value = 200e-09
        self._beam_shift.value = Point(0, 0)
        #self._beam_current.value = 500e-9
        self._beam_current.source = "Ion"

        self._sem=sem

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    
    def convert(self, meter_unit, units):
        """meter_units value gviven in string with included units. 
            units: iss the dictionary with unit systemn and strings"""
        useFactor,useName = units[0]
        for factor,name in units:
            if name in meter_unit:
                useFactor = factor
                useName = name
                value = float(meter_unit[:meter_unit.find(name)])
                break
        print(f"Converting {name} multplying {useFactor} and {value}")
        return (value*useFactor,useName)

    def get_current(self):
        print('I was here')
        #current=self._sem.GetState("DP_FIB_PROBE")
        #string=self._sem.GetState("DP_FIB_IMAGE_PROBE")
        current=string.split(':')[1]
        print(current)
        
        #nA=1e-09
        #pA=1e-12
        #print(self.convert(current,SI_AMPERES,'nA'))
        #print(self.convert(current,SI_AMPERES))
        current=self.convert(current,SI_AMPERES)[0]

        print(current)
        #self._sem.GetValue("DP_FIB_MODE")
        return(current)
        #return(current)

    @property
    def beam_shift(self) -> BeamShift:
        """Get the current Beamshift object"""
        return self._beam_shift

    @property
    def beam_current(self) -> BeamCurrent:
        """Get the current beam current object"""
        return self._beam_current

    @property
    def horizontal_field_width(self) -> FieldOfView:
        """Get the current beam current object"""
        return self._horizontal_field_width

    @property
    def is_blanked(self) -> bool:
        """Get the set ebeam blanker status"""
        return self._is_blanked

    @is_blanked.setter
    def is_blanked(self, is_blanked) -> None:
        self._is_blanked = is_blanked



# TODO:
class ElectronBeam():
    def __init__(self, sem) -> None:
        self._is_blanked = True
        self._horizontal_field_width = FieldOfView()
        self._scanning = Scanning()
        self._beam_shift = BeamShift(sem)
        self._beam_current = BeamCurrent(sem)
        self._sem = sem

        self._scanning.resolution.value = "1024 * 768"
        self._scanning.dwell_time.value = 200e-09
        self._beam_shift.value = Point(0, 0)
        #self._beam_current.value = 500e-9

    def turn_on(self):
        #self._sem.Execute("CMD_BEAM_ON")
        pass

    def turn_off(self):
        #self._sem.Execute("CMD_BEAM_OFF")
        pass

    @property
    def beam_current(self) -> BeamCurrent:
        return self._beam_current

    @property
    def beam_shift(self) -> BeamShift:
        """Get the current Beamshift object"""
        return self._beam_shift

    @property
    def scanning(self) -> Scanning:
        """Get the current scanning object"""
        return self._scanning

    @property
    def horizontal_field_width(self) -> FieldOfView:
        """Get the current FieldOfView object"""
        return self._horizontal_field_width

    @property
    def is_blanked(self) -> bool:
        """Get the set ebeam blanker status"""
        return self._is_blanked

    @is_blanked.setter
    def is_blanked(self, is_blanked) -> None:
        self._is_blanked = is_blanked


class Beams():
    def __init__(self, sem) -> None:
        self.sem = sem
        self._beams = "Electon and Ion"
        self._electron_beam = ElectronBeam(sem)
        self._ion_beam = IonBeam(sem)

    def get_available_beams(self):
        return self._beams

    @property
    def electron_beam(self) -> ElectronBeam:
        """Get the current electron_beam object"""
        return self._electron_beam

    @property
    def ion_beam(self) -> IonBeam:
        """Get the current ion_beam object"""
        return self._ion_beam
    
    def change_beam(self,beam='ION') -> None:
        if beam == "ION":
            print('CHANGING TO ION BEAM IN CROSSBEAM')
            self.sem.set_active_beam('ION')
            self.freeze()
        elif beam == "ELECTRON":
            self.sem.set_active_beam('ELECTRON')
            self.freeze()
        return None
    
    def freeze(self,cmd="FREEZE"):
        self.sem.freeze(cmd)


# TODO: do not implement
class Patterning():
    def __init__(self, sem) -> None:
        self._sem = sem
        self._mode = "sequential"  # "parallel"
        self._state = "Idle"  # "Running"

    def stop(self):
        pass

    def start(self):
        pass

    def clear_patterns(self):
        pass

    def set_default_beam_type(self):
        pass

    def set_default_application_file(self, recipe="Si.epm"):
        pass

    def load_pattern(self, fname,testing=False):
        shutil.copyfile(fname, "C:/ProgramData/Carl Zeiss/SmartFIB/API/Drop/ApiLayout.ely")
        #self._sem.Execute("CMD_SMARTFIB_LOAD_ELY")    #r"C:\ProgramData\Carl Zeiss\SmartFIB\API\Drop\ApiLayout.ely"
        time.sleep(1)
        #self._sem.Execute("CMD_SMARTFIB_PREPARE_EXPOSURE")
        time.sleep(1)
        #self._sem.Execute("CMD_FIB_START_MILLING")
        #self._sem.SetState("DP_PATTERNING_MODE","FIB")
        if testing:
            print('This is a test case for patterning as SerialFIB is run via a SmartSEM Simulation')
        else:
            while self._sem.GetState("DP_FIB_MODE") != "Milling":
                time.sleep(0.3) 
            while self._sem.GetState("DP_FIB_MODE") == "Milling":
                time.sleep(0.3) 
    @property
    def is_idle(self):
        print('check idle')
        #if self._sem.GetState("DP_FIB_MODE")=="Milling":
        #    #time.sleep(0.3)
        #    idle=False
        #else:
        #    idle=True
        #    #time.sleep(0.3)
        return idle

    @property
    def mode(self) -> str:
        """Get the patterning mode"""
        return self._mode

    @mode.setter
    def mode(self, mode) -> None:
        self._mode = mode

    @property
    def state(self) -> str:
        """Get the patterning mode"""
        #self._state = self._sem.GetValue("DP_FIB_MODE")
        #return self._state

    @state.setter
    def state(self, state) -> None:
        #success = self._sem.SetValue("DP_FIB_MODE", state)
        #self._state = state
        print("Not Implemented")


class GrabFrameSettings():
    def __init__(self, dwell_time: float, resolution: str, line_integration: str) -> None:
        self._dwell_time = dwell_time
        self._resolution = resolution
        self._line_integration = line_integration


class Imaging():
    def __init__(self, sem) -> None:
        self._sem = sem
        self.image_output=r'C:/api/Grab.tif'

    def set_active_device(self):
        """setting imaging column (FIB mode ... SEM or FIB)"""
        pass

    def get_active_view(self) -> int:
        return 1

    def set_active_view(self, view: int):
        pass

    def grab_frame(self, framesettings: GrabFrameSettings):
        """Grabbing a single full frame image"""
        #image = self._sem.grab_full_image(r"D:/Images/RoSa/Images/test.tif")
        print(framesettings._resolution)
        string1=framesettings._resolution.split('x')
        print(string1)
        resolution=string1[0]+' * '+string1[1]
        print(resolution)
        #self._sem.SetState('DP_IMAGE_STORE',resolution)
        #image = self._sem.grab_full_image(self.image_output)

        #return image

    def grab_multiple_frames(self, framesettings: GrabFrameSettings):
        """Grabbing images of all set channels"""
        images = []
        #images.append(self._sem.grab_full_image(r"D:/Images/RoSa/Images/test.tif"))
        #images.append(self._sem.grab_full_image(self.image_output))
        return images

    def set_contrast(self,value):
        #self._sem.SetValue("AP_CONTRAST", value)
        return
    def set_brightness(self,value):
        #self._sem.SetValue("AP_BRIGHTNESS", value)
        return
    def set_field_width(self,value):
        #self._sem.Execute("CMD_UNFREEZE_ALL")
        #self._sem.SetValue("AP_WIDTH", value)
        #self._sem.Execute("CMD_FREEZE_ALL")
        return

# TODO: 2
class Stage():
    def __init__(self, sem) -> None:
        self._sem = sem
        #self._current_position = self._sem.GetStagePosition()
        self._is_moving = False
        #self._sem.Set_Notify("DP_STAGE_IS")
        #self._sem.Add_Event(self._stage_move_inpect)

    def absolute_move_xy(self, stagepos: Tuple):
        self._is_moving = True
        #self._sem.move_stage_absolute_xy(stagepos[0], stagepos[1])
        print(f"Moving stage x to {stagepos[0]} m and y to {stagepos[1]} m")

        #self._sem.wait_for_stage_idle() # use this when working with PyQt5
        # while self._is_moving: sleep(0.5) is not working at the moment in combination with PyQt5

    def relative_move_xy(self, stagepos: Tuple):
        self._is_moving = True
        #self._sem.move_stage_relative_xy(stagepos[0], stagepos[1])
        print(f"Moving stage by {stagepos[0]} m in x and by {stagepos[1]} m in y direction.")
        
        #self._sem.wait_for_stage_idle() # use this when working with PyQt5
        # while self._is_moving: sleep(0.5) is not working at the moment in combination with PyQt5
    
    def absolute_move(self, stagepos: Tuple):
        self._is_moving = True
        #self._sem.move_stage_absolute(stagepos)
        print(f"Moving stage x to {stagepos[0]} m and y to {stagepos[1]} m")

        #self._sem.wait_for_stage_idle() # use this when working with PyQt5
        # while self._is_moving: sleep(0.5) is not working at the moment in combination with PyQt5

    def relative_move(self, stagepos: Tuple):
        self._is_moving = True
        #self._sem.move_stage_relative(stagepos)
        print(f"Moving stage by {stagepos[0]} m in x and by {stagepos[1]} m in y direction.")
        
        #self._sem.wait_for_stage_idle() # use this when working with PyQt5
        # while self._is_moving: sleep(0.5) is not working at the moment in combination with PyQt5

    def _stage_move_inpect(self, *args):
        if args[0] == "DP_STAGE_IS" and args[3] == 0:
            self._is_moving = False

    @property
    def current_position(self) -> Tuple:
        self._current_position = self._sem.GetStagePosition()
        return self._current_position


# TODO:
class AutoFunctions():
    def __init__(self, sem) -> None:
        self._sem = sem

    def run_auto_cb(self):
        #self._sem.Execute("CMD_QUICK_BC")
        time.sleep(0.5)
        #self._sem.Execute("CMD_QUICK_BC")
        #while self._sem.GetState("DP_AUTO_FUNCTION") != "Idle":
        #    time.sleep(0.5) # use this when working with PyQt5
    def run_auto_focus(self):
        time.sleep(0.5)
        #self._sem.Execute("CMD_AUTO_FOCUS_FINE")
        #while self._sem.GetState("DP_AUTO_FUNCTION") != "Idle": time.sleep(0.5) # use this when working with PyQt5


# TODO: 2
class Specimen():
    def __init__(self, sem) -> None:
        self._sem = sem
        self._stage = Stage(self._sem)

    @property
    def stage(self) -> Stage:
        """Get the current stage object"""
        return self._stage


# TODO: 1
from tescanautomation import Automation
class MicroscopeClient():
    def __init__(self) -> None:
        # self._sem_api: SEM_API = None
        # self._beams: Beams = None
        # self._imaging: Imaging = None
        # self._specimen: Specimen = None
        # self._auto_functions: AutoFunctions = None
        # self._patterning: Patterning = None
        
        print("Initialising microscope.")

    def connect(self):
        
        import time
        # for easier usage
        from tescanautomation.Common import Bpp

        microscope_ip = 'localhost'
        self.session = Automation(microscope_ip)
        #self._sem_api = SEM_API()
        self._beams = Beams(self.session)
        self._imaging = Imaging(self.session)
        self._specimen = Specimen(self.session)
        self._auto_functions = AutoFunctions(self.session)
        self._patterning = Patterning(self.session)

        #probe_table_path = probeTable

        print("Connecting microscope!")

    def disconnect(self):
        self.session.Disconnect()
        print("Disconnecting microscope!")

    @property
    def beams(self) -> Beams:
        """Get the current electron_beam object"""
        return self._beams

    @property
    def specimen(self) -> Specimen:
        """Get the current specimen object"""
        return self._specimen

    @property
    def imaging(self) -> Imaging:
        """Get the current imaging object"""
        return self._imaging

    @property
    def auto_functions(self) -> AutoFunctions:
        """Get the current auto functions object"""
        return self._auto_functions


# grabframesettings = GrabFrameSettings()
# microscope = MicroscopeClient()
# print(microscope.beams.get_available_beams())

# old_mag = microscope.beams.ion_beam.horizontal_field_width.value = #image.metadata.optics.scan_field_of_view.width

# value = microscope.beams.electron_beam.beam_shift.value = Point(0,0)
# microscope.beams.electron_beam.beam_shift.value += Point(x,y) # incremental

# old_mag = microscope.beams.electron_beam.horizontal_field_width.value = #image.metadata.optics.scan_field_of_view.width

# rotation=microscope.beams.electron_beam.scanning.rotation.value

# old_resolution = microscope.beams.electron_beam.scanning.resolution.value = #img_resolution
# stageposition=microscope.specimen.stage.current_position
# microscope.specimen.stage.absolute_move(stagepos)
# microscope.specimen.stage.relative_move(stagepos)

# microscope.auto_functions.run_auto_cb()
# microscope.auto_functions.run_auto_focus()

###### CODE FROM ROLAND
# microscope = MicroscopeClient()
# microscope.connect()
# microscope.specimen.stage.absolute_move((65e-3, 65e-3))
# microscope.specimen.stage.relative_move((-2e-3, -10e-3))
# # microscope.beams.electron_beam.beam_shift.value = Point(1,1)
# # microscope.beams.electron_beam.beam_shift.value += Point(1,1)
# microscope.beams.electron_beam.turn_on()
# microscope.beams.electron_beam.beam_current.value = 1e-9

# microscope.beams.electron_beam.beam_shift.value = Point(20,20)
# time.sleep(3)
# microscope.beams.electron_beam.beam_shift.value += Point(2,7)
#beamshift = BeamShift()
#beamshift.value = Point(1, 1)
#print(beamshift.value)
#beamshift.value += Point(10, 10)
#print(beamshift.value)
#microscope.disconnect()

####### /CODE FROM ROLAND


# microscope.disconnect()
# beamshift = BeamShift()
# print(beamshift.value)
# beamshift.value += Point(1,1)
