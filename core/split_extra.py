import pandas as pd
import math
import os
import time
from core import utils

def process_csv(path_to_file):
    combined_page_df = pd.read_csv(path_to_file, sep=",", index_col=False)
    
    userID = []
    Page = []
    AOI_TYPE = []

    for index, row in combined_page_df.iterrows():
        extra = row["Extra"]
        strings = extra.split("-")
        userID.append(strings[0])
        Page.append(strings[1])         
        AOI_TYPE.append(strings[2])

    combined_page_df["userID"] = userID
    combined_page_df["Page"] = Page
    combined_page_df["AOI_TYPE"] = AOI_TYPE 
    combined_page_df = combined_page_df.sort_values(['userID', 'Page', 'AOI_TYPE'], ascending=[True, True, True])

    current_userID = ""
    current_page = ""
    aoi_count = 0
    correct_prediction_count = 0
    page_count = 0    
    correct_page_count = 0

    six_count = 0
    six_count_correct = 0
    for index, row in combined_page_df.iterrows():
        if row["userID"] == current_userID and row["Page"] == current_page:
            if(row["actual"] == row["predicted"]):
                correct_prediction_count += 1
            aoi_count += 1
        else:
            if(aoi_count != 0):
                if aoi_count == 6:
                    six_count += 1
                    if correct_prediction_count >= 3:
                        six_count_correct += 1
                page_count += 1
                correct_page_count += round(correct_prediction_count/aoi_count)
            current_userID = row["userID"]
            current_page = row["Page"]
            aoi_count = 1
            if(row["actual"] == row["predicted"]):
                correct_prediction_count = 1  
            else:
                correct_prediction_count = 0
    if aoi_count == 6:
        six_count += 1
        if correct_prediction_count >= 3:
            six_count_correct += 1
    page_count += 1
    correct_page_count += round(correct_prediction_count/aoi_count)

    print(correct_page_count)
    print(page_count)
    print(correct_page_count/page_count)
    print(six_count_correct)
    print(six_count)
    print((correct_page_count+six_count_correct)/(page_count+six_count))
