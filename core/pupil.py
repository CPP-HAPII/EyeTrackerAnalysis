import pandas as pd
import math
import os
import time
from core import utils

#left_diameter_baseline = 3.3
#right_diameter_baseline = 3.3

def calculate_pupil(input_file, task_file):
    """
    Calculate difference of pupil diameter to the baseline
    :param input_file: The collapsed fixation file
    """
    print("Calculating pupil difference...")
    task_dataframe = pd.read_csv(task_file, sep=",", index_col=False)    
    pd_dataframe = pd.read_csv(input_file, sep=",", index_col=False)
    print("Finished loading in \"{}\" file".format(input_file))

    
    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    # if (os.path.exists(input_file)):
    #    overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(input_file).replace("\\", "/"))

    if overwrite.lower() == "y":
        #fixation_included = set()
        # Iterate over all the rows
        # Reference: https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas

        time_in = task_dataframe.loc[task_dataframe['Task'] == 0]['createdAt'][0]
        time_out = task_dataframe.loc[task_dataframe['Task'] == 0]['exitAt'][0]        

        start_hour, start_minute, start_second = time_in.split(" ")[1].split(":")
        baseline_start_time = int(start_hour) * 3600 + int(start_minute) * 60 + int(float(start_second))
        end_hour, end_minute, end_second = time_out.split(" ")[1].split(":")
        baseline_end_time = int(end_hour) * 3600 + int(end_minute) * 60 + int(float(end_second))


        time_column_name = pd_dataframe.columns.tolist()[3]
        time_column_name = time_column_name.split(" ")[1][:-1]
        hour, minute, second = time_column_name.split(":")
        experiment_start_time = int(hour) * 3600 + int(minute) * 60 + int(float(second))
        
        count = 0
        left_diameter_baseline = 0
        right_diameter_baseline = 0

        row_iterator = pd_dataframe.iterrows()
        for index, row in row_iterator:
            if row[3] + experiment_start_time > baseline_start_time and row[3] + experiment_start_time < baseline_end_time:
                left_diameter_baseline += row['LPMM']
                right_diameter_baseline += row['RPMM']
                count += 1                

        left_diameter_baseline /= count
        right_diameter_baseline /= count

        #print(left_diameter_baseline)
        #print(right_diameter_baseline)

        left_difference = []
        right_difference = []

        num_rows = len(pd_dataframe.index)
        count = 0
        # print("Iterating over every row:")
        starttime = time.time()
        
        row_iterator = pd_dataframe.iterrows()
        for index, row in row_iterator:
            left_diameter = row['LPMM'] 
            right_diameter = row['RPMM'] 
            left_difference.append(left_diameter - left_diameter_baseline)
            right_difference.append(right_diameter - right_diameter_baseline)
            
            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")

        pd_dataframe['Left_Difference'] = left_difference
        pd_dataframe['Right_Difference'] = right_difference
        
        pd_dataframe.to_csv(input_file, index=False)

        print("Finished exporting to {}".
              format(input_file).replace("\\", "/"))
    else:
        print("Exiting...")
