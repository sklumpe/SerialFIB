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
#from win32com import client
#microscope = client.Dispatch('CZ.EMApiCtrl.1')
#microscope.InitialiseRemoting()

#from crossbeam_client import *
from src.Zeiss.crossbeam_client import *
microscope = MicroscopeClient()

from src.Zeiss.custom_matchers_Zeiss import *

#from src.read_SAV import read_SAV_params
import cv2
import numpy as np
import time
import xml.etree.ElementTree as ET
import os
import datetime
import sys

class binary_result():
    def __init__(self):
        self.pixel_size=(0.09615e-06,0.09615e-06)

class scan_field_of_view():
    def __init__(self):
        self.width=100e-06
class optics():
    def __init__(self):
        SFOV=scan_field_of_view()
        self.scan_field_of_view=SFOV
class metadata():
    def __init__(self):
        binary=binary_result()
        self.binary_result=binary
        opt=optics()
        self.optics=opt

class DummyAdorned():
    def __init__(self):
        self.data=[]
        meta=metadata()
        self.metadata=meta
        ### HARDCODE
        self.bit_depth=8
        self.height=768
        #self.metadata.binary_result.pixel_size=1e-06
    def save(self,filepath):
        cv2.imwrite(filepath,self.data)
        print("An Image should have been saved, to be implemented!!")

class DummyPattern():
    def __init__(self):
        self.x=0
        self.y=0
        self.width=0
        self.height=0
        self.depth=0
        self.center_x=0
        self.center_y=0


#try:
#    microscope.connect()
#except:
#    print("Couldn't connect to microscope, connecting to localhost")
#    try:
#        microscope.connect('localhost')
#    except:
#        print("Loading Testimages")


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
        self.testing=False
        # Default alignment current
        self.alignment_current = float(1e-11)
        self.trench_offset = 4e-06
        # Variable for stopping operation
        self.continuerun = True

        #self.dummy_pattern=r"C:/Users/Sven/Desktop/GitHub/SerialFIB/TemplatePatterns/Zeiss/layout001.ely"
        #self.probe_table=r'C:/Users/Sven/Desktop/GitHub/SerialFIB/src/Zeiss/ExampleFiles/ProbeTable.xml'
        #self.APIpath=r'C:/Users/Sven/Pictures/test3.tif'
        

        self.dummy_pattern=r"D:/UserData/RoSa/SerialFIB/TemplatePatterns/Zeiss/layout001.ely"
        self.probe_table=r"D:/UserData/RoSa/SerialFIB/src/Zeiss/ExampleFiles/ProbeTable.xml"
        self.APIpath="C:/api/Grab.tif"
        self.connect()
    
    def __exit__(self):
        self.disconnect()

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
        #if microscope.patterning.state=="Running":
        #    microscope.patterning.stop()
        return()
    def disconnect(self):
        '''
        Input: None
        Output: None
        Action: Disconnect AutoScript4 server
        '''
        microscope.disconnect()
        return()
    def connect(self):
        '''
        Input: None
        Output: None
        Action: Connect AutoScript4 server
        '''
        microscope.connect()
        return()
    def is_idle(self):
        '''
        Input: None
        Output: Returns True if microscope is idle, returns false if microscope is milling
        Action: None
        '''
        #if microscope.patterning.state==PatterningState.IDLE:
        #    return(True)
        #else:
        #    return(False)
        return()
    def get_current(self):
        '''
        Input: None
        Output: Returns the current ion beam current as float
        Action: None
        '''
        current=microscope.beams.ion_beam.get_current()
        #print('Hello')
        #try:
        #    return(float(microscope.beams.ion_beam.beam_current.value))
        #except:
        #    print("No microscope connected.")
        return(current)
    def take_image_IB(self,settings=None):
        '''
        Input: None
        Output: AdornedImage
        Action: Take IB image with standard parameters
        '''
        
        #return(img)
        #self.connect()
        if settings==None:
            settings=GrabFrameSettings(dwell_time=10e-08,resolution='1024x768',line_integration=1)
        else:
            print("Other imaging settings than standard given")
        time.sleep(1)
        microscope.beams.change_beam('ION')
        time.sleep(1)
        microscope.imaging.grab_frame(settings)
        #self.disconnect()
        #path=r'D:/Images/RoSa/Images/test.tif'
        #image_output=r'c:/Users/Sven/Pictures/test.tif'
        path=self.APIpath
        #time.sleep(1)
        img=cv2.imread(path)
        #print(img)
        image=DummyAdorned()
        image.data=img

        

        from src.Zeiss.tiff_handle import read_tiff
        try:
            img, pix = read_tiff(path)
            print(img,pix)
            image_pixel_size=pix
            #image_pixel_size = get_tiff_info(path)["AP_IMAGE_PIXEL_SIZE"].split()

            image.metadata.binary_result.pixel_size=Point(image_pixel_size,image_pixel_size)
        except AttributeError:
            print('Testversion without CrossBeam connected is running, pixel sizes are going to be off.')
            image.metadata.binary_result.pixel_size=Point(1e-09,1e-09)
        #tilt_angle = tiff_handle.get_tiff_info(self.fname)["AP_STAGE_AT_T"].split()
        #self.angle = float(tilt_angle[0])
        #if image_pixel_size[1] == "nm": self.pix = float(image_pixel_size[0])*1e-9
        #elif image_pixel_size[1] == "µm": self.pix = float(image_pixel_size[0])*1e-6
        


        #if image.data.shape[2]==3:
        #    image.data=image.data[:,:,2]
        #else:
        #    print('8bit image')
        #print(image)
        return(image)
    def take_image_EB(self):
        '''
        Input: None
        Output: Image as numpy array
        Action: Take EB image with standard parameters
        '''
        #return(img)
        return()

    def take_image_EB_SAV(self):
        '''
        Input: None
        Output: list of images as numpy array depending on amount of active Detectors in Quadrants (ETD, T1, T2)
        Action: Take EB image with defined parameters from SAVparamsfile
        '''

        #try:
            # Set view to electron beam
            #microscope.imaging.set_active_view(1)

            # Read parameters from defined SAVparams file
        paramsfile=self.SAVparamsfile
        params = read_SAV_params(paramsfile)
        res=params['Resolution']
        dwell=float(params['DwellTime'])
        LI=int(params['LineIntegration'])






            # Aquire Snapshot in EB window
        print("Acquiring EB snapshot")
            #images = microscope.imaging.grab_multiple_frames(GrabFrameSettings(dwell_time=dwell,resolution=res,line_integration=LI))
            #array = images[0].data


        #return(images)

    def getStagePosition(self):
        '''
        Input: None
        Output: current stageposition as directory
        Action: None
        '''

        #### Microscope dependent code ####
        
        try:
            #self.connect()
            stageposition=microscope.specimen.stage.current_position
            #self.disconnect()
            x=stageposition[0]
            y=stageposition[1]
            z=stageposition[2]
            r=stageposition[4]
            t=stageposition[3]
        except:
            #stageposition=StagePosition(x=0,y=0,z=0,r=0,t=0)
            print('did not get stage position')
            x=0#stageposition.x
            y=0#stageposition.y
            z=0#stageposition.z
            r=0#stageposition.r
            t=0#stageposition.t

        
        print(stageposition)

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
        stagepos=(x,y,z,t,r)
        #self.connect()
        microscope.specimen.stage.absolute_move(stagepos)
        #self.disconnect()
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
        #stagepos=StagePosition(x=x,y=y,z=z,t=t,r=r)
        #microscope.specimen.stage.relative_move(stagepos)
        stagepos=(x,y,z,t,r)
        #self.connect()
        microscope.specimen.stage.relative_move(stagepos)
        #self.disconnect()
        return("Stage Moved")


    def align_test(self,image,beam,current=1.0e-11):
        print('Running alignment')
        microscope.imaging.set_active_view(2)

        ## Get old resolution of images to go back after alignment
        old_resolution=microscope.beams.ion_beam.scanning.resolution.value

        print(old_resolution)
        old_mag=microscope.beams.ion_beam.horizontal_field_width.value
        print(old_mag)
        ## Get resolution of reference image and set microscope to given HFW
        img_resolution=str(np.shape(image.data)[1])+'x'+str(np.shape(image.data)[0])
        
        microscope.beams.ion_beam.scanning.resolution.value=img_resolution

        microscope.beams.ion_beam.scanning.resolution.value='512 * 384'
        
        microscope.beams.ion_beam.beam_current.value=current

        ### COMMENTED FOR TESTING
        #microscope.auto_functions.run_auto_cb()

        microscope.beams.ion_beam.beam_shift.value=Point(0,0)
        #print(image.data)
        current_img=self.take_image_IB()
        print(image.data)

        # Load Matcher function and locate feature
        favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
        from src.Zeiss.LocateFeature import locate_feature
        print(np.shape(current_img.data,image.data))
        l = locate_feature(current_img, image, favourite_matcher)
        #print(l.confidence)
        #print(locate_feature)
        
        #beam_current_string=str(microscope.beams.ion_beam.beam_current.value)
        move_count=0
        while l.confidence < 0.98 and move_count < 3:
            #self.log_output = self.log_output + "Move Count =" + str(move_count) + '\n'
            x = l.center_in_meters.x * -1 # sign may need to be flipped depending on matcher
            y = l.center_in_meters.y * -1
            distance = np.sqrt(x ** 2 + y ** 2)
            print("Deviation (in meters): " + str(distance))
            #self.log_output = self.log_output + "Deviation (in meters): " + str(distance) + '\n'
            
            if distance > 1e-05:



                #pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
                pos_cor={'x':x,'y':y,'z':0.0,'r':0.0,'t':0.0}
                #microscope.specimen.stage.relative_move(pos_corr)
                self.moveStageRelative(pos_cor)

                #move_count += 1

            else:
                # apply (additional) beam shift
                print("Shifting beam by ("+str(x)+","+str(y)+")...")
                #self.log_output = self.log_output + "Shifting beam by ("+str(x)+","+str(y)+")... \n"
                print(microscope.beams.ion_beam.beam_shift.value)
                microscope.beams.ion_beam.beam_shift.value += Point(x,y) # incremental

            current_img = self.take_image_IB()
                #now = datetime.datetime.now()
                #current_img.save(self.output_dir+ self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_") + self.lamella_name +'_'+ beam_current_string + '_first_move_' + str(move_count)+'.tif')

                #self.log_output = self.log_output + "Saved Image as : " +self.output_dir+ self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_") + self.lamella_name +'_'+ beam_current_string + '_first_move_' + str(move_count)+'.tif'+'\n'
            l = locate_feature(current_img, image, favourite_matcher)
            move_count+=1
        #microscope.beams.ion_beam.beam_shift.value = Point(0,0)


        print("I made it here")

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
                time.sleep(2)
                beam_current_string=str(microscope.beams.ion_beam.beam_current.value)


                # Get HFW from Image

                # Run auto contrast brightness and reset beam shift. Take an image as reference for alignment
                microscope.beams.ion_beam.horizontal_field_width.value=image.metadata.optics.scan_field_of_view.width
                #microscope.auto_functions.run_auto_cb()
                self.auto_cb()
                microscope.beams.ion_beam.beam_shift.value=Point(0,0)
                current_img=self.take_image_IB()


                # Load Matcher function and locate feature
                favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
                from src.Zeiss.LocateFeature import locate_feature
                l = locate_feature(current_img, image, favourite_matcher)
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
                        rotation=microscope.beams.electron_beam.scanning.rotation.value
                        possible_rotations=[0,3.14]
                        #print(min(possible_rotations, key=lambda x: abs(x - rotation)))

                        pos_cor={'x':x,'y':y,'z':0.0,'r':0.0,'t':0.0}
                        #microscope.specimen.stage.relative_move(pos_corr)
                        self.moveStageRelative(pos_cor)
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
                    l = locate_feature(current_img, image, favourite_matcher)
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
                        if num==3.14:
                            pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
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
                time.sleep(2)

                # Get HFW from Image

                microscope.beams.ion_beam.horizontal_field_width.value = image.metadata.optics.scan_field_of_view.width
                #microscope.auto_functions.run_auto_cb()
                self.auto_cb()
                microscope.beams.ion_beam.beam_shift.value = Point(0, 0)
                current_img = self.take_image_IB()


                favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
                l = locate_feature(current_img, image, favourite_matcher)
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
                        pos_corr = StagePosition(coordinate_system='Specimen', x=x, y=y)
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
                    l = locate_feature(current_img, image, favourite_matcher)
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

    def align_current_test(self,new_current):
        print(new_current)
        microscope.beams.ion_beam.beam_current.value = new_current
        print(microscope.beams.ion_beam.beam_current.value)
    def align_current(self,new_current,beam='ION'):
        '''
        Input: Current to change towards, beam (currently "ION" only)
        Output: None
        Action: Take a reference image at the old current, change current and align to that reference image
        '''
        from src.Zeiss.LocateFeature import locate_feature
        if beam=="ION":
            #microscope.imaging.set_active_view(2)
            #pos1=microscope.specimen.stage.current_position
            #microscope.auto_functions.run_auto_cb()
            #self.auto_cb()
            beam_current_string = str(microscope.beams.ion_beam.beam_current.value)
            ref_img=self.take_image_IB()
            now = datetime.datetime.now()
            try:
                ref_img.save(self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name + '_' + beam_current_string + '_align_current_refimg' + '.tif')
                self.log_output=self.log_output+"Saved Image as : " + self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name + '_' + beam_current_string + '_align_current_refimg' + '.tif'+'\n'
            except:
                print("Run in Scripting Mode")
            microscope.beams.ion_beam.beam_current.value = new_current
            time.sleep(5)
            microscope.beams.ion_beam.scanning.dwell_time.value=200e-09
            microscope.beams.ion_beam.scanning.resolution.value = '768x512'
            #microscope.auto_functions.run_auto_cb()
            self.auto_cb()
            current_img=self.take_image_IB()


            move_count = 0
            now = datetime.datetime.now()
            try:
                current_img.save(self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name  + '_'+ beam_current_string +  '_align_current_' + str(move_count)+'.tif')
                self.log_output = self.log_output + "Saved Image as : " + self.output_dir + self.lamella_name + '_out/' +now.strftime("%Y-%m-%d_%H_%M_%S_")+ self.lamella_name  + '_'+ beam_current_string +  '_align_current_' + str(move_count)+'.tif'+'\n'
            except:
                pass

            favourite_matcher = CustomCVMatcher(cv2.TM_CCOEFF_NORMED, tiling=False)
            l = locate_feature(current_img, ref_img, favourite_matcher)
            
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
                    l = locate_feature(current_img, ref_img, favourite_matcher)
                    print("Current confidence: " + str(l.confidence))
                    self.log_output = self.log_output + "Current confidence: " + str(l.confidence) + '\n'
                else:
                    print("Distance is greater than 10 microns. Abort.")
                    self.log_output = self.log_output + "Distance is greater than 10 microns. Abort.\n"
                    break
            #microscope.auto_functions.run_auto_cb()
            #self.auto_cb()


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

        #Set viewport of microscope#
        #microscope.imaging.set_active_view(2)

        #create pattern
        #pattern=microscope.patterning.create_rectangle(center_x=inp_center_x, center_y=inp_center_y,depth=inp_depth,height=inp_height,width=inp_width)
        
        #pattern=''
        pattern=DummyPattern()
        pattern.x=x
        pattern.y=y
        pattern.width=w
        pattern.height=h
        pattern.depth=d
        return(pattern)

    def test_pattern(self,fname=r'D:/Images/RoSa/SerialFIB/Bla/Bla/0_out/0_step_0_pattern_1.ptf'):
        print(fname)
        print('CHANGING TO ION BEAM TO PREPARE PATTERNING')
        microscope.beams.change_beam('ION')
        #x=0
        microscope._patterning.load_pattern(fname,testing=self.testing)
        while not microscope._patterning.is_idle:
            time.sleep(0.3)
            #print(x)
            #time.sleep(1)
        #
        #print(dir(microscope._patterning))
        time.sleep(1)
        microscope.beams.change_beam('ION')
        return()

    def pattern_parser(self,directory,filename):
        '''
        Input: Directory path as string and filename of xT pattern file as string
        Output: Pattern as AutoScript4 object
        Action: Draws pattern from file in xT GUI
        '''
        #import pattern Zeiss specific here
        pattern=DummyPattern()
        #pattern.center_x=0.0
        #pattern.center_y=0.0
        #pattern.width=0.0
        #pattern.height=0.0
        #pattern.depth=10.0e-06

        #dummy_pattern=r'c:/Users/Sven/Desktop/GitHub/SerialFIB/TemplatePatterns/Zeiss/layout001.ely'
        tree = ET.parse(os.path.join(directory+filename))
        root = tree.getroot()

        for i in root.iter('RECT'):
            center_x=float(i.attrib['x'])
            center_y=float(i.attrib['y'])
            height=float(i.attrib['height'])
            width=float(i.attrib['width'])
            print(center_x,center_y,height,width)
        
        pattern.center_x=center_x*1e-06
        pattern.center_y=center_y*1e-06
        pattern.width=width*1e-06
        pattern.height=height*1e-06
        pattern.depth=10.0e-06
        #raise SystemExit
        print(center_x,center_y,height,width)
        #try:
        #tree.write(directory+filename)
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

    def save_pattern(self,directory,filename,pattern,current=1e-011, time=10):
        '''
        Input: Directory path as string, output filename as string, Pattern as AutoScript4 Pattern object
        Output: None
        Action: Writes pattern as xT xml given the AutoScript Pattern object's parameters
        '''
        # scan_type=Pattern.__class__.__name__
        # if scan_type=="CleaningCrossSectionPattern":
        #     name_tag='Pattern'+scan_type[:-7]
        #     dummy_pattern=r"./TemplatePatterns/clean_cross.ptf"
        # elif scan_type=="RegularCrossSectionPattern":
        #     name_tag='Pattern'+scan_type[:-7]
        #     dummy_pattern=r"./TemplatePatterns/cross.ptf"
        # else:
        #     name_tag="PatternRectangle"
        #     dummy_pattern=r"./TemplatePatterns/regular.ptf"


        # tree = ET.parse(dummy_pattern)
        # root = tree.getroot()

        # CenterX=Pattern.center_x
        # CenterY=Pattern.center_y
        # Depth=Pattern.depth
        # Length=Pattern.height
        # Width=Pattern.width
        # ScanDirection=Pattern.scan_direction
        
        # for element in root:
        #     if element.tag == name_tag:
        #         element.find('CenterX').text=str(CenterX)
        #         element.find('CenterY').text=str(CenterY)
        #         print(Depth)
        #         element.find('Depth').text=str(Depth)
        #         element.find('Length').text=str(Length)
        #         element.find('Width').text=str(Width)
        #         element.find('ScanDirection').text=str(ScanDirection)

        #dummy_pattern=r'c:/Users/Sven/Desktop/GitHub/SerialFIB/TemplatePatterns/Zeiss/layout001.ely'
        dummy_pattern=self.dummy_pattern
        tree = ET.parse(dummy_pattern)
        root = tree.getroot()
        #mill_time-time

        from src.Zeiss.read_probe_table import getProbe
        params=getProbe(current,self.probe_table)

        from src.Zeiss.caculate_mill_time_fct import calculate_dwell_time
        
        #print("THE CURRENT IS",current)
        for i in root.iter('RECT'):
            i.attrib['x']=str(pattern.x*1e06)
            i.attrib['y']=str(pattern.y*1e06)
            i.attrib['height']=str(pattern.height*1e06)
            i.attrib['width']=str(pattern.width*1e06)
            height=pattern.height
            width=pattern.width

            for j in i.iter('PROBE'):
                j.attrib['name']=params['name']
                j.attrib['current']=params['current'] + " A"
                j.attrib['diameter']=params['diameter']+" m"
            for k in i.iter('EXPOSURE'):
                pixel_spacing=float(int(k.attrib['pixel_spacing_area'].split(' ')[0])/100)
                track_spacing=float(int(k.attrib['track_spacing'].split(' ')[0])/100)
                dose=float(k.attrib['dose_area'].split(' ')[0])

                cycle=6125
                probe_current=float(params['current'])
                probe_size=float(params['diameter'])
                

            #mill_time=calculate_mill_time(params['current'],params['diameter'],params['pixel_spacing_area'],params['track_spacing'],params['dose_area'],cycle=params['']
           
                dose=calculate_dwell_time(probe_current,probe_size,pixel_spacing,track_spacing,dose,cycle,time,width,height)
                k.attrib['dose_area']=str(np.absolute(dose))+str(" C/m²")
                print(str(dose)+str(" C/m&#178;"))

            #j.attrib['name']="30kV:50pA ref"
            #j.attrib['current']="5e-011 A"
            #j.attrib['diameter']="4.5e-008 m"
                #print(dwell_time)
                #k.attrib['dwell_times_area']=str(dwell_time)+" s"

        #try:
        #print("Probe_current is:",probe_current)
        #print("Track_Spacing is:",track_spacing)
        #print("Pixel spacing is:",pixel_spacing)
        #print("Dose is:",dose)
        #print("Cycle:",cycle)
        #print("Time is:",time)
        #print("Width is:",width)
        #print("height: ", height)
        #print(probe_current,probe_size,pixel_spacing,track_spacing,dose,cycle,time,width,height)
        tree.write(directory+filename)
        #except:
        #    print("Files already exist! Please check InputDir")

        return()

    def auto_cb(self):
        '''
        Input: None
        Output: None
        Action: runs auto contrast brightness
        '''
        #microscope.auto_functions.run_auto_cb()
        
        print('Insert AutoCB function here')
        contrast_values=[10,20,30,40,50]
        #
        print('Beam current is:')
        #print(microscope._beams.ion_beam.beam_current.value)
        settings=GrabFrameSettings(dwell_time=10e-08,resolution='512x384',line_integration=1)
        current=self.get_current()
        print(current)
        if current < 500e-12:
            contrast_values=[20,30,40,50,60,70,80,90,100]
        if current > 500e-12:
            contrast_values=[15,20,25,30,35,40,45,50,55,60,65,70,75,80]
        contrast_list=[]
        for value in contrast_values:
            self.set_cb(value)
            image1=self.take_image_IB(settings)
            image1=image1.data
            min=np.min(image1)
            max=np.max(image1)
            print(min)
            print(max)
            if max > 220:
                break
                #contrast = (max-min)/(max+min)
                contrast = (max-min)
                contrast_list.append(contrast)
        
        print(contrast_list)
        #self.set_cb(40)
        #image1=self.take_image_IB()
        #data1=image1.data
        #print(data1)
        ##time.sleep(5)
        #self.set_cb(30)
        ##time.sleep(0.5)
        #image2=self.take_image_IB()
        #data2=image2.data
        #print(data2)
        
        

        return
    
  
    def set_cb(self,contrast,brightness=50.1):
        microscope.imaging.set_contrast(contrast)
        microscope.imaging.set_brightness(brightness)
        return



    def run_milling_Zeiss(self,tp_filename,bp_filename,milling_time):
        self.load_pattern(tp_filename)
        self.load_pattern(bp_filename)
        return()

    def run_milling(self,pattern_dir,tp_filename,bp_filename,milling_time):
        print("Clearing all patterns in the active view...")
        #microscope.patterning.clear_patterns()
        print("Creating new rectangle pattern on top...")
        #microscope.patterning.set_default_beam_type(BeamType.ION)
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
        #start_position_above = pattern_above.center_y + 0.5 * pattern_above.height
        start_position_above = pattern_above.center_y + pattern_above.height
        pattern_below = self.pattern_parser(directory, pattern_below)
        #start_position_below = pattern_below.center_y - 0.5 * pattern_below.height
        start_position_below = pattern_below.center_y
        pattern_lamella = self.pattern_parser(directory, pattern_lamella)
        lamella_center_x = pattern_lamella.center_x

        # CODE CHANGES FOR TFS TO ZEISS CONVENTION
        lamella_center_y = pattern_lamella.center_y + 0.5 * pattern_lamella.height
        width_lamella = pattern_lamella.width

        ### DOESNT EXIST FOR ZEISS ###
        #microscope.patterning.clear_patterns()

        from src.Zeiss.makePatterns_LamellaDesigner import make_protocol
        from src.Zeiss.makePatterns_LamellaDesigner import read_protocolfile
        from src.Zeiss.makePatterns_LamellaDesigner import write_protocolfile
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
                    ### COMMENTED OUT TO ADJUST TO ZEISS CONVENTION
                    center_y = lamella_center_y - float(j['Offset_y']) #+ pattern_lamella.height
                    center_x = lamella_center_x + float(j['Offset_x'])
                    height = float(j['Height_y'])
                    if j['Width_x'] == "'Lamella'":
                        width = width_lamella
                    else:
                        width = float(j['Width_x'])

                    try:
                        pattern_type = j['PatternType']
                        if pattern_type == "Cross-Section":
                            #pattern = microscope.patterning.create_regular_cross_section(center_x=center_x,
                            #                                                             center_y=center_y,
                            #                                                             depth=10e-06, width=width,
                            #                                                             height=height)
                            pattern = self.create_pattern(center_x,
                                                                center_y,
                                                                height,
                                                                width,
                                                                10e-06)
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
                        #pattern = microscope.patterning.create_rectangle(center_x=center_x, center_y=center_y,
                        #                                                 depth=10e-06, width=width, height=height)
                        pattern = self.create_pattern(center_x,
                                                            center_y,
                                                            height,
                                                            width,
                                                            10e-06)
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

            #pixel_size = alignment_image.metadata.binary_result.pixel_size[0]
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

                        #x = (px - image_shape[1] / 2) + h / 2
                        #y = -w / 2 - (py - image_shape[0] / 2)
                        x = (px - image_shape[1] / 2)
                        y = - (py - image_shape[0] / 2)

                        try:
                            pattern = self.create_pattern(x * pixel_size, y * pixel_size, w * pixel_size,
                                                           h * pixel_size)
                            self.save_pattern(lamella_dir, pattern_filename, pattern)
                        except:
                            print("Error in Pattern Writing: No Microscope connected?")
                            #pattern = Pattern(0, 0, 0, 0, 0, 'UP')
                            pattern=DummyPattern()
                            self.save_pattern(lamella_dir, pattern_filename, pattern)
                           
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
                ### TEST
                self.save_pattern(patterns_output_directory,pattern_name,pattern,current=steps_current[step_num],time=steps_time[step_num])
                ###
                pattern_names.append(pattern_name)
                pattern_num=pattern_num+1
            step_pattern_names.append(pattern_names)
            step_num=step_num+1
        


        self.moveStageAbsolute(stagepos)
        ref_img.save(patterns_output_directory[:-1] + '/initial_fine_alignment_img.tif')
        #self.align(ref_img,'ION')

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
                #current needs to go here
                current=steps_current[step_num]
                time=float(steps_time[step_num])
                self.save_pattern(patterns_output_directory, pattern_name, pattern,current,time)
                pattern_names.append(pattern_name)
                pattern_num = pattern_num + 1

            step_pattern_names.append(pattern_names)
            step_num = step_num + 1


        self.moveStageAbsolute(stagepos)
        ref_img.save(patterns_output_directory[:-1] + '/initial_fine_alignment_img.tif')
        

        ### COMMENT OUT FOR TEST
        #self.align_test(ref_img, 'ION')
        self.align(ref_img,'ION')


        # for i in range(0, step_num):
        #     if self.continuerun:
        #         if float(steps_current[i]) == 0:
        #             self.align_current(new_current=1e-11, beam='ION')
        #         else:
        
        #             self.align_current(new_current=float(steps_current[i]), beam='ION')
        #         self.run_custom_milling(patterns_output_directory, step_pattern_names[i], int(steps_time[i]))
        print(pattern_names)
        for j in range(0,len(step_pattern_names)):
            #if self.continuerun:
            if float(steps_current[j]) == 0:
                    self.align_current(new_current=1e-11, beam='ION')
            else:
                new_current=float(steps_current[j])
                self.align_current(new_current)
            pattern_names=step_pattern_names[j]
            for i in range(0,len(pattern_names)):
                if self.continuerun:
                    print(pattern_names[i])
                    self.test_pattern(patterns_output_directory+'/'+pattern_names[i])
                    #time.sleep(15)


        return (self.log_output)





####


#scope=fibsem()


#scope.test_pattern()