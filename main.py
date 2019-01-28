# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 11:20:29 2018

@author: y.wei
"""

from data_reading_video import making_video
from my_functions import readepos, ion_sequence
import os
from line_detection import motion_tracking,save_data
from coords_transform_more import  to_Cartisian
#if __name__ == '__main__' :
#    data_path=os.path.join(os.path.dirname(os.path.abspath(__file__)))
##save_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'columns')
#    data_dir_list = os.listdir(data_path)
#    
#    
#    
#    for dataset in data_dir_list:
#        filename = dataset
#        X=os.path.splitext(filename)[0]
#        print(filename)
#        print(X)
#        making_video(data_path+'\\'+filename)
##  
#    video() #name of the video as input

# this is for 35053
#ion_num_1=5000000  
#interval=500000
#ion_num_2=39000000 

# reading epos file and make a video
filename='R5076_31053-v01.epos'  
file=list(readepos(filename))
#
ion_seq=68
ion_num_1=5000000 
interval=500000
ion_num_2=10000000
#ions=ion_sequence(file,ion_num_1,ion_num_2)    
#making_video(filename,file, ion_seq, ion_num_1, ion_num_2, interval)
#
##object tracking
X=os.path.splitext(filename)[0]
#video_name ='video_{}_{}_{}_{}.avi'.format(X,ion_seq,ion_num_1,interval,ion_num_2)
#lines=motion_tracking(video_name)        
#import pandas as pd
#new_name='31053_all_lines.csv'  
#lines = pd.read_csv(new_name)
#save the lines
#save_data(lines,X)
#
to_Cartisian(file, X, ion_num_1, ion_num_2, interval)
#
#import pandas as pd
#new_name='GB_3Dcoords_500000.csv'  
#df_1 = pd.read_csv(new_name)
