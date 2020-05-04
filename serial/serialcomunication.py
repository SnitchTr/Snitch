import matplotlib.pyplot as plt
import math
import serial
ser = serial.Serial('/dev/ttyACM0',baudrate = 9600, timeout=1)
while 1:
    line = ser.readline().decode("ascii")
    if "done" in line: break
    distance = int(line[(line.find("D")+1):(line.find("A"))])
    angle = int(line[(line.find("A")+1):(line.find("X"))])
    posx = int(line[(line.find("X")+1):(line.find("Y"))])
    posy =int(line[(line.find("Y")+1):])
    vx = math.sqrt((distance**2)/(1+(math.tan(math.radians(angle)))**2))
    vy = math.tan(math.radians(angle))*vx
    x = posx + vx
    y = posy + vy
    plt.scatter(x,y,s=1)

plt.show()
exit()

