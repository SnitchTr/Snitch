#!/usr/bin/env python3

import rospy
import os
import cv2
import numpy as np
import shutil
import importlib.util
from picamera import PiCamera
from std_msgs.msg import String
folder = '/home/pi/Images'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
os.mkdir('/home/pi/Images/humans')
class Human_Detection_Node(object):
    def __init__(self):
        rospy.loginfo("Looking for Humans")
        self.pic_name = 0
        self.camera = PiCamera()
        # TODO fill in the TOPIC_NAME and MESSAGE_TYPE
        rospy.Subscriber("x", String, self.humancheck)

    def humancheck(self,msg):
    #    if data.msg == 'stop':exit()
        human = False
        #define a name for the snapshot by giving a number
        img = '/home/pi/Images'+ str(self.pic_name) + ".jpg"
        self.camera.capture(img)
        self.pic_name= self.pic_name +1
        # Define and parse input argumets
        MODEL_NAME = '/home/pi/Sample_TFLite_model'
        GRAPH_NAME = 'detect.tflite'
        LABELMAP_NAME = 'labelmap.txt'
        min_conf_threshold = 0.5


        # Import TensorFlow libraries
        # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter

        else:
            from tensorflow.lite.python.interpreter import Interpreter

            # Get path to current working directory
        CWD_PATH = os.getcwd()

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



        # Load image and resize to expected shape [1xHxWx3]
        image = cv2.imread(img)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imH, imW, _ = image.shape
        image_resized = cv2.resize(image_rgb, (height, width))
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

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                if object_name == 'person': #if label is person stop looking and label it as a human
                    human = True
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    x = str(xmin+((xmax-xmin)/2))
                    y= str(ymin+((ymax-ymin)/2))
                    info ='('+ x +','+ y+')'
                    break
        if human==True:
            human_folder='/home/pi/Images/humans/'+ img[15:]
            rospy.Publisher("human", String, queue_size=10).publish(info)
            #shutil.move(human_folder)
            rospy.loginfo('Human Found!')



        else:
            rospy.Publisher("human", String, queue_size=10).publish('No humans found')
            rospy.loginfo('No Human found')



if __name__ == "__main__":
    rospy.init_node("Human_Detection_Node")
    node = Human_Detection_Node()
    rospy.spin()
