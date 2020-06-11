import pandas as pd
import math
import os
import time
from core import utils

def compare_by_relevance(file):
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
    aoi_df = aoi_df[["userID", "Duration", "Page", "Order", "Language", "TaskPage", "Answer"]]
    aoi_df = aoi_df.loc[aoi_df['Duration'] != 0]

    count = 0
    duration = []
    for index, row in aoi_df.iterrows():
        language = row["Language"]
        answer = row["Answer"]

        if language == "Chinese" and answer == 1:
            count += 1
            duration.append(row["Duration"])

    path = "analysis_results/comparison_results/by_relevance/"
    chinese = aoi_df.loc[aoi_df["Language"] == "Chinese"]
    chinese_yes = chinese.loc[chinese["Answer"] == 0]
    chinese_yes.to_csv(path + "Chinese_Relevant.csv", index=False)
    chinese_no = chinese.loc[chinese["Answer"] == 1]
    chinese_no.to_csv(path + "Chinese_Not_Relevant.csv", index=False)

    english = aoi_df.loc[aoi_df["Language"] == "English"]
    english_yes = english.loc[english["Answer"] == 0]
    english_yes.to_csv(path + "English_Relevant.csv", index=False)
    english_no = english.loc[english["Answer"] == 1]
    english_no.to_csv(path + "English_Not_Relevant.csv", index=False)

    spanish = aoi_df.loc[aoi_df["Language"] == "Spanish"]
    spanish_yes = spanish.loc[spanish["Answer"] == 0]
    spanish_yes.to_csv(path + "Spanish_Relevant.csv", index=False)
    spanish_no = spanish.loc[spanish["Answer"] == 1]
    spanish_no.to_csv(path + "Spanish_Not_Relevant.csv", index=False)