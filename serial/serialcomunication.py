import matplotlib.pyplot as plt
import math
import serial
ser = serial.Serial('/dev/ttyACM0',baudrate = 9600, timeout=1)
while 1:
    try:
         line = ser.readline().decode("ascii")
    except:continue
    if "done" in line: break
    if not line.startswith("D"):continue
    distance = int(line[(line.find("D")+1):(line.find("A"))])
    angle = int(line[(line.find("A")+1):(line.find("X"))])
    posx = int(line[(line.find("X")+1):(line.find("Y"))])
    posy =int(line[(line.find("Y")+1):])
    vy = math.sqrt((distance**2)/(1+(math.tan(math.radians(angle)))**2))
    vx = math.tan(math.radians(angle))*vy
    x = posx + vx
    y = posy + vy
    plt.scatter(x,y,c='r', marker='.')
    plt.plot([x,posx],[y,posy],c = 'b', marker = ',')

plt.savefig('/home/pi/Desktop/fig.png')
exit()
