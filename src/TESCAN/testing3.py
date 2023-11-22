# TESCAN Automation Connecting to microscope
#
# Copyright (c) 2023 TESCAN GROUP, a.s.
# http://www.tescan.com
#

# Script in which is shown complete example of settings and milling of a trench using rectangular stairs object
# 20x20x8 µm including parameter and beam settings. Such trench can be used for rough milling in TEM lamella preparation
# process or for inspection of features of interest buried under material surface
#
#     WARNING: It is not recommended to start doing any tests on a real microscope until the script is debugged.
#     For the first steps with scripting it is strongly recommended working with Essence demo software!!

import time
from tescanautomation import Automation

# for easier usage
from tescanautomation.DrawBeam import IEtching
from tescanautomation.DrawBeam import Layer
from tescanautomation.DrawBeam import DepthUnit as DBDepthUnit
from tescanautomation.DrawBeam import Error as DBError
from tescanautomation.DrawBeam import Status as DBStatus
from tescanautomation.DrawBeam import ScanningPath
from tescanautomation.DrawBeam import ExpositionMeshAccuracy as DBAccuracy
from tescanautomation.FIB import HVBeamStatus as FIBStatus


# Print iterations progress
def printProgressBar(value, total, prefix='', suffix='', decimals=0, length=100, fill='█'):
    """
    terminal progress bar
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (value / float(total)))
    filled_length = int(length * value // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="")
    return


# Definition of object which should be milled by FIB
def MillStairs(session, x, y, width, height, depth, angle, label):
    # settings of one layer, single view/write field using one set of conditions for milling of objects
    layerSettings = IEtching(False, 55e-6, 10e-9, 50e-9, 4.7e-10, 1e-6, DBAccuracy.Fine, 1, True)
    layer = Layer(label, layerSettings)
    layer.addRectangleStairs(x, y, depth, width, height, angle, DBDepthUnit.Meter, 1, 1, ScanningPath.ZigZag)
    session.DrawBeam.LoadLayer(layer)
    session.DrawBeam.Start()
    session.Progress.Show("DrawBeam", label + " milling", False, False, 0, 100)
    while True:
        status = session.DrawBeam.GetStatus()
        running = status[0] == DBStatus.ProjectLoadedExpositionInProgress or status[0] == DBStatus.ProjectLoadedExpositionPaused
        if running:
            progress = 0
            if status[1] > 0:
                progress = min(100, status[2] / status[1] * 100)
            printProgressBar(progress, 100)
            session.Progress.SetPercents(progress)
            time.sleep(1)
        else:
            if status[0] == DBStatus.ProjectLoadedExpositionIdle:
                printProgressBar(100, 100, suffix='Finished')
                print('')
            break
    session.DrawBeam.UnloadLayer()
    print("Trench done")
    return


def testWrite(session, x, y, width, height, depth, angle, label):
    # settings of one layer, single view/write field using one set of conditions for milling of objects
    layerSettings = IEtching(False, 55e-6, 10e-9, 50e-9, 4.7e-10, 1e-6, DBAccuracy.Fine, 1, True)
    layer = Layer(label, layerSettings)
    layer.addRectangleStairs(x, y, depth, width, height, angle, DBDepthUnit.Meter, 1, 1, ScanningPath.ZigZag)
    xml=layer.toXml()
    return(layer,xml)

#def main():
# check that we use compatible Automation SDK version
Automation.VersionCheck("3.2.6")

session = Automation("localhost")
###########################################################################

# Turn FIB Beam on:
fib_status = session.FIB.Beam.GetStatus()
if fib_status == FIBStatus.BeamOff:
    print("FIB is being turned on")
    session.FIB.Beam.On()
print("FIB On")

# Activation of preset used for FIB milling
session.FIB.Preset.Activate('30 keV; 11 nA')

# Milling execution with definition of object position, dimensions and angle
#MillStairs(session, 0, 0, 20e-6, 20e-6, 1e-6, 0, 'Trench')
layer,xml=testWrite(session, 0, 0, 20e-6, 20e-6, 1e-6, 0, 'Trench')
#print(xml.save(r'D:\sklumpe\SerialFIB\bla.xml'))
print('All is done, script ends')

    ###########################################################################
    #return


#if __name__ == '__main__':
#    main()
