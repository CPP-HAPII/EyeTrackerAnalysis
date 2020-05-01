import pandas as pd
import math
import os
import time
from core import utils

def calculate_switch(df):
    count = [0 for i in range(4)] 
    total = [0 for i in range(4)]
    switch0 = []
    switch1 = []
    switch2 = []
    switch3 = []
    for index, row in df.iterrows():
        if row["Order"] == 0:
            count[0] += 1
            total[0] += row["Duration"]
            switch0.append(row["Duration"])
        elif row["Order"] == 1:
            count[2] += 1
            total[2] += row["Duration"]
            switch2.append(row["Duration"])
        elif row["Order"] == 2:
            if row["TaskPage"] < 3:
                count[0] += 1
                total[0] += row["Duration"]
                switch0.append(row["Duration"])            
            else:
                count[2] += 1
                total[2] += row["Duration"]
                switch2.append(row["Duration"])
        elif row["Order"] == 3:
            if row["TaskPage"] >= 3:
                count[0] += 1
                total[0] += row["Duration"]
                switch0.append(row["Duration"])
            else:
                count[2] += 1
                total[2] += row["Duration"]
                switch2.append(row["Duration"])
        elif row["Order"] == 4:
            if row["TaskPage"] % 2 == 0:
                count[1] += 1
                total[1] += row["Duration"]
                switch1.append(row["Duration"])
            else:
                count[3] += 1
                total[3] += row["Duration"]
                switch3.append(row["Duration"])
    for x in range(0,4):
        print (total[x]/count[x])

    print ("FOR CH/SP -> CH/SP: ")
    for elem in switch0:
        print (elem)
    print ("FOR CH/SP -> Eng: ")
    for elem in switch1:
        print (elem)
    print ("FOR Eng -> Eng: ")
    for elem in switch2:
        print (elem)
    print ("FOR Eng -> CH/SP: ")
    for elem in switch3:
        print (elem)

def calculate_switch_prep(file):
    aoi_df = pd.read_csv(file, sep=",", index_col=False)
    
    # FOR CHINESE USERS, L1 ENGLISH
    aoi_df_ce = aoi_df.loc[(aoi_df['userID'] == 5385) | (aoi_df['userID'] == 1338) | (aoi_df['userID'] == 671)]
    print("English L1, Chinese l2")
    calculate_switch(aoi_df_ce)

    # FOR CHINESE USERS, L1 CHINESE
    aoi_df_cc = aoi_df.loc[(aoi_df['userID'] == 3545) | (aoi_df['userID'] == 132) | (aoi_df['userID'] == 1586) | (aoi_df['userID'] == 2068) | (aoi_df['userID'] == 2591)]
    print("English L2, Chinese l1")
    calculate_switch(aoi_df_cc)    

    # FOR SPANISH USERS, L1 ENGLISH
    aoi_df_se = aoi_df.loc[(aoi_df['userID'] == 5890) | (aoi_df['userID'] == 2899) | (aoi_df['userID'] == 7734) | (aoi_df['userID'] == 1855) | (aoi_df['userID'] == 1572)]
    print("English L1, Spanish l2")
    calculate_switch(aoi_df_se)        

    # FOR SPANISH USERS, L1 SPANISH
    aoi_df_ss = aoi_df.loc[(aoi_df['userID'] == 2128) | (aoi_df['userID'] == 2156) | (aoi_df['userID'] == 5492) | (aoi_df['userID'] == 5689) | (aoi_df['userID'] == 4799) | (aoi_df['userID'] == 2934) | (aoi_df['userID'] == 6853)]
    print("English L2, Spanish l1")
    calculate_switch(aoi_df_ss)            

    # FOR SPANISH USERS, L1 BOTH
    aoi_df_b = aoi_df.loc[(aoi_df['userID'] == 6673) | (aoi_df['userID'] == 6515) | (aoi_df['userID'] == 6965) | (aoi_df['userID'] == 3816) | (aoi_df['userID'] == 1699) | (aoi_df['userID'] == 452) | (aoi_df['userID'] == 2929)]    
    print("Both English Spanish L1")
    calculate_switch(aoi_df_b)  