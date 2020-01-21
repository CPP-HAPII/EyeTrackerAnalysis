import pandas as pd
import math
import os
import time
from core import utils

top_x = [630, 640, 640, 640, 640, 640, 640]
top_y = [95, 169, 300, 431, 562, 693, 824]
bot_x = [1290, 1280, 1280, 1280, 1280, 1280, 1280]
bot_y = [165, 274, 405, 536, 667, 798, 929]

def add_label(input_file, task_file):
    """
    Add Page to CSV File.

    :param input_file: The large, uncollapsed CSV file
    """
    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    # if (os.path.exists(input_file)):
    #    overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(input_file).replace("\\", "/"))

    if overwrite.lower() != "y":
        print("Exiting...")
        return

    print("Adding AOI and Page Label...")
    pd_dataframe = pd.read_csv(input_file, sep=",", index_col=False)
    # print("Finished loading in \"{}\" file".format(input_file))
    
    time_file = pd.read_csv(task_file, sep=",", index_col=False)
    enter_time = []
    time_file['TIME_IN'] = pd.to_datetime(time_file['createdAt'], format='%Y-%m-%d %H:%M:%S.%f')
    time_file['TIME_OUT'] = pd.to_datetime(time_file['updatedAt'], format='%Y-%m-%d %H:%M:%S.%f')

    time_column_name = pd_dataframe.columns.tolist()[3]
    time_column_name = time_column_name.split(" ")[1][:-1]
    start_hour, start_minute, start_second = time_column_name.split(":")
    start_time = int(start_hour) * 3600 + int(start_minute) * 60 + int(float(start_second))

    id = 0

    for index, row in time_file.iterrows():
        id = row['userID']
        if row['Task'] > 0:
            time_row = row['TIME_IN']
            time_in_second = time_row.hour * 3600 + time_row.minute * 60 + time_row.second
            enter_time.append(time_in_second - start_time)
        if row['Task'] == 30:
            time_row = row['TIME_OUT']
            time_in_second = time_row.hour * 3600 + time_row.minute * 60 + time_row.second                        
            enter_time.append(time_in_second - start_time)            

    overwrite = "y"
    # Export to csv file
    if overwrite.lower() == "y":

        df = pd.read_csv(input_file)
        
        num_rows = len(pd_dataframe.index)
        count = 0
        # print("Iterating over every row:")
        starttime = time.time()

        ID_List = []
        Page_List = []
        AOI_Type_List = []

        for index, row in df.iterrows():
            ID_List.append(id)

            x_coord = row['X_Coordinate'] 
            y_coord = row['Y_Coordinate']

            if x_coord < 630 or x_coord > 1290:
                AOI_Type_List.append("NOT_AOI")
            else:
                if x_coord >= 630 and x_coord <= 1290 and y_coord >= 95 and y_coord <= 165:
                    AOI_Type_List.append("QUERY")
                elif x_coord >= 640 and x_coord <= 1280:
                    if y_coord >= top_y[1] and y_coord <= bot_y[1]:
                        AOI_Type_List.append("RESULT1")
                    elif y_coord >= top_y[2] and y_coord <= bot_y[2]:
                        AOI_Type_List.append("RESULT2")
                    elif y_coord >= top_y[3] and y_coord <= bot_y[3]:
                        AOI_Type_List.append("RESULT3")   
                    elif y_coord >= top_y[4] and y_coord <= bot_y[4]:
                        AOI_Type_List.append("RESULT4")   
                    elif y_coord >= top_y[5] and y_coord <= bot_y[5]:
                        AOI_Type_List.append("RESULT5")   
                    elif y_coord >= top_y[6] and y_coord <= bot_y[6]:
                        AOI_Type_List.append("RESULT6")   
                    else:
                        AOI_Type_List.append("NOT_AOI")
                else:
                    AOI_Type_List.append("NOT_AOI")

            timestamp = row[3]

            if timestamp < enter_time[0] or timestamp > enter_time[len(enter_time) - 1]:
                Page_List.append(0)
            else:
                i = len(enter_time) - 1
                while(i >= 0):
                    if timestamp >= enter_time[i]:
                        Page_List.append(i+1)
                        break
                    i -= 1
                    
            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")
        df['userID'] = ID_List
        df['AOI_TYPE'] = AOI_Type_List        
        df['Page'] = Page_List
        df.to_csv(input_file, index=False)
        print("Finished exporting to {}".
              format(input_file).replace("\\", "/"))
    else:
        print("Exiting...")
