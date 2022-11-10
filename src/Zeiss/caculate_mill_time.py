import numpy as np


probe_current = 1.00e-9 # A

probe_size = 2.00e-9 # m

pixel_spacing = 0.5

track_spacing = 0.5



dose = 2000 # Columb / square meter





spot_area = probe_size**2 * pixel_spacing * track_spacing #* np.pi

cycle = 10



dwell_time = dose / cycle * spot_area / probe_current

print(dwell_time)

height = 10.0e-6
width = 10.0e-6

area = height * width
n_pixel = area / (spot_area)
mill_time = dwell_time * n_pixel * cycle

print(mill_time)
