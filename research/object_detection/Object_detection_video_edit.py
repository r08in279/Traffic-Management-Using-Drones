# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 07:15:45 2019

@author: Baakchsu
"""

import tensorflow as tf
import tensornets as nets
import os
import sys
import cv2
import numpy as np
import time
from utils import label_map_util
from utils import visualization_utils as vis_util
import PIL.Image as Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C://Program Files (x86)//Tesseract-OCR//tesseract.exe"
#tf.reset_default_graph()
#frame=cv2.imread("D://pyworks//yolo//truck.jpg",1)






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
    min_score_thresh=0.90)
#print(lis)
    image_pil = Image.fromarray(np.uint8(ff)).convert('RGB')
    
    for i in lis:
        if i[0]=='n':
            co=lis[i]
            
            
            im_width, im_height = image_pil.size
            (left, right, top, bottom) = (co[0] * im_width, co[1] * im_width,
                                  co[2] * im_height, co[3] * im_height)
        
            num_plate_detected=ff[int(top):int(bottom),int(left):int(right)]
            config = ('-l eng --oem 1 --psm 3')
            #gray = cv2.cvtColor(num_plate_detected,cv2.COLOR_BGR2GRAY)
# Run tesseract OCR on image
            text = pytesseract.image_to_string(num_plate_detected, config=config)    
            return text
    return ''
    







print('reached')
tf.reset_default_graph()

d = {'time': ['ff'], 'car': [0],'truck':[0],'bike':[0],'bus':[0],'person':[0]}
classes={'0':'person','1':'bicycle','2':'car','3':'bike','5':'bus','7':'truck'}
list_of_classes=[0,1,2,3,5,7]
with tf.Session() as sesss:
    inputss = tf.placeholder(tf.float32, [None, 416, 416, 3])
    model = nets.YOLOv3COCO(inputss, nets.Darknet19)
    sesss.run(model.pretrained())
#"D://pyworks//yolo//videoplayback.mp4"    
    vidcap = cv2.VideoCapture('bb.mp4')
                             
    
    
    
    while(vidcap.isOpened()):
        ret, frame = vidcap.read()
        img=cv2.resize(frame,(416,416))
        imge=np.array(img).reshape(-1,416,416,3)
        start_time=time.time()
        preds = sesss.run(model.preds, {inputss: model.preprocess(imge)})
    
        print("--- %s seconds ---" % (time.time() - start_time)) 
        boxes = model.get_boxes(preds, imge.shape[1:3])
        cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        
        



        cv2.resizeWindow('image', 700,700)
        #print("--- %s seconds ---" % (time.time() - start_time)) 
        boxes1=np.array(boxes)
        for j in list_of_classes:
            count =0
            if str(j) in classes:
                lab=classes[str(j)]
            if len(boxes1) !=0:
                
                
                for i in range(len(boxes1[j])):
                    box=boxes1[j][i] 
                    
                    if boxes1[j][i][4]>=.40:
                        
                            
                        count += 1    
 
                        cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(0,255,0),1)
                        if j==2 or j==3 or j==5 or j==7:
                            
                            crop=img[int(box[1]):int(box[3]),int(box[0]):int(box[2])]
                            plate_text=rcnn(crop)
                            print(plate_text)
                        
                        cv2.putText(img, lab, (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), lineType=cv2.LINE_AA)
            print(lab,": ",count)
    
              
        cv2.imshow("image",img)  
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break          

print("run")
df = pd.DataFrame(data=d)

print(df.head)
df.set_index('time')
df.to_csv('df.csv',index=False)


cap.release()
cv2.destroyAllWindows()           
