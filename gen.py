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


def stokeprocess(stoke,flag):
#stoke is a list of gcode from the entry to exit
    del stoke[0]
    del stoke[1]
    vX = random.randint(-30, 30)/100
    vY = random.randint(-40, 40)/100
    if len(stoke) >1:
        d0 = cvgline(stoke[0])
        d1 = cvgline(stoke[1])
        l = 0
        ldlist = [0]
        dxlist = [0]
        dylist = [0]
    if len(stoke)>2:
        for i in range(2,len(stoke)):
            dx = d1[0]-d0[0]
            dxlist.append(dx)
            dy = d1[1]-d0[1]
            dylist.append(dy)
            ldlist.append(math.sqrt(dx**2 + dy**2))
            l = l+ ldlist[i-1]
            d0 = d1
            d1 = cvgline(stoke[i])
        if flag :
            stoke[0] = addvec(stoke[0],vX,vY)
            for i in range(1,len(stoke)):
                stoke[i] = addvec(stoke[i],vX,vY)
                vX = int(vX*(l-ldlist[i-1])/l *100)/100
                vY = int(vY*(l-ldlist[i-1])/l *100)/100
        else:
            stoke[0] = addvec(stoke[0],vX,vY)
            temp = cvgline(stoke[0])
            pX = temp[0]
            pY = temp[1]
            for i in range(1,len(stoke)):
                pX = int((pX +dxlist[i-1]*0.9)*100)/100
                pY = int((pY +dylist[i-1]*0.95)*100)/100
                stoke[i] = f'G{getg01(stoke[i])} X{pX} Y{pY}\n'

    stoke.insert(0,'M5\n')
    stoke.insert(2,'M3\n')
    return stoke
            


stokenum =input('how many stokes for a length change?')
stokenum = int(stokenum)
Din = open(input('path to nc :'),'r')
Dout = open('out.nc','w')
stokes = []
Glist =  Din.readlines()
Beg = False
alt = True
for i in range(0,len(Glist)):
    if Glist[i] == 'M5\n':
        Beg = not Beg
    if i%stokenum == 0:
        alt = False
    else:
        alt = True
    if Beg:
        stokes.append(Glist[i])
    else:
        if len(stokes)!=0 :
            Dout.writelines(stokeprocess(stokes,alt))
            alt = True
            stokes=list()
            stokes.append(Glist[i])
            Beg = not Beg
        else :
            print(Glist[i],end='')
            Dout.write(Glist[i])
    i = i+1


