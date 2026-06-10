# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:26:55 2024

@author: JiminLee
"""

#1. start with 200up/down + SP measurement

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
import random
import pandas as pd
import numpy as np
import seaborn as sns
from numpy.random import randn, shuffle, seed

import os
import time

from RPU_Tester_without_print_working import * #for hardware demo
from RPU_functions_working import * #for hardware demo
#from RPU_functions_soft_bound import * #for simulation

import json
import measurement_class #for hardware demo
import pathlib 
import time
from datetime import datetime

import json
import itertools

VL= 1.2

def prepend_sign(series):
    return series.apply(lambda x: f"+{abs(x)}" if x >= 0 else f"-{abs(x)}")

#%%

initialize_HEKLA()

#%%

#1. parameters

row_list_C = [4,5] #4
col_list_C = [19,28] #28

row_list_A = [8,12]
col_list_A = [7,22]

#%%

#2. Extraction of Gmax, Gmin, Gmed, Gsym, NOS from actual measured value

#calculation from measurement result

#please type file path properly
df1 = pd.read_csv('C:/Users/RPU/Desktop/JMLee_measurements/241224_switching_sp_arr3/20241224_210902_X-2Y+1_A3_R04C19Cycling.csvall conductance_read.csv')  
df2 = pd.read_csv('C:/Users/RPU/Desktop/JMLee_measurements/241224_switching_sp_arr3/20241224_211213_X-2Y+1_A3_R04C28Cycling.csvall conductance_read.csv') 
df3 = pd.read_csv('C:/Users/RPU/Desktop/JMLee_measurements/241224_switching_sp_arr3/20241224_211543_X-2Y+1_A3_R05C19Cycling.csvall conductance_read.csv')
df4 = pd.read_csv('C:/Users/RPU/Desktop/JMLee_measurements/241224_switching_sp_arr3/20241224_211917_X-2Y+1_A3_R05C28Cycling.csvall conductance_read.csv')
df5 = pd.read_csv('C:/Users/RPU/Desktop/JMLee_measurements/241224_switching_sp_arr3/20241224_222641_X-2Y+1_A3_R08C07Cycling.csvall conductance_read.csv')
df6 = pd.read_csv('C:/Users/RPU/Desktop/JMLee_measurements/241224_switching_sp_arr3/20241224_222940_X-2Y+1_A3_R08C22Cycling.csvall conductance_read.csv')
df7 = pd.read_csv('C:/Users/RPU/Desktop/JMLee_measurements/241224_switching_sp_arr3/20241224_223240_X-2Y+1_A3_R12C07Cycling.csvall conductance_read.csv')
df8 = pd.read_csv('C:/Users/RPU/Desktop/JMLee_measurements/241224_switching_sp_arr3/20241224_223539_X-2Y+1_A3_R12C22Cycling.csvall conductance_read.csv')

G_dataframes_C = [df1, df2, df3, df4]
G_dataframes_A = [df5, df6, df7, df8]

pulse_number_all = len(df1)


G_cols_C = [df.iloc[:, 1] for df in G_dataframes_C] 
G_cols_A = [df.iloc[1:, 1] for df in G_dataframes_A] 


def calculate_stats(series,pulse_number_all):
    G_max = series.iloc[:int(pulse_number_all/2)].max()
    G_min = series.iloc[:int(pulse_number_all/2)].min()

    SP_mean = series.iloc[int(pulse_number_all/2):].mean()
    
    G_med = (G_max + G_min)/2

    
    dw = series.iloc[int(pulse_number_all/2):].diff().abs().dropna().reset_index(drop=True)
    
    dw_mean = dw.mean()
    
    NOS = (G_max-G_min)/dw_mean
    
    on_off_ratio = G_max/G_min

    
    return G_max, G_min, G_med, SP_mean, dw_mean, NOS, on_off_ratio


results_C = [calculate_stats(series,pulse_number_all) for series in G_cols_C]
results_A = [calculate_stats(series,pulse_number_all) for series in G_cols_A]

G_max_arr_C = np.array([result[0] for result in results_C]).reshape(len(row_list_C),len(col_list_C)) #(2,2)
G_min_arr_C = np.array([result[1] for result in results_C]).reshape(len(row_list_C),len(col_list_C)) #(2,2)

print("before change Gmax:",G_max_arr_C)
print("before change Gmin:",G_min_arr_C)

max_value = np.max(G_max_arr_C) #choose the highest value in G_max_arr_C
G_max_arr_C[:] = max_value #change all values with the highest value

min_value = np.min(G_min_arr_C) #choose the lowest value in G_max_arr_C
G_min_arr_C[:] = min_value #change all values with the lowest value

print("after change Gmax:",G_max_arr_C)
print("after change Gmin:",G_min_arr_C)

G_med_arr_C = np.array([result[2] for result in results_C]).reshape(len(row_list_C),len(col_list_C)) #(2,2) #individual
G_sym_arr_C = np.array([result[3] for result in results_C]).reshape(len(row_list_C),len(col_list_C))  #(2,2)#individual
dw_mean_arr_C = np.array([result[4] for result in results_C]).reshape(len(row_list_C),len(col_list_C)) #(2,2) #individual
NOS_arr_C = np.array([result[5] for result in results_C]).reshape(len(row_list_C),len(col_list_C))#(2,2) #individual
on_off_ratio_arr_C = np.array([result[6] for result in results_C]).reshape(len(row_list_C),len(col_list_C))#(2,2) #individual


G_max_arr_A = np.array([result[0] for result in results_A]).reshape(len(row_list_A),len(col_list_A)) #(2,2)
G_min_arr_A = np.array([result[1] for result in results_A]).reshape(len(row_list_A),len(col_list_A)) #(2,2)

print("before change Gmax:",G_max_arr_A)
print("before change Gmin:",G_min_arr_A)

max_value = np.max(G_max_arr_A) #choose the highest value in G_max_arr_A
G_max_arr_A[:] = max_value #change all values with the highest value

min_value = np.min(G_min_arr_A) #choose the lowest value in G_max_arr_A
G_min_arr_A[:] = min_value #change all values with the lowest value

print("after change Gmax:",G_max_arr_A)
print("after change Gmin:",G_min_arr_A)

G_med_arr_A = np.array([result[2] for result in results_A]).reshape(len(row_list_A),len(col_list_A)) #(2,2) #individual
G_sym_arr_A = np.array([result[3] for result in results_A]).reshape(len(row_list_A),len(col_list_A)) #(2,2) #individual
dw_mean_arr_A = np.array([result[4] for result in results_A]).reshape(len(row_list_A),len(col_list_A)) #(2,2) #individual
NOS_arr_A = np.array([result[5] for result in results_A]).reshape(len(row_list_A),len(col_list_A)) #(2,2) #individual
on_off_ratio_arr_A = np.array([result[6] for result in results_A]).reshape(len(row_list_A),len(col_list_A)) #(2,2) #individual


print("NOS_devC:" , NOS_arr_C)
print("NOS_devA:" , NOS_arr_A)

print("on_off_ratio_devC:",on_off_ratio_arr_C)
print("on_off_ratio_devA:",on_off_ratio_arr_A)

#%%

#3. dataset preparation

#dataset parameter

dataset_params= dict(
            seed = 123, #number for random
            Numofweight = 4, 
            Numofdata=100 #100
)

num_row = len(row_list_C) #arr_size
num_col = len(col_list_C) #arr_size

#numofweight dynamically
dataset_params["Numofweight"] = num_row * num_col

seed(dataset_params["seed"])
Numofweight = dataset_params["Numofweight"]
Numofdata = dataset_params["Numofdata"]

#%%
#function for dataset generation

def create_dataset(Numofweight=10,Numofdata=100):
    np.random.seed(dataset_params["seed"])
    target_weight = np.random.normal(0.0,0.3,Numofweight)  #target weight ~ N(0,0.3)
    target_weight = np.round(target_weight,2) 
        
    xj = np.random.normal(0.0,1.0,Numofdata) # Xj ~ N(0,1.0)
        
    return target_weight, xj

#%%

#check the plot of dataset and values

target_weight, xj = create_dataset(Numofweight,Numofdata) #target_weight: 1d vector
target_weight = np.array([-0.5,0,0,-0.5])
target_weight_array = target_weight.reshape(num_row,num_col) #target_weight_array : 2d array

#noise insertion 
#max_xj = max(xj)
#min_xj = min(xj)
#noise_level = 0.01

#y_range = max_xj - min_xj
#noise_std = noise_level * y_range

# Generate Gaussian noise
#noise = np.random.normal(loc=0.0, scale=noise_std, size=xj.shape)

# Add noise to y
#noisy_y = (xj * target_weight) + noise

print('target_weight: ',target_weight_array)
print('xj:',xj)
print('number of data: ',len(xj))

#comparison with noise input
#plt.plot(xj,target_weight*xj,color='black')
#plt.scatter(xj,noisy_y)

# Subplot
# fig, axes = plt.subplots(num_row, num_col, figsize=(40, 25), sharex=True)


# if num_row == 1 and num_col == 1 :
#     axes = np.array([[axes]])
    
# elif num_row == 1 or num_col == 1 :
#     axes = axes.reshape(num_row,num_col)

# fig.suptitle("Array Weight Mapping xj, y Plots", fontsize=16)

# # Iterate through the 2D array of weights and subplots
# for i in range(num_row):
#     for j in range(num_col):
#         idx = i * num_col + j
#         weight = target_weight[idx]
#         y = weight * xj
        
#         # Access the appropriate subplot
#         ax = axes[i, j]
#         ax.scatter(xj, y, s=20, label=f'Weight: {weight:.2f}')
#         ax.set_ylabel("y = xj * weight")
#         ax.set_title(f"Plot for Weight {idx + 1}")
#         ax.grid(True, linestyle='--')
#         ax.legend(loc='lower right', fontsize=8)

# # Add shared labels
# fig.text(0.5, 0.04, 'xj', ha='center')
# fig.text(0.04, 0.5, 'y = xj * weight', va='center', rotation='vertical')

# plt.tight_layout(rect=[0, 0, 1, 0.99])  # Adjust layout to fit title
# plt.show()

#%%
#dataset save as csv format

pathname="C:/Users/RPU/Desktop/JMLee_measurements/241224_demo_trial/"
os.makedirs(pathname, exist_ok=True)
time_experiment = time.strftime("%Y%m%d_%H%M")

# Create a dictionary to store data for each weight
data_dict = {
    "xj": np.tile(xj, len(target_weight)),  # Repeat xj for each weight
    "weight": np.repeat(target_weight, len(xj)),  # Repeat each weight for all xj
    "output": np.concatenate([w * xj for w in target_weight])  # Concatenate outputs for all weights
}

# Convert to DataFrame
dataset_df = pd.DataFrame(data_dict)

# Save to CSV
output_filename = pathname + f'target_weight_mapping_dataset_{time_experiment}.csv'
dataset_df.to_csv(output_filename, index=False)

print(f"Dataset saved to {output_filename}")

#%%

#demonstration parameter setting again

array_selected = 'A-B'

dev_num_A = 3
dev_num_C = 3 #2

#declare again for confirmation
row_list_A = row_list_A
col_list_A = col_list_A
G_max_arr_A = G_max_arr_A
G_min_arr_A = G_min_arr_A
G_med_arr_A = G_med_arr_A
G_sym_arr_A = G_sym_arr_A

row_list_C = row_list_C
col_list_C = col_list_C
G_max_arr_C = G_max_arr_C #np.array([[8e-5]])
G_min_arr_C = G_min_arr_C 
G_med_arr_C = G_med_arr_C 
G_sym_arr_C = G_sym_arr_C 

row_total = 20 # TOTAL ROWS
col_total = 32 # TOTAL COLS

num_row = len(row_list_C) #arr_size
num_col = len(col_list_C) #arr_size

## define a scale factor (normalized hw read to min_max) to FP data
CF=1#2

#Update and read voltage condition definition
# *******************
VL= 1.2
set_bias_A = 1.9 #1.6 #1.6 #1.5#1.4#2#1
reset_bias_A = -1.7 #-1.7 #-1.7 #-1.6#-1.5#-2.1#-1

set_bias_C = 1.6 #1.6 #1.6 #1.6 #1.5 
reset_bias_C = -1.7  #-1.7 #1.7 #-1.7 #-1.6

read_bias = 0.2#0.2
# *******************
# Define update and read time (for each pulse). Similar to voltage, once defined here, not change in training.
# *******************
#max = 1.28ms, min 3.2e-7
t_prog = 3.2e-7#1.2e-3
t_read = 2.5e-6

# *******************
# Bias setups
# *******************

read_fwd_bias_set = {
        "V33":2, # low V33 for reading mode
        "V12":VL,
        "VN":0,
        "VCP":2, # =V33
        "VCN":1.2, # compliance voltage 

        "Rd":VL,
        "Me":0,
        "Fw":VL,
        "En":VL,

        "is_forward":True
        }

set_bias_set = {
        "V33":2.8,#3.3,
        "V12":VL,
        "VN":0,
        "VCP":0,#1.5,#3.3, # =V33
        "VCN":1.0,#1.1,##1.2,#0.9, #1.8 compliance voltage 
        
        "Rd":0,
        "Me":0,
        "Fw":VL,
        "En":VL,
        }

reset_bias_set = {
        "V33":2.8,#3.3,
        "V12":VL,
        "VN":0,#-1.6,
        "VCP": 0.5,#abs(reset_bias) - 1.0,#1.2, #abs(reset_bias) - set_bias_set["VCN"],#0.3,#0.6,#-0.8, #-0.7,-1.2 compliance voltage 
        "VCN":0.0,#abs(reset_bias) ,#1.5,#2.8,#3.3,  # =V33
        
        "Rd":0,
        "Me":0,
        "Fw":0,
        "En":VL
        }

imp_vars = dict(
                arr_total_size = (row_total, col_total),
                arr_size = (num_row, num_col),
                t_prog = t_prog,
                t_read = t_read,
                
                set_bias_A = set_bias_A,
                reset_bias_A = reset_bias_A,
                
                set_bias_C = set_bias_C,
                reset_bias_C = reset_bias_C,
                
                read_bias = read_bias,
                
                set_bias_set = set_bias_set,
                reset_bias_set = reset_bias_set,
                
                CF=CF,
                # N_w=N_w,
                lr_params=None,

                VL= VL,
                
                row_list_A = row_list_A,
                col_list_A = col_list_A,                
                row_list_C = row_list_C,
                col_list_C = col_list_C,

                read_fwd_bias_set = read_fwd_bias_set,
                array_selected = array_selected,

                dev_num_A = dev_num_A,
                dev_num_C = dev_num_C,

                train_params = None,
                dataset_params = None,
                device_params = None,
                )

#%%
#functions for hardware demonstration

def Config_array_device(x):
    if x =='matrix A1':
        rows = row_list_A
        dev_num=dev_num_A
        cols = col_list_A
        array= array_selected
    elif x=='matrix C1':
        rows = row_list_C
        
        dev_num=dev_num_C
        cols = col_list_C
        array= array_selected

    elif x =='digital A1':
        rows = row_list_A
        dev_num=dev_num_A
        cols = col_list_A
        array= digital_A
    elif x=='digital C1':
        rows = row_list_C
        dev_num=dev_num_C
        cols = col_list_C
        array= digital_C

    else:
        print("Something is wrong in the array_device configuration!!")
    return rows, dev_num, cols, array   

def read_G(array_selected = array_selected, dev_num=dev_num_C, rownum = row_list_C, colnum = col_list_C, 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1):

     G_arr = np.zeros(len(rownum)*len(colnum))
     
     for row in range(len(rownum)):
        rownumm = [rownum[row]]
        df,df_heatmap,df_current, df_Vadc = read_fast_HEKLA(
                                            v_read = read_bias,
                                            rows = rownumm,
                                            dev_num = dev_num,
                                            t_read = t_read,
                                            select_array = array_selected,
                                            change_bias = True,
                                            voltages_in = read_fwd_bias_set,
                                            verbose=False,
                                            average = num_of_reads
                                            )
        
#        print("read: ",rownumm)
#        pathname="C:/Users/RPU/Desktop/JMLee_measurements/241129_demo_trial/"
#        time_experiment = time.strftime("%Y%m%d_%H%M%S")
#        output_filename = pathname + f'read_{time_experiment}.csv'
#        df.to_csv(output_filename, index=False)
        
        for i in range(len(colnum)) :
            G_temp = 1.0 / df[df.Col == colnum[i]].Resistance 
#            print(G_temp)
            
            #print("G_temp:", G_temp)
            G = G_temp.values.astype(float)
            
            
            G_arr[row*len(rownum)+i] = G
            
            #print("G:", G)
                
     G_arr = G_arr.reshape(len(rownum),len(colnum))    
     print(G_arr)
    
     return G_arr
     
#functions for demonstration - read and normalization
def read_device(array_selected = array_selected, dev_num=dev_num_C, rownum = row_list_C, colnum = col_list_C, 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1
                ,G_sym = G_sym_arr_A, G_med = G_med_arr_A, G_max = G_max_arr_A, G_min = G_min_arr_A,ref=True):
    
    G_arr = np.zeros(len(rownum)*len(colnum))
    normalize_G = np.zeros((len(rownum),len(colnum)))
    norm_final_G = np.zeros((len(rownum),len(colnum)))
    
    ## read the results
    for row in range(len(rownum)):
        rownumm = [rownum[row]]
        df,df_heatmap,df_current, df_Vadc = read_fast_HEKLA(
                                            v_read = read_bias,
                                            rows = rownumm,
                                            dev_num = dev_num,
                                            t_read = t_read,
                                            select_array = array_selected,
                                            change_bias = True,
                                            voltages_in = read_fwd_bias_set,
                                            verbose=False,
                                            average = num_of_reads
                                            )
        
#        print("read: ",rownumm)
#        pathname="C:/Users/RPU/Desktop/JMLee_measurements/241129_demo_trial/"
#        time_experiment = time.strftime("%Y%m%d_%H%M%S")
#        output_filename = pathname + f'read_{time_experiment}.csv'
#        df.to_csv(output_filename, index=False)
        
        for i in range(len(colnum)) :
            G_temp = 1.0 / df[df.Col == colnum[i]].Resistance 
#            print(G_temp)
            
            #print("G_temp:", G_temp)
            G = G_temp.values.astype(float)
            
            
            G_arr[row*len(rownum)+i] = G
            
            #print("G:", G)
                
    G_arr = G_arr.reshape(len(rownum),len(colnum))    
    print("G_arr: ", G_arr)
    
    if ref :
         normalize_G = 2* (G_arr - G_sym)/(G_max-G_min) #C device : subtracting reference
         
    else :
         normalize_G = 2* (G_arr - G_med)/ (G_max-G_min) #A device : doesn't need reference
    
    #print("normalize_G:",normalize_G)
    norm_final_G = normalize_G
            
    return norm_final_G #original code
    #return G_arr, norm_final_G
     #return 2*(G - G_min) / (G_max - G_min) -1 #102824
     
def dn(array_selected = array_selected, dev_num=dev_num_C, rownum = row_list_C, colnum=col_list_C, 
       t_prog = t_prog, set_bias = set_bias_C, set_bias_set=set_bias_set): # dn - Positive voltage
    
    set_voltage_HEKLA(vh=abs(set_bias)-0.029, dev_num = dev_num, voltages=set_bias_set)
    
    time.sleep(5e-3)
        
    df_prog = update_HEKLA(v_prog=set_bias,
                t_prog=t_prog,
                row=rownum,
                col=colnum,
                select_Array=array_selected,
                voltages= set_bias_set,
                isLongpulse = False)

    #data_update.append(df_prog)

    time.sleep(5e-3)
    
    #for standby moode ? #120924
    set_voltage_HEKLA(vh=0, dev_num = dev_num, voltages=reset_bias_set)
    
    time.sleep(5e-3)
    
    df_prog = update_HEKLA(v_prog=0,
                t_prog=t_prog,
                row=rownum,
                col=colnum,
                select_Array=array_selected,
                voltages= reset_bias_set,
                isLongpulse = False)
    #data_update.append(df_prog)
    time.sleep(5e-3)
    

def up(array_selected = array_selected, dev_num = dev_num_C, rownum = row_list_C, colnum=col_list_C,
       t_prog = t_prog, reset_bias = reset_bias_C, reset_bias_set=reset_bias_set): # up - Negative voltage

    set_voltage_HEKLA(vh=abs(reset_bias)-0.029, dev_num = dev_num, voltages=reset_bias_set)
    
    time.sleep(5e-3)
    
    df_prog = update_HEKLA(v_prog=reset_bias,
                t_prog=t_prog,
                row=rownum,
                col=colnum,
                select_Array=array_selected,
                voltages= reset_bias_set,
                isLongpulse = False)
    
    time.sleep(5e-3)
    
    #for standby moode ? #102824
    set_voltage_HEKLA(vh=0, dev_num = dev_num, voltages=set_bias_set)
    
    time.sleep(5e-3)
    
    df_prog = update_HEKLA(v_prog=0,
                t_prog=t_prog,
                row=rownum,
                col=colnum,
                select_Array=array_selected,
                voltages= set_bias_set,
                isLongpulse = False)
    #data_update.append(df_prog)
    time.sleep(5e-3)
    
#%%
#def read device test
    
c_initial = read_device(array_selected = array_selected, dev_num=dev_num_C, rownum = row_list_C, colnum = col_list_C, 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1
                ,G_sym = G_sym_arr_C, G_med = G_med_arr_C, G_max = G_max_arr_C, G_min = G_min_arr_C,ref=True)

a_initial = read_device(array_selected = array_selected, dev_num=dev_num_A, rownum = row_list_A, colnum = col_list_A, 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1
                ,G_sym = G_sym_arr_A, G_med = G_med_arr_A, G_max = G_max_arr_A, G_min = G_min_arr_A,ref=False)

print("Normalized C:", c_initial)
print("Normalized A:", a_initial)

#%%
#initialization with update pulse or update check - individual check
test = []
numberofupdates=1
r = 5#5 #9
c = 28 #18 #20

neg_bias = -1.7
pos_bias = 1.8
#

for i in range(numberofupdates) :
    up(array_selected = array_selected, dev_num = dev_num_C, 
    rownum = [r], colnum=[c],
     t_prog = t_prog, reset_bias = neg_bias, reset_bias_set= reset_bias_set)
    
#    dn(array_selected = array_selected, dev_num = dev_num_C, 
#      rownum = [r], colnum=[c],
#     t_prog = t_prog, set_bias = pos_bias, set_bias_set= set_bias_set)
##    
#
    C_initial = read_device(array_selected = array_selected, dev_num=dev_num_C, rownum = [r], colnum = [c], 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1
                ,G_sym = G_sym_arr_C, G_med = G_med_arr_C, G_max = G_max_arr_C, G_min = G_min_arr_C,ref=True)

    print("Normalized C:", C_initial)
#    
#for i in range(numberofupdates) :
##    up(array_selected = array_selected, dev_num = dev_num_A, 
##    rownum = [r], colnum=[c],
##     t_prog = t_prog, reset_bias = neg_bias, reset_bias_set= reset_bias_set)
#    
#    dn(array_selected = array_selected, dev_num = dev_num_A, 
#    rownum = [r], colnum=[c],
#     t_prog = t_prog, set_bias = set_bias_A, set_bias_set= set_bias_set)
##    
##
#    A_initial = read_device(array_selected = array_selected, dev_num=dev_num_A, rownum = [r], colnum = [c], 
#                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1
#                ,G_sym = G_sym_arr_A, G_med = G_med_arr_A, G_max = G_max_arr_A, G_min = G_min_arr_A,ref=False)
#
#    print("Normalized A:", A_initial)
#%%
#simple 20 up 20 down check for 3 cycles - individual check

pathname="C:/Users/RPU/Desktop/JMLee_measurements/241224_updatecheck/"
os.makedirs(pathname, exist_ok=True)

lists = []
cycles = 3
updates = 20

r = 8
c = 7

neg_bias = -1.7
pos_bias = 1.9

for i in range(cycles) :
    for j in range(updates) :
       up(array_selected = array_selected, dev_num = dev_num_A, 
          rownum = [r], colnum=[c],
          t_prog = t_prog, reset_bias = neg_bias, reset_bias_set= reset_bias_set)  
       
       G_up = read_G(array_selected = array_selected, dev_num=dev_num_A, rownum = [r], colnum = [c], 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1)
        
       
       lists.append(G_up[0])
       
    for k in range(updates) :
        dn(array_selected = array_selected, dev_num = dev_num_A, 
           rownum = [r], colnum=[c],
              t_prog = t_prog, set_bias = pos_bias, set_bias_set= set_bias_set)
         
        G_down = read_G(array_selected = array_selected, dev_num=dev_num_A, rownum = [r], colnum = [c], 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1)
 
        lists.append(G_down[0])


print(lists)
time_experiment = time.strftime("%Y%m%d_%H%M%S")

plt.figure(dpi=200)
plt.plot(lists)
plt.xlabel("# or read")
plt.ylabel("Conductance(S)")

plt.savefig("C:/Users/RPU/Desktop/JMLee_measurements/241224_updatecheck/{}_{}_{}up_{}down_{}.png".format(r,c,updates,updates,time_experiment))

df_G = pd.DataFrame(lists)
df_G.to_csv("C:/Users/RPU/Desktop/JMLee_measurements/241224_updatecheck/{}_{}_{}up_{}down_G_{}.csv".format(r,c,updates,updates,time_experiment))

#%%
#update check

#time_experiment = time.strftime("%Y%m%d_%H%M")
#pathname="C:/Users/RPU/Desktop/JMLee_measurements/241213_update_check/"
#os.makedirs(pathname, exist_ok=True)
#
#plt.figure(dpi=200)
#plt.scatter(np.arange(0,numberofupdates,1),test)
#plt.plot(np.arange(0,numberofupdates,1),test)
#plt.xlabel("# of read")
#plt.ylabel("Normalized weight")
#plt.title('arr2_device_{}_{}_down_{}_{}'.format(row_list_C[0],col_list_C[0],numberofupdates,time_experiment))
#plt.savefig(pathname+'device_{}_{}_{}.png'.format(row_list_C[0],col_list_C[0], time_experiment))
#
#df_test = pd.DataFrame(test)
#df_test.to_csv(pathname+'arr2_device_{}_{}_down_{}_{}.csv'.format(row_list_C[0],col_list_C[0],numberofupdates,time_experiment))

    
#%%

#4. real demonstration start - parameter values assign

imp_vars["dataset_params"] = dataset_params
#training parameters
## means fixed

train_params = dict(
    mode = 'hardware',
    n_layer = 1, ##
    epoch = 4, 
    transfer_freq = 5 ,#ACTUALLY IT IS TRANSFER PERIOD :-)
    beta = 0.5, ##
    tiki_taka_on = 4, ##
    chopper_prob = 0.05, #0.02 0.05 #0.02 #0.1
    num_of_read = 1 ##S
    )

lr_params = { "decay_on" : False, ##
             "decay_freq" : 3, ##
             "lrH" : 0.3, #0.2
             "lrA" : 1,
             "lr" : 0.1}  #0.4 #0.01

imp_vars["lr_params"] = lr_params
imp_vars["train_params"] = train_params

# if train_params["mode"] == 'software':
#         imp_vars["device_params"] = { 
#                                         "dev_C1": digital_C1.print_info(),
#                                         "dev_A1": digital_A1.print_info(),
#                                         "sym_A": sym_A.tolist(),
#                                         "sym_C": sym_C.tolist(),
#                                         }

# target_weight, xj = create_dataset(Numofweight,Numofdata)

##################################################

n_epochs = train_params["epoch"]
ttv=train_params["tiki_taka_on"]
mode = train_params["mode"]
num_of_read=train_params["num_of_read"] ## how many times to read to get results
transfer_freq= train_params["transfer_freq"] 
beta = train_params["beta"]
chopper_probability = train_params["chopper_prob"]
lrH = lr_params["lrH"]
lrA = lr_params["lrA"]
lr = lr_params["lr"]
hasdecay = lr_params["decay_on"]
lr_params=lr_params
train_params = train_params

#SP_matrix_A_= sym_A
#SP_matrix_C = sym_C

if mode == 'software' :
    simulation  = 1

##################################################

if mode == 'hardware':
    m_A1 = 'matrix A1'
    m_C1 = 'matrix C1'

elif mode == 'software':
    m_A1 = 'digital A1'
    m_C1 = 'digital C1'

# rows_A, dev_num_A, cols_A, array_A = Config_array_device(m_A1)
# rows_C, dev_num_C, cols_C, array_C = Config_array_device(m_C1)  
    
#%%
def STR(x, d, learning_rate, dw_min, BL):
    abs_x = np.abs(x)
    abs_d = np.abs(d)

    Prob_x = np.sqrt(learning_rate/(BL*dw_min)) * abs_x
    Prob_d = np.sqrt(learning_rate/(BL*dw_min)) * abs_d

    if Prob_x > 1:
        Prob_x = 1
    if Prob_d > 1:
        Prob_d = 1

    STR_x = np.random.choice([0, 1], size = BL, p = [1 - Prob_x, Prob_x])
    STR_d = np.random.choice([0, 1], size = BL, p = [1 - Prob_d, Prob_d])

    nou = 0

    for i in range(BL):
        if STR_x[i] == 1 and STR_d[i] == 1:
            nou += 1

    if np.sign(x) == np.sign(d):
        return nou, -1
    else:
        return nou, 1
    
#demonstration main code

num_row = len(row_list_C)#5
num_col = len(col_list_C)#5

chop_counter1 = np.zeros((num_row,num_col))
switch_chopper1 = np.zeros((num_row,num_col))
numofupdates = np.zeros((num_row,num_col))
break_flag = np.zeros((num_row, num_col), dtype=bool)
working_device = ~break_flag

H = np.zeros((num_row,num_col))
average_mean = np.zeros((num_row,num_col))
past_mean = np.zeros((num_row,num_col))
C = np.zeros((num_row,num_col))
C_final = np.zeros((num_row,num_col))
A = np.zeros((num_row,num_col))
chopper_sign_C1= np.ones((num_row,num_col))
nou_arr = np.zeros((num_row,num_col))
direction_arr = np.zeros((num_row,num_col))

loss = np.zeros((num_row,num_col))

w_list = []

logs = [[[] for _ in range(num_col)] for _ in range(num_row)]  # Logs for each element
simulation = 0

A_pulse_up = np.zeros((num_row,num_col))
A_pulse_down = np.zeros((num_row,num_col))

C_pulse_up = np.zeros((num_row,num_col))
C_pulse_down = np.zeros((num_row,num_col))

#initial read
c_initial = read_device(array_selected = array_selected, dev_num=dev_num_C, rownum = row_list_C, colnum = col_list_C, 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1
                ,G_sym = G_sym_arr_C, G_med = G_med_arr_C, G_max = G_max_arr_C, G_min = G_min_arr_C,ref=True)

a_initial = read_device(array_selected = array_selected, dev_num=dev_num_A, rownum = row_list_A, colnum = col_list_A, 
                t_read = t_read, v_read = read_bias, read_fwd_bias_set = read_fwd_bias_set ,num_of_reads=1
                ,G_sym = G_sym_arr_A, G_med = G_med_arr_A, G_max = G_max_arr_A, G_min = G_min_arr_A,ref=False)

print("Normalized C:", c_initial)
print("Normalized A:", a_initial)

check_index = 0

for i_epoch in range(n_epochs) :
#    if np.all(break_flag) :
#        print("All positions converged. Stopping computation.")
#        break
    for i_data in range(len(xj)) : #len(xj)      
        x_in = xj[i_data]
        #noise_in = noise[i_data]
        
       # working_device = ~break_flag
        
        #1. forward C
        if simulation : 
            C = devC.read() #read weight
            target_y = x_in * target_weight_array
            y0 = x_in * C
            delta = y0 - target_y
            
            delta *= working_device
            
        else : #for hardware demo - serial read
             C1 = read_device(array_selected = array_selected, dev_num=dev_num_C, 
                             rownum = row_list_C, colnum = col_list_C, 
                              t_read = t_read, v_read = read_bias, 
                           read_fwd_bias_set = read_fwd_bias_set ,
                           num_of_reads=1,G_sym = G_sym_arr_C, G_med = G_med_arr_C, 
                           G_max = G_max_arr_C, G_min = G_min_arr_C,ref=True)
             
             #time.sleep(5e-3)
             
             target_y = x_in * target_weight_array #original code
             #target_y = (x_in * target_weight_array) + noise_in #gaussian noise add version
             
             y0 = x_in * C1
             #delta = target_y - y0 #wrong code
             delta = y0 - target_y #122024
             #delta = np.array([[-0.25]]) #value for mechanism demo
             
             delta *= working_device
             
             percentage_error = abs((target_weight_array - C_final)/target_weight_array)
#             #percentage_error = abs((target_weight_array - C_final) / target_weight_array)
#             
#             numofupdates[percentage_error >= 0.7] = 7 #7
#             numofupdates[(percentage_error < 0.7) & (percentage_error >= 0.4)] = 5 #5
#             numofupdates[(percentage_error < 0.4) & (percentage_error >= 0.1)] = 3 #3
#             numofupdates[(percentage_error < 0.1) & (percentage_error > 0)] = 1 #1
#             numofupdates[percentage_error == 0] = 0
            
        #2. update A
        if simulation :
            P = chopper_sign_C1 * x_in * delta

            pot_A = (P > 0) & working_device
            dep_A = (P < 0) & working_device
            
            rows_pot_A,cols_pot_A = np.where(pot_A)
            rows_dep_A,cols_dep_A = np.where(dep_A)
            
            for row, col in zip(rows_pot_A, cols_pot_A):
                devA.update('pot', row, col)
                
            for row, col in zip(rows_dep_A, cols_dep_A) :
                devA.update('dep',row, col)
            
            A = devA.read()
            
            A *= working_device
            
        else : #for hardware demo
            #P = chopper_sign_C1 * x_in * delta * lrA
            for i in range(len(row_list_A)) :
                for j in range(len(col_list_A)) :
                    nou,direction = STR(chopper_sign_C1[i][j] * x_in, delta[i][j],lr,1/NOS_arr_A[i][j],10)
                    nou_arr[i,j] = nou
                    direction_arr[i,j] = direction
            
            #pot_A = (P > 0) & working_device
            #dep_A = (P < 0) & working_device
            
            pot_A = (direction_arr > 0) & working_device
            dep_A = (direction_arr < 0) & working_device
            
            rows_pot_A, cols_pot_A = np.where(pot_A)
            rows_dep_A, cols_dep_A = np.where(dep_A)
            
 
            for row, col in zip(rows_pot_A, cols_pot_A) :
               # updates_pot = int(numofupdates[row, col])
        
                #NEED TO CHANGE FOR ARRAY
                for i in range(int(nou_arr[row, col])) :
                    
                    up(array_selected = array_selected, dev_num = dev_num_A, 
                       rownum = [row_list_A[row]], colnum=[col_list_A[col]],
                     t_prog = t_prog, reset_bias = reset_bias_A, reset_bias_set=reset_bias_set)
                                       
                    #time.sleep(5e-3)
                    
                A_pulse_up[row, col] = int(nou_arr[row, col])
                A_pulse_down[row, col] = 0
                
            
            for row, col in zip(rows_dep_A, cols_dep_A) :
                #updates_dep = int(numofupdates[row,col])
                #print(row,col)
                
                #NEED TO CHANGE FOR ARRAY
                for i in range(int(nou_arr[row,col])) :
                    dn(array_selected = array_selected, dev_num=dev_num_A, 
                       rownum = [row_list_A[row]], colnum=[col_list_A[col]], 
                      t_prog = t_prog, set_bias = set_bias_A, set_bias_set=set_bias_set)
                    
                    
                    #time.sleep(5e-3)
                    
                A_pulse_up[row, col] = 0
                A_pulse_down[row, col] = int(nou_arr[row, col])
                
            #time.sleep(5e-3)
            
            A = read_device(array_selected = array_selected, dev_num=dev_num_A, 
                            rownum = row_list_A, colnum = col_list_A, 
                             t_read = t_read, v_read = read_bias, 
                          read_fwd_bias_set = read_fwd_bias_set ,
                          num_of_reads=1,G_sym = G_sym_arr_A, G_med = G_med_arr_A, 
                          G_max = G_max_arr_A, G_min = G_min_arr_A,ref=False)
            
            #A += A_read
            
        #3. H accumulation
        if simulation :
            H += chopper_sign_C1 * lrH * (A - past_mean) * working_device
            average_mean = (1-beta) * average_mean + beta * A

            pot_C = (H > 1) & working_device
            dep_C = (H < -1) & working_device 
            
            rows_pot_C,cols_pot_C = np.where(pot_C)
            rows_dep_C,cols_dep_C = np.where(dep_C)
            
            for row, col in zip(rows_pot_C, cols_pot_C):
                devC.update('pot', row, col)
                
            for row, col in zip(rows_dep_C, cols_dep_C) :
                devC.update('dep',row, col)
            
            C = devC.read()
            C_final = np.where(pot_C|dep_C,C,C_final)
            H = np.where(pot_C|dep_C,0,H)
        
            chop_period = 1/chopper_probability
            chop_counter1 = (chop_counter1+ 1) % chop_period
            switch_chopper1 = chop_counter1 == 0
            
            chopper_sign_C1[switch_chopper1] *= -1
            past_mean[switch_chopper1 & working_device] = average_mean[switch_chopper1 & working_device]
            average_mean[switch_chopper1 & working_device] = 0
                    
        else : #for hardware demo
            if (check_index % transfer_freq == 0) & (check_index > 1):
                
                H += chopper_sign_C1 * lrH * (A - past_mean) * working_device
                average_mean = (1-beta) * average_mean + beta * A
    
                pot_C = (H > 1) & working_device #1
                dep_C = (H < -1) & working_device #-1
              
                rows_pot_C,cols_pot_C = np.where(pot_C)
                rows_dep_C,cols_dep_C = np.where(dep_C)
              
                nou = 1
                for row, col in zip(rows_pot_C, cols_pot_C) :
                    for i in range(nou) :
                        up(array_selected = array_selected, dev_num = dev_num_C, 
                           rownum = [row_list_C[row]], colnum=[col_list_C[col]],
                         t_prog = t_prog, reset_bias = reset_bias_C, reset_bias_set=reset_bias_set)
                                                
                        #time.sleep(5e-3)
                        
                    C_pulse_up[row, col] = nou
                    C_pulse_down[row, col] = 0
                        
                
                for row, col in zip(rows_dep_C, cols_dep_C) :
                    if (row == 1) and (col == 1) :
                        set_bias_C += 0.1
                    
                    for i in range(nou) :
                        dn(array_selected = array_selected, dev_num=dev_num_C, 
                           rownum = [row_list_C[row]], colnum=[col_list_C[col]], 
                          t_prog = t_prog, set_bias = set_bias_C, set_bias_set=set_bias_set)
                        
                        #time.sleep(5e-3)
                        
                    C_pulse_up[row, col] = 0
                    C_pulse_down[row, col] = nou
                    
                #time.sleep(5e-3)
                
                C = read_device(array_selected = array_selected, dev_num=dev_num_C, 
                                    rownum = row_list_C, colnum = col_list_C, 
                                     t_read = t_read, v_read = read_bias, 
                                  read_fwd_bias_set = read_fwd_bias_set ,
                                  num_of_reads=1,G_sym = G_sym_arr_C, G_med = G_med_arr_C, 
                                  G_max = G_max_arr_C, G_min = G_min_arr_C,ref=True)
                
                
                #time.sleep(5e-3)
                
                #w_list.append(C[0][0]) #for 1by1 demo
#                w_list.append(C)
#                
#                #average = sum(w_list)/len(w_list) #for 1by1 demo
#                average = sum(w_list)/len(w_list)
#                
#                #C_AVG = np.array([[average]]) #for 1by1 demo
#                C_AVG = average
                
                C_final = np.where(pot_C|dep_C,C,C_final) #ORIGIINAL CODE
                #C_final = np.where(pot_C|dep_C,C_AVG,C_final)
                H = np.where(pot_C|dep_C,0,H)
                
                loss = 0.5 * ((target_weight_array - C_final) ** 2) #for 1 by 1 demo
                
#                if np.any(C_final != 0):  #for 1 by 1 demo
#                    w_list = [] #for 1 by 1 demo
                
#                if np.any(C_final != 0 & (pot_C == np.array(False))) :
#                    for i in range(len(w_list)):  # Iterate through all arrays in w_list
#                       w_list[i][C_final != 0] = 0
        
            chop_period = 1/chopper_probability
            chop_counter1 = (chop_counter1+ 1) % chop_period
            switch_chopper1 = chop_counter1 == 0
            
            chopper_sign_C1[switch_chopper1] *= -1
            past_mean[switch_chopper1 & working_device] = average_mean[switch_chopper1 & working_device]
            average_mean[switch_chopper1 & working_device] = 0
            
            check_index += 1     
        
        #if simulation: 
        #percentage error < 5% -> error calc
#        break_condition = (
#               np.abs(target_weight_array - C_final) / np.abs(target_weight_array)
#           ) * 100 < 5
#        
#        break_condition = (percentage_error < 0.05) &( np.abs(H) > 0.5 )
#        break_flag = np.logical_or(break_flag, break_condition)
               
        if simulation: 
            for row_C in range(num_row):
               for col_C in range(num_col):
                   if not break_flag[row_C, col_C]: 
                        log_val = {
                            "row_C" : row_C,
                            "col C" : col_C,
                            "row A" : row_A,
                            "col_A" : col_A,
                            "epoch" :i_epoch,
                            "x": x_in,
                            "target_w" : target_weight_array[row_C, col_C],
                            "W": C[row_C,col_C],
                            "C_final" : C_final[row_C,col_C],
                            "target_y" :target_y,
                            "y_0": y0,
                            "delta" : delta,
                            "A": A[row_C,col_C],
                            "H": H[row_C,col_C],
                            "average_mean": average_mean[row_C,col_C],
                            "past_mean": past_mean[row_C,col_C],
                            "chopper_sign_1":chopper_sign_C1[row_C,col_C],
                            "switch_chopper1": switch_chopper1[row_C,col_C],
                            "chopper probability": chopper_probability,
                            "lrH" : lrH
                            }
                    
                        logs[row_C][col_C].append(log_val)
                        
                        print("Epoch: {}".format(i_epoch), log_val)
        
            if check_index % 100 == 0:
                 i_epoch += 1
    
        else : #for hardware demo
            for row_C in range(num_row):
               for col_C in range(num_col):
                   if not break_flag[row_C, col_C]: 
                        log_val = {
                            "check index" :check_index,
                            "row_C" : row_list_C[row_C], 
                            "col C" : col_list_C[col_C], 
                            "row A" : row_list_A[row_C], 
                            "col_A" : col_list_A[col_C], 
                            "epoch" :i_epoch,
                            "x": x_in,
                            "target_w" : target_weight_array[row_C, col_C],
                            "C1" :C1[row_C,col_C],
                            "W": C[row_C,col_C],
                            "C_pulse_up" : C_pulse_up[row_C,col_C],
                            "C_pulse_down" : C_pulse_down[row_C,col_C],
                            "C_final" : C_final[row_C,col_C],
                            "target_y" :target_y[row_C,col_C],
                            "y_0": y0[row_C,col_C],
                            "delta" : delta[row_C,col_C],
                            "percentage error":percentage_error[row_C,col_C],
                            "loss" : loss[row_C, col_C],
                            "A": A[row_C,col_C],
                            "A_pulse_up" : A_pulse_up[row_C,col_C],
                            "A_pulse_down" : A_pulse_down[row_C,col_C],
                            #"P":P[row_C,col_C],
                            #"numberofupdates":numofupdates[row_C,col_C],
                            "H": H[row_C,col_C],
                            "average_mean": average_mean[row_C,col_C],
                            "past_mean": past_mean[row_C,col_C],
                            "chopper_sign_1":chopper_sign_C1[row_C,col_C],
                            "switch_chopper1": switch_chopper1[row_C,col_C],
                            "chopper probability": chopper_probability,
                            "lrH" : lrH,
                            "lrA" : lrA,
                            "lr" : lr
                            }
                    
                        logs[row_C][col_C].append(log_val)
                        
                        print("Epoch: {}".format(i_epoch), log_val)

final_weight_array = C_final

C_positions = [(i, j) for i in range(num_row) for j in range(num_col)]

for row_C, col_C in C_positions:
    # Save logs to CSV
    pathname="C:/Users/RPU/Desktop/JMLee_measurements/241224_demo_trial/"
    time_experiment = time.strftime("%Y%m%d_%H%M%S")
    
    df = pd.DataFrame(logs[row_C][col_C])
    df.to_csv(pathname + f"C_({row_C},{col_C})_weight_programming_logs_ttv{train_params['tiki_taka_on']}_{time_experiment}.csv",index=False)
    
    #plt.figure(figsize=(9, 6),dpi=200) #for 500 epochs
    #plt.figure(figsize=(12,6),dpi=200) #for 1000 epochs
    plt.figure(1, figsize=(15,6),dpi=200) #for 1500 epochs
    plt.plot([log["W"] for log in logs[row_C][col_C]], label='Analog weight', color='orange')
    plt.plot([log["A"] for log in logs[row_C][col_C]], label='Analog gradient', color='red')
    plt.plot([log["H"] for log in logs[row_C][col_C]], label='Hidden weight', color='green')
    plt.plot([log["past_mean"] for log in logs[row_C][col_C]], label='Reference mean', color='black')
    plt.plot([log["average_mean"] for log in logs[row_C][col_C]], label='Average mean', color='blue')
     
    #plot
    x_values = range(len(logs[row_C][col_C]))
    x_scaled = [x/len(xj) for x in x_values]
    plt.xticks(x_values[::200], [int(val) for val in x_scaled[::200]])

    plt.xlabel("Epochs")
    plt.ylabel("Normalized weight")
    plt.ylim([-1.5,1.5])
    plt.title("Target weight:{}_row_{}_col_{}_{}".format(target_weight_array[row_C,col_C],row_C,col_C,time_experiment))
    plt.grid(True, linestyle='--')
    plt.legend(fontsize=6, loc='lower left')
    plt.tight_layout()
    plt.savefig(pathname+"Target weight_{}_row_{}_col_{}_{}.png".format(target_weight_array[row_C,col_C],row_C,col_C,time_experiment))
    plt.show()
    plt.close()
    
    plt.figure(2,figsize=(15,6),dpi=200) 
    plt.plot([log["A_pulse_up"] for log in logs[row_C][col_C]], label='A_pulse_up', color='blue')
    plt.plot([log["A_pulse_down"] for log in logs[row_C][col_C]], label='A_pulse_down', color='red')
    plt.plot([log["C_pulse_up"] for log in logs[row_C][col_C]], label='C_pulse_up', color='green')
    plt.plot([log["C_pulse_down"] for log in logs[row_C][col_C]], label='C_pulse_down', color='orange')
    
    plt.xlabel("Epochs")
    plt.ylabel("# of updates")
    plt.title("Update pulse check_{}".format(time_experiment))
    plt.grid(True, linestyle='--')
    plt.legend(fontsize=6, loc='lower left')
    plt.tight_layout()
    plt.savefig(pathname+"Update pulse check_{}.png".format(time_experiment))
    plt.show()          
    plt.close()
             
    
    #last weight append
    final_weight_array[row_C][col_C] = logs[row_C][col_C][-1]["W"]

with open(os.path.join(pathname, "imp_vars_{}.txt".format(time_experiment)), "w") as outfile:
    json.dump(imp_vars, outfile)

#%%

#weight mapping accuracy with heatmap
    
import seaborn as sns

final_weight_array = np.round(final_weight_array, 2) #소수점 둘째 자리에서 반올림

print("target weight array: ",target_weight_array)
print("final weight array: ",final_weight_array)

# Avoid division by zero: handle target_weight_array == 0
safe_target_weight_array = np.where(target_weight_array == 0, np.nan, target_weight_array)

print("safe weight array: ",safe_target_weight_array)

# Calculate accuracy
# accuracy_matrix = (
#     1 - np.abs(final_weight_array - target_weight_array) / np.abs(safe_target_weight_array)) * 100
accuracy_matrix = np.abs(final_weight_array-target_weight_array) ** 2

# Replace NaN (caused by division by zero) with 0 accuracy
accuracy_matrix = np.nan_to_num(accuracy_matrix, nan=0.0)

MSE = np.mean((final_weight_array - target_weight_array) ** 2)
std_dev = np.std(final_weight_array-target_weight_array)

# calculate MSE, standard deviation
print("Mean square error:")
print(MSE)

print("standard deviation: ")
print(std_dev)

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    accuracy_matrix,
    annot=True,
    fmt=".2f",
    cmap="Spectral",
    cbar=True,
    xticklabels=[f"Col {i}" for i in range(accuracy_matrix.shape[1])],
    yticklabels=[f"Row {i}" for i in range(accuracy_matrix.shape[0])],
)
plt.title("Accuracy Matrix: Target vs Final Weights")
plt.xlabel("Columns")
plt.ylabel("Rows")

plt.savefig(pathname+"{}x{}_Final Accuracy Matrix.png".format(num_row,num_col))
plt.tight_layout()
plt.show()

             
             
             
             
             
             
