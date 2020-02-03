import pandas as pd
import math
import os
import time
from core import utils

def combine(per_aoi, per_page, output_file):
    user_aoi_df = pd.read_csv(per_aoi, sep=",", index_col=False)
    user_page_df = pd.read_csv(per_page, sep=",", index_col=False)

    #1
    total_fixation_count = [[0 for i in range(30)] for j in range(6)]
    total_fixation_duration = [[0 for i in range(30)] for j in range(6)]
    average_fixation_duration = [[0 for i in range(30)] for j in range(6)]
    fixation_duration_sd = [[0 for i in range(30)] for j in range(6)]
    longest_fixation_duration = [[0 for i in range(30)] for j in range(6)]
    total_refixation_count = [[0 for i in range(30)] for j in range(6)]
    refixation_ratio = [[0 for i in range(30)] for j in range(6)]
    total_saccade_length = [[0 for i in range(30)] for j in range(6)]
    average_saccade_length = [[0 for i in range(30)] for j in range(6)]
    saccade_length_sd = [[0 for i in range(30)] for j in range(6)]
    total_saccade_absolute_angle = [[0 for i in range(30)] for j in range(6)]
    average_saccade_absolute_angle = [[0 for i in range(30)] for j in range(6)]
    saccade_absolute_angle_sd = [[0 for i in range(30)] for j in range(6)]
    total_saccade_relative_angle = [[0 for i in range(30)] for j in range(6)]
    average_saccade_relative_angle = [[0 for i in range(30)] for j in range(6)]
    saccade_relative_angle_sd = [[0 for i in range(30)] for j in range(6)]
    total_left_eye_difference = [[0 for i in range(30)] for j in range(6)]
    average_left_eye_difference = [[0 for i in range(30)] for j in range(6)]
    left_eye_difference_sd = [[0 for i in range(30)] for j in range(6)]
    total_right_eye_difference = [[0 for i in range(30)] for j in range(6)]
    average_right_eye_difference = [[0 for i in range(30)] for j in range(6)]
    right_eye_difference_sd = [[0 for i in range(30)] for j in range(6)]
    blink_count = [[0 for i in range(30)] for j in range(6)]    
    total_blink_duration = [[0 for i in range(30)] for j in range(6)]
    average_blink_duration = [[0 for i in range(30)] for j in range(6)]

    counter = 0
    
    for index, row in user_aoi_df.iterrows():
        page = row["Page"]
        #2
        total_fixation_count[counter][page-1] = row["Total_Fixation_Count"]
        total_fixation_duration[counter][page-1] = row["Total_Fixation_Duration"]
        average_fixation_duration[counter][page-1] = row["Average_Fixation_Duration"]
        fixation_duration_sd[counter][page-1] = row["Fixation_Duration_SD"]
        longest_fixation_duration[counter][page-1] = row["Longest_Fixation_Duration"]
        total_refixation_count[counter][page-1] = row["Total_Refixation_Count"]
        refixation_ratio[counter][page-1] = row["Refixation_Ratio"]
        total_saccade_length[counter][page-1] = row["Total_Saccade_Length"]
        average_saccade_length[counter][page-1] = row["Average_Saccade_Length"]
        saccade_length_sd[counter][page-1] = row["Saccade_Length_SD"]
        total_saccade_absolute_angle[counter][page-1] = row["Total_Saccade_Absolute_Angle"]
        average_saccade_absolute_angle[counter][page-1] = row["Average_Saccade_Absolute_Angle"]
        saccade_absolute_angle_sd[counter][page-1] = row["Saccade_Absolute_Angle_SD"]
        total_saccade_relative_angle[counter][page-1] = row["Total_Saccade_Relative_Angle"]
        average_saccade_relative_angle[counter][page-1] = row["Average_Saccade_Relative_Angle"]
        saccade_relative_angle_sd[counter][page-1] = row["Saccade_Relative_Angle_SD"]
        total_left_eye_difference[counter][page-1] = row["Total_Left_Eye_Difference"]
        average_left_eye_difference[counter][page-1] = row["Average_Left_Eye_Difference"]
        left_eye_difference_sd[counter][page-1] = row["Left_Eye_Difference_SD"]
        total_right_eye_difference[counter][page-1] = row["Total_Right_Eye_Difference"]
        average_right_eye_difference[counter][page-1] = row["Average_Right_Eye_Difference"]
        right_eye_difference_sd[counter][page-1] = row["Right_Eye_Difference_SD"]
        blink_count[counter][page-1] = row["Blink_Count"]
        total_blink_duration[counter][page-1] = row["Total_Blink_Duration"]
        average_blink_duration[counter][page-1] = row["Average_Blink_Duration"]

        counter += 1
        if counter == 6:
            counter = 0

    for x in range (0, 6):
        number = str(x + 1)
        #3
        tfc = "Total_Fixation_Count_AOI" + number
        tfd = "Total_Fixation_Duration_AOI" + number
        avd = "Average_Fixation_Duration_AOI" + number
        fdsd = "Fixation_Duration_SD_AOI" + number
        lfd = "Longest_Fixation_Duration_AOI" + number
        trc = "Total_Refixation_Count_AOI" + number 
        rr = "Refixation_Ratio_AOI" + number 
        tsl = "Total_Saccade_Length_AOI" + number
        asl = "Average_Saccade_Length_AOI" + number 
        slsd = "Saccade_Length_SD_AOI" + number 
        tsaa = "Total_Saccade_Absolute_Angle_AOI" + number
        asaa = "Average_Saccade_Absolute_Angle_AOI" + number
        saasd = "Saccade_Absolute_Angle_SD_AOI" + number
        tsra = "Total_Saccade_Relative_Angle_AOI" + number
        asra = "Average_Saccade_Relative_Angle_AOI" + number
        srasd = "Saccade_Relative_Angle_SD_AOI" + number
        tled = "Total_Left_Eye_Difference_AOI" + number
        aled = "Average_Left_Eye_Difference_AOI" + number
        ledsd = "Left_Eye_Difference_SD_AOI" + number
        tred = "Total_Right_Eye_Difference_AOI" + number
        ared = "Average_Right_Eye_Difference_AOI" + number
        redsd = "Right_Eye_Difference_SD_AOI" + number
        bc = "Blink_Count_AOI" + number
        tbd = "Total_Blink_Duration_AOI" + number
        abd = "Average_Blink_Duration_AOI" + number

        #4
        user_page_df[tfc] = total_fixation_count[x]
        user_page_df[tfd] = total_fixation_duration[x] 
        user_page_df[avd] = average_fixation_duration[x]
        user_page_df[fdsd] = fixation_duration_sd[x]
        user_page_df[lfd] = longest_fixation_duration[x] 
        user_page_df[trc] = total_refixation_count[x]
        user_page_df[rr] = refixation_ratio[x]
        user_page_df[tsl] = total_saccade_length[x] 
        user_page_df[asl] = average_saccade_length[x]
        user_page_df[slsd] = saccade_length_sd[x]
        user_page_df[tsaa] = total_saccade_absolute_angle[x] 
        user_page_df[asaa] = average_saccade_absolute_angle[x]
        user_page_df[saasd] = saccade_absolute_angle_sd[x]
        user_page_df[tsra] = total_saccade_relative_angle[x] 
        user_page_df[asra] = average_saccade_relative_angle[x]
        user_page_df[srasd] = saccade_relative_angle_sd[x]
        user_page_df[tled] = total_left_eye_difference[x] 
        user_page_df[aled] = average_left_eye_difference[x]
        user_page_df[ledsd] = left_eye_difference_sd[x]
        user_page_df[tred] = total_right_eye_difference[x] 
        user_page_df[ared] = average_right_eye_difference[x]
        user_page_df[redsd] = right_eye_difference_sd[x]
        user_page_df[bc] = blink_count[x] 
        user_page_df[tbd] = total_blink_duration[x]
        user_page_df[abd] = average_blink_duration[x]

    cols_at_end = ['Number of English AOIs', 'L1', "Eng Prof (Self)", "Eng Prof (Test)", "Chinese/Spanish Prof (Self)", "Chinese/Spanish Prof (Test)"]
    user_page_df = user_page_df[[c for c in user_page_df if c not in cols_at_end] + [c for c in cols_at_end if c in user_page_df]]
    user_page_df.to_csv(output_file, index=False)