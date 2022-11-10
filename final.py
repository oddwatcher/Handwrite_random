
#this file used to reconfigure laser plotter to z plotter
#G0 is rapid move ,G1 is writing move
ncpath = "./out.nc"
while 1:
    try:
        din = open(ncpath,'r')
        break
    except:
        ncpath = input('input path:')
mode = input('default z settings enter 1;else press any')
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

