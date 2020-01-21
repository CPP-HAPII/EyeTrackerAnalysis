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

def calculate(input_file):
    """
    Calculate Refixation features per AOI.

    :param input_file: Fixation CSV file
    """
    print("Calculating Refixation Features per AOI...")
    pd_dataframe = pd.read_csv(input_file, sep=",", index_col=False)

    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    # if (os.path.exists(input_file)):
    #    overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(input_file).replace("\\", "/"))

    if overwrite.lower() == "y":

        fixation_list = [[[] for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        refixation_count = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]

        is_refixation_list = []

        df = pd.read_csv(input_file)

        num_rows = len(pd_dataframe.index)
        count = 0
        # print("Iterating over every row:")
        starttime = time.time()

        for index, row in df.iterrows():   
            page = row['Page'] 
            aoi_type = row['AOI_TYPE']
            numbered_aoi = AOI_STRING_TO_AOI_NUMBER[aoi_type]

            x_coord = row['X_Coordinate']
            y_coord = row['Y_Coordinate']

            if page < 31 and page > 0 and numbered_aoi < 7:
                if check_if_refixation(fixation_list, x_coord, y_coord, numbered_aoi, page):
                    refixation_count[numbered_aoi][page] += 1
                    is_refixation_list.append(1)
                else:
                    is_refixation_list.append(0)                    
                fixation_list[numbered_aoi][page].append([x_coord, y_coord])
            else:
                is_refixation_list.append(0)                    
                
            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")

        #print(refixation_count)
        df['Is_Refixation'] = is_refixation_list
        df.to_csv(input_file, index=False)
        print("Finished exporting to {}".
              format(input_file).replace("\\", "/"))
    else:
        print("Exiting...")

def check_if_refixation(fixation_list, x_coord, y_coord, numbered_aoi, page):
    existing_fixations = fixation_list[numbered_aoi][page]
    for coordinate in existing_fixations:
        x = coordinate[0]
        y = coordinate[1]

        x_square = pow(x - x_coord, 2)
        y_square = pow(y - y_coord, 2)

        distance = math.sqrt(x_square + y_square)

        if distance <= 10:
            return 1

    return 0