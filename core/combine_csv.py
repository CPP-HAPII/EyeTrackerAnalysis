import pandas as pd
import math
import os
import time
from core import utils

def combine_csv(path_to_folder):
    root = path_to_folder
    dirlist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    dirlist = [x for x in dirlist if "NAH" not in x]
    dirlist = [x for x in dirlist if "User" in x]
    combine_all_per_aoi(path_to_folder, dirlist)
    combine_all_per_page(path_to_folder, dirlist)
    combine_all_per_aoipage(path_to_folder, dirlist)    

def combine_all_per_aoi(path_to_folder, dirlist):
    aoi_dataframes = []
    for x in dirlist:
        path_to_combined_AOI_file = path_to_folder + x + "/combined_aoi.csv"
        user_aoi_df = pd.read_csv(path_to_combined_AOI_file, sep=",", index_col=False)
        aoi_dataframes.append(user_aoi_df)

    all_users_aoi = pd.concat(aoi_dataframes)
    all_users_aoi_english = all_users_aoi[all_users_aoi.AOILanguage == "English"]
    all_users_aoi_chinese = all_users_aoi[all_users_aoi.AOILanguage == "Chinese"]
    all_users_aoi_spanish = all_users_aoi[all_users_aoi.AOILanguage == "Spanish"]

    all_users_aoi.to_csv(path_to_folder + "/Combined/all_users_aoi all.csv")
    all_users_aoi_english.to_csv(path_to_folder + "/Combined/all_users_aoi english.csv")
    all_users_aoi_chinese.to_csv(path_to_folder + "/Combined/all_users_aoi spanish.csv")
    all_users_aoi_spanish.to_csv(path_to_folder + "/Combined/all_users_aoi chinese.csv")

def combine_all_per_page(path_to_folder, dirlist):
    chinese_users = []
    spanish_users = []

    user_df = pd.read_csv(path_to_folder + "users.csv", sep=",", index_col=False)

    for index, row in user_df.iterrows():
        if(row["Language"] == "Chinese"):
            chinese_users.append(row["Participant"])
        elif(row["Language"] == "Spanish"):
            spanish_users.append(row["Participant"])        
    
    all_page_dataframes = []
    chinese_page_dataframes = []
    spanish_page_dataframes = []
    for x in dirlist:
        path_to_combined_page_file = path_to_folder + x + "/combined_page.csv"
        user_page_df = pd.read_csv(path_to_combined_page_file, sep=",", index_col=False)
        all_page_dataframes.append(user_page_df)
        if user_page_df["userID"].iloc[0] in chinese_users:
            chinese_page_dataframes.append(user_page_df)
        elif user_page_df["userID"].iloc[0] in spanish_users:
            spanish_page_dataframes.append(user_page_df)

    all_users_page = pd.concat(all_page_dataframes)
    all_users_page_chinese = pd.concat(chinese_page_dataframes)
    all_users_page_spanish = pd.concat(spanish_page_dataframes)

    all_users_page.to_csv(path_to_folder + "/Combined/all_users_page all.csv")
    all_users_page_chinese.to_csv(path_to_folder + "/Combined/all_users_page chinese.csv")
    all_users_page_spanish.to_csv(path_to_folder + "/Combined/all_users_page spanish.csv")

def combine_all_per_aoipage(path_to_folder, dirlist):
    chinese_users = []
    spanish_users = []

    user_df = pd.read_csv(path_to_folder + "users.csv", sep=",", index_col=False)

    for index, row in user_df.iterrows():
        if(row["Language"] == "Chinese"):
            chinese_users.append(row["Participant"])
        elif(row["Language"] == "Spanish"):
            spanish_users.append(row["Participant"])        
    
    all_aoipage_dataframes = []
    chinese_aoipage_dataframes = []
    spanish_aoipage_dataframes = []
    for x in dirlist:
        path_to_combined_page_file = path_to_folder + x + "/combined_aoipage.csv"
        user_aoipage_df = pd.read_csv(path_to_combined_page_file, sep=",", index_col=False)
        all_aoipage_dataframes.append(user_aoipage_df)
        if user_aoipage_df["userID"].iloc[0] in chinese_users:
            chinese_aoipage_dataframes.append(user_aoipage_df)
        elif user_aoipage_df["userID"].iloc[0] in spanish_users:
            spanish_aoipage_dataframes.append(user_aoipage_df)

    all_users_page = pd.concat(all_aoipage_dataframes)
    all_users_page_chinese = pd.concat(chinese_aoipage_dataframes)
    all_users_page_spanish = pd.concat(spanish_aoipage_dataframes)

    all_users_page.to_csv(path_to_folder + "/Combined/all_users_aoipage all.csv")
    all_users_page_chinese.to_csv(path_to_folder + "/Combined/all_users_aoipage chinese.csv")
    all_users_page_spanish.to_csv(path_to_folder + "/Combined/all_users_aoipage spanish.csv")