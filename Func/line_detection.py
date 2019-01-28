# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 22:52:03 2018

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 17:09:31 2018

@author: y.wei
"""
from time import sleep
import cv2
import sys
import os 
import numpy as np
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split(".")
cd=os.path.dirname(os.path.abspath(__file__))
#path1=os.path.join(dir)
path_data=os.path.join(cd,'default')
path_tracking=os.path.join(cd,'tracking')
i=1
def process_img(original_image, thresholdVal, minlinelengthVal, maxlinegapVal):
    

    processed_img =(cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY))# np.invert cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img  = cv2.medianBlur(processed_img ,11)

    processed_img = cv2.GaussianBlur(processed_img, (11,11), 0 )
    
    new_img = processed_img
    new_img = cv2.cvtColor(new_img, cv2.COLOR_GRAY2RGB) 


    processed_img = cv2.erode(processed_img, None, iterations=4)
    
    processed_img = cv2.dilate(processed_img, None, iterations=8)

    processed_img = cv2.Canny(processed_img, threshold1=1, threshold2=20)#100,200

    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
    
    processed_img  = cv2.medianBlur(processed_img ,3)
    

    
    lines = cv2.HoughLinesP(processed_img, rho=1.0, theta=np.pi/180.0,
                                    threshold=int(thresholdVal),
                                    minLineLength=int(minlinelengthVal),
                                    maxLineGap=int(maxlinegapVal))
    
    processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2RGB)
    lap_img =(cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY))# np.invert cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap_img  = cv2.medianBlur(lap_img ,11)
    
    lap_img = cv2.GaussianBlur(lap_img, (11,11), 0 )
    lap_img = cv2.erode(lap_img, None, iterations=4)
    
    lap_img = cv2.dilate(lap_img, None, iterations=7)
    lap_img = cv2.Sobel(lap_img,cv2.CV_32F,1,0,ksize=5)
#    lap_img = cv2.Laplacian(lap_img,cv2.CV_32F)
    lap_img = cv2.cvtColor(lap_img, cv2.COLOR_GRAY2RGB).astype(np.uint8)
#    print(lines)

#    print(lines)
#    image_with_circle=Blob_detector(original_image, processed_img, minThres,maxThres,minArea)
#    plt.figure(3)
#    plt.imshow(image_with_circle)
#    image_lines= draw_lines(image_with_circle,lines)#image_with_circle
#    height,width,channel =original_image.shape
#    blank_image = np.zeros((height,width,3), np.uint8)
#    try:
#        for line in lines:
#            coords = line[0]
#            if only_line==1:
#                new_image =  cv2.line(original_image, (coords[0],coords[1]), (coords[2],coords[3]), [0,255,0], 3)
#            else:
#                new_image =  cv2.line(blank_image, (coords[0],coords[1]), (coords[2],coords[3]), [0,255,0], 3)
#       
#    except:
#        pass
    
    return lines, new_img


def slope(line):
    points = line[0]
    p1 = np.asarray([np.int(points[0]),np.int(points[1])])
    p2 = np.asarray([np.int(points[2]),np.int(points[3])])
    length =np.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )
    if abs(p1[0]-p2[0])<0.001:
        m = 50
    else:
        m = (p1[1]-p2[1])/(p1[0]-p2[0])        
    return m, length

def save_data(new_all_lines,name):
    
    import pandas as pd
#    data = dict()
    new_name='GB_coords_{}.csv'.format(name)
    raw_data = {
        'frame': [],
        'line_10': [],
        'line_11': [],
        'line_20': [],
        'line_21': []}
    for p0 in new_all_lines:    
        raw_data['frame'].append(p0[0])
        raw_data['line_10'].append(p0[1])
        raw_data['line_11'].append(p0[2])
        raw_data['line_20'].append(p0[3])
        raw_data['line_21'].append(p0[4])
    my_df = pd.DataFrame(raw_data)
    my_df.to_csv(new_name, columns=['frame','line_10','line_11','line_20','line_21'], index=False)

def motion_tracking(video_name):
#def motion_tracking(video_name):
#    filename='R5076_31053-v01.epos' 
#    X=os.path.splitext(filename)[0]
#    video_name ='video_{}.avi'.format(X)
    # Set up tracker.
    # Instead of MIL, you can also use
    thresholdVal=50 #51
    minlinelengthVal=40 #44
    maxlinegapVal=2
     
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[0]
     
    
    tracker_1 = cv2.TrackerBoosting_create()
    tracker_2 = cv2.TrackerBoosting_create()
    
    # Read video
    
    video = cv2.VideoCapture(video_name)#myvideo
     
    # Exit if video not opened.
    if not video.isOpened():
        print('Could not open video')
        sys.exit()
     
    # Read first frame.
    ok, old_frame = video.read()
    lines, frame = process_img(old_frame, thresholdVal, minlinelengthVal, maxlinegapVal)
    if not ok:
        print('Cannot read video file')
        sys.exit()
     
    # Define an initial bounding box
    #    bbox = (287, 23, 86, 320)
    p=[]
    q=[]
    new_all_lines = []
    i=0
    # Uncomment the line below to select a different bounding box
    bbox_1 = cv2.selectROI(frame, False)
    p1 = (int(bbox_1[0]), int(bbox_1[1]))
    p2 = (int(bbox_1[0] + bbox_1[2]), int(bbox_1[1] + bbox_1[3]))
    cv2.rectangle(frame, p1, p2, (0,0,255), 2, 1)    
    bbox_2 = cv2.selectROI(frame, False)
    q1 = (int(bbox_2[0]), int(bbox_2[1]))
    q2 = (int(bbox_2[0] + bbox_2[2]), int(bbox_2[1] + bbox_2[3]))
    #    bbox_1 = cv2.selectROI(frame, False) 
    # Initialize tracker with first frame and bounding box
    
    ok = tracker_1.init(frame, bbox_1)
    ok = tracker_2.init(frame, bbox_2) 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if frame is None:
            print("this frame is none")
            break
        else:
            print("this frame is %d"% i) 
            lines, frame = process_img(frame, thresholdVal, minlinelengthVal, maxlinegapVal)            
            if not ok:
                break
             
            # Start timer
        #        timer = cv2.getTickCount()
         
            # Update tracker
            ok, bbox_1 = tracker_1.update(frame)
            bbox_10=bbox_1
            bbox_10=[int(bbox_1[0]), int(bbox_1[1]), int(bbox_1[2]), int(bbox_1[3])]
            p.append(bbox_10)
            ok, bbox_2 = tracker_2.update(frame)
            bbox_20=bbox_2
            bbox_20=[int(bbox_2[0]), int(bbox_2[1]), int(bbox_2[2]), int(bbox_2[3])]
            q.append(bbox_20)
        #    print(lines)
        #    image_with_circle=Blob_detector(original_image, processed_img, minThres,maxThres,minArea)
        #    plt.figure(3)
        #    plt.imshow(image_with_circle)
        #    image_lines= draw_lines(image_with_circle,lines)#image_with_circle
            try:    
                all_lines=[]
                #x=lines[0:5,:,:]
                for line in lines:
                    slope_line,_ = slope(line)
                    
                    coords = line[0]
        #                print(slope_line)      and slope_line <= 1 and slope_line>=3      
                    if (((coords[0] >= p1[0] and coords[1] >= p1[1] and coords[2] <= p2[0] and coords[3] <= p2[1]) or
                        (coords[0] >= q1[0] and coords[1] >= q1[1] and coords[2] <= q2[0] and coords[3] <= q2[1])) and slope_line<=-1 
                      ): # and  and slope_line>=0 and slope_line<=2and slope_line<=-1
                        frame =  cv2.line(frame, (coords[0],coords[1]), (coords[2],coords[3]), [0,255,0], 3)
                        print(slope_line)
                        all_lines.append(line)
                        
            except:
                pass
        #        q.append[bbox_2]
            # Calculate Frames per second (FPS)
        #        fps =8# cv2.getTickFrequency() / (cv2.getTickCount() - timer);
            for line in all_lines:
                x=[i, line[0][0],line[0][1],line[0][2],line[0][3]]
                new_all_lines.append(x)
        #        new_all_lines = [line for line in all_lines]
                                  
        #            new_all_lines.append(all_lines)
            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox_1[0]), int(bbox_1[1]))
                p2 = (int(bbox_1[0] + bbox_1[2]), int(bbox_1[1] + bbox_1[3]))            
                cv2.rectangle(frame, p1, p2, (0,0,255), 2, 1)
                q1 = (int(bbox_2[0]), int(bbox_2[1]))
                q2 = (int(bbox_2[0] + bbox_2[2]), int(bbox_2[1] + bbox_2[3]))
                cv2.rectangle(frame, q1, q2, (255,0,0), 2, 1)
            else :
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
         
            # Display tracker type on frame
            cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
            name="frame %d.jpg" % i
            # Display FPS on frame
            cv2.putText(frame,"No."+ name, (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,170,255), 2);
            # "FPS : " + str(int(fps))
            # Display result
            cv2.imshow("Tracking", frame)
        
            cv2.imwrite(path_tracking + '\\' + name, frame)
            i+=1
        #        sleep(0.3)
        #         Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27 : break
    return new_all_lines
if __name__ == '__main__':
#    filename='R5076_31053-v01_500000.avi' 
#    X=os.path.splitext(filename)[0]
#    video_name ='video_{}.avi'.format(X)
    video_name = 'Tapsim_2.avi'
    lines = motion_tracking(video_name)    
#    import pandas as pd
#    
#    my_df = pd.DataFrame(new_all_lines)
#    my_df.to_csv('30943_lines.csv', index=True, sep=' ', header=False)

#x=motion_tracking()    
#    