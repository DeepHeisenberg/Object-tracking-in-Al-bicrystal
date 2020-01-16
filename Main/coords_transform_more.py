import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from my_functions import readepos, ion_sequence
#filename='R5076_31053-v01.epos'
#file=list(readepos(filename))
#ion_num_1=1000000
#ion_num_2=2000000
#interval =1000000
def to_Cartisian(file, name, ion_num_1,ion_num_2, interval):
    my_df=ion_sequence(file, ion_num_1, ion_num_2)
    #df = pd.read_csv("GB_lines_31054.csv")

    new_name='GB_coords_{}.csv'.format(name)
#    new_name='R5076_31053-v01.csv'   
#    df = pd.read_csv(new_name)
    df = pd.read_csv('GB_coords_Jazmin_all_lines_2.csv')
#    x_max=my_df['my_x'].max()
    x_min=my_df['my_x'].min()
#    y_max=my_df['my_y'].max()
    y_min=my_df['my_y'].min()
    #df_b = pd.read_csv("dictsZ_blue.csv")
    
    
    #8000000-9000000
    #data = df.drop(["line_20","line_21"], axis=1)
    x_30=pd.DataFrame({'line_30': df["line_10"]+2/3*(df["line_20"]-df["line_10"])})
    x_30['line_30'] =x_30['line_30'].apply(lambda x: np.int(x))
    
    x_31=pd.DataFrame({'line_31': df["line_21"]+1/3*(df["line_11"]-df["line_21"])})
    x_31['line_31'] =x_31['line_31'].apply(lambda x: np.int(x))
    
    x_40=pd.DataFrame({'line_40': df["line_10"]+1/3*(df["line_20"]-df["line_10"])})
    x_40['line_40'] =x_40['line_40'].apply(lambda x: np.int(x))
    
    x_41=pd.DataFrame({'line_41': df["line_21"]+2/3*(df["line_11"]-df["line_21"])})
    x_41['line_41'] =x_41['line_41'].apply(lambda x: np.int(x))
    
    df=df.join(x_30)
    df=df.join(x_31)
    df=df.join(x_40)
    df=df.join(x_41)
    
    print("all data loaded")
    #x=[df['line_10'][0],df['line_20'][0],df['line_30'][0],df['line_40'][0]]
    #y=[df['line_11'][0],df['line_21'][0],df['line_31'][0],df['line_41'][0]]
    #plt.figure()
    #plt.scatter(x,y)
    
    #frames = [x_30, x_31, x_40, x_41]
    #result = pd.concat(frames)
    #df=df.join(frame)
    
    #data=data.values
    #data.loc[:,"line_10"] /= 6 #
    #data.loc[:,"line_10"] *= 2*abs(x_min)/120
    #data.loc[:,"line_10"] += x_min
    
    # rescaling
    df["line_10"] = df["line_10"].apply(lambda x: 2*abs(x_min)*x/720 + x_min)
    df["line_11"] = df["line_11"].apply(lambda x: -2*abs(y_min)*x/720 - y_min)
    df["line_20"] = df["line_20"].apply(lambda x: 2*abs(x_min)*x/720 + x_min)
    df["line_21"] = df["line_21"].apply(lambda x: -2*abs(y_min)*x/720 - y_min)
    df["line_30"] = df["line_30"].apply(lambda x: 2*abs(x_min)*x/720 + x_min)
    df["line_31"] = df["line_31"].apply(lambda x: -2*abs(y_min)*x/720 - y_min)
    df["line_40"] = df["line_40"].apply(lambda x: 2*abs(x_min)*x/720 + x_min)
    df["line_41"] = df["line_41"].apply(lambda x: -2*abs(y_min)*x/720 - y_min)
    print("recscaling complete")
    #df_frame_1 = data.loc[(data['frame'] <= 29)]
    #width = 0.5
    #height = 0.5
    #
    #x = df_frame_1["line_10"]
    #y = df_frame_1["line_11"]
    final_df=pd.DataFrame()
    kk=1
    n_range=0.25
    for i_1,j_1,i_2,j_2,i_3,j_3,i_4,j_4,k in zip(df["line_10"], df["line_11"], df["line_20"], df["line_21"],df["line_30"],df["line_31"], df["line_40"],df["line_41"], df['frame']):
        if k <=53:
            if k>kk:
                print(k)
                ion_num_1-=interval
                ion_num_2-=interval
                my_df=ion_sequence(file, ion_num_1, ion_num_2)
            q=my_df[my_df['my_x'].between(i_1-n_range,i_1+ n_range, inclusive=False)]
            q=q[q['my_y'].between(j_1-n_range,j_1+ n_range, inclusive=False)]
            if len(q)>0:
                final_df=final_df.append(q, ignore_index=True)
            print("coordinate no.1")
            q=my_df[my_df['my_x'].between(i_2-n_range, i_2+ n_range, inclusive=False)]
            q=q[q['my_y'].between(j_2-n_range, j_2+ n_range, inclusive=False)]
            if len(q)>0:
                final_df=final_df.append(q, ignore_index=True)    
            print("coordinate no.2")
            q=my_df[my_df['my_x'].between(i_3-n_range, i_3+ n_range, inclusive=False)]
            q=q[q['my_y'].between(j_3-n_range, j_3+ n_range, inclusive=False)]
            if len(q)>0:
                final_df=final_df.append(q, ignore_index=True)
            print("coordinate no.3")
            q=my_df[my_df['my_x'].between(i_4-n_range, i_4+ n_range, inclusive=False)]
            q=q[q['my_y'].between(j_4-n_range, j_4+ n_range, inclusive=False)]
            if len(q)>0:
                final_df=final_df.append(q, ignore_index=True)
            print("coordinate no.4")        
            kk=k    
    ##appended_data = pd.concat(final_df, axis=1)
    ##df = df[(df['line_10'] >= ) & (df['closing_price'] <= 101)]  
    new_name='new_full_GB_3Dcoords_{}_with_m.csv'.format(name)    
    final_df.to_csv(new_name, columns=['X','Y','Z','my_x','my_y','m'], index=False)

#xedges=np.linspace(x_min, x_max, num=100)

#hist, xedges, yedges = np.histogram2d(my_x,  my_y, bins=120, range=[[x_min, x_max],[y_min,y_max]])#120
#hist =np.rot90(hist).astype('uint8')
#plt.imshow(hist)


