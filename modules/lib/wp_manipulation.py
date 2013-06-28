# Waypoint Manipulation Module
# C:\Python27\lib
# Written by Mark Palframan
# Last update 6/26/13

import mp_util #from MAVProxy

def validation_readwps(pattern = '1Accw.txt', filepath = r'C:\Documents and Settings\LARSS\My Documents\GitHub\MAVProxy'):
    '''Imports a waypoint file into Python for upload vaidation'''
    f = open(filepath + '\\' + pattern, 'r')
    list = [] #Import waypoint file
    for line in f:
        a=line.strip().split() #Remove line end tags
        if len(a) > 3: #Don't import the first line
            toremove = [0]*2
            for i in toremove:
                a.pop(i) #Remove unnecessary list points
                for j in range(10):
                    a[j] = float(a[j]) #Convert strings to floats
            list.append(a) #Return validation matrix
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

def closest_wp(loc, list):
    '''Takes plane location and wp list in form [lat , lon, alt]'''
    dists = [mp_util.gps_distance(list[i][0], list[i][1], loc[0], loc[1]) for i in range(1,len(list))]
    return dists.index(min(dists))+1

#if __name__ == '__main__':
#    L=readwps()
#    print L
#    K=removeloop(L)
#    #print K
