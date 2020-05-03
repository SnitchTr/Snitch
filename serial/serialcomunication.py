import matplotlib.pyplot as plt
import math
import serial
ser = serial.Serial('COM4',baudrate = 9600, timeout=1)
while 1:
    line = ser.readline()
    if line.decode('ascii') is "done":break
    distance = float(line[line.find("D")+1:line.find("A")])
    angle = int(line[line.find("A")+1:line.find("X")])
    posx = int(line[line.find("X")+1:line.find("Y")])
    posy =int(line[line.find("Y")+1:line.find(" ")])
    vx = math.sqrt((distnce**2)/(1+(math.tan(math.radiants(angle)))**2))
    vy = math.tan(math.radians(angle))*x
    x = posx + vx
    y = posy + vy
    plt.scatter(x,y,s=1)
    print(distance)
plt.show()
exit()
