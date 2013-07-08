# Waypoint Manipulation Module
# C:\Python27\lib
# Written by Mark Palframan
# Last update 6/26/13

import mp_util #from MAVProxy

def readwps(pattern = '1Accw.txt', filepath = r'C:\Documents and Settings\LARSS\My Documents\GitHub\MAVProxy'):
    '''Imports a waypoint file into Python'''
    f = open(filepath + '\\' + pattern, 'r')
    #f = open(r'C:\Documents and Settings\LARSS\My Documents\GitHub\MAVProxy\1Accw.txt', 'r')
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
    
#if __name__ == '__main__':
#    L=readwps()
#    print L
#    K=removeloop(L)
#    #print K
