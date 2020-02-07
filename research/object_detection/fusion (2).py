
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 07:15:45 2019

@author: Baakchsu
"""
import pandas as pd
import tensorflow as tf
import tensornets as nets
import os
import sys
import cv2
import numpy as np
import time
import matplotlib
matplotlib.use('TkAgg')


import matplotlib.pyplot as plt
from utils import label_map_util
from utils import visualization_utils as vis_util
import PIL.Image as Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C://Program Files (x86)//Tesseract-OCR//tesseract.exe"
#tf.reset_default_graph()
#frame=cv2.imread("D://pyworks//yolo//truck.jpg",1)

"""import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import cv2
import matplotlib.pyplot as plt

fig = plt.figure()
cap = cv2.VideoCapture(0)


x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)


line1, = plt.plot(x1, y1, 'ko-')        # so that we can update data later

for i in range(1000):
    # update data
    line1.set_ydata(np.cos(2 * np.pi * (x1+i*3.14/2) ) * np.exp(-x1) )

    # redraw the canvas
    fig.canvas.draw()

    # convert canvas to image
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
            sep='')
    img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # img is rgb, convert to opencv's default bgr
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)


    # display image with opencv or any operation you like
    cv2.imshow("plot",img)

    # display camera feed
    ret,frame = cap.read()
    cv2.imshow("cam",frame)

    k = cv2.waitKey(33) & 0xFF
    if k == 27:
        break""" 



file = open('testfile.txt','w') 
 

 


import tkinter as tk
search_query=''
class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self,width=50)
        self.button = tk.Button(self, text="ENTER", command=self.on_button)
        self.button.pack()
        self.entry.pack()
        

    def on_button(self):
        #print(self.entry.get())
        global search_query
        search_query = self.entry.get()
        w.destroy()

w = SampleApp()

w.mainloop()






def preprocess(img):
   kernel = np.ones((1, 1), np.uint8)
   img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC) 
   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   img = cv2.dilate(img, kernel, iterations=1)
   img = cv2.erode(img, kernel, iterations=1)
   imgBlurred = cv2.GaussianBlur(img, (5,5), 0)
   return imgBlurred







# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites


# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'


# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Path to video


# Number of classes the object detector can identify
NUM_CLASSES = 2


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

def rcnn(ff):
    image_expanded = np.expand_dims(ff, axis=0)
    old_img = ff.copy()
# Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
    [detection_boxes, detection_scores, detection_classes, num_detections],
    feed_dict={image_tensor: image_expanded})

# Draw the results of the detection (aka 'visulaize the results')
#print('boxes',boxes,'scores', scores,'classes', classes,'num', num)
    im,lis=vis_util.visualize_boxes_and_labels_on_image_array(
    ff,
    np.squeeze(boxes),
    np.squeeze(classes).astype(np.int32),
    np.squeeze(scores),
    category_index,
    use_normalized_coordinates=True,
    line_thickness=8,
    min_score_thresh=0.80)
#print(lis)
    image_pil = Image.fromarray(np.uint8(ff)).convert('RGB')
    text=''
    flag=0
    
    for i in lis:
        if i[0]=='n':
            co=lis[i]
            
            
            im_width, im_height = image_pil.size
            (left, right, top, bottom) = (co[0] * im_width, co[1] * im_width,
                                  co[2] * im_height, co[3] * im_height)
        
            num_plate_detected=old_img[int(top):int(bottom),int(left):int(right)]
            num_plate_detected=preprocess(num_plate_detected)
            
            config = ('-l eng --oem 1 --psm 3')
            #gray = cv2.cvtColor(num_plate_detected,cv2.COLOR_BGR2GRAY)
# Run tesseract OCR on image
            text = pytesseract.image_to_string(num_plate_detected, config=config)  
        elif i[0]=='h':
            flag=1            
            
    return text,flag
    







print('reached')
tf.reset_default_graph()
list_of_plates=[]
classes={'0':'person','1':'bicycle','2':'car','3':'bike','5':'bus','7':'truck'}
list_of_classes=[0]
list_of_bike_coords=[]
list_of_people_coords=[]
vehicle_counter=0
count =0
with tf.Session() as sesss:
    inputss = tf.placeholder(tf.float32, [None, 416, 416, 3])
    model = nets.YOLOv3COCO(inputss, nets.Darknet19)
    sesss.run(model.pretrained())
#"D://pyworks//yolo//videoplayback.mp4"    
    cap = cv2.VideoCapture("helmet_test.mp4")
    list_of_bike_coords=[]
    list_of_people_coords=[]
    while(cap.isOpened()):
        ret, frame = cap.read()
        img=cv2.resize(frame,(416,416))
        imge=np.array(img).reshape(-1,416,416,3)
        start_time=time.time()
        preds = sesss.run(model.preds, {inputss: model.preprocess(imge)})
        
        #print("--- %s seconds ---" % (time.time() - start_time)) 
        boxes = model.get_boxes(preds, imge.shape[1:3])
        cv2.namedWindow('image',cv2.WINDOW_NORMAL)

        cv2.resizeWindow('image', 700,700)
        #print("--- %s seconds ---" % (time.time() - start_time)) 
        boxes1=np.array(boxes)
        count += 1
        
        for j in list_of_classes:
            
            if str(j) in classes:
                lab=classes[str(j)]
            if len(boxes1) !=0:
                
                
                for i in range(len(boxes1[j])):
                    box=boxes1[j][i] 
                    
                    if boxes1[j][i][4]>=.40:
                        
                        
                            
                            
                        cv2.line(img,(0,320),(511,320),(255,0,0),1)
                        if box[3] > 320 and box[1] > 315 and (box[1]-320)<1:
                            vehicle_counter += 1
                            cv2.line(img,(0,320),(511,320),(255,255,0),3)
 
                        #cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(0,255,0),1)
                        if j==0 and j==3 :
                            
                            crop=img[int(box[1]):int(box[3]),int(box[0]):int(box[2])]
                            plate_text,flag=rcnn(crop)
                            print(plate_text)
                            print(flag)
                            if plate_text not in list_of_plates:
                                list_of_plates.append(plate_text)
                            if search_query == plate_text:
                                cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(170,60,200),1)
                                cv2.putText(img, 'Found', (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), lineType=cv2.LINE_AA)
                            if flag==0 :
                                cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(255,255,0),1)
                                cv2.putText(img, 'NoHelmet', (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), lineType=cv2.LINE_AA)
                                print("No Helmet found:",plate_text)
                        
                        
            #print(lab,": ",count)
    
              
        cv2.imshow("image",img)  
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break          
file.write("List of number plates")
file.write(" ".join([str(i) for i in list_of_plates]))



print("Total vehicles passed: %d" % vehicle_counter)
cap.release()
cv2.destroyAllWindows()           

file.close()

# Sample image file is available at http://plates.openalpr.com/ea7the.jpg
