# Waypoint Manipulation Module
# C:\Python27\lib
# Written by Mark Palframan
# Last update 6/26/13

import mp_util #from MAVProxy
import decimal

def waypoint_scale(pattern = 'A.txt', scale = '1', scale_x = 39.333420, scale_y = -86.029472, filepath = r'C:\Documents and Settings\LARSS\My Documents\GitHub\MAVProxy'):
    '''Scales a waypoint file based on cruise speed in the lateral direction''' 
    try:
        f = open(filepath + '\\' + pattern, 'r')
    except Exception:
        print('%s is not a valid filename. Better luck next time!' % pattern)
        return []
    list = []
    scaling = float(scale)
    for line in f:
        a=line.strip().split()
        if len(a)>3:
            #a[3] = a[3]*scaling
            lat1 = float(a[8])
            lon1 = float(a[9])
            angle = mp_util.gps_bearing(scale_x, scale_y, lat1, lon1)
            # angle = 360 - angle
            dist = mp_util.gps_distance(scale_x, scale_y, lat1, lon1)*scaling
            newlat, newlon = mp_util.gps_newpos(lat1, lon1, angle, dist)
            #from decimal import *
            decimal.getcontext().prec = 8
            a[8] = str(decimal.Decimal(newlat)*1)
            a[9] = str(decimal.Decimal(newlon)*1)
            list.append(a)
    newpattern = pattern[0:len(pattern)-4] + '_' + scale + '.txt'
    make_waypoint_file(list, newpattern)
    return newpattern

def make_waypoint_file(list, newfile):
    '''Outputs a waypoint file given the inputted matrix'''
    if len(list[0]) > 3:
        list.insert(0, 'QGC WPL 110\n')
    f = open(newfile, 'w')
    for i in range(len(list)):
        if i != 0:
            list[i] = '\t'.join(e for e in list[i])+'\n'
        f.write(list[i])
        
def validation_readwps(pattern = '1Accw.txt', filepath = r'C:\Documents and Settings\LARSS\My Documents\GitHub\MAVProxy'):
    '''Imports a waypoint file into Python for upload vaidation'''
    decimal.getcontext().prec = 7
    try:
        f = open(filepath + '\\' + pattern, 'r')
    except Exception:
        print('%s is not a valid filename. Better luck next time!' % pattern)
        return []
    list = [] #Import waypoint file
    for line in f:
        a=line.strip().split() #Remove line end tags
        if len(a) > 3: #Don't import the first line
            toremove = [0]*2
            for i in toremove:
                a.pop(i) #Remove unnecessary list points
                for j in range(10):
                    a[j] = decimal.Decimal(a[j])*1 #Convert strings to floats
                    #a[j] = str(a[j]) #Round to 5 decimal points
            list.append(a) #Return validation matrix
    f.close()
    return list

def readwps(pattern = '1Accw.txt', filepath = r'C:\Documents and Settings\LARSS\My Documents\GitHub\MAVProxy'):
    '''Imports a waypoint file into Python'''
    f = open(filepath + '\\' + pattern, 'r')
    list = [] #Import waypoint file
    for line in f:
        a=line.strip().split() #Remove line end tags
        if len(a) > 3: #Don't import the first line
            toremove = [0]*3+[1]*4 + [4]
            for i in toremove:
                a.pop(i) #Remove unnecessary list points
                for j in range(4):
                    a[j] = float(a[j]) #Convert strings to floats
            list.append(a) #Return matrix of [type, lat , lon, alt]
    list = removeloop(list) #Return matrix of [lat , lon, alt]
    f.close()
    return list
    
def removeloop(list): #Takes matrix of [type, lat , lon, alt]
    '''Removes the looping function and any extraneous lines'''
    removed = 0
    for i in range(len(list)):
        if list[i][0] == 177:
            list[i]=[]
            removed +=1
            #Remove loop line
            for j in range(i+1,len(list)):
                list[j]=[]
                removed +=1
                #Remove all lines following the loop
            break
        else:
            list[i][0] = []
            list[i].remove([])
            #Remove waypoint type indicator
    for _ in range(removed):
        list.remove([])
    return list
    #Return matrix of [lat , lon, alt]

def closest_wp(heading, loc, list):
    '''Takes plane location and wp list in form [lat , lon, alt]'''
    head = heading
    dists = [0]*(len(gpslist)-1)
    heads = [0]*(len(gpslist)-1)
    result = [0]*(len(list)-1)
    param = [[0]*(len(gpslist)-1) for i in range(3)]
    for i in range(1,len(list)):
        dists[i-1] = gps_distance(list[i][0], list[i][1], loc[0], loc[1])
        param[0][i-1] = dists[i-1] #delta
        heads[i-1] = gps_bearing(loc[0], loc[1], list[i][0], list[i][1])
    for i in range(1,len(list)):
        x = abs(head-heads[i-1])
        if x > 180:
            x = 360 - x
        param[1][i-1] = x #alpha
        if i == len(list)-1:
            x = abs(gps_bearing(list[i][0], list[i][1], list[0][0], list[0][1])-heads[i-1])
            if x > 180:
                x = 360 - x
            param[2][i-1] = x #beta
        else:
            x = abs(gps_bearing(list[i][0], list[i][1], list[i+1][0], list[i+1][1])-heads[i-1])
            if x > 180:
                x = 360 - x
            param[2][i-1] = x #beta
    a = 1/min(dists)
    b = 1.9
    c = 0.9
    for i in range(0,len(list)-1):
        result[i] = param[0][i]*a + math.sin(param[1][i]*math.pi/360)*b + math.sin(param[2][i]*math.pi/360)*c
    min_index = result.index(min(result))
    return min_index+1

def validate_wps(wmat, filemat, current_wp_file):
    apm_wp_num = len(wmat)
    pc_wp_num = len(filemat)
    failed_wps = []
    print('********************************************************************************')
    print(' ')
    if apm_wp_num != pc_wp_num:
        print("VALIDATION FAILED!!! Expected %u waypoints, autopilot has %u waypoints." % (
            pc_wp_num, apm_wp_num))       
    else:
        for i in range(pc_wp_num):
            if wmat[i] == filemat[i]:
                print("Waypoint #%u . . . check." % (i))
            else:
                print("Waypoint #%u . . . failed!" % (i))
                # print("APM: "),
                # print(wmat[i])
                # print("PC: "),
                # print(filemat[i])
                failed_wps.append(i)
        if failed_wps == []:
            print("Validation successful. %u waypoints have been properly uploaded from" % 
                pc_wp_num),
            print(current_wp_file)
        else:
            print("VALIDATION FAILED!!! A total of %u waypoints did not pass." % (len(failed_wps)))
            print("Failed waypoints are:"),
            print(", ".join(repr(e) for e in failed_wps))
    print(' ')
    print('********************************************************************************')
    return failed_wps
    
def jump_set_4D(wmat, wpnum, time, lat, lon, head, wmat2):
    n = len(wmat)
    print("Number of waypoints: %u" % (n))
    if n > 2:
        nm1 = str(wmat[n-1][0])
        nm2 = str(wmat[n-2][0])
        nm3 = str(wmat[n-3][0])  
        if (nm1 == '177') & (nm2 == '16'):
            print("ends with a jump")
            nwp = n
            njmp = n-1
        elif (nm1 == '16') & (nm2 == '177') & (nm3 == '16'):
            print("ends with a dummy")
            nwp = n-1
            njmp = n-2
        else:
            print("Incorrect waypoint file format. Should end with <wp, jump> or <wp, jump, wp>.")
            return
    else:
        print("There are not enough waypoints (%u) in the file." % n)
        return
    
        
    
    
#if __name__ == '__main__':
#    L=readwps()
#    print L
#    K=removeloop(L)
#    #print K
