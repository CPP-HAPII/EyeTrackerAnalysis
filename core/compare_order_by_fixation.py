import pandas as pd
import math
import os
import time
from core import utils

def compare_order_by_fixation(file):
    aoi_df = pd.read_csv(file, sep=",", index_col=False)
    selected_aoi_df = aoi_df[['userID','Page','Total_Fixation_Duration','AOILanguage']]    

    dirlist = [item for item in os.listdir("user_study_data/") if os.path.isdir(os.path.join("user_study_data/", item))]
    dirlist = [x for x in dirlist if "NAH" not in x]
    dirlist = [x for x in dirlist if "User" in x]

    task_dataframes = []
    for x in dirlist:
        path_to_combined_taskpage = "user_study_data/" + x + "/task_file.csv"
        user_task_df = pd.read_csv(path_to_combined_taskpage, sep=",", index_col=False)
        task_dataframes.append(user_task_df)

    all_users_task = pd.concat(task_dataframes)
    selected_task_df = all_users_task[['userID','Task','Result Order']]

    order_dict = {}
    for index, row in selected_task_df.iterrows():
        id = row['userID']
        page = row['Task']
        order_dict[id,page] = row['Result Order']        

    order_list = []
    for index, row in selected_aoi_df.iterrows():
        id = row['userID']
        page = row['Page']
        order_list.append(order_dict[id,page])
    
    selected_aoi_df['Order'] = order_list

    chineseCount = [0 for i in range(5)] 
    chineseTotal = [0 for i in range(5)]
    englishCount = [0 for i in range(5)]
    englishTotal = [0 for i in range(5)]
    spanishCount = [0 for i in range(5)]
    spanishTotal = [0 for i in range(5)]

    for index, row in selected_aoi_df.iterrows():
        language = row['AOILanguage']
        order = row['Order']
        duration = row['Total_Fixation_Duration']

        if language == "English":
            englishCount[order] += 1
            englishTotal[order] += duration
        elif language == "Spanish":
            spanishCount[order] += 1
            spanishTotal[order] += duration
        elif language == "Chinese":
            chineseCount[order] += 1
            chineseTotal[order] += duration
    
    for x in range(0, 5):
        print ("English order " + str(x) + " =")
        print (englishTotal[x]/englishCount[x])
    for x in range(0, 5):
        print ("Chinese order " + str(x) + " =")
        print (chineseTotal[x]/chineseCount[x])
    for x in range(0, 5):
        print ("Spanish order " + str(x) + " =")
        print (spanishTotal[x]/spanishCount[x])