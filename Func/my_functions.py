# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 10:09:17 2018

@author: y.wei
"""
import numpy as np
import pandas as pd
from tqdm import tqdm

def readepos(file_name):

    f = open(file_name, 'rb')

    dt_type = np.dtype({'names':['x', 'y', 'z', 'm', 't', 'vdc', 'vp', 'dx', 'dy', 'nulls', 'Nat_pulse'],

                  'formats':['>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>i4', '>i4']})

    epos = np.fromfile(f, dt_type, -1)

    f.close()

    return epos

def ion_sequence(file,n,m):
    i=n
    raw_data = {
        'X': [],
        'Y': [],
        'Z': [],
        'my_x': [],
        'my_y': [],
        'm':[]}
    
    
    for i in tqdm(range(n,m)):
        raw_data['X'].append(file[i][0])
        raw_data['Y'].append(file[i][1])
        raw_data['Z'].append(file[i][2])
        raw_data['my_x'].append(file[i][-4])
        raw_data['my_y'].append(file[i][-3])
        raw_data['m'].append(file[i][3])
        i+=1
    
    my_df = pd.DataFrame(raw_data)    
    return my_df

def ion_sequence_new(file,n,m):
    i=n
    raw_data = {
        'X': [],
        'Y': [],
        'Z': [],
        'my_x': [],
        'my_y': [],
        'm':[]}
    
    
    for i in tqdm(range(n,m)):
        raw_data['X'].append(file[i][0])
        raw_data['Y'].append(file[i][1])
        raw_data['Z'].append(file[i][2])
        raw_data['my_x'].append(file[i][-4])
        raw_data['my_y'].append(file[i][-3])
        raw_data['m'].append(file[i][3])
        i+=1
    
    my_df = pd.DataFrame(raw_data)    
    return my_df

#from multiprocessing import Pool
#from multiprocessing import cpu_count


#if __name__ == '__main__':
#
#    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"    
#    iris = parallelize_dataframe(iris, multiply_columns)
#    df=iris
#    time_series = pd.read_pickle("test_chunks/test_set_chunk1.pickle")
#    print("data loading...")    
#    filename='R5076_31054-v01.epos'
#    file=list(readepos(filename))
#    print("data loaded...") 
##    x=file[100:10000]
#    n=1
#    m=1000000
#    x=ion_sequence_new(file,n,m)
#    processed = parallelize_dataframe(x,  ion_sequence_new)
#def readepos_new(file_name):
#    f = open(file_name, 'rb')
#    ncols=3
#    mcols=2
#    dt_type = np.dtype([('spatial', np.float16, ncols), ('m', np.float16),('t',np.float16), ('vdc',np.float16), ('vp',np.float16),
#                        ('detector', np.float16, mcols), ('nulls',np.int16), ('Nat_pulse',np.int16)])
#
#    epos = np.fromfile(f, dt_type, -1)
#
#    f.close()
#
#    return epos
##        process(line)
#def ion_sequence_new(file,n,m):
#    i=n
#    raw_data = {
#        'X': [],
#        'Y': [],
#        'Z': [],
#        'my_x': [],
#        'my_y': []}
#    
#    
#    while(i<=m):
#        spatial=file[i]['spatial']
#        detector=file[i]['detector']
#        raw_data['X'].append(spatial[0])
#        raw_data['Y'].append(spatial[1])
#        raw_data['Z'].append(spatial[2])
#        raw_data['my_x'].append(detector[0])
#        raw_data['my_y'].append(detector[1])
#        
#        i+=1
#    
#    my_df = pd.DataFrame(raw_data)    
#    return my_df
#import multiprocessing as mp
#import time
#init objects
#pool = mp.Pool(cores)
#jobs = []
#
#file_name ='R5076_31054-v01.epos'
#tic = time.clock()
#x=readepos_new('R5076_31054-v01.epos')
#y_1=ion_sequence_new(x,1,10000)
#toc = time.clock()
#p=toc - tic
#
#
#tic = time.clock()
#x=readepos('R5076_31054-v01.epos')
#y_2=ion_sequence(x,1,10000)
#toc = time.clock()
#q=toc - tic
#x=file[0:12]