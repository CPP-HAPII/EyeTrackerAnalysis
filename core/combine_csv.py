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

