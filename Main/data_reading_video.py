# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 16:54:43 2018

@author: y.wei
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
from my_functions import readepos, ion_sequence
import os

def making_video(filename, file, ion_seq, ion_num_1, ion_num_2, interval):    
    X=os.path.splitext(filename)[0]

    #ii=0
    #x = np.random.randint(255, size=(480, 640)).astype('uint8')
    video_name ='video_{}.avi'.format(X)
    writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'PIM1'), 25, (720, 720), False)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
    for i in range(ion_seq):
        
    #    my_x,my_y=ion_sequence(file,ion_num_1,ion_num_2)
    #    
    #    #print(my_x)
    #    my_x=(np.array(my_x))
    #    my_y=(np.array(my_y))
    #    
    #    x_max=max(my_x)
    #    x_min=min(my_x)
    #    y_max=max(my_y)
    #    y_min=min(my_y)
        my_df=ion_sequence(file, ion_num_1 ,ion_num_2)
        print("frame No.{} generated from ion number{} to ion number{}".format(i,ion_num_1,ion_num_2))
        x_max=my_df['my_x'].max()
        x_min=my_df['my_x'].min()
        y_max=my_df['my_y'].max()
        y_min=my_df['my_y'].min()
        #xedges=np.linspace(x_min, x_max, num=100)
        
        hist, xedges, yedges = np.histogram2d(my_df['my_x'],  my_df['my_y'], bins=120, range=[[x_min, x_max],[y_min,y_max]])#120
        hist =np.rot90(hist).astype('uint8')
        original_height, original_width = hist.shape[:2]
        factor = 6
        resized_image = cv2.resize(hist, (int(original_height*factor), int(original_width*factor)), interpolation=cv2.INTER_CUBIC)
        writer.write(resized_image)
    #    plt.figure()
    #    plt.imshow(resized_image,cmap='jet',origin="upper")
    #    plt.show()
    #    plt.colorbar()
    #    plt.axis('off')
    #    my_title='ion_sequence{}to{}.png'.format(ion_num_1,ion_num_2)
    #    Image_name = 'image_{}.png'.format(ii)
    #    plt.title(my_title)
    #    plt.savefig(my_title, dpi=1000, format='png', bbox_inches='tight')
    #    plt.close()
        ion_num_1-=interval
        ion_num_2-=interval 
    cv2.destroyAllWindows()  
#
#making_video('R5076_31054-v01.epos')