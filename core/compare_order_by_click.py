import pandas as pd
import math
import os
import time
from core import utils

def compare_order_by_click(file):
    aoi_df = pd.read_csv(file, sep=",", index_col=False)

    duration_list = []
    previous_time = 0
    for index, row in aoi_df.iterrows():
        time_in = row["In"]
        minutes,seconds = time_in.split(":")
        time_in = int(minutes) * 60 + float(seconds)
        if row["TaskPage"] == 0:
            duration_list.append(0)
        else:
            if time_in - previous_time < 0:
                duration_list.append(time_in - previous_time + 3600)
            else:
                duration_list.append(time_in - previous_time)
        previous_time = time_in
    aoi_df["Duration"] = duration_list

    page_list = []
    for x in range(1,31):
        for y in range(0,6):
            page_list.append(x)

    page_list2 = page_list
    for x in range(0,26):
        page_list = page_list + page_list2

    aoi_df["Page"] = page_list

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
    for index, row in aoi_df.iterrows():
        id = row['userID']
        page = row['Page']
        order_list.append(order_dict[id,page])
    
    aoi_df['Order'] = order_list

    user_df = pd.read_csv("user_study_data/users.csv", sep=",", index_col=False)
    chinese_users = []
    spanish_users = []

    for index, row in user_df.iterrows():
        if(row["Language"] == "Chinese"):
            chinese_users.append(row["Participant"])            
        elif(row["Language"] == "Spanish"):
            spanish_users.append(row["Participant"])         
    
    language_list = []
    for index, row in aoi_df.iterrows():
        id = row['userID']
        if row["Order"] == 0:
            if id in  spanish_users:
                language_list.append("Spanish")
            else:
                language_list.append("Chinese")
        elif row["Order"] == 1:
            language_list.append("English")
        elif row["Order"] == 2:
            if row["TaskPage"] < 3:
                if id in spanish_users:
                    language_list.append("Spanish")
                else:
                    language_list.append("Chinese")
            else:
                language_list.append("English")
        elif row["Order"] == 3:
            if row["TaskPage"] >= 3:
                if id in spanish_users:
                    language_list.append("Spanish")
                else:
                    language_list.append("Chinese")
            else:
                language_list.append("English")
        elif row["Order"] == 4:
            if row["TaskPage"] % 2 == 0:
                if id in spanish_users:
                    language_list.append("Spanish")
                else:
                    language_list.append("Chinese")
            else:
                language_list.append("English")                  
    
    aoi_df["Language"] = language_list
    aoi_df = aoi_df[["userID", "Duration", "Page", "Order", "Language", "TaskPage"]]
    aoi_df = aoi_df.loc[aoi_df['Duration'] != 0]

    chineseCount = [0 for i in range(5)] 
    chineseTotal = [0 for i in range(5)]
    englishCount = [0 for i in range(5)]
    englishTotal = [0 for i in range(5)]
    spanishCount = [0 for i in range(5)]
    spanishTotal = [0 for i in range(5)]

    for index, row in aoi_df.iterrows():
        language = row['Language']
        order = row['Order']
        duration = row['Duration']

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
        if englishCount[x] != 0:
            print ("English order " + str(x) + " =")
            print (englishTotal[x]/englishCount[x])
    for x in range(0, 5):
        if chineseCount[x] != 0:
            print ("Chinese order " + str(x) + " =")
            print (chineseTotal[x]/chineseCount[x])
    for x in range(0, 5):            
        if spanishCount[x] != 0:            
            print ("Spanish order " + str(x) + " =")
            print (spanishTotal[x]/spanishCount[x])