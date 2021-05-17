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

def read_SAV_params(filename):
    '''
    Input: Volume Imaging parameter file
    Output: Dictionary of Volume Imaging parameters
    Notes: 
    Parameters include:
    Process Parameters
    Milling current, Slice Thickness, Pattern_type, Scan_direction,
    realign every X, focus in the beginning, focus every X,
    Imaging Parameters
    dwell_time, resolution, line_integration
    '''
    with open(filename,'r') as param_file:
        lines=param_file.readlines()
        params={}
        for line in lines:
            param=line.split('=')
            #print(param)
            params.update({param[0]:param[1].rstrip()})
        #print(params)
    return(params)

def write_SAV_params(filename):
    return()


#read_SAV_params(r'../SAVparams.txt')