# this is a script that worked when tested with sample data below to plot and get max index
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import sys

# input is three filepaths: 
# one is for time: []
# other is for position: []
# last is for rssi: [time, uuid, rssi]
position_fp = sys.argv[0]
rssi_fp = sys.argv[1]

TIME_THRESHOLD = 0.1
device_info = {} # {uuid: {time: [x,y,rssi]}}
# TODO: add some processing here where we merge the information in the two files together
with open(rssi_fp) as rssi_f, open(position_fp) as position_f:
    print(rssi_f.readlines())
    print(position_f.readline())

'''
Given some coordinates and RSSI of device packets at those coordinates, 
we use interpolation to predict the location of a device. 
- coords contains the x and y coordinates of where packet was detected  
- rssi is a list of signal strength values of the packets corresponding to coords.
'''
def localize_device(coords, rssi):
    # TODO: change these
    minX = 0
    minZ = 0
    maxX = 6
    maxZ = 6

    xsteps = np.arange(minX, maxX, 0.1) # we want these in centimeters
    zsteps = np.arange(minZ, maxZ, 0.1)  # pretty sure this should be y

    xgrid, ygrid = np.meshgrid(xsteps, zsteps, indexing='xy')
    zgrid = griddata(coords, rssi, (xgrid, ygrid))

    # clean out nan data
    if ~np.count_nonzero(zgrid[~np.isnan(zgrid)]):
        zgrid[np.isnan(zgrid)] = np.nanmin(zgrid[:])
        peak2d = np.unravel_index(zgrid.argmax(), zgrid.shape)

    # plot mesh grid
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.plot_surface(xgrid, ygrid, zgrid)
    plt.show()