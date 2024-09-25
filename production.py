#idea : alter each beginning of a stroke ,for the source file over this is not word splitted so we can only focous on strokes
import math
import random
def cvgline(str) :
    str = str.replace('G1 ','')
    str = str.replace('G0 ','')
    str = str.replace('\n','')
    XYlist = str.split(' ')
    XYlist [0] = float(XYlist[0].lstrip('X'))
    XYlist [1] = float(XYlist[1].lstrip('Y'))
    return XYlist

def cvlineg(XYlist,flag):
    return f'G{flag} X{XYlist[0]} Y{XYlist[1]}\n'

def getg01(str):
    if str.find('G0')!=-1:
        return 0
    else:
        return 1
def addvec(str,vX,vY):
    nums = cvgline(str)
    nums[0] = nums[0]+vX
    nums[1] = nums[1]+vY
    return cvlineg(nums,getg01(str))


def stokeprocess(stoke,flag,ranX,ranY,lengthadj):
#stoke is a list of gcode from the entry to exit
    del stoke[0]
    del stoke[1]
    vX = random.randint(-ranX, ranX)/100
    vY = random.randint(-ranY, ranY)/100
    if len(stoke) >1:
        d0 = cvgline(stoke[0])
        d1 = cvgline(stoke[1])
        l = 0
        ldlist = [0]
        dxlist = [0]
        dylist = [0]
    if len(stoke)>2:
        for i in range(2,len(stoke)): #calculate the total length of stoke
            dx = d1[0]-d0[0]
            dxlist.append(dx)
            dy = d1[1]-d0[1]
            dylist.append(dy)
            ldlist.append(math.sqrt(dx**2 + dy**2))
            l = l+ ldlist[i-1]
            d0 = d1
            d1 = cvgline(stoke[i])
        if flag :
            stoke[0] = addvec(stoke[0],vX,vY) #if flag is true then apply drag to stroke
            for i in range(1,len(stoke)):
                stoke[i] = addvec(stoke[i],vX,vY)
                vX = int(vX*(l-ldlist[i-1])/l *100)/100
                vY = int(vY*(l-ldlist[i-1])/l *100)/100
        else:
            stoke[0] = addvec(stoke[0],vX,vY) #use gradual movement to shorten stroke
            temp = cvgline(stoke[0])
            pX = temp[0]
            pY = temp[1]
            for i in range(1,len(stoke)):
                pX = int((pX +dxlist[i-1]*lengthadj)*100)/100
                pY = int((pY +dylist[i-1]*lengthadj)*100)/100
                stoke[i] = f'G{getg01(stoke[i])} X{pX} Y{pY}\n'

    stoke.insert(0,'M5\n')
    stoke.insert(2,'M3\n')
    return stoke
            


stokenum =input('how many stokes for a length change?')
stokenum = int(stokenum)

try:
    Din = open('C:/Users/scien/Desktop/1.nc','r')
    
except:
    Din = open(input('path to nc :'),'r')

Dout = open('out.nc','w')
stokes = []
Glist =  Din.readlines()
Beg = False
alt = True
#ranX = int(input('the X random range 1/100 mm: '))
#ranY = int(input('the Y random range 1/100 mm: '))
#lengthadj = (100-int(input('adjust the length alter level 0 - 100: ')))/100
lengthadj = 0.97
ranX = 40
ranY = 20
p=0
for i in range(0,len(Glist)):
    if Glist[i] == 'M5\n':
        Beg = not Beg
    if p%stokenum == 0:
        alt = False
    else:
        alt = True
    if Beg:
        stokes.append(Glist[i])
    else:
        if len(stokes)!=0 :
            Dout.writelines(stokeprocess(stokes,alt,ranX,ranY,lengthadj))
            alt = True
            stokes=list()
            stokes.append(Glist[i])
            Beg = not Beg
            p = p+1
        else :
            print(Glist[i],end='')
            Dout.write(Glist[i])
    i = i+1

Dout.close()
#this file used to reconfigure laser plotter to z plotter
#G0 is rapid move ,G1 is writing move
ncpath = "./out.nc"
while 1:
    try:
        din = open(ncpath,'r')
        break
    except:
        ncpath = input('input path:')
mode = '1'
if mode!='1' :
    zpenup = input('the pen up mm: ')
    zpendown = input('the pen down mm: ')
    zfeed = input('zspeed:')
    feed = input('feedrate: ')
else:
    zpenup = 2
    zpendown = -0.25
    zfeed = 1500
    feed = 1500
zupstr = f'G0 Z{zpenup}'
zdownstr = f'G1 Z{zpendown} F{zfeed}'
g1str = f'G1 F{feed}'
dinstr = din.read()
doutstr = dinstr.replace('G1 F1000\n','')
doutstr = doutstr.replace('G1',g1str)
doutstr = doutstr.replace('M3',zdownstr)
doutstr = doutstr.replace('M5',zupstr)
doutstr = doutstr.replace('G92 X0 Y0\n','')
doutstr = doutstr.replace('S1000\n','')
dout = open('out.nc','w')
dout.write(doutstr)
dout.close()


