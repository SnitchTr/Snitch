# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
import shutil
from picamera import PiCamera
def humancheck(self):
    human = False
    #define a name for the snapshot by giving a number
    img = "/home/pi/Desktop/snapshots/"+ str(self.pic_name) + ".jpg"
    self.camera.capture(img)
    self.pic_name= self.pic_name +1
    # Define and parse input argumets
    MODEL_NAME = 'Sample_TFLite_model'
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

                break
    if human==True:
        shutil.move(img,img[:27] + "humans/"+ img[27:])
        print('Human found!',scores[i]*100,'%')

    else:
        print('No humans found')
