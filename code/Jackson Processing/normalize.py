
import scipy.integrate

with open('cs598cg/code/Jackson Processing/mo.txt','r') as the_in:
    lins = the_in.readlines()
time_nums = []
the_list = []
for line in lins:
    if line != '':
        the = line.strip('\n').strip(',').split(',')
        #print(the)
        the_list += [the[:-1]]
        time_nums.append(float(the[-1]))
velocity = [0]
sum = 0
areax=[]
areay=[]
areaz=[]

for p in range(len(the_list)):

    numx = float(the_list[p][3])*100
    numy = float(the_list[p][4])*100
    numz = float(the_list[p][5])*100
    areax.append(numx)
    areay.append(numy)
    areaz.append(numz)
    
set_dx = time_nums
print(len(areaz))
range_check = 0

areax_list = scipy.integrate.cumulative_trapezoid(areax, x=set_dx)
print("x':", areax_list[-10:])
# for a in range(range_check,len(areax_list)):
#     vel = areax_list[a]
#     err = True
#     for k in range(range_check):
#         if abs(vel - areax_list[a-k]) != 0:
#             err = False
#     if err == True:
#         for k in range(range_check):
#             areax_list[a-k] = 0
print(scipy.integrate.cumulative_trapezoid(areax_list,x=set_dx[:-1])[-10:])
print(scipy.integrate.trapezoid(areax_list,x=set_dx[:-1]))

areay_list = scipy.integrate.cumulative_trapezoid(areay, x=set_dx)
print("y':", areay_list[-10:])
# for a in range(range_check,len(areay_list)):
#     vel = areay_list[a]
#     err = True
#     for k in range(range_check):
#         if abs(vel - areay_list[a-k]) != 0:
#             err = False
#     if err == True:
#         for k in range(range_check):
#             areay_list[a-k] = 0
        
print(scipy.integrate.cumulative_trapezoid(areay_list,x=set_dx[:-1])[-10:])
print(scipy.integrate.trapezoid(areay_list,x=set_dx[:-1]))

#areaz_list = scipy.integrate.cumulative_trapezoid(areaz, x=set_dx)
#print(scipy.integrate.cumulative_trapezoid(areaz_list,dx=set_dx))
#print(scipy.integrate.trapezoid(areaz_list,x=set_dx[:-1]))

