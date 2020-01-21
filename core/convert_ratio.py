import pandas as pd
import math
import os
import time
from core import utils


def convert_ratio_to_pixel(input_file):
    """
    Convert fixation ratio to fixation pixel.

    :param input_file: The large, uncollapsed CSV file
    """
    print("Converting ratio to pixels...")
    pd_dataframe = pd.read_csv(input_file, sep=",", index_col=False)
    # print("Finished loading in \"{}\" file".format(input_file))

    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    # if (os.path.exists(input_file)):
    #    overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(input_file).replace("\\", "/"))

    if overwrite.lower() == "y":
        df = pd.read_csv(input_file)
        
        num_rows = len(pd_dataframe.index)
        count = 0
        # print("Iterating over every row:")
        starttime = time.time()
        
        x_coordinate_list = []
        y_coordinate_list = []  

        for index, row in df.iterrows():
            x_coord = row['FPOGX'] * 1920
            y_coord = row['FPOGY'] * 1080

            x_coordinate_list.append(round(x_coord))
            y_coordinate_list.append(round(y_coord))
            
            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")
        df['X_Coordinate'] = x_coordinate_list
        df['Y_Coordinate'] = y_coordinate_list
        df.to_csv(input_file, index=False)
        print("Finished exporting to {}".
              format(input_file).replace("\\", "/"))
    else:
        print("Exiting...")
