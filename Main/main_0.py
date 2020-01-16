# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 11:20:29 2018

@author: y.wei
"""

#from data_reading_video import making_video
from my_functions import readepos, ion_sequence
import os
from line_detection import motion_tracking, save_data
from coords_transform_more import  to_Cartisian

filename='R5076_31053.epos' 


#tracking the grain boundary and save the data
video_name ='R5076_31053.avi'
lines=motion_tracking(video_name)        
import pandas as pd
new_name='31053_all_lines.csv'  
lines = pd.read_csv(new_name)
save_data(lines,new_name)

#convert to cartisian
#ion_seq=68
#ion_num_1=5000000 
#interval=500000
#ion_num_2=10000000
#to_Cartisian(file, filename, ion_num_1, ion_num_2, interval)
#
#import pandas as pd
#new_name='111.csv'  
#df_1 = pd.read_csv(new_name)
