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


session = Automation("localhost")
beamCurrent=session.FIB.Beam.ReadProbeCurrent()

print(beamCurrent)