
import scipy.integrate

with open('./data.csv','r') as the_in:
    lins = the_in.readlines()
time_nums = []
the_list = []
for line in lins:
    if line != '':
        the = line.strip('\n').strip(',').split(',')
        #print(the)
        the_list += [the]
        time_nums.append(float(the[0]) / 1000)

areax=[]
areay=[]
areaz=[]

print(the_list)

for p in range(len(the_list)):
    numx = float(the_list[p][1])
    numy = float(the_list[p][2])
    numz = float(the_list[p][3])
    areax.append(numx)
    areay.append(numy)
    areaz.append(numz)
    
set_dx = time_nums
print(len(areaz))
range_check = 0

areax_list = scipy.integrate.cumulative_trapezoid(areax, x=set_dx)
print("vel_x:", areax_list[-10:])
# for a in range(range_check,len(areax_list)):
#     vel = areax_list[a]
#     err = True
#     for k in range(range_check):
#         if abs(vel - areax_list[a-k]) != 0:
#             err = False
#     if err == True:
#         for k in range(range_check):
#             areax_list[a-k] = 0
print('dist_x:', scipy.integrate.cumulative_trapezoid(areax_list,x=set_dx[:-1])[-10:])
print('disp_x:', scipy.integrate.trapezoid(areax_list,x=set_dx[:-1]))

areay_list = scipy.integrate.cumulative_trapezoid(areay, x=set_dx)
print("vel_y':", areay_list[-10:])
# for a in range(range_check,len(areay_list)):
#     vel = areay_list[a]
#     err = True
#     for k in range(range_check):
#         if abs(vel - areay_list[a-k]) != 0:
#             err = False
#     if err == True:
#         for k in range(range_check):
#             areay_list[a-k] = 0
        
print('dist_y', scipy.integrate.cumulative_trapezoid(areay_list,x=set_dx[:-1])[-10:])
print('disp_y:', scipy.integrate.trapezoid(areay_list,x=set_dx[:-1]))

#areaz_list = scipy.integrate.cumulative_trapezoid(areaz, x=set_dx)
#print(scipy.integrate.cumulative_trapezoid(areaz_list,dx=set_dx))
#print(scipy.integrate.trapezoid(areaz_list,x=set_dx[:-1]))

