import numpy as np

def calculate_dwell_time(probe_current,probe_size,pixel_spacing,track_spacing,dose,cycle,mill_time,width,height):

    '''
    probe_current = 1.00e-9 # A

    probe_size = 2.00e-9 # 
    probe table ; beam diameter from probe table


    pixel_spacing = 0.5
    track_spacing = 0.5
    dose = 2000 # Columb / square meter
    cycle = 10


    height = 10.0e-6
    width = 10.0e-6
    '''
    area = height * width
    spot_area = probe_size**2 * pixel_spacing * track_spacing #* np.pi

    #dwell_time=1e-06
    #dwell_time = dose / cycle * spot_area / probe_current

    #print(dwell_time)
    n_pixel = area / (spot_area)
    dwell_time = mill_time / (n_pixel*cycle)
    dose=dwell_time*cycle*probe_current/spot_area

    
    
    #mill_time = dwell_time * n_pixel * cycle
    

    return(dose)