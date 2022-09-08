#### FIB SEM Aquilos Driver ####
'''
################################################################
#                         SerialFIB                            #
#                                                              #
#            Sven Klumpe, Sara Goetz, Herman Fung              #
#                                                              #
#                  Julia Mahamid, Jürgen Plitzko               #
#                                                              #
#             Max-Planck-Institute for Biochemistry            #
#                    Martinsried, Germany                      #
#                                                              #
#             European Molecular Biology Laboratory            #
#                    Heidelberg, Germany                       #
#                                                              #
#                                                              #
#                                                              #
#          if you use SerialFIB in your work, please cite:     #
#                   DOI:                                       #
#                                                              #
#                                                              #
#          SerialFIB: A Developer’s Tool for Automated         #
#                 cryo-FIB Customized Workflows                #
#                                                              #
#     with bug reports, suggestions, etc. please contact:      #
#                   klumpe@biochem.mpg.de                      #
################################################################
'''


#### IMPORT MICROSCOPE
try:
    from autoscript_sdb_microscope_client import SdbMicroscopeClient
    from autoscript_sdb_microscope_client.enumerations import *
    from autoscript_sdb_microscope_client.structures import *
    # Set Up Microscope
    microscope = SdbMicroscopeClient()


    from autoscript_toolkit.template_matchers import * 
    import autoscript_toolkit.vision as vision_toolkit
    from src.custom_matchers_v3 import *
except:
    print("No Autoscript installed")


from src.read_SAV import read_SAV_params
import cv2
import numpy as np
import time
import xml.etree.ElementTree as ET
import os
import datetime
import sys

try:
    microscope.connect()
except:
    print("Couldn't connect to microscope, connecting to localhost")
    try:
        microscope.connect('localhost')
    except:
        print("Loading Testimages")


class fibsem:
    def __init__(self):
        '''
        Definition of directories and intrinsic handlers
        '''

        # History for milling actions
        self.history=[]

        # Output
        self.output_dir=''
        self.log_output = ''
        self.lamella_name=''
        self.alignment_img_buffer=None
        self.SAVparamsfile=''

        # Default alignment current
        self.alignment_current = float(1e-11)
        self.trench_offset = 4e-06
        # Variable for stopping operation
        self.continuerun = True
        
        self.GIS=None
        microscope.specimen.stage.set_default_coordinate_system('Raw')

    def define_output_dir(self,directory):
        '''
        Input: directory as string
		Output: None
		Action: defines output directory
        '''
        self.output_dir=directory+'/'
        return()
    def stop(self):
        '''
        Input: None
        Ouput: None
        Action: Stop operation by setting class variable "continuerun"
        '''
        self.continuerun=False
        return()
    def define_SAVparams_file(self,file):
        '''
        Input: File path as string
        Output: None
        Action: changing class variable "SAVparamsfile" for Volume Imaging runs
        '''
        self.SAVparamsfile=file
        return()
    def stop_patterning(self):
        '''
        Input: None
        Output: None
        Action: stop patterning if it is running
        '''
        if microscope.patterning.state=="Running":
            microscope.patterning.stop()
    def disconnect(self):
        '''
        Input: None
        Output: None
        Action: Disconnect AutoScript4 server
        '''
        microscope.disconnect()
    def connect(self):
        '''
        Input: None
        Output: None
        Action: Connect AutoScript4 server
        '''
        microscope.connect()

    def is_idle(self):
        '''
        Input: None
        Output: Returns True if microscope is idle, returns false if microscope is milling
        Action: None
        '''
        if microscope.patterning.state==PatterningState.IDLE:
            return(True)
        else:
            return(False)

    def get_current(self):
        '''
        Input: None
        Output: Returns the current ion beam current as float
        Action: None
        '''
        try:
            return(float(microscope.beams.ion_beam.beam_current.value))
        except:
            print("No microscope connected.")

    def insert_GIS(self):
        '''
        Input: None
        Output: None
        Action: Insert GIS Needle. Initialize if needed.
        '''
        if self.GIS==None:
            #port_list=microscope.gas.get_gis_port('Pt dep')
            
            #self.GIS=port_list['Pt dep']
            self.GIS=microscope.gas.get_gis_port('Pt dep')
        #microscope.
        else:
            print('GIS has been initialized previously.')
        self.GIS.insert()
        return()

    def retract_GIS(self):
        '''
        Input: None
        Output: None
        Action: Retract GIS Needle. Initialize if needed.
        '''
        if self.GIS==None:
            self.GIS=microscope.gas.get_gis_port('Pt dep')
            #self.GIS=port_list['Pt dep']
        #microscope.
        else:
            print('GIS has been initialized previously.')
        self.GIS.retract()
        return()
    
    def open_GIS(self,runtime):
        #start_time=time.time()
        #current_time=time.time()
        #diff=current_time-start_time
        #while diff<runtime:
        #    print(diff)
        #    diff=current_time-start_time
        #    current_time=time.time()
        if self.GIS==None:
            self.GIS=microscope.gas.get_gis_port('Pt dep')
        else:
            print('GIS has been initialized previously.')
        
        
        self.GIS.turn_heater_on()
        time.sleep(10)
        
        
        self.GIS.open()
        x=time.time()
        while True:
            y=time.time()
            if float(y)-float(x) < runtime:
                time.sleep(0.5)  # sec
                print(float(y)-float(x))
            else:
                self.GIS.close()
                self.GIS.turn_heater_off()
                print('Sample has been GISed for '+str(runtime)+' seconds.')
                return()
    def ion_on(self):
        microscope.beams.ion_beam.turn_on()
        return()
    def electron_on(self):
        microscope.beams.electron_beam.turn_on()
        return()
    
    def setIonHFW(self,value=104):
        microscope.beams.ion_beam.horizontal_field_width.value=value*1e-06
        return()
    def link_stage(self):
        microscope.specimen.stage.link()
        return()
    def unlink_stage(self):
        microscope.specimen.stage.unlink()
        return()
    def take_image_IB(self):
        '''
        Input: None
        Output: AdornedImage
        Action: Take IB image with standard parameters
        '''
        try:
            # Set view to electron beam
            microscope.imaging.set_active_view(2)


            #Check if EB is on, Turn on EB if not the case
            if microscope.beams.ion_beam.is_blanked:
                print("Ion beam blanked ")
                microscope.beams.ion_beam.turn_on()
            else:
                print("Ion beam turned on")
                



            # Aquire Snapshot in EB window
            print("Acquiring IB snapshot")
            framesettings = GrabFrameSettings(bit_depth=8)
            img = microscope.imaging.grab_frame(framesettings)
            array = img.data


            #microscope.beams.electron_beam.turn_off()
            #print("Electron beam turned off")
            return(img)
        except:
            print("ERROR: No Microscope connected")
        return()
    def take_image_EB(self):
        '''
        Input: None
        Output: Image as numpy array
        Action: Take EB image with standard parameters
        '''
        try:
            # Set view to electron beam
            microscope.imaging.set_active_view(1)


            #Check if EB is on, Turn on EB if not the case
            if microscope.beams.electron_beam.is_blanked:
                print("Ion beam blanked ")
            else:
                print("Electron beam turned on")
                microscope.beams.electron_beam.turn_on()



            # Aquire Snapshot in EB window
            print("Acquiring EB snapshot")
            img = microscope.imaging.grab_frame()
            array = img.data


            return(img)
        except:
            print("ERROR: No Microscope connected")
        return()

    def take_image_EB_SAV(self):
        '''
        Input: None
        Output: list of images as numpy array depending on amount of active Detectors in Quadrants (ETD, T1, T2)
        Action: Take EB image with defined parameters from SAVparamsfile
        '''

        try:
            # Set view to electron beam
            microscope.imaging.set_active_view(1)

            # Read parameters from defined SAVparams file
            paramsfile=self.SAVparamsfile
            params = read_SAV_params(paramsfile)
            res=params['Resolution']
            dwell=float(params['DwellTime'])
            LI=int(params['LineIntegration'])






            # Aquire Snapshot in EB window
            print("Acquiring EB snapshot")
            images = microscope.imaging.grab_multiple_frames(GrabFrameSettings(dwell_time=dwell,resolution=res,line_integration=LI))
            array = images[0].data


            return(images)
        except:
            print("ERROR: No Microscope connected or no active detector in quadrants")
            return()

    def getStagePosition(self):
        '''
        Input: None
        Output: current stageposition as directory
        Action: None
        '''

        #### Microscope dependent code ####
        try:
            stageposition=microscope.specimen.stage.current_position
        except:
            stageposition=StagePosition(x=0,y=0,z=0,r=0,t=0)
        x=stageposition.x
        y=stageposition.y
        z=stageposition.z
        r=stageposition.r
        t=stageposition.t
        

        #### Microscope independent code####
        stage_dict={'x':float(x),'y':float(y),'z':float(z),'r':float(r),'t':float(t)}
        return(stage_dict)
    def moveStageAbsolute(self, stageposition):
        '''
        Input: Stage position as dictionnary
        Output: None
        Action: Move stage to provided stage position
        '''
        ### Microscope Independet Code ###
        x=float(stageposition['x'])
        y=float(stageposition['y'])
        z=float(stageposition['z'])
        r=float(stageposition['r'])
        t=float(stageposition['t'])
        #print(x,y,z,r,t)
        

        ### Microscope Dependent Code ###
        stagepos=StagePosition(x=x,y=y,z=z,t=t,r=r)
        microscope.specimen.stage.absolute_move(stagepos)
        return()
    def moveStageRelative(self,stageposition):
        '''
        Input: Change in stage position as directory
        Output: None
        Action: Move stage relative to previous position by given parameters
        '''
        ### Microscope Independet Code ###
        x=float(stageposition['x'])
        y=float(stageposition['y'])
        z=float(stageposition['z'])
        r=float(stageposition['r'])
        t=float(stageposition['t'])

        ### Microscope Dependent Code ###
        stagepos=StagePosition(x=x,y=y,z=z,t=t,r=r)
        microscope.specimen.stage.relative_move(stagepos)
        return("Stage Moved")
    def print_stage_rot(self):
        print(microscope.beams.ion_beam.scanning.rotation.value)
        return None


    def align(self,image,beam,current=1.0e-11):
        '''
        Input: Alignment image, Beam ("ION" or "ELECTRON"), optionally current but replaced by the GUI option
        Output: None
        Action: Align the stage and beam shift to the reference image at the current stage position
        '''
        current=self.alignment_current


        try:
            if beam=='ION':
                print('Running alignment')
                microscope.imaging.set_active_view(2)

                # Get old resolution of images to go back after alignment
                old_resolution=microscope.beams.ion_beam.scanning.resolution.value
                old_mag=microscope.beams.ion_beam.horizontal_field_width.value

                # Get resolution of reference image and set microscope to given HFW
                img_resolution=str(np.shape(image.data)[1])+'x'+str(np.shape(image.data)[0])
                microscope.beams.ion_beam.scanning.resolution.value=img_resolution
                microscope.beams.ion_beam.beam_current.value=current
                beam_current_string=str(microscope.beams.ion_beam.beam_current.value)


                # Get HFW from Image

                # Run auto contrast brightness and reset beam shift. Take an image as reference for alignment
                microscope.beams.ion_beam.horizontal_field_width.value=image.metadata.optics.scan_field_of_view.width
                #microscope.beams.ion_beam.horizontal_field_width.value =
                microscope.auto_functions.run_auto_cb()
                microscope.beams.ion_beam.beam_shift.value=Point(0,0)
                current_img=self.take_image_IB()


                # Load Matcher function and locate feature
                #favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
                favourite_matcher = CustomCVMatcher('phase')
                l = vision_toolkit.locate_feature(current_img, image, favourite_matcher)
                print("Current confidence: " + str(l.confidence))
                self.log_output=self.log_output+"Step Clarification: Initial Alignment after Stage move \n"
                self.log_output=self.log_output+"Current confidence: " + str(l.confidence)+'\n'


                # Start movements and log images
                move_count = 0

                now = datetime.datetime.now()
                current_img.save(self.output_dir + self.lamella_name+'_out/'+now.strftime("%Y-%m-%d_%H_%M_%S_")+self.lamella_name +'_'+ beam_current_string + '_first_move_'+str(move_count)+'.tif')
                self.log_output=self.log_output+"Saved Image as : "+self.output_dir + self.lamella_name+'_out/'+now.strftime("%Y-%m-%d_%H_%M_%S_")+self.lamella_name +'_'+ beam_current_string + '_first_move_'+str(move_count)+'.tif'+'\n'

                # If cross correlation metric too low, continue movements for maximum 3 steps
                while l.confidence < 0.98 and move_count < 3:
                    self.log_output = self.log_output + "Move Count =" + str(move_count) + '\n'
                    x = l.center_in_meters.x * -1 # sign may need to be flipped depending on matcher
                    y = l.center_in_meters.y * -1
                    distance = np.sqrt(x ** 2 + y ** 2)
                    print("Deviation (in meters): " + str(distance))
                    self.log_output = self.log_output + "Deviation (in meters): " + str(distance) + '\n'


                    # If distance, meaning offset between images low enough, stop.
                    if distance < 82.9e-06/3072/2:
                        break
                    elif distance > 1e-05:
                        # move stage and reset beam shift
                        print("Moving stage by ("+str(x)+","+str(y)+") and resetting beam shift...")
                        self.log_output = self.log_output + "Moving stage by ("+str(x)+","+str(y)+") and resetting beam shift... \n"
                        rotation=microscope.beams.ion_beam.scanning.rotation.value
                        print(rotation)
                        possible_rotations=[0,3.14]
                        #print(min(possible_rotations, key=lambda x: abs(x - rotation)))

                        if rotation==0:

                            pos_corr = StagePosition(coordinate_system='Specimen', x=-x, y=-y)

                            print('Rotation is zero')
                        else:
                            pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
                            print('Rotation is NOT zero')
                        microscope.specimen.stage.relative_move(pos_corr)
                        microscope.beams.ion_beam.beam_shift.value = Point(0,0)

                    else:
                        # apply (additional) beam shift
                        print("Shifting beam by ("+str(x)+","+str(y)+")...")
                        self.log_output = self.log_output + "Shifting beam by ("+str(x)+","+str(y)+")... \n"
                        print(microscope.beams.ion_beam.beam_shift.value)
                        microscope.beams.ion_beam.beam_shift.value += Point(x,y) # incremental

                    move_count += 1

                    current_img = self.take_image_IB()
                    now = datetime.datetime.now()
                    current_img.save(self.output_dir+ self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_") + self.lamella_name +'_'+ beam_current_string + '_first_move_' + str(move_count)+'.tif')

                    self.log_output = self.log_output + "Saved Image as : " +self.output_dir+ self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_") + self.lamella_name +'_'+ beam_current_string + '_first_move_' + str(move_count)+'.tif'+'\n'
                    l = vision_toolkit.locate_feature(current_img, image, favourite_matcher)
                    print("Current confidence: " + str(l.confidence))
                    self.log_output = self.log_output + "Current confidence: " + str(l.confidence) + '\n'

                # Go back to old resolution
                microscope.beams.ion_beam.scanning.resolution.value = old_resolution
                microscope.beams.ion_beam.horizontal_field_width.value = old_mag

                self.alignment_img_buffer = current_img
                print("Done.")



            if beam=="ELECTRON":
                # Same as above, just for alignment in SEM imaging
                print('Running alignment')
                microscope.imaging.set_active_view(1)
                old_resolution = microscope.beams.electron_beam.scanning.resolution.value
                old_mag = microscope.beams.electron_beam.horizontal_field_width.value

                img_resolution = str(np.shape(image.data)[1]) + 'x' + str(np.shape(image.data)[0])
                microscope.beams.electron_beam.scanning.resolution.value = img_resolution
                microscope.beams.electron_beam.horizontal_field_width.value = image.metadata.optics.scan_field_of_view.width
                microscope.beams.electron_beam.beam_shift.value = Point(0, 0)

                current_img = self.take_image_EB()


                favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
                l = vision_toolkit.locate_feature(current_img, image, favourite_matcher)
                print("Current confidence: " + str(l.confidence))
                move_count = 0

                while l.confidence < 0.98 and move_count < 1:
                    x = l.center_in_meters.x * -1  # sign may need to be flipped depending on matcher
                    y = l.center_in_meters.y * -1
                    distance = np.sqrt(x ** 2 + y ** 2)
                    print("Deviation (in meters): " + str(distance))


                    if distance > 1e-05:
                        # move stage and reset beam shift
                        print("Moving stage by ("+str(x)+","+str(y)+") and resetting beam shift...")
                        #self.log_output = self.log_output + "Moving stage by ("+str(x)+","+str(y)+") and resetting beam shift... \n"

                        rotation = microscope.beams.electron_beam.scanning.rotation.value
                        possible_rotations = [0, 3.14]
                        num=min(possible_rotations, key=lambda x: abs(x - rotation))
                        print(num)
                        if num==0:
                            pos_corr = StagePosition(coordinate_system='Specimen', x=-x, y=-y)
                        else:
                            pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
                        #pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
                        microscope.specimen.stage.relative_move(pos_corr)
                        microscope.beams.electron_beam.beam_shift.value = Point(0,0)

                    else:
                        # apply (additional) beam shift
                        print("Shifting beam by ("+str(x)+","+str(y)+")")
                        #self.log_output = self.log_output + "Shifting beam by ("+str(x)+","+str(y)+")... \n"
                        print(microscope.beams.electron_beam.beam_shift.value)
                        microscope.beams.electron_beam.beam_shift.value += Point(x,y) # incremental

                    move_count += 1
                    current_img = self.take_image_EB()
                    l = vision_toolkit.locate_feature(current_img, image, favourite_matcher)
                microscope.beams.electron_beam.scanning.resolution.value = old_resolution
                microscope.beams.electron_beam.horizontal_field_width.value = old_mag
                #self.alignment_img_buffer = current_img

        except:
            if beam == 'ION':
                print('Running alignment')
                microscope.imaging.set_active_view(2)
                old_resolution = microscope.beams.ion_beam.scanning.resolution.value
                old_mag = microscope.beams.ion_beam.horizontal_field_width.value

                # microscope.beams.ion_beam.scanning.resolution.value='768x512'
                img_resolution = str(np.shape(image.data)[1]) + 'x' + str(np.shape(image.data)[0])
                microscope.beams.ion_beam.scanning.resolution.value = img_resolution
                microscope.beams.ion_beam.beam_current.value = current

                # Get HFW from Image

                microscope.beams.ion_beam.horizontal_field_width.value = image.metadata.optics.scan_field_of_view.width
                microscope.auto_functions.run_auto_cb()
                microscope.beams.ion_beam.beam_shift.value = Point(0, 0)
                current_img = self.take_image_IB()


                #favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
                favourite_matcher = CustomCVMatcher('phase')
                l = vision_toolkit.locate_feature(current_img, image, favourite_matcher)
                print("Current confidence: " + str(l.confidence))

                self.log_output = self.log_output + "Step Clarification: Initial Alignment after Stage move \n"
                self.log_output = self.log_output + "Current confidence: " + str(l.confidence) + '\n'

                move_count = 0

                while l.confidence < 0.98 and move_count < 3:
                    self.log_output = self.log_output + "Move Count =" + str(move_count) + '\n'
                    x = l.center_in_meters.x * -1  # sign may need to be flipped depending on matcher
                    y = l.center_in_meters.y * -1
                    distance = np.sqrt(x ** 2 + y ** 2)
                    print("Deviation (in meters): " + str(distance))
                    self.log_output = self.log_output + "Deviation (in meters): " + str(distance) + '\n'

                    if distance < 82.9e-06 / 3072 / 2:
                        break
                    elif distance > 1e-05:
                        # move stage and reset beam shift
                        print("Moving stage by (" + str(x) + "," + str(y) + ") and resetting beam shift...")
                        self.log_output = self.log_output + "Moving stage by (" + str(x) + "," + str(
                            y) + ") and resetting beam shift... \n"
                        #pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)

                        rotation = microscope.beams.ion_beam.scanning.rotation.value
                        print(rotation)
                        possible_rotations = [0, 3.14]
                        #pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
                        if rotation==0:
                            pos_corr = StagePosition(coordinate_system='Specimen', x=-x, y=-y)
                            print('Rotation is zero')
                        else:
                            pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
                            print('Rotation is NOT zero')
                        microscope.specimen.stage.relative_move(pos_corr)
                        microscope.beams.ion_beam.beam_shift.value = Point(0, 0)

                    else:
                        # apply (additional) beam shift
                        print("Shifting beam by (" + str(x) + "," + str(y) + ")...")
                        self.log_output = self.log_output + "Shifting beam by (" + str(x) + "," + str(y) + ")... \n"
                        print(microscope.beams.ion_beam.beam_shift.value)
                        microscope.beams.ion_beam.beam_shift.value += Point(x, y)  # incremental

                    move_count += 1

                    current_img = self.take_image_IB()
                    l = vision_toolkit.locate_feature(current_img, image, favourite_matcher)
                    print("Current confidence: " + str(l.confidence))
                    self.log_output = self.log_output + "Current confidence: " + str(l.confidence) + '\n'
                microscope.beams.ion_beam.scanning.resolution.value = old_resolution
                microscope.beams.ion_beam.horizontal_field_width.value = old_mag

                print("Done.")

            if beam=="ELECTRON":
                #print("Not implemented yet")
                print('Running alignment')
                microscope.imaging.set_active_view(1)
                old_resolution = microscope.beams.electron_beam.scanning.resolution.value
                old_mag = microscope.beams.electron_beam.horizontal_field_width.value

                img_resolution = str(np.shape(image.data)[1]) + 'x' + str(np.shape(image.data)[0])
                microscope.beams.electron_beam.scanning.resolution.value = img_resolution
                microscope.beams.electron_beam.horizontal_field_width.value = image.metadata.optics.scan_field_of_view.width
                microscope.beams.electron_beam.beam_shift.value = Point(0, 0)

                current_img = self.take_image_EB()

                favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
                l = vision_toolkit.locate_feature(current_img, image, favourite_matcher)
                print("Current confidence: " + str(l.confidence))
                move_count = 0

                while l.confidence < 0.98 and move_count < 1:
                    x = l.center_in_meters.x * -1  # sign may need to be flipped depending on matcher
                    y = l.center_in_meters.y * -1
                    distance = np.sqrt(x ** 2 + y ** 2)
                    print("Deviation (in meters): " + str(distance))


                    if distance > 1e-05:
                        # move stage and reset beam shift
                        print("Moving stage by ("+str(x)+","+str(y)+") and resetting beam shift...")
                        #self.log_output = self.log_output + "Moving stage by ("+str(x)+","+str(y)+") and resetting beam shift... \n"
                        #pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
                        if num==0:
                            pos_corr = StagePosition(coordinate_system='Specimen', x=-x, y=-y)
                        if num==3.14:
                            pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
                        microscope.specimen.stage.relative_move(pos_corr)
                        microscope.beams.electron_beam.beam_shift.value = Point(0,0)

                    else:
                        # apply (additional) beam shift
                        print("Shifting beam by ("+str(x)+","+str(y)+")...")
                        #self.log_output = self.log_output + "Shifting beam by ("+str(x)+","+str(y)+")... \n"
                        print(microscope.beams.electron_beam.beam_shift.value)
                        microscope.beams.electron_beam.beam_shift.value += Point(x,y) # incremental
                        if num==0:
                            microscope.beams.electron_beam.beam_shift.value += Point(-x, -y)  # incremental
                        if num==3.14:
                            microscope.beams.electron_beam.beam_shift.value += Point(x, y)  # incremental

                    move_count += 1
                    current_img = self.take_image_EB()
                    l = vision_toolkit.locate_feature(current_img, image, favourite_matcher)
                microscope.beams.electron_beam.scanning.resolution.value = old_resolution
                microscope.beams.electron_beam.horizontal_field_width.value = old_mag

        return()

    def align_current(self,new_current,beam='ION'):
        '''
        Input: Current to change towards, beam (currently "ION" only)
        Output: None
        Action: Take a reference image at the old current, change current and align to that reference image
        '''
        if beam=="ION":
            microscope.imaging.set_active_view(2)
            #pos1=microscope.specimen.stage.current_position
            microscope.auto_functions.run_auto_cb()
            beam_current_string = str(microscope.beams.ion_beam.beam_current.value)
            ref_img=self.take_image_IB()
            now = datetime.datetime.now()
            try:
                ref_img.save(self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name + '_' + beam_current_string + '_align_current_refimg' + '.tif')
                self.log_output=self.log_output+"Saved Image as : " + self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name + '_' + beam_current_string + '_align_current_refimg' + '.tif'+'\n'
            except:
                print("Run in Scripting Mode")
            microscope.beams.ion_beam.beam_current.value = new_current
            microscope.beams.ion_beam.scanning.dwell_time.value=200e-09
            microscope.beams.ion_beam.scanning.resolution.value = '768x512'
            microscope.auto_functions.run_auto_cb()
            current_img=microscope.imaging.grab_frame()


            move_count = 0
            now = datetime.datetime.now()
            try:
                current_img.save(self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name  + '_'+ beam_current_string +  '_align_current_' + str(move_count)+'.tif')
                self.log_output = self.log_output + "Saved Image as : " + self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name  + '_'+ beam_current_string +  '_align_current_' + str(move_count)+'.tif'+'\n'
            except:
                pass

            favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
            l = vision_toolkit.locate_feature(current_img, ref_img, favourite_matcher)
            
            print("Current confidence: " + str(l.confidence))

            self.log_output = self.log_output + "Step Clarification: Current Alignment \n"
            self.log_output = self.log_output + "Current confidence: " + str(l.confidence) + '\n'


            while l.confidence < 0.999 and move_count < 3:
                self.log_output = self.log_output + "Move Count =" +str(move_count) +'\n'
                x = l.center_in_meters.x * -1
                y = l.center_in_meters.y * -1
                distance = np.sqrt(x ** 2 + y ** 2)

                
                print("Deviation (in meters): " + str(distance))
                self.log_output = self.log_output + "Deviation (in meters): " + str(distance) + '\n'
                if distance < 82.9e-06/768/2:
                    break
                elif distance < 1e-05:
                    print("Shifting beam by ("+str(x)+","+str(y)+")...")
                    self.log_output = self.log_output + "Shifting beam by (" + str(x) + "," + str(y) + ")... \n"
                    microscope.beams.ion_beam.beam_shift.value += Point(x,y)
                    move_count += 1
                    current_img = self.take_image_IB()
                    now = datetime.datetime.now()
                    try:
                        current_img.save(self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name + '_'+ beam_current_string + '_align_current_' + str(move_count)+'.tif')
                        self.log_output = self.log_output + "Saved Image as : " + self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name + '_'+ beam_current_string + '_align_current_' + str(move_count)+'.tif'+'\n'
                    except:
                        pass
                    l = vision_toolkit.locate_feature(current_img, ref_img, favourite_matcher)
                    print("Current confidence: " + str(l.confidence))
                    self.log_output = self.log_output + "Current confidence: " + str(l.confidence) + '\n'
                else:
                    print("Distance is greater than 10 microns. Abort.")
                    self.log_output = self.log_output + "Distance is greater than 10 microns. Abort.\n"
                    break
            microscope.auto_functions.run_auto_cb()



        return()



    def auto_focus(self,beam="ELECTRON"):
        '''
        Input: Beam , currently only "ELECTRON" as autofocus in ION is damaging (also on a smaller sacrifice area...)
        Output: None
        Action: Autofocus function from the xT server
        '''
        active_view=microscope.imaging.get_active_view()
        if beam=="ELECTRON":
            microscope.imaging.set_active_view(1)
        else:
            microscope.imaging.set_active_view(2)
        microscope.auto_functions.run_auto_focus()
        microscope.imaging.set_active_view(active_view)
        return()


    def create_pattern(self,x,y,h,w,d=10e-06):
        '''
        Input: Center in X,Y of the pattern; Width(w), Height(h), and optionally Depth (d) of the Pattern
        Output: Pattern as AutoScript4 object
        Action: Draws a rectangular pattern within the xT Server given the parameters
        '''
        
        inp_center_x=x
        inp_center_y=y
        inp_depth=d
        inp_height=h
        inp_width=w
        microscope.imaging.set_active_view(2)
        pattern=microscope.patterning.create_rectangle(center_x=inp_center_x, center_y=inp_center_y,depth=inp_depth,height=inp_height,width=inp_width)
        return(pattern)

    def pattern_parser(self,directory,filename):
        '''
        Input: Directory path as string and filename of xT pattern file as string
        Output: Pattern as AutoScript4 object
        Action: Draws pattern from file in xT GUI
        '''
        tree = ET.parse(directory+filename)
        root = tree.getroot()

        for element in root:
            if element.tag == 'PatternRectangle':
                inp_pattern_type='Rectangle'
                inp_center_x = float(element.find('CenterX').text)
                inp_center_y = float(element.find('CenterY').text)
                inp_depth = float(element.find('Depth').text)
                inp_height = float(element.find('Length').text)
                inp_width = float(element.find('Width').text)
                inp_scan_direction = str(element.find('ScanDirection').text)
                inp_dwell_time=float(element.find('DwellTime').text)

            if element.tag == 'PatternRegularCrossSection':
                inp_pattern_type='RegularCrossSection'
                inp_center_x = float(element.find('CenterX').text)
                inp_center_y = float(element.find('CenterY').text)
                inp_depth = float(element.find('Depth').text)
                inp_height = float(element.find('Length').text)
                inp_width = float(element.find('Width').text)
                inp_scan_direction = str(element.find('ScanDirection').text)
                inp_dwell_time=float(element.find('DwellTime').text)

            if element.tag == 'PatternCleaningCrossSection':
                inp_pattern_type='CleaningCrossSection'
                inp_center_x = float(element.find('CenterX').text)
                inp_center_y = float(element.find('CenterY').text)
                inp_depth = float(element.find('Depth').text)
                inp_height = float(element.find('Length').text)
                inp_width = float(element.find('Width').text)
                inp_scan_direction = str(element.find('ScanDirection').text)
                inp_dwell_time=float(element.find('DwellTime').text)

        if inp_pattern_type=='Rectangle':
            pattern=microscope.patterning.create_rectangle(center_x=inp_center_x, center_y=inp_center_y,depth=inp_depth,height=inp_height,width=inp_width)
        elif inp_pattern_type=='CleaningCrossSection':
            pattern = microscope.patterning.create_cleaning_cross_section(center_x=inp_center_x, center_y=inp_center_y, depth=inp_depth, height=inp_height, width=inp_width)
        elif inp_pattern_type=='RegularCrossSection':
            pattern=microscope.patterning.create_regular_cross_section(center_x=inp_center_x, center_y=inp_center_y, depth=inp_depth, height=inp_height, width=inp_width)


        pattern.dwell_time=inp_dwell_time
        if inp_scan_direction=='BottomToTop':
            pattern.scan_direction = PatternScanDirection.BOTTOM_TO_TOP
        elif inp_scan_direction=='TopToBottom':
            pattern.scan_direction = PatternScanDirection.TOP_TO_BOTTOM
        elif inp_scan_direction=='LeftToRight':
            pattern.scan_direction = PatternScanDirection.LEFT_TO_RIGHT
        elif inp_scan_direction=='RightToLeft':
            pattern.scan_direction = PatternScanDirection.RIGHT_TO_LEFT
        else:
            print("!!! CATION !!! \n Could not recognize ScanDirection of pattern \n !!! CAUTION !!!")
        return(pattern)
    def pattern_directory_parser(self,directory):
        '''
        Input: Directory path as string
        Output: Patterns as list of AutoScript4 "pattern" objects
        Action: Draws and returns all patterns within a directory
        '''
        directory_content = os.listdir(directory)
        rectangle_list={}
        for filename in directory_content:
            tree = ET.parse(directory+filename)
            root = tree.getroot()
            if len(root)>2:
                print("File "+filename+ "has multiple patterns defined. Please double-check!")
            else:
                for element in root:
                    if element.tag == 'PatternRectangle':
                        inp_center_x = float(element.find('CenterX').text)
                        inp_center_y = float(element.find('CenterY').text)
                        inp_depth = float(element.find('Depth').text)
                        inp_height = float(element.find('Length').text)
                        inp_width = float(element.find('Width').text)
                rectangle=[inp_center_x, inp_center_y,inp_depth,inp_height,inp_width]
                rectangle_list.update({filename[:-4]:rectangle})
        return(rectangle_list)

    def save_pattern(self,directory,filename,Pattern):
        '''
        Input: Directory path as string, output filename as string, Pattern as AutoScript4 Pattern object
        Output: None
        Action: Writes pattern as xT xml given the AutoScript Pattern object's parameters
        '''
        scan_type=Pattern.__class__.__name__
        if scan_type=="CleaningCrossSectionPattern":
            name_tag='Pattern'+scan_type[:-7]
            dummy_pattern=r"./TemplatePatterns/clean_cross.ptf"
        elif scan_type=="RegularCrossSectionPattern":
            name_tag='Pattern'+scan_type[:-7]
            dummy_pattern=r"./TemplatePatterns/cross.ptf"
        else:
            name_tag="PatternRectangle"
            dummy_pattern=r"./TemplatePatterns/regular.ptf"


        tree = ET.parse(dummy_pattern)
        root = tree.getroot()

        CenterX=Pattern.center_x
        CenterY=Pattern.center_y
        Depth=Pattern.depth
        Length=Pattern.height
        Width=Pattern.width
        ScanDirection=Pattern.scan_direction
        
        for element in root:
            if element.tag == name_tag:
                element.find('CenterX').text=str(CenterX)
                element.find('CenterY').text=str(CenterY)
                print(Depth)
                element.find('Depth').text=str(Depth)
                element.find('Length').text=str(Length)
                element.find('Width').text=str(Width)
                element.find('ScanDirection').text=str(ScanDirection)
        try:
            tree.write(directory+filename)
        except:
            print("Files already exist! Please check InputDir")

        return()

    def auto_cb(self):
        '''
        Input: None
        Output: None
        Action: runs auto contrast brightness
        '''
        microscope.auto_functions.run_auto_cb()
        return()


    def create_trench_patterns(self,directory,pattern_lamella,pattern_above,pattern_below):
        '''
        Input: Directory containing the user input from the SerialFIB GUI as xT patterns
        Output: AutoScript4 "pattern" objects for trench milling
        Action: None
        '''
        pattern_above = self.pattern_parser(directory, pattern_above)
        start_position_above = pattern_above.center_y + 0.5 * pattern_above.height
        pattern_below = self.pattern_parser(directory, pattern_below)
        start_position_below = pattern_below.center_y - 0.5 * pattern_below.height
        pattern_lamella = self.pattern_parser(directory, pattern_lamella)
        lamella_center_x = pattern_lamella.center_x
        lamella_center_y = pattern_lamella.center_y
        width_lamella = pattern_lamella.width
        top_center_y=pattern_above.center_y
        bottom_center_y=pattern_below.center_y
        height=abs(top_center_y-bottom_center_y)

        left_trench_x=lamella_center_x+0.5*width_lamella+self.trench_offset
        right_trench_x=lamella_center_x-(0.5*width_lamella+self.trench_offset)
        width = 1e-06
        pattern_left = microscope.patterning.create_rectangle(center_x=left_trench_x, center_y=lamella_center_y, depth=10e-06,
                                                                width=width, height=height)
        pattern_right = microscope.patterning.create_rectangle(center_x=right_trench_x, center_y=lamella_center_y,
                                                              depth=10e-06,
                                                              width=width, height=height)



        return (pattern_left, pattern_right)




    def run_trench_milling(self,lamella_name,alignment_image,stagepos,pattern_ref_directory):
        '''
        Input: Lamella Name from positions list, Alignment image as Numpy array,
                stageposition as dictionary, Directory of the patterns defined through the SerialFIB GUI
        Output: log for printing
        Action: Runs the trench milling for the provided position
        '''

        patterns_reference_directory = pattern_ref_directory
        patterns_output_directory = pattern_ref_directory[:-1] + '_out/'
        try:
            os.mkdir(patterns_output_directory)
        except:
            self.log_output = self.log_output + "Pattern Directory already existed!!!" + '\n'
        self.lamella_name = lamella_name
        pattern_left,pattern_right=self.create_trench_patterns(patterns_reference_directory,str(lamella_name)+'_lamella.ptf',str(lamella_name)+'_tp.ptf',str(lamella_name)+'_bp.ptf')

        pattern_left_name = lamella_name + str('_trench_left.ptf')
        pattern_right_name = lamella_name + str('_trench_right.ptf')
        self.save_pattern(patterns_output_directory, pattern_left_name, pattern_left)
        self.save_pattern(patterns_output_directory, pattern_right_name, pattern_right)

        self.moveStageAbsolute(stagepos)

        ref_img = alignment_image
        ref_img.save(patterns_output_directory[:-1] + '/before_trenches.tif')
        self.align(ref_img, 'ION')

        self.align_current(new_current=5e-10, beam='ION')


        self.run_milling(patterns_output_directory, pattern_left_name, pattern_right_name,milling_time=60)

        current_img=scope.take_image_IB()
        current_img.save(patterns_output_directory[:-1] + '/after_trenches.tif')
        return(self.log_output)

    def run_milling(self,pattern_dir,tp_filename,bp_filename,milling_time):
        print("Clearing all patterns in the active view...")
        microscope.patterning.clear_patterns()
        print("Creating new rectangle pattern on top...")
        microscope.patterning.set_default_beam_type(BeamType.ION)
        #microscope.patterning.set_default_application_file("Si")
        tp = self.pattern_parser(pattern_dir,tp_filename)
        bp = self.pattern_parser(pattern_dir,bp_filename)
        print("Patterns have been parsed")
        microscope.patterning.mode = 'Parallel'

        print("Set Ion Beam as active")
        microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
        print("Done")

        print("Starting patterning...")
        microscope.patterning.start()
        timestamp=0

        while microscope.patterning.state=="Running":
            if timestamp < milling_time:
                time.sleep(1)  # sec
                timestamp=timestamp+1
            else:
                microscope.patterning.stop()
                return()

        print("Stopping patterning...")
        #microscope.patterning.stop()
        print("Done")
        return()

    def create_custom_protocol(self, directory, pattern_lamella, pattern_above, pattern_below, protocol_filename,mode='fine'):
        '''
        Input: Directory path as string, filename of lamella pattern, and extreme point patterns as string
                protocol file path as string, optionally mode ('rough' or 'fine'). "Rough" takes extreme points into
                account, "fine" does not.
        Output: 3 lists. One for the patterns, one for the beam currents of the steps in the protocol,
                and one for the time variable of the steps in the protocol
        Action: None
        '''
        pattern_above = self.pattern_parser(directory, pattern_above)
        start_position_above = pattern_above.center_y + 0.5 * pattern_above.height
        pattern_below = self.pattern_parser(directory, pattern_below)
        start_position_below = pattern_below.center_y - 0.5 * pattern_below.height
        pattern_lamella = self.pattern_parser(directory, pattern_lamella)
        lamella_center_x = pattern_lamella.center_x
        lamella_center_y = pattern_lamella.center_y
        width_lamella = pattern_lamella.width

        microscope.patterning.clear_patterns()

        from src.makePatterns_LamellaDesigner import make_protocol
        from src.makePatterns_LamellaDesigner import read_protocolfile
        from src.makePatterns_LamellaDesigner import write_protocolfile
        protocolfile_lists=read_protocolfile(protocol_filename)
        for i in protocolfile_lists:
            i.update({'width':width_lamella})
            i.update({'y_center':lamella_center_y})
            i.update({'output_dir':str(self.output_dir)})


        if mode=='rough':
            make_protocol(protocolfile_lists,mode='rough',y_min=start_position_below,y_max=start_position_above)
        else:
            make_protocol(protocolfile_lists)

        filename_from_protocol = str(self.output_dir) + 'patternfile_from_protocol.pf'

        pattern_dict, steps_current, steps_time = self.custom_file_parser(filename_from_protocol)
        step_patterns = []

        for i in pattern_dict:

            patterns = []
            for j in pattern_dict[i]:

                try:
                    IB_Current = j['IB_Current'].split('=')[1]
                    if IB_Current == 0:
                        IB_Current = 1e-11
                except:
                    center_y = lamella_center_y - float(j['Offset_y'])
                    center_x = lamella_center_x + float(j['Offset_x'])
                    height = float(j['Height_y'])
                    if j['Width_x'] == "'Lamella'":
                        width = width_lamella
                    else:
                        width = float(j['Width_x'])

                    try:
                        pattern_type = j['PatternType']
                        if pattern_type == "Cross-Section":
                            pattern = microscope.patterning.create_regular_cross_section(center_x=center_x,
                                                                                         center_y=center_y,
                                                                                         depth=10e-06, width=width,
                                                                                         height=height)
                        elif pattern_type == "Cleaning Cross-Section":
                            pattern = microscope.patterning.create_regular_cross_section(center_x=center_x,
                                                                                         center_y=center_y,
                                                                                         depth=10e-06, width=width,
                                                                                         height=height)
                        else:
                            pattern = microscope.patterning.create_rectangle(center_x=center_x, center_y=center_y,
                                                                             depth=10e-06, width=width,
                                                                             height=height)
                    except:
                        print("No Pattern Type defined")
                        pattern = microscope.patterning.create_rectangle(center_x=center_x, center_y=center_y,
                                                                         depth=10e-06, width=width, height=height)

                    try:
                        if j['ScanDirection'] == "TopToBottom":
                            pattern.scan_direction = PatternScanDirection.TOP_TO_BOTTOM
                        # Rectangle.scan_direction = PatternScanDirection.BOTTOM_TO_TOP
                        elif j['ScanDirection'] == "BottomToTop":
                            pattern.scan_direction = PatternScanDirection.BOTTOM_TO_TOP
                        elif j['ScanDirection'] == "LeftToRight":
                            pattern.scan_direction = PatternScanDirection.LEFT_TO_RIGHT
                        elif j['ScanDirection'] == "RightToLeft":
                            pattern.scan_direction = PatternScanDirection.RIGHT_TO_LEFT
                    except:
                        print("No Scan Direction defined")
                    # pattern1_above.scan_direction = PatternScanDirection.TOP_TO_BOTTOM
                    patterns.append(pattern)
            step_patterns.append(patterns)




        return (step_patterns, steps_current, steps_time)






    def create_custom_patterns(self, directory, pattern_lamella, pattern_above, pattern_below,custom_filename):
        '''
        Input: Directory path as string, filename of lamella pattern, and extreme point patterns as string
                pattern sequence file path as string, custom_filename path as string
        Output: 3 lists. One for the patterns, one for the beam currents of the steps in the protocol,
                and one for the time variable of the steps in the protocol
        Action: None
        '''
        pattern_above = self.pattern_parser(directory, pattern_above)
        start_position_above = pattern_above.center_y + 0.5 * pattern_above.height
        pattern_below = self.pattern_parser(directory, pattern_below)
        start_position_below = pattern_below.center_y - 0.5 * pattern_below.height
        pattern_lamella = self.pattern_parser(directory, pattern_lamella)
        lamella_center_x = pattern_lamella.center_x
        lamella_center_y = pattern_lamella.center_y
        width_lamella = pattern_lamella.width

        microscope.patterning.clear_patterns()

        pattern_dict,steps_current, steps_time=self.custom_file_parser(custom_filename)
        step_patterns=[]
        for i in pattern_dict:

            patterns=[]
            for j in pattern_dict[i]:
                # pattern1_above
                try:
                    IB_Current=j['IB_Current'].split('=')[1]
                    if IB_Current==0:
                        IB_Current=1e-11
                except:
                    center_y = lamella_center_y - float(j['Offset_y'])
                    center_x = lamella_center_x + float(j['Offset_x'])
                    height = float(j['Height_y'])
                    if j['Width_x']=="'Lamella'":
                        width=width_lamella
                    else:
                        width=float(j['Width_x'])



                    try:
                        pattern_type=j['PatternType']
                        if pattern_type=="Cross-Section" :
                            pattern = microscope.patterning.create_regular_cross_section(center_x=center_x, center_y=center_y, depth=10e-06, width=width, height=height)
                        elif pattern_type=="Cleaning Cross-Section":
                            pattern = microscope.patterning.create_regular_cross_section(center_x=center_x,center_y=center_y,depth=10e-06, width=width,height=height)
                        else:
                            pattern = microscope.patterning.create_rectangle(center_x=center_x, center_y=center_y,depth=10e-06, width=width, height=height)
                    except:
                        print("No Pattern Type defined")
                        pattern = microscope.patterning.create_rectangle(center_x=center_x, center_y=center_y, depth=10e-06, width=width, height=height)

                    try:
                        if j['ScanDirection']=="TopToBottom":
                            pattern.scan_direction = PatternScanDirection.TOP_TO_BOTTOM

                        elif j['ScanDirection']=="BottomToTop":
                            pattern.scan_direction = PatternScanDirection.BOTTOM_TO_TOP
                        elif j['ScanDirection']=="LeftToRight":
                            pattern.scan_direction = PatternScanDirection.LEFT_TO_RIGHT
                        elif j['ScanDirection']=="RightToLeft":
                            pattern.scan_direction = PatternScanDirection.RIGHT_TO_LEFT
                    except:
                        print("No Scan Direction defined")

                    patterns.append(pattern)
            step_patterns.append(patterns)





        return(step_patterns,steps_current,steps_time)

    def write_patterns(self,label,patterns,alignment_image,output_dir=' '):
        '''
        Input: Label of the lamella position, List of patterns as AutoScript4 objects, alignment image as numpy array,
                output directory path as string
        Output: None
        Action: Writes the patterns as xT .ptf files
        '''

        if output_dir==' ':
            directory = self.output_dir + '/'
        else:
            directory=output_dir+'/'
        for i in range(0, len(patterns)):
            # print(i)
            #label = self.tableWidget.item(i, 0).text()
            lamella_dir = directory + label + '/'
            try:
                os.mkdir(lamella_dir)
            except:
                print("Directory " + label + " already exists")

            pixel_size = alignment_image.metadata.binary_result.pixel_size.x
            image_shape = np.shape(alignment_image.data)


            if i == None:
                continue
            else:
                try:
                    #patterns = patterns
                    patterns = sorted(patterns, key=lambda pattern: pattern[1])
                    name_list = ['tp', 'lamella', 'bp']
                    num = 0

                    for i in patterns:

                        pattern_filename = str(label) + '_' + str(name_list[num]) + ".ptf"
                        num = num + 1
                        px=i[0]
                        py=i[1]

                        w=i[2]
                        h=i[3]
                        x = (px - image_shape[1] / 2) + h / 2
                        y = -w / 2 - (py - image_shape[0] / 2)

                        try:
                            pattern = scope.create_pattern(x * pixel_size, y * pixel_size, w * pixel_size,
                                                           h * pixel_size)
                            scope.save_pattern(lamella_dir, pattern_filename, pattern)
                        except:
                            pattern = Pattern(0, 0, 0, 0, 0, 'UP')
                            scope.save_pattern(lamella_dir, pattern_filename, pattern)
                            print("Error in Pattern Writing: No Microscope connected?")
                except KeyError:
                    print('No Patterns were found')

        return()
    
    def run_custom_milling(self,pattern_dir,step_pattern_names,milling_time):
        '''
        Input: Pattern Directory as string, list of pattern file names as string, and milling time as int
        Output: None
        Action: Runs provided patterns for the provided time at the set ion beam current
        '''
        print("Clearing all patterns in the active view...")
        microscope.patterning.clear_patterns()
        print("Creating new rectangle pattern on top...")
        microscope.patterning.set_default_beam_type(BeamType.ION)

        microscope.patterning.mode = 'Parallel'

        for pattern in step_pattern_names:
            #for pattern in step:
            self.pattern_parser(pattern_dir,pattern)
        print("Patterns have been parsed")


        print("Set Ion Beam as active")
        microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
        print("Done")

        print("Starting patterning...")
        microscope.patterning.start()
        import time
        x=time.time()
        print(milling_time)
        while microscope.patterning.state=="Running":

            y=time.time()
            if float(y)-float(x) < milling_time:
                time.sleep(1)  # sec
                #timestamp=timestamp+1
            else:
                microscope.patterning.stop()
                microscope.patterning.clear_patterns()
                return()

        print("Stopping patterning...")
        microscope.patterning.stop()
        print("Done")
        microscope.patterning.clear_patterns()
        return()
    
    def run_milling_custom(self,lamella_name,alignment_image,stagepos,pattern_ref_directory,custom_filename):
        '''
        Input: Lamella name as string, alignment image as numpy array, stageposition as dictionary,
                path to the pattern directory as string, path to pattern sequence file (custom_filename) as string
        Output: Logging
        Action: Runs provided pattern sequence file at the given position
        '''

        patterns_reference_directory=pattern_ref_directory#+'/'#+str(lamella_name)+str('/')
        patterns_output_directory=pattern_ref_directory[:-1]+'_out/'#''/'+str(lamella_name)+str('_out/')
        try:
            os.mkdir(patterns_output_directory)
        except:
            self.log_output=self.log_output+"Pattern Directory already existed!!!"+'\n'
        self.lamella_name=lamella_name

        ref_img=alignment_image


        step_pattern_list,steps_current,steps_time=self.create_custom_patterns(patterns_reference_directory,str(lamella_name)+'_lamella.ptf',str(lamella_name)+'_tp.ptf',str(lamella_name)+'_bp.ptf',custom_filename)
        
        #step_current=[]
        step_num=0
        step_pattern_names=[]
        for step in step_pattern_list:
            pattern_num=0
            pattern_names=[]
            for pattern in step:

                pattern_name = lamella_name + str('_step_') + str(step_num)+str('_pattern_')+str(pattern_num)+str('.ptf')
                self.save_pattern(patterns_output_directory,pattern_name,pattern)
                pattern_names.append(pattern_name)
                pattern_num=pattern_num+1
            step_pattern_names.append(pattern_names)
            step_num=step_num+1
        


        self.moveStageAbsolute(stagepos)
        ref_img.save(patterns_output_directory[:-1] + '/initial_fine_alignment_img.tif')
        self.align(ref_img,'ION')

        for i in range(0,step_num):
            if self.continuerun:
                if float(steps_current[i])==0:
                    self.align_current(new_current=3e-11, beam='ION')
                else:
                    self.align_current(new_current=float(steps_current[i])*0.001,beam='ION')
                self.run_custom_milling(patterns_output_directory,step_pattern_names[i],int(steps_time[i]))


        return(self.log_output)

    def custom_file_parser(self, custom_filename):
        '''
        Input: path to pattern sequence file
        Output: Dictionnary of AutoScript4 patterns corresponding to step names, list of step names,
                list of ion beam currents corresponding to the step names
        Action: None
        '''
        steps_current = []
        steps = []
        step = []
        steps_time = []
        with open(custom_filename, 'r') as input_file:
            inRecordingMode = False
            for line in input_file.readlines():
                # print(line)
                if line.startswith('#'):
                    pass
                if line.startswith('IB_Current'):
                    steps_current.append(line.split('=')[1])
                    # print(steps_current)
                if line.startswith('Time'):
                    steps_time.append(line.split('=')[1])

                if not inRecordingMode:
                    if line.startswith('Step='):
                        inRecordingMode = True
                elif line.startswith('/Step'):
                    inRecordingMode = False
                    steps.append(step)
                    step = []

                else:
                    step.append(line)

        inRecordingMode = False
        pattern_dict = {}
        num = 0
        for i in steps:
            patterns = []
            pattern = {}
            for j in i:
                if j.startswith('#'):
                    pass
                if not inRecordingMode:
                    if j.startswith('Pattern'):
                        inRecordingMode = True

                elif j.startswith('/Pattern'):
                    inRecordingMode = False
                    patterns.append({'IB_Current': i[0][:-1]})
                    patterns.append(pattern)
                    pattern = {}

                else:
                    try:
                        pattern.update({j.split('=')[0]: j.split('=')[1][:-1]})
                    except:
                        continue
            pattern_dict.update({num: patterns})
            num = num + 1


        return (pattern_dict, steps_current, steps_time)

    def run_SAV(self, lamella_name, alignment_image, stagepos, pattern_ref_directory, paramsfile):
        '''
        Input: Lamella name from position as string, alignment image as numpy array, pattern directory path as string,
                path to the SAV params file as string
        Output: Logging
        Action: Runs Volume Imaging at the given lamella position using the parameters from the SAV params file
        '''

        patterns_reference_directory = pattern_ref_directory  # +'/'#+str(lamella_name)+str('/')
        patterns_output_directory = pattern_ref_directory[:-1] + '_out/'  # ''/'+str(lamella_name)+str('_out/')
        self.define_SAVparams_file(paramsfile)
        try:
            os.mkdir(patterns_output_directory)
        except:
            self.log_output = self.log_output + "Pattern Directory already existed!!!" + '\n'
        self.lamella_name = lamella_name

        ref_img = alignment_image

        step_pattern_list, steps_current = self.create_SAV_patterns(patterns_reference_directory,
                                                                       str(lamella_name) + '_lamella.ptf',
                                                                       str(lamella_name) + '_tp.ptf',
                                                                       str(lamella_name) + '_bp.ptf')

        # step_current=[]
        step_num = 0
        step_pattern_names = []
        for step in step_pattern_list:
            pattern_num = 0
            pattern_names = []
            for pattern in step:
                pattern_name = lamella_name + str('_step_') + str(step_num) + str('_pattern_') + str(pattern_num) + str(
                    '.ptf')
                self.save_pattern(patterns_output_directory, pattern_name, pattern)
                pattern_names.append(pattern_name)
                pattern_num = pattern_num + 1
            step_pattern_names.append(pattern_names)
            step_num = step_num + 1

        self.moveStageAbsolute(stagepos)
        ref_img.save(patterns_output_directory[:-1] + '/initial_fine_alignment_img.tif')

        try:
            os.mkdir(self.output_dir+self.lamella_name+'_out/'+'output/')
        except:
            print("Directory already exists!")


        params=read_SAV_params(self.SAVparamsfile)
        for i in range(0, step_num):
            #if float(steps_current[i]) == 0:
            if self.continuerun:
                if i==0:
                    if int(params['AlignInitial'])==1:
                    #self.align_current(new_current=1e-11, beam='ION')
                        self.align(ref_img, 'ION')
                    self.align_current(new_current=float(steps_current[i]), beam='ION')
                if (i+1) % int(params['FocusEvery']) == 0:
                    #microscope.imaging.set_active_view(1)
                    scope.auto_focus(beam="ELECTRON")
                if i==0:
                    if int(params['FocusInitial']) == 1:
                    #microscope.imaging.set_active_view(1)
                        scope.auto_focus(beam="ELECTRON")
                if (i+1) % int(params['RealignEvery']) == 0:
                    self.align(ref_img,'ION',current=float(steps_current[i]))
                    #self.align_current(new_current=float(steps_current[i]), beam='ION')
                if (i + 1) % int(params['RealignSEMEvery']) == 0:
                    self.align(first_image,'ELECTRON')
                    microscope.imaging.set_active_view(2)


                self.run_custom_milling(patterns_output_directory, step_pattern_names[i], int(params['MillingTime']))

                current_images=self.take_image_EB_SAV()
                if i==0:
                    first_image=current_images[0]
                now = datetime.datetime.now()
                for j in range(len(current_images)):
                    current_images[j].save(self.output_dir + self.lamella_name+'_out/output/'+now.strftime("%Y-%m-%d_%H_%M_%S_")+self.lamella_name +'_'+str(i)+'_mode_'+str(j)+'.tif')

                microscope.imaging.set_active_view(2)

        return (self.log_output)


    def create_SAV_patterns(self, directory, pattern_lamella, pattern_above, pattern_below):
        '''
        Input: path to the directory of the lamella position, name of the three definition patterns from the SerialFIB GUI
        Output: list of patterns and list of currents to be used for milling
        Action: Creates patterns for volume imaging jobs
        '''
        pattern_lamella = self.pattern_parser(directory, pattern_lamella)
        lamella_center_x = pattern_lamella.center_x
        lamella_center_y = pattern_lamella.center_y
        pattern_above = self.pattern_parser(directory, pattern_above)
        start_position_above = (pattern_above.center_y + 0.5 * pattern_above.height)
        pattern_below = self.pattern_parser(directory, pattern_below)
        start_position_below = (pattern_lamella.center_y + 0.5 * pattern_lamella.height)

        width_lamella = pattern_lamella.width

        microscope.patterning.clear_patterns()
        params=read_SAV_params(self.SAVparamsfile)
        slice_thickness=float(params['SliceThickness'])
        pattern_type=params['PatternType']
        scan_direction=params['ScanDirection']
        milling_current=float(params['IB_Current'])




        self.makePatterns_SAV(start_position_above, start_position_below, slice_thickness, width_lamella, pattern_type, scan_direction, milling_current, directory)
        custom_filename=str(directory) + 'SAV_pattern_file.pf'
        pattern_dict,steps_current, steps_time=self.custom_file_parser(custom_filename)
        step_patterns=[]
        steps_current=[]
        for i in pattern_dict:

            patterns=[]
            for j in pattern_dict[i]:

                try:
                    IB_Current=j['IB_Current'].split('=')[1]
                    if IB_Current==0:
                        IB_Current=1e-11
                except:
                    center_y = -float(j['Offset_y'])
                    center_x = lamella_center_x + float(j['Offset_x'])
                    height = float(j['Height_y'])
                    if j['Width_x']=="'Lamella'":
                        width=width_lamella
                    else:
                        width=float(j['Width_x'])



                    try:
                        pattern_type=j['PatternType']
                        if pattern_type=="Cross-Section" :
                            pattern = microscope.patterning.create_regular_cross_section(center_x=center_x, center_y=center_y, depth=10e-06, width=width, height=height)
                        elif pattern_type=="Cleaning Cross-Section":
                            pattern = microscope.patterning.create_regular_cross_section(center_x=center_x,center_y=center_y,depth=10e-06, width=width,height=height)
                        else:
                            pattern = microscope.patterning.create_rectangle(center_x=center_x, center_y=center_y,depth=10e-06, width=width, height=height)
                    except:
                        print("No Pattern Type defined")
                        pattern = microscope.patterning.create_rectangle(center_x=center_x, center_y=center_y, depth=10e-06, width=width, height=height)

                    try:
                        if j['ScanDirection']=="TopToBottom":
                            pattern.scan_direction = PatternScanDirection.TOP_TO_BOTTOM
                        #Rectangle.scan_direction = PatternScanDirection.BOTTOM_TO_TOP
                        elif j['ScanDirection']=="BottomToTop":
                            pattern.scan_direction = PatternScanDirection.BOTTOM_TO_TOP
                        elif j['ScanDirection']=="LeftToRight":
                            pattern.scan_direction = PatternScanDirection.LEFT_TO_RIGHT
                        elif j['ScanDirection']=="RightToLeft":
                            pattern.scan_direction = PatternScanDirection.RIGHT_TO_LEFT
                    except:
                        print("No Scan Direction defined")

                    patterns.append(pattern)
            step_patterns.append(patterns)
            steps_current.append(IB_Current)

        return(step_patterns,steps_current)

    def makePatterns_SAV(self,y_start, y_end, slice_thickness, width, pattern_type, scan_direction, milling_current,
                         output_dir):
        '''
        Input: Start and end position from SerialFIB GUI, parameters from SAV params file (slice thickness int, width float,
                pattern_type string, scan_direction string, milling_current float)
        Output: None
        Action: Creates pattern sequence file for volume imaging jobs, writes it out in lamella output directory as
                "SAV_pattern_file.pf"
        '''
        import numpy as np
        offsets = np.arange(y_start, y_end, -slice_thickness)
        with open(str(output_dir) + 'SAV_pattern_file.pf', 'w') as output_file:
            output_file.write('')

            for i in range(len(offsets)):
                output_file.write('Step_Name=Step ' + str(i) + '\n')
                output_file.write('Step=' + str(i) + '\n')
                output_file.write('IB_Current=' + str(milling_current) + '\n')
                output_file.write('Pattern=0' + '\n')
                output_file.write('Offset_y=' + str(-offsets[i]) + '\n')
                output_file.write('Offset_x=0.0e-06' + '\n')
                output_file.write('Height_y=' + str(slice_thickness) + '\n')
                output_file.write('Width_x=' + str(width) + '\n')
                output_file.write('PatternType=' + str(pattern_type) + '\n')
                output_file.write('ScanDirection=' + str(scan_direction) + '\n')
                output_file.write('/Pattern\n')
                output_file.write('/Step\n')




    def run_milling_protocol(self, lamella_name, alignment_image, stagepos, pattern_ref_directory, protocol_filename,mode='fine'):
        '''
        Input: lamella name from positions, alignment image as numpy array, stageposition as dictionary,
                site definition directory from the SerialFIB GUI, path to protocol file as string,
                optional mode , "Rough" takes extreme positions for material ablation into account, "fine" does not
        Output: Logging
        Action: Runs milling defined by given protocol file at the provided lamella position
        '''
        patterns_reference_directory = pattern_ref_directory  # +'/'#+str(lamella_name)+str('/')
        patterns_output_directory = pattern_ref_directory[:-1] + '_out/'  # ''/'+str(lamella_name)+str('_out/')
        try:
            os.mkdir(patterns_output_directory)
        except:
            self.log_output = self.log_output + "Pattern Directory already existed!!!" + '\n'
        self.lamella_name = lamella_name

        ref_img = alignment_image

        step_pattern_list, steps_current, steps_time = self.create_custom_protocol(patterns_reference_directory,
                                                                                   str(
                                                                                       lamella_name) + '_lamella.ptf',
                                                                                   str(lamella_name) + '_tp.ptf',
                                                                                   str(lamella_name) + '_bp.ptf',
                                                                                   protocol_filename,mode)

        step_num = 0
        step_pattern_names = []
        for step in step_pattern_list:
            pattern_num = 0
            pattern_names = []
            for pattern in step:
                pattern_name = lamella_name + str('_step_') + str(step_num) + str('_pattern_') + str(
                    pattern_num) + str(
                    '.ptf')
                self.save_pattern(patterns_output_directory, pattern_name, pattern)
                pattern_names.append(pattern_name)
                pattern_num = pattern_num + 1

            step_pattern_names.append(pattern_names)
            step_num = step_num + 1


        self.moveStageAbsolute(stagepos)
        ref_img.save(patterns_output_directory[:-1] + '/initial_fine_alignment_img.tif')
        self.align(ref_img, 'ION')


        for i in range(0, step_num):
            if self.continuerun:
                if float(steps_current[i]) == 0:
                    self.align_current(new_current=1e-11, beam='ION')
                else:

                    self.align_current(new_current=float(steps_current[i]), beam='ION')

                self.run_custom_milling(patterns_output_directory, step_pattern_names[i], int(steps_time[i]))

        return (self.log_output)





####


scope=fibsem()


