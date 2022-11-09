#idea : alter each beginning of a stroke ,for the source file over this is not word splitted so we can only focous on strokes
import math

def stokeprocess(stroke,out):
    ran


stokenum =input('how many stokes for a length change?')
raidus = input('the size of circle the alter victor mm :')

Din = open(input('path to nc :','r'))
Dout = open('out.nc','w')


glist =  Din.readlines
stokelist = list()
for i in range(4,len(glist)):
    if glist[i] == 'M5\n':
        i = i+1
        stokelist.append(glist[i])
    else:
        if glist[i] =='M3\n':
            stokeprocess(stokelist,Dout)
            i=i+1
        else:
            i = i+1
            stokelist.append(glist[i])


