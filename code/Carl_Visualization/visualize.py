# this is a script that worked when tested with sample data below to plot and get max index
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import sys
import pandas as pd

'''
Given some coordinates and RSSI of device packets at those coordinates, 
we use interpolation to predict the location of a device. 
- xs contains the x coordinates of where packet was detected  
- ys contains the y coordinates of where packet was detected  
- rssis is a list of signal strength values of the packets corresponding to coords.
'''
def localize_device(xs, ys, rssis):
    # TODO: change these
    minX = 0
    minY = 0
    maxX = 100
    maxY = 20

    xsteps = np.arange(minX, maxX, 0.1) # lets put as decimeters
    ysteps = np.arange(minY, maxY, 0.1)  # pretty sure this should be y

    xgrid, ygrid = np.meshgrid(xsteps, ysteps, indexing='xy')
    zgrid = griddata((xs, ys), rssis, (xgrid, ygrid))

    # clean out nan data
    if ~np.count_nonzero(zgrid[~np.isnan(zgrid)]):
        zgrid[np.isnan(zgrid)] = np.nanmin(zgrid[:])
        print(np.argmax(zgrid))
        print('x:', xsteps.shape)
        print('y:', ysteps.shape)
        print('z:', zgrid.shape)
        peak2d = np.unravel_index(zgrid.argmax(), zgrid.shape)
    x_peak = round(peak2d[1] * 0.1, 1)
    y_peak = round(peak2d[0] * 0.1, 1)
    print('x:', round(peak2d[1] * 0.1, 1), 'y:', round(peak2d[0] * 0.1, 1))

    # plot mesh grid
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    print(xs, ys, rssis)
    ax.scatter(xs, ys, rssis, marker='o', c='r')
    ax.scatter([x_peak], [y_peak], [np.amax(zgrid)], marker='X', c='black')
    ax.plot_wireframe(xgrid, ygrid, zgrid)
    plt.show()

# input is three filepaths: 
# one is for time: []
# other is for position: []
# last is for rssi: [time, uuid, rssi]
try:
    position_fp = sys.argv[1]
    rssi_fp = sys.argv[2]
except IndexError:
    print('Please add command line arguments position_file_path, rssi_file_path')
    exit()

TIME_THRESHOLD = 0.25#seconds

device_info = {} # {uuid: [[x,y,rssi]]} need to correlate timestamps to get x,y,rssi with uuid
# TODO: add some processing here where we merge the information in the two files together
rssi_data= pd.read_csv(filepath_or_buffer=rssi_fp, header=None, names=['timestamp', 'rssi', 'uuid'], skipinitialspace=True)
pos_data = pd.read_csv(filepath_or_buffer=position_fp, header=None, names=['timestamp', 'x', 'y'], skipinitialspace=True)

for rssi_ind in range(len(rssi_data)):
    for pos_ind in range(len(pos_data)):
        if np.abs(float(rssi_data['timestamp'][rssi_ind]) - float(pos_data['timestamp'][pos_ind])) < TIME_THRESHOLD:
            uuid = rssi_data['uuid'][rssi_ind]
            x = round(pos_data['x'][pos_ind], 1)
            y = round(pos_data['y'][pos_ind], 1)
            rssi = rssi_data['rssi'][rssi_ind]
            if uuid in device_info:
                device_info[uuid].append((x, y, rssi))
            else:
                device_info[uuid] = [(x, y, rssi)]
            continue

# test
test_res = np.array(device_info['0000feed-0000-1000-8000-00805f9b34fb'])

xs = test_res[:,0]
ys = test_res[:,1]
rssis = test_res[:,2]
localize_device(xs, ys, rssis)