from pyPS4Controller.controller import Controller, Event
from pyfirmata import Arduino, util
from picamera import PiCamera
import shutil
import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
pic_name = 0
board = Arduino('/dev/ttyACM0')
pindretaf = board.get_pin("d:13:o")
pindretab = board.get_pin("d:12:o")
PWMdreta = board.get_pin("d:11:p")
pinesquerraf = board.get_pin("d:8:o")
pinesquerrab = board.get_pin("d:7:o")
PWMesquerra = board.get_pin("d:10:p")
MaxAnalog = 32767
MinAnalog = -32767
MaxPWM = 255
MinPWM = 60
camera = PiCamera()





class State:
    def __init__(self):
        self.pic_name = 0
        self.PWM = 0
        self.is_up_arrow_pressed = False
        self.is_down_arrow_pressed = False
        self.is_right_arrow_pressed = False
        self.is_left_arrow_pressed = False
        self.is_R1_pressed = False


class MyController(Controller):
    pic_name = 0
    img = None
    is_up_arrow_pressed = False
    is_down_arrow_pressed = False
    is_right_arrow_pressed = False
    is_left_arrow_pressed = False
    is_R1_pressed = False
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def rightmotorf(self):
        pindretaf.write(1)
        pindretab.write(0)
        PWMdreta.write(self.PWM)
    def rightmotorb(self):
        pindretaf.write(0)
        pindretab.write(1)
        PWMdreta.write(self.PWM)
    def rightmotorstop(self):
        pindretaf.write(0)
        pindretab.write(0)
        PWMdreta.write(0)
    def leftmotorf(self):
        pinesquerraf.write(1)
        pinesquerrab.write(0)
        PWMesquerra.write(self.PWM)
    def leftmotorb(self):
        pinesquerraf.write(0)
        pinesquerrab.write(1)
        PWMesquerra.write(self.PWM)
    def leftmotorstop(self):
        pinesquerraf.write(0)
        pinesquerrab.write(0)
        PWMesquerra.write(0)


    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_up_arrow_press(self):
        self.is_up_arrow_pressed = True

    def on_down_arrow_press(self):
        self.is_down_arrow_pressed = True

    def on_up_down_arrow_release(self):
        self.is_up_arrow_pressed = False
        self.is_down_arrow_pressed = False
        self.rightmotorstop()
        self.leftmotorstop()


    def on_right_arrow_press(self):
        self.is_right_arrow_pressed = True

    def on_left_arrow_press(self):
        self.is_left_arrow_pressed = True

    def on_left_right_arrow_release(self):
        self.is_right_arrow_pressed = False
        self.is_left_arrow_pressed = False
        self.rightmotorstop()
        self.leftmotorstop()
    def on_L1_press(self):
        self.is_R1_pressed = True
    def on_L1_release(self):
        self.is_R1_pressed = False
    def on_x_press(self):
        human = False
        self.img = "/home/pi/Desktop/snapshots/"+ str(self.pic_name) + ".jpg"
        camera.capture(self.img)
        self.pic_name= self.pic_name +1
        # Define and parse input argumets
        MODEL_NAME = 'Sample_TFLite_model'
        GRAPH_NAME = 'detect.tflite'
        LABELMAP_NAME = 'labelmap.txt'
        min_conf_threshold = 0.5


        # Parse input image name and directory.
        IM_NAME = self.img

        # Import TensorFlow libraries
        # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter

        else:
            from tensorflow.lite.python.interpreter import Interpreter

        # Get path to current working directory
        CWD_PATH = os.getcwd()

        # Define path to images and grab all image filenames

        PATH_TO_IMAGES = os.path.join(CWD_PATH,IM_NAME)
        images = glob.glob(PATH_TO_IMAGES)

        # Path to .tflite file, which contains the model that is used for object detection
        PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

        # Path to label map file
        PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

        # Load the label map
        with open(PATH_TO_LABELS, 'r') as f:
            labels = [line.strip() for line in f.readlines()]

        # Have to do a weird fix for label map if using the COCO "starter model" from
        # https://www.tensorflow.org/lite/models/object_detection/overview
        # First label is '???', which has to be removed.
        del(labels[0])

        # Load the Tensorflow Lite model.
        # If using Edge TPU, use special load_delegate argument

        interpreter = Interpreter(model_path=PATH_TO_CKPT)

        interpreter.allocate_tensors()

        # Get model details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]

        floating_model = (input_details[0]['dtype'] == np.float32)

        input_mean = 127.5
        input_std = 127.5

        # Loop over every image and perform detection
        for image_path in images:

            # Load image and resize to expected shape [1xHxWx3]
            image = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            imH, imW, _ = image.shape
            image_resized = cv2.resize(image_rgb, (width, height))
            input_data = np.expand_dims(image_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'],input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
            scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
            #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                    # Draw label
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                    if object_name == 'person':
                        human = True
                        break
        print(human)

    def on_L2_press(self,value):
        if value == -32767: self.PWM = 0
        self.PWM = ((((value + MaxAnalog)/(MaxAnalog*2))*(MaxPWM-MinPWM)+MinPWM)/MaxPWM)
        if self.is_up_arrow_pressed == True:
            self.rightmotorf()
            self.leftmotorf()
        elif self.is_down_arrow_pressed == True:
            self.rightmotorb()
            self.leftmotorb()
        elif self.is_right_arrow_pressed == True:
            if self.is_R1_pressed == True:
                self.rightmotorb()
                self.leftmotorf()
            else:
                self.rightmotorstop()
                self.leftmotorf()
        elif self.is_left_arrow_pressed == True:
            if self.is_R1_pressed == True:
                self.rightmotorf()
                self.leftmotorb()
            else:
                self.rightmotorf()
                self.leftmotorstop()
        else:
            self.rightmotorstop()
            self.leftmotorstop()
    def on_L2_release(self):
        self.PWM = 0

    def on_share_press(self):
        self.rightmotorstop()
        self.leftmotorstop()
    def on_share_release(self):
        exit()





class MyEventDefinition(Event):


    def x_pressed(self):
        return self.button_id == 0 and self.button_type == 1 and self.value == 1

    def x_released(self):
        return self.button_id == 0 and self.button_type == 1 and self.value == 0

    def circle_pressed(self):
        return self.button_id == 1 and self.button_type == 1 and self.value == 1

    def circle_released(self):
        return self.button_id == 1 and self.button_type == 1 and self.value == 0

    def triangle_pressed(self):
        return self.button_id == 2 and self.button_type == 1 and self.value == 1

    def triangle_released(self):
        return self.button_id == 2 and self.button_type == 1 and self.value == 0

    def square_pressed(self):
        return self.button_id == 3 and self.button_type == 1 and self.value == 1

    def square_released(self):
        return self.button_id == 3 and self.button_type == 1 and self.value == 0


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False, event_definition=MyEventDefinition)
controller.listen()
