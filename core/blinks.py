import pandas as pd
import math
import os
import time
from core import utils


def collapse_to_blinks(input_file, output_file):
    """
    Collapse a larger input file to a smaller output file in respect to blink

    :param input_file: The large, uncollapsed CSV file
    :param output_file: The collapsed CSV file
    """
    print("Collapsing blink file...")
    pd_dataframe = pd.read_csv(input_file, sep=",", index_col=False)
    # print("Finished loading in \"{}\" file".format(input_file))

    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    # if (os.path.exists(output_file)):
    #    overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(output_file).replace("\\", "/"))

    if overwrite.lower() == "y":
        new_df = pd.DataFrame(columns=pd_dataframe.columns)
        # Iterate over all the rows
        # Reference: https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
        num_rows = len(pd_dataframe.index)
        count = 0
        # print("Iterating over every row:")
        starttime = time.time()
        
        row_iterator = pd_dataframe.iterrows()
        _, last = row_iterator.__next__()
        for index, row in row_iterator:
            blink_dur = row['BKDUR'] 

            if blink_dur > 0:
                row['BKID'] = last['BKID']
                new_df_len = len(new_df.index)
                new_df.loc[new_df_len] = row

            last = row
            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")
        column_to_drop = list(range(2, 28)) + list(range(31,50))
        df = new_df.drop(new_df.columns[column_to_drop], axis=1)
        
        df.to_csv(output_file, index=False)


        print("Finished exporting to {}".
              format(output_file).replace("\\", "/"))
    else:
        print("Exiting...")
