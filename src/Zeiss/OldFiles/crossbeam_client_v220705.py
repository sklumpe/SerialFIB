import sys

#sys.coinit_flags = 0  # type: ignore
#import pythoncom  # isort:skip  # noqa: E402, F401
from time import sleep
from typing import List, Tuple
import numpy as np
#from SEM_API import SEM_APItry:
try:
    from src.Zeiss.SEM_API import SEM_API
except ModuleNotFoundError:
    from SEM_API import SEM_API
import math

# TODO Use modern api but i need to think how we can get just the api without entire sem
# automation maybe separate repository for api?
DWELLTIMES = {
    "25e-9": "25 ns",
    "50e-9": "50 ns",
    "100e-9": "100 ns",
    "200e-9": "200 ns",
    "400e-9": "400 ns",
    "800e-9": "800 ns",
    "1.6e-6": "1.6 µs",
    "3.2e-6": "3.2 µs",
    "6.4e-6": "6.4 µs",
    "12.8e-6": "12.8 µs",
    "25.6e-6": "25.6 µs",
    "51.2e-6": "51.2 µs",
    "102.4e-6": "102.4 µs",
    "204.8e-6": "204.8 µs",
    "405.6e-6": "405.6 µs",
    "819.2e-6": "819.2 µs",
    "1.64e-3": "1.64 ms"

}


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


class DwellTime:
    def __init__(self, sem: SEM_API = None) -> None:
        self._value = 100e-9
        self._sem = sem

    @property
    def value(self) -> float:
        """Get the current dwelltime value"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        # TODO IS it the right parameter to set ?
        dwell_time = self._closest(value)
        if self._sem is not None:
            self._sem.SetState("DP_DWELL_TIME", DWELLTIMES[dwell_time])
        self._value = value

    @staticmethod
    def _closest(value):
        lst = list(DWELLTIMES)
        return lst[min(range(len(lst)), key=lambda i: abs(float(lst[i]) - value))]


class Resolution:
    def __init__(self, sem: SEM_API) -> None:
        self._sem = sem
        self._value = "1024 * 768"
        if self._sem is not None:
            self._sem.SetState("DP_IMAGE_STORE", self._value)

    @property
    def value(self) -> str:
        """Get the current resolution"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        # TODO check available resolutions or not?
        if self._sem is not None:
            self._sem.SetState("DP_IMAGE_STORE", value)
        self._value = value


class Rotation:
    def __init__(self, sem: SEM_API) -> None:
        self._value = 0.0
        self._sem = sem

    @property
    def value(self) -> float:
        """Get the set scan rotation angle"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        if self._sem is not None:
            self._sem.set_rotation(value)
        self._value = value


class Scanning:
    def __init__(self, sem: SEM_API) -> None:
        self._dwell_time = DwellTime(sem)
        self._resolution = Resolution(sem)
        self._rotation = Rotation(sem)

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


class BeamShift:
    def __init__(self, sem: SEM_API) -> None:
        self._value = Point(0, 0)
        self._sem = sem

    @property
    def value(self) -> Point:
        """Get the current beam shift angle"""
        return self._value

    @value.setter
    def value(self, value: Point) -> None:
        if self._sem is not None:
            self._sem.SetValue("AP_BEAMSHIFT_X", value.x)
            self._sem.SetValue("AP_BEAMSHIFT_Y", value.y)
        self._value = value


class BeamCurrent:
    def __init__(self, sem: SEM_API) -> None:
        self._value = 0.0e-9
        self._sem = sem

    @property
    def value(self) -> float:
        """Get the set beam current"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        """set the available beam current that is closest to the required one"""
        if self._sem is not None:
            self._sem.SetValue("AP_IPROBE", value)
            # TODO make sure this command is executed some event?
        self._value = value


class FieldOfView:
    def __init__(self, sem: SEM_API) -> None:
        self._value = 0
        self._sem = sem

    @property
    def value(self) -> float:
        """Get the set scan rotation angle"""
        return self._value

    @value.setter
    def value(self, value) -> None:
        """Set field of view width in microns."""
        #TODO is it right
        if self._sem is not None:
            #pixel_size = self._sem.GetValue("AP_PIXEL_SIZE")
            #resulution = int(str.split(self._sem.GetState("DP_IMAGE_STORE"), "*")[1])
            self._sem.SetValue("AP_WIDTH", value)

        self._value = value


# TODO: do not implement
class IonBeam:
    def __init__(self) -> None:
        self._is_blanked = True
        self._horizontal_field_width = FieldOfView(None)
        self.scanning = Scanning(None)
        self._beam_shift = BeamShift(None)
        self._beam_current = BeamCurrent(None)

        self.scanning.resolution.value = "1024 * 768"
        self.scanning.dwell_time.value = 200e-09
        self._beam_shift.value = Point(0, 0)
        self._beam_current.value = 500e-9

    def turn_on(self):
        pass

    def turn_off(self):
        pass

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


# TODO: Field of view
class ElectronBeam:
    def __init__(self, sem: SEM_API) -> None:
        self._is_blanked = True
        self._horizontal_field_width = FieldOfView(sem)
        self._scanning = Scanning(sem)
        self._beam_shift = BeamShift(sem)
        self._beam_current = BeamCurrent(sem)
        self._sem = sem

        self._scanning.resolution.value = "1024 * 768"
        self._scanning.dwell_time.value = 200e-09
        self._beam_shift.value = Point(0, 0)
        self._beam_current.value = 500e-9

    def turn_on(self):
        self._sem.Execute("CMD_BEAM_ON")

    def turn_off(self):
        self._sem.Execute("CMD_BEAM_OFF")

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
    def is_blanked(self, is_blanked: bool) -> None:
        if is_blanked:
            self._sem.SetState("DP_BEAM_BLANKED", "Yes")
        else:
            self._sem.SetState("DP_BEAM_BLANKED", "No")
        self._is_blanked = is_blanked


class Beams:
    def __init__(self, sem: SEM_API) -> None:
        self.sem = sem
        self._beams = "Electon and Ion"
        self._electron_beam = ElectronBeam(sem)
        self._ion_beam = IonBeam()

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


# TODO: do not implement
class Pattering:
    def __init__(self, sem: SEM_API) -> None:
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
        self._state = self._sem.GetValue("DP_FIB_MODE")
        return self._state

    @state.setter
    def state(self, state) -> None:
        success = self._sem.SetValue("DP_FIB_MODE", state)
        self._state = state


class GrabFrameSettings:
    def __init__(self, dwell_time: float, resolution: str, line_integration: str) -> None:
        self._dwell_time = dwell_time
        self._resolution = resolution
        self._line_integration = line_integration


class Imaging:
    def __init__(self, sem: SEM_API) -> None:
        self._sem = sem

    def set_active_device(self):
        """setting imaging column (FIB mode ... SEM or FIB)"""
        pass

    def get_active_view(self) -> int:
        return 1

    def set_active_view(self, view: int):
        pass

    ''' From ROLAND
    def grab_frame(self, framesettings: GrabFrameSettings):
        """Grabbing a single full frame image"""
        image = self._sem.grab_full_image("C:\test.tif")
        return image

    def grab_multiple_frames(self, framesettings: GrabFrameSettings):
        """Grabbing images of all set channels"""
        images = []
        images.append(self._sem.grab_full_image("C:\test.tif"))
        return images
    '''
    def grab_frame(self, framesettings: GrabFrameSettings):
        """Grabbing a single full frame image"""
        image = self._sem.grab_full_image(r"c:/Users/Sven/Pictures/test.tif")
        return image

    def grab_multiple_frames(self, framesettings: GrabFrameSettings):
        """Grabbing images of all set channels"""
        images = []
        images.append(self._sem.grab_full_image(r"c:/Users/Sven/Pictures/test.tif"))
        return images


class Stage:
    """Class for manipulating stage parameters."""

    def __init__(self, sem: SEM_API) -> None:
        """Initialise stage class."""
        self._sem = sem
        self._current_position = self._sem.GetStagePosition()

    def absolute_move(self, stage_pos: Tuple):
        """Move stage to absolute position x,y."""
        #self._sem.move_stage_absolute_xy(stage_pos[0], stage_pos[1])
        self._is_moving = True
        self._sem.move_stage_absolute(stage_pos)
        print(f"Moving stage x to {stage_pos[0]} m and y to {stagepos[1]} m")

        self._sem.wait_for_stage_idle() # use this when working with PyQt5
    def relative_move(self, stage_pos: Tuple):
        """Move stage relative by dx,dy."""
        #self._sem.move_stage_relative_xy(stage_pos[0], stage_pos[1])
        self._is_moving = True
        self._sem.move_stage_relative(stagepos)
        print(f"Moving stage by {stagepos[0]} m in x and by {stagepos[1]} m in y direction.")
        
        self._sem.wait_for_stage_idle() # use this when working with PyQt5
        
    @property
    def current_position(self) -> Tuple:
        """Get stage current position."""
        self._current_position = self._sem.GetStagePosition()
        return self._current_position


class AutoFunctions:
    def __init__(self, sem: SEM_API) -> None:
        self._sem = sem

    def run_auto_cb(self) -> None:
        """Run auto rcb."""
        self._sem.Execute("CMD_QUICK_BC")

    def run_auto_focus(self) -> None:
        """Run sem autofocus."""
        self._sem.Execute("CMD_AUTO_FOCUS_FINE")


class Specimen:
    def __init__(self, sem: SEM_API) -> None:
        self._sem = sem
        self._stage = Stage(self._sem)

    @property
    def stage(self) -> Stage:
        """Get the current stage object"""
        return self._stage


class MicroscopeClient:
    """Use this client as singleton single instance for single microscope."""

    def __init__(self) -> None:
        self._sem_api: SEM_API = None
        self._beams: Beams = None
        self._imaging: Imaging = None
        self._specimen: Specimen = None
        self._auto_functions: AutoFunctions = None

    def connect(self, address: str = "local"):
        self._sem_api = SEM_API(address)
        self._beams = Beams(self._sem_api)
        self._imaging = Imaging(self._sem_api)
        self._specimen = Specimen(self._sem_api)
        self._auto_functions = AutoFunctions(self._sem_api)

        print("Connecting microscope!")

    def disconnect(self):
        self._sem_api.close()
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


#microscope = MicroscopeClient()
#microscope.connect()
#microscope.beams.electron_beam.scanning.dwell_time.value = 150e-9
#microscope.beams.electron_beam.horizontal_field_width.value = 5
# microscope.specimen.stage.absolute_move((5e-3, 6e-3))
# microscope.specimen.stage.relative_move((2e-3, 10e-3))
# microscope.beams.electron_beam.beam_shift.value = Point(1,1)
# microscope.beams.electron_beam.beam_shift.value += Point(1,1)
# microscope.beams.electron_beam.turn_on()
# microscope.beams.electron_beam.beam_current.value = 1e-9
#
# microscope.beams.electron_beam.beam_shift.value = Point(2,2)
#
# microscope.beams.electron_beam.scanning.rotation.value = 10
# microscope.beams.electron_beam.is_blanked = False
# beamshift = BeamShift()
# beamshift.value = Point(1, 1)
# print(beamshift.value)
# beamshift.value += Point(10, 10)
# print(beamshift.value)
#microscope.disconnect()
# microscope.disconnect()
# beamshift = BeamShift()
# print(beamshift.value)
# beamshift.value += Point(1,1)
