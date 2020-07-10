import time
import melopero_amg8833 as mp
minvalue = 30.0 #these are treshold values i'll update them once we can test the camera
maxvalue = 45.0
sensor = mp.AMGGridEye()
sensor.set_fps_mode(mp.AMGGridEye.FPS_10_MODE)

while(True):

    #update and print matrix
    sensor.update_pixel_temperature_matrix()
    matrix = sensor.get_pixel_temperature_matrix()
    for y in matrix:
        line = matrix[y,:]
        for x in line
        pixel = line[x]
            if minvalue < pixel < maxvalue:
                print(pixel)
                human = humancheck()
                if human == True:
                    print('Human found')


    #wait 0.1 seconds
    time.sleep(0.1)

def humancheck()
from TFLite_detection_image.py import human
return human    
