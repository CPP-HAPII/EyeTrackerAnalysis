import pandas as pd
import math
import os
import time
from core import utils

def calculate_switch(df, type):
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
    
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df4 = pd.DataFrame()

    df1["CH/SP -> CH/SP:"] = switch0
    df2["CH/SP -> Eng:"] = switch1
    df3["Eng -> Eng:"] = switch2
    df4["Eng -> CH/SP:"] = switch3
    
    combined_df = pd.concat([df1,df2,df3,df4], axis=1)
    combined_df.to_csv("analysis_results/comparison_results/by_switch/" + type + ".csv", index=False)

def calculate_switch_prep(file):
    aoi_df = pd.read_csv(file, sep=",", index_col=False)
    proficiency_df = pd.read_csv("user_study_data/users_proficiency.csv", sep=",", index_col=False)

    c2e1 = proficiency_df["c2e1"].tolist()
    c1e2 = proficiency_df["c1e2"].tolist()
    s2e1 = proficiency_df["s2e1"].tolist()
    s1e2 = proficiency_df["s1e2"].tolist()
    s1e1 = proficiency_df["s1e1"].tolist()

    # FOR CHINESE USERS, L1 ENGLISH
    aoi_df_ce = aoi_df.loc[aoi_df['userID'].isin(c2e1)]  
    calculate_switch(aoi_df_ce, "Chinese L2, English L1")

    # FOR CHINESE USERS, L1 CHINESE
    aoi_df_cc = aoi_df.loc[aoi_df['userID'].isin(c1e2)]
    calculate_switch(aoi_df_cc, "Chinese L1, English L2")    

    # FOR SPANISH USERS, L1 ENGLISH
    aoi_df_se = aoi_df.loc[aoi_df['userID'].isin(s2e1)]
    calculate_switch(aoi_df_se, "Spanish L2, English L1")        

    # FOR SPANISH USERS, L1 SPANISH
    aoi_df_ss = aoi_df.loc[aoi_df['userID'].isin(s1e2)]
    calculate_switch(aoi_df_ss, "Spanish L1, English L2")            

    # FOR SPANISH USERS, L1 BOTH
    aoi_df_b = aoi_df.loc[aoi_df['userID'].isin(s1e1)]
    calculate_switch(aoi_df_b, "Spanish L1, English L1")  