import pandas as pd
import math
import os
import time
from core import utils

AOI_STRING_TO_AOI_NUMBER = {
    'QUERY' : 0,
    'RESULT1' : 1,
    'RESULT2' : 2,
    'RESULT3' : 3,
    'RESULT4' : 4,
    'RESULT5' : 5,
    'RESULT6' : 6,
    'NOT_AOI' : 7,
}

AOI_NUMBER_TO_AOI_STRING = {
    0 : 'QUERY',
    1 : 'RESULT1',
    2 : 'RESULT2',
    3 : 'RESULT3',
    4 : 'RESULT4',
    5 : 'RESULT5',
    6 : 'RESULT6',
    7 : 'NOT_AOI',
}

NUMBER_OF_AOI_TYPES = 8
NUMBER_OF_PAGES = 31

def calculate_blink_per_aoi(input_file, output_file):
    """
    Calculate Blinking features per AOI.

    :param input_file: Blinking CSV file
    :param output_file: Blinking per AOI file    
    """
    print("Calculating Blinking Features per AOI...")
    pd_dataframe = pd.read_csv(input_file, sep=",", index_col=False)
    # print("Finished loading in \"{}\" file".format(input_file))

    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    # if (os.path.exists(output_file)):
    #    overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(input_file).replace("\\", "/"))

    if overwrite.lower() == "y":

        blink_count = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        blink_duration_total = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]

        df = pd.read_csv(input_file)
        new_df = pd.DataFrame()

        num_rows = len(pd_dataframe.index)
        count = 0
        # print("Iterating over every row:")
        starttime = time.time()

        for index, row in df.iterrows():   
            page = row['Page'] 
            aoi_type = row['AOI_TYPE']
            numbered_aoi = AOI_STRING_TO_AOI_NUMBER[aoi_type]
            blink_duration = row['BKDUR']

            blink_count[numbered_aoi][page] += 1
            blink_duration_total[numbered_aoi][page] += blink_duration

            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")

        AOI_TYPE_LIST = []
        PAGE_LIST = []
        BLINK_COUNT_LIST = []
        TOTAL_BLINK_DURATION_LIST = []
        AVERAGE_BLINK_DURATION_LIST = []

        for i in range(NUMBER_OF_PAGES):
            for j in range(NUMBER_OF_AOI_TYPES):
                AOI_TYPE_LIST.append(AOI_NUMBER_TO_AOI_STRING[j])
                PAGE_LIST.append(i)
                BLINK_COUNT_LIST.append(blink_count[j][i])
                TOTAL_BLINK_DURATION_LIST.append(blink_duration_total[j][i])
                if blink_count[j][i] != 0:
                    AVERAGE_BLINK_DURATION_LIST.append(blink_duration_total[j][i]/blink_count[j][i])
                else:
                    AVERAGE_BLINK_DURATION_LIST.append(0)

        new_df['Page'] = PAGE_LIST
        new_df['AOI_TYPE'] = AOI_TYPE_LIST
        new_df['Blink_Count'] = BLINK_COUNT_LIST
        new_df['Total_Blink_Duration'] = TOTAL_BLINK_DURATION_LIST  
        new_df['Average_Blink_Duration'] = AVERAGE_BLINK_DURATION_LIST  

        new_df.to_csv(output_file, index=False)
        print("Finished exporting to {}".
              format(output_file).replace("\\", "/"))
    else:
        print("Exiting...")