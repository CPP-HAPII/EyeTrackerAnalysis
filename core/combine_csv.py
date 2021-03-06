import pandas as pd
import math
import os
import time
from core import utils

NUMBER_TO_LMH = {
    1 : "Low",
    2 : "Low",
    3 : "Low",
    4 : "Medium",
    5 : "High"
}

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

    extraList = []
    for index, row in all_users_aoi.iterrows():
        id = row['userID']
        page = row['Page']
        aoi = row['AOI_TYPE']
        extra = str(id) + "-" + str(page) + "-" + aoi
        extraList.append(extra)
    all_users_aoi['Extra'] = extraList    

    all_users_aoi_english = all_users_aoi[all_users_aoi.AOILanguage == "English"]
    all_users_aoi_chinese = all_users_aoi[all_users_aoi.AOILanguage == "Chinese"]
    all_users_aoi_spanish = all_users_aoi[all_users_aoi.AOILanguage == "Spanish"]

    all_users_aoi.to_csv(path_to_folder + "/Combined/all_users_aoi all.csv", index=False)
    all_users_aoi_english.to_csv(path_to_folder + "/Combined/all_users_aoi english.csv", index=False)
    all_users_aoi_chinese.to_csv(path_to_folder + "/Combined/all_users_aoi chinese.csv", index=False)
    all_users_aoi_spanish.to_csv(path_to_folder + "/Combined/all_users_aoi spanish.csv", index=False)

    all_users_aoi_pred = all_users_aoi.drop(columns="Self AOI_Language_Prof")
    all_users_aoi_pred = all_users_aoi_pred.drop(columns="Test AOI_Language_Prof")

    user_df = pd.read_csv(path_to_folder + "users.csv", sep=",", index_col=False)

    self_english = {}
    test_english = {}
    self_chinese = {}
    test_chinese = {}
    self_spanish = {}
    test_spanish = {}
    chinese_users = []
    spanish_users = []

    for index, row in user_df.iterrows():
        self_english[row["Participant"]] = NUMBER_TO_LMH[row["Self-English Prof"]]
        test_english[row["Participant"]] = row["Test-English"]
        if(row["Language"] == "Chinese"):
            self_chinese[row["Participant"]] = NUMBER_TO_LMH[row["Self-Chinese Prof"]]
            test_chinese[row["Participant"]] = row["Test-Chinese"]
            chinese_users.append(row["Participant"])            
        elif(row["Language"] == "Spanish"):
            self_spanish[row["Participant"]] = NUMBER_TO_LMH[row["Self-Spanish Prof"]]
            test_spanish[row["Participant"]] = row["Test-Spanish"]
            spanish_users.append(row["Participant"])            
    
    all_users_aoi_english_pred = all_users_aoi_pred
    english_prof_list_self = []
    english_prof_list_test = []
    for index, row in all_users_aoi_english_pred.iterrows():
        english_prof_list_self.append(self_english[row["userID"]])
        english_prof_list_test.append(test_english[row["userID"]])
    all_users_aoi_english_pred["Self English"] = english_prof_list_self
    all_users_aoi_english_pred["Test English"] = english_prof_list_test   
    all_users_aoi_english_pred.to_csv(path_to_folder + "/Combined/all_users_aoi all_predict_english.csv", index=False)
    
    all_users_aoi_chinese_pred = all_users_aoi_pred[all_users_aoi_pred["userID"].isin(chinese_users)]
    chinese_prof_list_self = []
    chinese_prof_list_test = []
    for index, row in all_users_aoi_chinese_pred.iterrows():
        chinese_prof_list_self.append(self_chinese[row["userID"]])
        chinese_prof_list_test.append(test_chinese[row["userID"]])
    all_users_aoi_chinese_pred["Self Chinese"] = chinese_prof_list_self
    all_users_aoi_chinese_pred["Test Chinese"] = chinese_prof_list_test
    all_users_aoi_chinese_pred.to_csv(path_to_folder + "/Combined/all_users_aoi all_predict_chinese.csv", index=False)

    all_users_aoi_spanish_pred = all_users_aoi_pred[all_users_aoi_pred["userID"].isin(spanish_users)]
    spanish_prof_list_self = []
    spanish_prof_list_test = []
    for index, row in all_users_aoi_spanish_pred.iterrows():
        spanish_prof_list_self.append(self_spanish[row["userID"]])
        spanish_prof_list_test.append(test_spanish[row["userID"]])
    all_users_aoi_spanish_pred["Self Spanish"] = spanish_prof_list_self
    all_users_aoi_spanish_pred["Test Spanish"] = spanish_prof_list_test
    all_users_aoi_spanish_pred.to_csv(path_to_folder + "/Combined/all_users_aoi all_predict_spanish.csv", index=False)        

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

    all_users_page.to_csv(path_to_folder + "/Combined/all_users_page all.csv", index=False)
    all_users_page_chinese.to_csv(path_to_folder + "/Combined/all_users_page chinese.csv", index=False)
    all_users_page_spanish.to_csv(path_to_folder + "/Combined/all_users_page spanish.csv", index=False)

    english = all_users_page.loc[all_users_page['Number of English AOIs'] != 0]
    chinese = all_users_page_chinese.loc[all_users_page_chinese['Number of English AOIs'] != 6]
    spanish = all_users_page_spanish.loc[all_users_page_spanish['Number of English AOIs'] != 6]

    english.to_csv(path_to_folder + "/Combined/all_users_page_at_least_one_english.csv", index=False)
    chinese.to_csv(path_to_folder + "/Combined/all_users_page_at_least_one_chinese.csv", index=False)
    spanish.to_csv(path_to_folder + "/Combined/all_users_page_at_least_one_spanish.csv", index=False)

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

    all_users_page.to_csv(path_to_folder + "/Combined/all_users_aoipage all.csv", index=False)
    all_users_page_chinese.to_csv(path_to_folder + "/Combined/all_users_aoipage chinese.csv", index=False)
    all_users_page_spanish.to_csv(path_to_folder + "/Combined/all_users_aoipage spanish.csv", index=False)

    english = all_users_page.loc[all_users_page['Number of English AOIs'] != 0]
    chinese = all_users_page_chinese.loc[all_users_page_chinese['Number of English AOIs'] != 6]
    spanish = all_users_page_spanish.loc[all_users_page_spanish['Number of English AOIs'] != 6]

    english.to_csv(path_to_folder + "/Combined/all_users_aoipage_at_least_one_english.csv", index=False)
    chinese.to_csv(path_to_folder + "/Combined/all_users_aoipage_at_least_one_chinese.csv", index=False)
    spanish.to_csv(path_to_folder + "/Combined/all_users_aoipage_at_least_one_spanish.csv", index=False)