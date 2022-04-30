
import scipy.integrate

lins = []
with open('./data.csv','r') as the_in:
    lins = the_in.readlines()

sensor_readings = []
for line in lins:
    if line != '':
        sensor_read_line = line.strip('\n').strip(',').split(',')
        sensor_readings += [sensor_read_line]
print(sensor_readings)

time_nums = []
acc_x_list = []
acc_y_list = []
acc_z_list = []

for p in range(len(sensor_readings)):
    time_val = int(sensor_readings[p][0]) / 1000
    numx = float(sensor_readings[p][1])
    numy = float(sensor_readings[p][2])
    numz = float(sensor_readings[p][3])
    time_nums.append(time_val)
    acc_x_list.append(numx)
    acc_y_list.append(numy)
    acc_z_list.append(numz)


vel_x_list = scipy.integrate.cumulative_trapezoid(y=acc_x_list, x=time_nums)
dist_x_list = scipy.integrate.cumulative_trapezoid(y=vel_x_list,x=time_nums[:-1])
dist_x = scipy.integrate.trapezoid(y=vel_x_list,x=time_nums[:-1])
print('acc x list:', acc_x_list[-10:])
print("vel x list:", vel_x_list[-10:])
print('dist x list:', dist_x_list[-10:])
print('dist x val:', dist_x)

vel_y_list = scipy.integrate.cumulative_trapezoid(y=acc_y_list, x=time_nums)
dist_y_list = scipy.integrate.cumulative_trapezoid(y=vel_y_list,x=time_nums[:-1])
dist_y = scipy.integrate.trapezoid(y=vel_y_list,x=time_nums[:-1])
print('acc_y list:', acc_y_list[-10:])
print("vel y list':", vel_y_list[-10:])
print('dist y list:', dist_y_list)
print('dist y val:', dist_y)

vel_z_list = scipy.integrate.cumulative_trapezoid(y=acc_z_list, x=time_nums)
dist_z_list = scipy.integrate.cumulative_trapezoid(y=vel_z_list,x=time_nums[:-1])
dist_z = scipy.integrate.trapezoid(y=vel_z_list,x=time_nums[:-1])
print('acc_y list:', acc_z_list[-10:])
print("vel y list':", vel_z_list[-10:])
print('dist y list:', dist_z_list)
print('dist y val:', dist_z)
