# -*- coding: utf-8 -*-
"""
This is an implementation of SEM API Wrapper

How to use:
    
The SEM_API class provides a context manager. It is highly recommended to use
it through _with_ expression

with SEM_API(state='remote') as sem:
    do_something(sem)

Alternatively, the class can be initiated and closed manually.

sem = SEM_API(state='remote')
# do something
sem.close()

The SEM_API class must be initialized by specifying if the EM Server is running
remotely or locally (state = 'remote' or 'local'). This will influence the 
behavior of how the real time image interface behaves.

The interface provides following functions:
    
1. Functions derived from SmartSEM API:
    
    GetValue(AP_name, style='float')
    SetValue(AP_name, value)
    GetValueMin(AP_name)
    GetValueMax(AP_name)
    GetState(DP_name, style='string')
    SetState(DP_name, value)
    Execute(CMD_name)
    GetStagePosition()
    MoveStage(coord)
    Grab(self, fname, X=0, Y=0, W=1024, H=768, overlay = False)
    GetCurrentUserName()

2.  Interface to get real time image. The real time image will be updated in
    following properties:
    img_array   
        If running remotely, it provides uint8 array of current image using the current 
        pixel store. If running locally, it provides uint16 array instead.
    img_array_reduced   
        Only present if running locally. It provides uint8 array of current image in 
        1024x768 pixel store.
                        
    The following commands control the start, pause and terminate of continuous
    image acquisition:
        UpdateImage_Start()
        UpdateImage_Pause()
        UpdateImage_Terminate()
    The update rate can be set through the following property:
        update_rate  
            possible values from 0.01 to 10
    
3.  Often used high level function:
    wait_for_stage_idle(wait_time = 0.0)
        Wait till the stage arrives in destination, with extra delay by wait_time.
    grab_full_image(fname)
        Freeze and wait till scan finished to capture a full image.
        Depending on the current channels, the function will save 1, 2 or 4 images.
        The fname parameter is either a single string or a list of strings.
        For single string like foobar.tif, it will save foobar.tif, foobar_b.tif, foobar_c.tif etc.
        Else for a list of stings, it will save each channel to corresponding string. 
    set_scan_speed(scan_speed)
        Directly set certain scan speed without calling the command.
    set_scan_mode(scan_mode)
        Directly set the noise reduction mode of scan without calling the command.
    do_autofocus()
        Peform autofocus, wait till it finishes.
    get_detector_list(refresh = False)
        Obtain a list of detectors. When first time used on a machine this might take up to 30 seconds.
        Use refresh=True to enforce scanning through all possible detectors.
    
4.  Event interface:
    The event interface is implemented as "bag of handler function". The handler function is
    called as:
    handler(ParameterName, Reason, ParameterID, LastKnownValue)
    The following function and attributes are used to control the event interface:
    Add_Event(func)
        Add func in the bag of handler.
    Remove_Event(func)
        Remove func from the bag of handler.
    Set_Notify(PARAM)
        Start monitoring PARAM, trigger the event when PARAM is changed.
    Unset_Notify(PARAM)
        Stop monitoring PARAM.
    event_time
        Set the time interval in second to check event trigger. Default is 0.1 S.



Version: 0.3.11
Author: Luyang Han

ChangLog:
v 0.3.11
add function to make sure the grab_full_image returns a image with content, avoid blank images.
v 0.3.10
get_imaging_detector_list() to be more specific, only return SEM detectors, not chamberscope.
v.0.3.9
Use Variant to enforce data type.
v.0.3.8
The detector list is saved for specific machine serial number. So that the refresh will just happen once.
The function to get detector list also contains a parameter to force refresh.
v.0.3.7
Add function to get detector list.
v 0.3.6
Add additional wait_time parameter for wait_for_stage_idle() function.
v 0.3.5
grab_full_image now automatically saves multiple images in 2 and 4 channel mode.
v 0.3.4
Change the early binding method. Now it is faster.
v 0.3.3
Minor changes to the context manager. Add function to get user name. API_ERROR does not raise exception, only gives a warning.
v 0.3.2
Remove hard dependency on numpy and imread. If these packages are not found, the real time image array function will be disabled.
v 0.3.1
Change to the grab function.
v 0.3
04.09.2019 : Add event interface
"""
__version__ = "0.3.10"

import sys

#sys.coinit_flags = 0

# import asyncio

from win32com import client
import pythoncom
import threading, time, tempfile, mmap, warnings
import pickle, os
from win32com.client import VARIANT

# import logger
import logging

log = logging.getLogger(__name__)
log.level = logging.DEBUG

try:
    from imageio import imread
except:
    try:
        from scipy.misc import imread
    except:
        try:
            from skimage.io import imread
        except:
            imread = None
            log.warning(
                "[SEM_API] Cannot find the module with imread. Please install one of the following package:\n imageio, skimage or scipy.")

try:
    import numpy as np
except:
    np = None
    log.warning("[SEM_API] Cannot find the numpy. Realtime image array will be disabled.")

# following changes are necessary for event to work
from win32com.client import gencache

gencache.EnsureModule("{71BD42C1-EBD3-11D0-AB3A-444553540000}", 0, 1, 0)

# from win32com.client import makepy
# sys.argv = ["makepy", r"CZ.EmApiCtrl.1"]
# makepy.main()


_excpetion_dict = \
    {1000: ('API_E_GET_TRANSLATE_FAIL',
            'Failed to translate parameter into an id'),
     1001: ('API_E_GET_AP_FAIL', 'Failed to get analogue value'),
     1002: ('API_E_GET_DP_FAIL', 'Failed to get digital value'),
     1003: ('API_E_GET_BAD_PARAMETER',
            'Parameter supplied is not analogue nor digital'),
     1004: ('API_E_SET_TRANSLATE_FAIL',
            'Failed to translate parameter into an id'),
     1005: ('API_E_SET_STATE_FAIL', 'Failed to set a digital state'),
     1006: ('API_E_SET_FLOAT_FAIL', 'Failed to set a float value'),
     1007: ('API_E_SET_FLOAT_LIMIT_LOW', 'Value supplied is too low'),
     1008: ('API_E_SET_FLOAT_LIMIT_HIGH', 'Value supplied is too high'),
     1009: ('API_E_SET_BAD_VALUE', 'Value supplied is is of wrong type'),
     1010: ('API_E_SET_BAD_PARAMETER',
            'Parameter supplied is not analogue nor digital'),
     1011: ('API_E_EXEC_TRANSLATE_FAIL', 'Failed to translate command into an id'),
     1012: ('API_E_EXEC_CMD_FAIL', 'Failed to execute command'),
     1013: ('API_E_EXEC_MCF_FAIL', 'Failed to execute file macro'),
     1014: ('API_E_EXEC_MCL_FAIL', 'Failed to execute library macro'),
     1015: ('API_E_EXEC_BAD_COMMAND', 'Command supplied is not implemented'),
     1016: ('API_E_GRAB_FAIL', 'Grab command failed'),
     1017: ('API_E_GET_STAGE_FAIL', 'Get Stage position failed'),
     1018: ('API_E_MOVE_STAGE_FAIL', 'Move Stage position failed'),
     1019: ('API_E_NOT_INITIALISED', 'API not initialised'),
     1020: ('API_E_NOTIFY_TRANSLATE_FAIL',
            'Failed to translate parameter to an id'),
     1021: ('API_E_NOTIFY_SET_FAIL', 'Set notification failed'),
     1022: ('API_E_GET_LIMITS_FAIL', 'Get limits failed'),
     1023: ('API_E_GET_MULTI_FAIL', 'Get multiple parameters failed'),
     1024: ('API_E_SET_MULTI_FAIL', 'Set multiple parameters failed'),
     1025: ('API_E_NOT_LICENSED', 'Missing API license'),
     1026: ('API_E_NOT_IMPLEMENTED', 'Reserved or not implemented'),
     1027: ('API_E_GET_USER_NAME_FAIL',
            'Failed to get user name (Remoting Interface only)'),
     1028: ('API_E_GET_USER_IDLE_FAIL',
            'Failed to get user idle state (Remoting Interface only)'),
     1029: ('API_E_GET_LAST_REMOTING_CONNECT_ERROR_FAIL',
            'Failed to get the last remoting connection error string (Remoting Interface Only)'),
     1030: ('API_E_EMSERVER_LOGON_FAILED',
            'Failed to remotely logon to the EM Server (username and password may be incorrect or EM Server is not running or User is already logged on, Remoting only)'),
     1031: ('API_E_EMSERVER_START_FAILED',
            'Failed to start the EM Server. This may be because the Server is already running or has an internal error (Remoting Interface only)'),
     1032: ('API_E_PARAMETER_IS_DISABLED',
            'The command or parameter is currently disabled (you cannot execute or set it. Remoting Interface only)'),
     2027: ('API_E_REMOTING_NOT_CONFIGURED',
            'Remoting incorrectly configured, use RConfigure to correct'),
     2028: ('API_E_REMOTING_FAILED_TO_CONNECT',
            'Remoting did not connect to the server'),
     2029: ('API_E_REMOTING_COULD_NOT_CREATE_INTERFACE',
            'Remoting could not start (unknown reason)'),
     2030: ('API_E_REMOTING_EMSERVER_NOT_RUNNING',
            'Remoting: Remote server is not running currently'),
     2031: ('API_E_REMOTING_NO_USER_LOGGED_IN',
            'Remoting: Remote server has no user logged in')}

# FIXED: Ignore channel 16 to 18 to avoid crashing SmartSEM.
DETECTOR_MAX = 32
DETECTOR_SKIP = [16, 17, 18]
DETECTOR_DATA = "detector_list.pickle"


# class to handle exceptions
class API_ERROR(Exception):
    def __init__(self, error_code):
        global _excpetion_dict
        self.error_text = ('\n').join(_excpetion_dict[error_code])
        warnings.warn(self.error_text)


# periodically run function
class SwitchThread(threading.Thread):
    """
    class to run a function repeatedly in the background.
    The delay between each run is given as delay in s.
    The thread can be paused and also ended.
    """

    def __init__(self, target=None, name=None, args=(), kwargs={}, delay=1):
        super(SwitchThread, self).__init__(group=None, target=target, name=name, args=(),
                                           kwargs={})
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.delay = delay
        self.enable = True
        self.stop = False
        return

    def run(self):
        while not self.stop:
            if self.enable:
                self.target(*self.args, **self.kwargs)
            time.sleep(self.delay)

    def pause(self):
        self.enable = False

    def resume(self):
        self.enable = True

    def terminate(self):
        self.stop = True


EventBase = client.getevents("CZ.EMApiCtrl.1")


class SEM_Handle(EventBase):
    def __init__(self, sem):
        self.subscribers = []
        super().__init__(sem)

    def OnNotifyWithCurrentValue(self, lpszParameter, Reason, paramid, dLastKnownValue):
        for sub in self.subscribers:
            sub(lpszParameter, Reason, paramid, dLastKnownValue)


class SEM_API:
    """
    Python Wrapper to SEM API interface
    
    The class provide a context manager to do some house keeping, it is advised
    to use with statement.
    
    with SEM_API(state='remote') as sem:
        do_something(sem)
    
    """
    IMAGE_RETRY = 3
    IMAGE_THRESHOLD = 2

    def __init__(self, state='local'):
        """
        Function to initialize the API interface.
        This function uses the long InitialiseRemote(void) command.
        
        """
        self.mic = client.Dispatch('CZ.EMApiCtrl.1')
        if not (state == "remote" or state == "local"):
            raise ValueError("state is either remote or local")
        self.__state = state
        # first initialize
        res = self.mic.InitialiseRemoting()
        if res == 0:
            # prepare the background working
            # prepare the MMF for local operation
            if imread is not None:
                if self.__state == "local":
                    self.__pymap = mmap.mmap(-1, 1024 * 768 + 1064, "Capture0.MMF",
                                             mmap.ACCESS_READ)
                time.sleep(0.1)
                self.__background_worker = SwitchThread(target=self.__update_image,
                                                        delay=1.0)
                self.__background_worker.start()
                self.__background_worker.pause()
                time.sleep(0.1)
            # self.subs = []
            # self.event = SEM_Handle(seflf.mic, self.subs)
            self.event_time = 0.1
            self.event = SEM_Handle(self.mic)
            self.__event_stop = False
            self.__event_thread = threading.Thread(target=self.__pump)
            self.__event_thread.start()
            # detector list
            if os.path.exists(DETECTOR_DATA):
                with open(DETECTOR_DATA, "rb") as fname:
                    old_dict = pickle.load(fname)
                    machine_sn = self.GetState("SV_SERIAL_NUMBER")
                    if machine_sn in old_dict.keys():
                        self.__detector_list = old_dict[machine_sn]
                    else:
                        self.__detector_list = []
            else:
                self.__detector_list = []
        else:
            raise API_ERROR(res)

    def get_detector_list(self, refresh=False):
        if len(self.__detector_list) > 0 and refresh == False:
            # detector list already updated.
            return self.__detector_list
        else:
            # detector list update sequence, takes about 1 minute
            self.__detector_list = []
            self.Execute("CMD_MODE_NORMAL")
            for i in range(DETECTOR_MAX):
                if i not in DETECTOR_SKIP:
                    try:
                        self.SetState("DP_DETECTOR_CHANNEL", i)
                        time.sleep(0.5)
                        name = self.GetState("DP_DETECTOR_CHANNEL")
                        if name != "":
                            self.__detector_list.append(name)
                    except:
                        break
            return self.__detector_list

    def get_imaging_detector_list(self, refresh=False):
        # get only the imaging detectors.
        res = self.get_detector_list(refresh)
        filter_res = [det for det in res if not "TV" in det]
        return filter_res

    # decorator for the wrapper function
    def __error_handling(func):
        def func_wrapper(*arg, **kwargs):
            res = func(*arg, **kwargs)
            if type(res) == int:
                return_code = res
                if return_code != 0:
                    raise API_ERROR(return_code)
            elif type(res) == tuple:
                return_code = res[0]
                result = res[1]
                if return_code == 0:
                    return result
                else:
                    raise API_ERROR(return_code)

        return func_wrapper

    # function to handle the event
    def __pump(self):
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        while self.__event_stop is not True:
            pythoncom.PumpWaitingMessages()
            time.sleep(self.event_time)
        pythoncom.CoUninitialize()

    def Add_Event(self, func):
        self.event.subscribers.append(func)

    def Remove_Event(self, func):
        self.event.subscribers.remove(func)

    @__error_handling
    def Set_Notify(self, PARAM):
        res = self.mic.SetNotify(PARAM, True)
        return res

    @__error_handling
    def Unset_Notify(self, PARAM):
        res = self.mic.SetNotify(PARAM, False)
        return res

    # some variables to hold the data
    __fname = tempfile.TemporaryFile(suffix='.bmp').name

    # function to update the image file
    def __update_image(self):
        if self.__state == 'remote':
            # when working remote, write the image to a bmp file and read back.
            self.mic.Grab(0, 0, 1024, 768, 0, self.__fname)
            self.img_array = imread(self.__fname)
        elif self.__state == 'local':
            # when working local, write the image to mmap file and read back.
            # as each time the size of the frame can change, we create a mmap
            # every time on the fly to grab the image
            pixel_density = tuple(map(int, self.GetState("DP_IMAGE_STORE").split("*")))
            self.mic.Grab(0, 0, 1024, 768, 0, "CZ.MMF")
            py_map = mmap.mmap(-1, pixel_density[0] * pixel_density[1] * 2, "CZ.MMF",
                               mmap.ACCESS_READ)
            self.img_array = np.copy(np.frombuffer(py_map, dtype="uint16").reshape(
                (pixel_density[1], pixel_density[0])))
            py_map.close()
            # update local image
            self.img_array_reduce = np.flip(
                np.frombuffer(self.__pymap, dtype="uint8", offset=1064).reshape(
                    (768, 1024)), axis=0)
        return

    @property
    def update_rate(self):
        return self.__background_worker.delay

    @update_rate.setter
    def update_rate(self, value):
        if value < 0.01:
            value = 0.01
            warnings.warn("Update delay cannot be smaller than 10 ms.")
        elif value > 10:
            value = 10
            warnings.warn("Update delay cannot be larger than 10 s.")
        self.__background_worker.delay = value

    # function for AP
    @__error_handling
    def GetValue(self, AP_name, style='float'):
        """
        function to get an analog value.
        style: float or string
        float returns a floating number, string returns a string representation with unit.
        """
        if style == 'float':
            # buffer = 0.0
            # res = self.mic.Get(AP_name, buffer)
            res = self.mic.Get(AP_name, VARIANT(pythoncom.VT_R4, 0))
            return res
        elif style == 'string':
            # buffer = ''
            # res = self.mic.Get(AP_name, buffer)
            res = self.mic.Get(AP_name, VARIANT(pythoncom.VT_BSTR, ""))
            return res
        else:
            raise AttributeError("style = float or string")

    @__error_handling
    def GetValueMin(self, AP_name):
        buffer = 0.0
        res = self.mic.GetLimits(AP_name, buffer, buffer)
        return (res[0], res[1])

    @__error_handling
    def GetValueMax(self, AP_name):
        buffer = 0.0
        res = self.mic.GetLimits(AP_name, buffer, buffer)
        return (res[0], res[2])

    @__error_handling
    def SetValue(self, AP_name, value):
        """
        function to set an analog value.
        The function can only take floating point number.
        """
        # if type(value) == str:
        #     pass
        # else:
        #     value = float(value)
        # res = self.mic.Set(AP_name, value)
        # return res
        log.debug(f"{AP_name} to {value}")
        w = VARIANT(pythoncom.VT_R4, float(value))
        res = self.mic.Set(AP_name, w)
        return res

    # function for DP

    @__error_handling
    def GetState(self, DP_name, style='string'):
        """
        function to get an digital value.
        style: float or string
        int returns a integer number, string returns a string representation.
        """
        if style == 'int':
            # buffer = 0
            # res = self.mic.Get(DP_name, buffer)
            # return res
            res = self.mic.Get(DP_name, VARIANT(pythoncom.VT_R4, 0))
            return res
        elif style == 'string':
            # buffer = ''
            # res = self.mic.Get(DP_name, buffer)
            # return res
            res = self.mic.Get(DP_name, VARIANT(pythoncom.VT_BSTR, ""))
            return res
        else:
            raise AttributeError("style = int or string")

    @__error_handling
    def SetState(self, DP_name, value):
        """
        function to set a digital state.
        The function can take either integer or a formatted string.
        """
        # if type(value) == str:
        #     pass
        # else:
        #     value = float(value)
        # res = self.mic.Set(DP_name, value)
        # return res
        log.debug(f"{DP_name} to {value}")
        if type(value) == str:
            w = VARIANT(pythoncom.VT_BSTR, value)
        else:
            w = VARIANT(pythoncom.VT_R4, int(value))
        res = self.mic.Set(DP_name, w)
        return res

    # function for CMD
    @__error_handling
    def Execute(self, CMD_name):
        res = self.mic.Execute(CMD_name)
        return res

    # function about stage
    @__error_handling
    def GetStagePosition(self):
        buffer = 0.0
        res = self.mic.GetStagePosition(buffer, buffer, buffer, buffer, buffer, buffer)
        return (res[0], res[1:])

    @__error_handling
    def MoveStage(self, coord):
        log.debug(f"Stage to {coord[0]}, {coord[1]}, {coord[2]}, {coord[3]}, {coord[4]}")
        if len(coord) == 6:
            res = self.mic.MoveStageDoubles(*coord)
            return res
        else:
            raise IndexError("coord must be a list or tuple of 6 floating number")

    # function about grab image
    @__error_handling
    def Grab(self, fname, X=0, Y=0, W=1024, H=768, overlay=False):
        """
        The function to grab the current image.
        left, right, top, button defines the desired size of the imaged, express as the 
        coordinate relative to the full image.
        For example, if 10% of the edge should be excluded, the coordinate should be
            left = 0.1, right = 0.9, top = 0,1, button = 0.9
        overlay determines whether the image overlay such as datazone should be included.
        """
        # X = int(left * 1024)
        # Y = int(top * 768)
        # W = int((right-left)*1024)
        # H = int((bottom-top)*768)
        if overlay:
            res = self.mic.Grab(X, Y, W, H, -1, fname)
        else:
            res = self.mic.Grab(X, Y, W, H, 0, fname)
        return res

    @__error_handling
    def GetCurrentUserName(self):
        """Return EM server user name and windows user name"""
        buffer = ""
        res = self.mic.GetCurrentUserName(buffer, buffer)
        return (res[0], res[1:])

    # parameter and functions dealing with the memory map file and real time imaging.

    # 2 different interface are supplied, the img_array gives the real time image with
    # current pixel density in 16 bit grey. the image_array_reduced gives 8 bit grey
    # image of image reduced to 1024x768
    # the value should be updated regularly by a seperate thread in the background.
    if np is not None:
        img_array = np.zeros((768, 1024))
        img_array_reduce = np.zeros((768, 1024))

    # img_array = np.zeros((768,1024)).astype('uint16')
    def UpdateImage_Start(self):
        """
        function to start continuous updating the imaging array
        """
        self.__background_worker.resume()

    def UpdateImage_Pause(self):
        """
        function to pause continuous updating the imaging array
        """
        self.__background_worker.pause()

    # some typically used higher level functions
    # implementation pending
    def move_stage_relative_xy(self, dx, dy):
        pos = self.GetStagePosition()
        self.MoveStage((pos[0] + dx, pos[1] + dy, pos[2], pos[3], pos[4], pos[5]))

    def move_stage_absolute_xy(self, x, y):
        pos = self.GetStagePosition()
        self.MoveStage((x, y, pos[2], pos[3], pos[4], pos[5]))
    
    def move_stage_absolute(self, stagepos):
        pos = self.GetStagePosition()
        x=stagepos[0]
        y=stagepos[1]
        z=stagepos[2]
        t=stagepos[3]
        r=stagepos[4]
        self.MoveStage((x, y, z, t, r, pos[5]))
    
    def move_stage_relative(self, stagepos):
        pos = self.GetStagePosition()
        dx=stagepos[0]
        dy=stagepos[1]
        dz=stagepos[2]
        dt=stagepos[3]
        dr=stagepos[4]
        self.MoveStage((pos[0]+dx, pos[1]+dy, pos[2]+dz, pos[3]+dt, pos[4]+dr, pos[5]))

    def wait_for_stage_idle(self, wait_time=0.0):
        """
        wait for the stage movement to finish.
        """
        while not self.GetState("DP_STAGE_IS") == "Idle":
            time.sleep(0.3)
        time.sleep(wait_time)

    # async def await_for_stage_idle(self, wait_time = 0.0):
    #     """
    #     wait for the stage movement to finish.
    #     """
    #     while not self.GetState("DP_STAGE_IS") == "Idle":
    #         await asyncio.sleep(0.1)
    #     time.sleep(wait_time)

    def set_scan_speed(self, DP_Param):
        c_dict = {
            "0": "CMD_SCANRATE0",
            "1": "CMD_SCANRATE1",
            "2": "CMD_SCANRATE2",
            "3": "CMD_SCANRATE3",
            "4": "CMD_SCANRATE4",
            "5": "CMD_SCANRATE5",
            "6": "CMD_SCANRATE6",
            "7": "CMD_SCANRATE7",
            "8": "CMD_SCANRATE8",
            "9": "CMD_SCANRATE9",
            "10": "CMD_SCANRATE10",
            "11": "CMD_SCANRATE11",
            "12": "CMD_SCANRATE12",
            "13": "CMD_SCANRATE13",
            "14": "CMD_SCANRATE14",
            "15": "CMD_SCANRATE15"
        }
        self.Execute(c_dict[str(DP_Param)])

    def set_scan_mode(self, DP_Param):
        c_dict = {
            "Pixel Avg.": "CMD_PIXNR",
            "Frame Avg": "CMD_FRAME_AVERAGE",
            "Frame Int. Busy": "CMD_FRAME_INT",
            "Frame Int. Done": "CMD_FRAME_INT",
            "Line Avg": "CMD_LINE_AVG",
            "Line Int. Busy": "CMD_LINE_INT",
            "Line Int. Done": "CMD_LINE_INT",
            "Line Int.": "CMD_LINE_INT",
            "Continuous Avg.": "CMD_CONTINUOUS_AVG",
            "Drift Comp. Frame Int. Busy": "CMD_DC_FRAME_INT",
            "Drift Comp. Frame Int. Done": "CMD_DC_FRAME_INT",
            "Drift Comp. Frame Int.": "CMD_DC_FRAME_INT",
            "Drift Comp. Frame Avg.": "CMD_DC_FRAME_AVG"
        }
        self.Execute(c_dict[DP_Param])

    def do_autofocus(self):
        self.SetState("DP_AUTOFOCUS_VERSION", "Line Scan based Autofocus Version")
        time.sleep(0.5)
        self.Execute("CMD_AUTO_FOCUS_FINE")
        time.sleep(2)
        while self.GetState("DP_AUTO_FN_STATUS") == "Busy":
            time.sleep(0.1)

    def set_active_beam(self, DP_Param):
        c_dict = {
            "ION": "CMD_FIB_MODE_FIB",
            "ELECTRON": "CMD_FIB_MODE_SEM"
        }
        self.Execute(c_dict[str(DP_Param)])
    
    def freeze(self, DP_Param):
        c_dict = {
            "FREEZE": "CMD_FREEZE_ALL",
            "UNFREEZE": "CMD_UNFREEZE_ALL"
        }
        self.Execute(c_dict[str(DP_Param)])

    def grab_full_image(self, fname, overlay=False, check=False):
        """
        grab the current full image by restarting the scan and till the complete
        frame is finished, and then save the image.

        This function contains a safe-guard against blank image. This might happen from time to time on SmartSEM.
        """
        self.SetState("DP_FREEZE_ON", "End Frame")
        accepted = False
        count = 0
        while not accepted and count <= self.IMAGE_RETRY:
            self.Execute("CMD_UNFREEZE_ALL")
            time.sleep(0.2)
            self.Execute("CMD_UNFREEZE_ALL")
            time.sleep(0.2)
            # self.Execute("CMD_SCANRATEDOWN")
            # time.sleep(0.2)
            # self.Execute("CMD_SCANRATEUP")
            # time.sleep(0.1)
            self.Execute("CMD_MODE_NORMAL")
            if self.GetState("DP_NOISE_REDUCTION") in ("Frame Avg", "Line Avg", \
                                                       "Pixel Avg.", "Continuous Avg.",
                                                       "Drift Comp. Frame Avg."):
                time.sleep(0.5)
                self.Execute("CMD_FREEZE_ALL")
            while self.GetState("DP_FROZEN") == "Live":
                time.sleep(0.1)
            channel_count = int(self.GetState("DP_DISPLAY_CHANNELS"))
            if channel_count == 1:
                try:
                    self.Grab(fname, overlay=overlay)
                    out_test = imread(fname)
                except:
                    warnings.warn("save image failed.")
            elif channel_count == 2:
                if type(fname) is str:
                    base, ext = os.path.splitext(fname)
                    fname_1 = fname
                    fname_2 = "{}_b.{}".format(base, ext)
                else:
                    fname_1, fname_2 = fname
                self.SetState("DP_ZONE", "0")
                self.Grab(fname_1, overlay=overlay)
                self.SetState("DP_ZONE", "1")
                self.Grab(fname_2, overlay=overlay)
                out_test = imread(fname_1)
            elif channel_count == 4:
                if type(fname) is str:
                    base, ext = os.path.splitext(fname)
                    fname_1 = fname
                    fname_2 = "{}_b.{}".format(base, ext)
                    fname_3 = "{}_c.{}".format(base, ext)
                    fname_4 = "{}_d.{}".format(base, ext)
                else:
                    fname_1, fname_2, fname_3, fname_4 = fname
                self.SetState("DP_ZONE", "0")
                self.Grab(fname_1, overlay=overlay)
                self.SetState("DP_ZONE", "1")
                self.Grab(fname_2, overlay=overlay)
                self.SetState("DP_ZONE", "2")
                self.Grab(fname_3, overlay=overlay)
                self.SetState("DP_ZONE", "3")
                self.Grab(fname_4, overlay=overlay)
                out_test = imread(fname_1)
            # test if image is blank
            if check:
                h, w = out_test.shape[0],out_test.shape[1]
                if np.std(out_test[h // 2:, :]) > self.IMAGE_THRESHOLD:
                    accepted = True
                    count += 1
                else:
                    accepted = False
                    # reset channel count and do it again.
                    old_channel_count = self.GetState("DP_DISPLAY_CHANNELS")
                    self.SetState("DP_DISPLAY_CHANNELS", "1")
                    time.sleep(0.5)
                    self.SetState("DP_DISPLAY_CHANNELS", old_channel_count)
                    count += 1
            else:
                accepted = True
        if not accepted:
            raise Exception(
                "Images are blank and cannot get useful images after retry. Please check the microscope.")

    def close(self):
        self.__exit__()

    # context interface
    # it is important to use this class through with statement
    # the exit function will properly clean up the wrapper.

    def __enter__(self):
        return self

    def __exit__(self, *arg):
        # try to save detector list for next time use
        # the detector list is ascribed to each machine SN.
        machine_sn = self.GetState("SV_SERIAL_NUMBER")
        if len(self.__detector_list) > 0:
            # we have detector data.
            if os.path.exists(DETECTOR_DATA):
                with open(DETECTOR_DATA, "rb") as fname:
                    old_dict = pickle.load(fname)
                    old_dict[machine_sn] = self.__detector_list
                with open(DETECTOR_DATA, "wb") as fname:
                    pickle.dump(old_dict, fname)
            else:
                outdict = {}
                outdict[machine_sn] = self.__detector_list
                with open(DETECTOR_DATA, "wb") as fname:
                    pickle.dump(outdict, fname)
        self.__background_worker.terminate()
        self.__background_worker.join()
        # stop event interface
        self.__event_stop = True
        self.__event_thread.join()
        self.event.close()
        del self.event
        # clear the MMF
        # if self.__state == 'local':
        #     self.__pymap.close()
        #     self.mic.Grab(0, 0, 0, 0, 0, "CZ.MMF")
        self.mic.ClosingControl()
