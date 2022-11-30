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

def makePatterns_LamellaDesigner(step,side,thickness_lamella,thickness_patterns,y_center, width, pattern_type, milling_current, output_dir,time,mode='fine',y_min=None,y_max=None):
    '''
    Input: Step as string, side as string ('both','top','bottom'), thickness_lamella as float, thickness_patterns as float,
            y_center as float, width as float, pattern_type as string ("Regular","Cross-Section","Cleaning Cross-Section"),
            milling current as float, output_dir as string, time as int,
            optional mode: "rough" takes extreme points for material ablation into account, "fine" does not,
            y_min and y_max: Extreme points for material ablation, only used if mode=="rough"
    Ouput: None
    Action: Function to create pattern sequence files for lamella jobs (protocols). Written as "patternfile_from_prtocol.pf"
            into the output directory
    '''
    import numpy as np
    
    offset_y=(thickness_patterns+thickness_lamella)/2#(thickness_lamella/2)#+thickness_patterns/2
    #Offset_x=
    filename='/patternfile_from_protocol.pf'


    factors=[-1,1]
    factors_rough=[0,-1]
    factors_rough2=[1,-1]
    print(str(output_dir[:-1])+filename)
    if mode=='rough':
        scan_direction = ['TopToBottom', 'BottomToTop', 'TopToBottom']
        pattern_num = [0, 1, 0]


        offsets_y=[]
        thicknesses=[]
        thickness1=(y_max-y_center)-thickness_lamella/2
        # OLD TFS solution
        #offset_y1=-(thickness_lamella/2+thickness1/2)
        offset_y1=-(thickness_lamella/2)
        thickness2 = (-y_min + y_center) - thickness_lamella / 2
        # OLD TFS solution
        #offset_y2 = -(-thickness_lamella / 2 - thickness2 / 2)
        offset_y2=(thickness_lamella / 2 + thickness2)

        offsets_y.append(offset_y1)
        offsets_y.append(offset_y2)
        thicknesses.append(thickness1)
        thicknesses.append(thickness2)

        with open(str(output_dir) + filename, 'a') as output_file:
            output_file.write('Step_Name=Step ' + str(step) + '\n')
            output_file.write('Step=' + str(step) + '\n')
            output_file.write('Time=' + str(time) + '\n')
            output_file.write('IB_Current=' + str(milling_current) + '\n')
            for j in range(2):
                output_file.write('Pattern=' + str(pattern_num[factors[j]]) + '\n')
                output_file.write('Offset_y=' + str(offsets_y[j]+factors_rough[j]*thicknesses[j]) + '\n')
                output_file.write('Offset_x=0.0e-06' + '\n')
                output_file.write('Height_y=' + str(factors_rough2[j]*thicknesses[j]) + '\n')
                output_file.write('Width_x=' + str(width) + '\n')
                output_file.write('PatternType=' + str(pattern_type) + '\n')
                output_file.write('ScanDirection=' + str(scan_direction[factors[j]]) + '\n')
                output_file.write('/Pattern\n')
            output_file.write('/Step\n')
    else:
        if side=="both":

            scan_direction=['TopToBottom','BottomToTop','TopToBottom']
            pattern_num=[0,1,0]
            with open(str(output_dir)+filename,'a') as output_file:
                output_file.write('Step_Name=Step '+str(step)+'\n')
                output_file.write('Step='+str(step)+'\n')
                output_file.write('Time=' + str(time) + '\n')
                output_file.write('IB_Current=' + str(milling_current) + '\n')
                for i in factors:

                    output_file.write('Pattern='+str(pattern_num[i])+'\n')
                    #output_file.write('Offset_y='+str(i*offset_y+i*(thickness_lamella/2))+'\n')
                    output_file.write('Offset_y='+str(i*offset_y/2)+'\n')
                    output_file.write('Offset_x=0.0e-06'+'\n')
                    output_file.write('Height_y='+str(-i*thickness_patterns)+'\n')
                    output_file.write('Width_x='+str(width)+'\n')
                    output_file.write('PatternType='+str(pattern_type)+'\n')
                    output_file.write('ScanDirection='+str(scan_direction[i])+'\n')
                    output_file.write('/Pattern\n')
                output_file.write('/Step\n')
        elif side=='top':

            with open(str(output_dir)+filename,'a') as output_file:
                output_file.write('Step_Name=Step '+str(step)+'\n')
                output_file.write('Step='+str(step)+'\n')
                output_file.write('IB_Current='+str(milling_current)+'\n')
                output_file.write('Time=' + str(time) + '\n')
                output_file.write('Pattern=0'+'\n')
                output_file.write('Offset_y='+str(-offset_y/2)+'\n')
                output_file.write('Offset_x=0.0e-06'+'\n')
                output_file.write('Height_y='+str(thickness_patterns)+'\n')
                output_file.write('Width_x='+str(width)+'\n')
                output_file.write('PatternType='+str(pattern_type)+'\n')
                output_file.write('ScanDirection=TopToBottom\n')#+str(scan_direction)+'\n')
                output_file.write('/Pattern\n')
                output_file.write('/Step\n')
        elif side=='bottom':

            with open(str(output_dir)+filename,'a') as output_file:
                output_file.write('Step_Name=Step '+str(step)+'\n')
                output_file.write('Step='+str(step)+'\n')
                output_file.write('IB_Current='+str(milling_current)+'\n')
                output_file.write('Time=' + str(time) + '\n')
                output_file.write('Pattern=0'+'\n')
                output_file.write('Offset_y='+str(offset_y/2)+'\n')
                output_file.write('Offset_x=0.0e-06'+'\n')
                output_file.write('Height_y='+str(-thickness_patterns)+'\n')
                output_file.write('Width_x='+str(width)+'\n')
                output_file.write('PatternType='+str(pattern_type)+'\n')
                output_file.write('ScanDirection=BottomToTop\n')#+str(scan_direction)+'\n')
                output_file.write('/Pattern\n')
                output_file.write('/Step\n')


def make_protocol(parameter_list,mode='fine',y_min=None,y_max=None):
    '''
    Input: Parameter list read from protocol file using read_protocolfile,
            optional mode : "rough" takes extreme points for material ablation into account, "fine" does not
            y_min and y_max: Extreme points for material ablation
    Ouput: None
    Action: Parses parameters from protcolfile to makePatterns_LamellaDesigner for writing pattern sequence file
            for the lamella milling job
    '''
    output_dir = parameter_list[0]['output_dir']
    filename = str(output_dir)+'/patternfile_from_protocol.pf'
    try:
        import os
        os.remove(filename)
    except:
        print("no file detected")
    i=0
    for param in parameter_list:
        step=param['step']
        side=param['side']
        thickness_lamella=param['thickness_lamella']
        thickness_patterns=param['thickness_patterns']
        y_center=param['y_center']
        width=param['width']
        pattern_type=param['pattern_type']

        milling_current=param['milling_current']

        time=param['time']

        if mode=='rough':
            if i==0:
                makePatterns_LamellaDesigner(step, side, thickness_lamella, thickness_patterns, y_center, width,
                                             pattern_type, milling_current, output_dir, time, mode, y_min, y_max)
            #if i==1:
            #    makePatterns_LamellaDesigner(step, side, thickness_lamella, -thickness_patterns, y_center-thickness_patterns, width,
            #                                 pattern_type, milling_current, output_dir, time)
            else:
                makePatterns_LamellaDesigner(step, side, thickness_lamella, thickness_patterns, y_center, width,
                                             pattern_type, milling_current, output_dir, time)
        else:
            makePatterns_LamellaDesigner(step, side, thickness_lamella, thickness_patterns, y_center, width, pattern_type, milling_current, output_dir,time)
        i=i+1
    return()

def read_protocolfile(filename):
    '''
    Input: Function to read protocol files
    Ouput: list of dictionaries defining parameters for the steps in lamella milling
    Action: None
    '''
    parameter_list=[]

    with open(filename,'r') as input_file:
        inRecordingMode = False
        dictionary = {}
        for line in input_file.readlines():
            # print(line)
            if line.startswith('#'):
                pass
            elif line.startswith('Step'):
                dictionary.update({'step':line.split('=')[1].rstrip('\n')})
            elif line.startswith('Side'):
                dictionary.update({'side': line.split('=')[1].rstrip('\n')})
            elif line.startswith('thickness_lamella'):
                dictionary.update({'thickness_lamella': float(line.split('=')[1].rstrip('\n'))})
            elif line.startswith('thickness_patterns'):
                dictionary.update({'thickness_patterns': float(line.split('=')[1].rstrip('\n'))})
            elif line.startswith('y_center'):
                dictionary.update({'y_center': float(line.split('=')[1].rstrip('\n'))})
            elif line.startswith('width'):
                dictionary.update({'width': float(line.split('=')[1].rstrip('\n'))})
            elif line.startswith('pattern_type'):
                dictionary.update({'pattern_type': line.split('=')[1].rstrip('\n')})
            elif line.startswith('IB_Current'):
                dictionary.update({'milling_current': float(line.split('=')[1].rstrip('\n'))})
            elif line.startswith('Time'):
                dictionary.update({'time': int(line.split('=')[1].rstrip('\n'))})
            #elif line.startswith('output_dir'):
            #    dictionary.update({'output_dir': line.split('=')[1].rstrip('\n')})


            if not inRecordingMode:
                if line.startswith('Step='):
                    inRecordingMode = True
            elif line.startswith('/Step'):
                inRecordingMode = False
                parameter_list.append(dictionary)
                dictionary = {}

            else:
                pass

    return(parameter_list)


def write_protocolfile(filename,lamella_center_y,width_lamella):
    '''
    Input: Function to write protocol files
    Ouput: list of dictionaries defining parameters for the steps in lamella milling
    Action: None
    '''

    liste=read_protocolfile('bla.txt')

    count = len(liste)
    with open(filename, 'w') as output_file:
        output_file.write("#    PROTOCOL FILE  " + '\n')
        for i in range(count):
            step=liste[i]
            output_file.write("#    Protocol Step Name : " +str(i)+ '\n')
            output_file.write('Step_Name= Step' +str(step['step'])+ '\n')
            output_file.write("Step=" +str(step['step'])+ '\n')

            output_file.write("IB_Current=" + str(step['milling_current']) + '\n')
            output_file.write("Time=" + str(step['time']) + '\n')
            output_file.write("Side=" + str(step['side']) + '\n')

            side=step['side']
            output_file.write('thickness_lamella=' + str(step['thickness_lamella']) + '\n')
            output_file.write('thickness_patterns=' + str(step['thickness_patterns']) + '\n')
            output_file.write('y_center=' + str(step['y_center']) + '\n')
            output_file.write('width=' + str(width_lamella) + '\n')
            output_file.write('pattern_type=' + str(step['pattern_type']) + '\n')
            output_file.write('output_dir=' + str(step['output_dir']) + '\n')
            output_file.write('/Step\n')

    return ()

#write_protocolfile('bla2.txt',1e-06,1e-06)
#print(read_protocolfile('bla.txt'))
#make_protocol('bla2.txt')