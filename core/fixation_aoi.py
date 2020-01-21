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

def calculate_fixation_per_aoi(input_file, output_file):
    """
    Calculate Fixation features per AOI.

    :param input_file: Fixation CSV file
    :param output_file: Fixation per AOI file    
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
        userID = 0

        fixation_count = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        valid_pupil_count = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        
        fixation_duration_total = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        longest_fixation_duration = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]

        saccade_length_total = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        saccade_absolute_angle_total = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        saccade_relative_angle_total = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]

        refixation_total = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]

        left_pupil_difference_total = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        right_pupil_difference_total = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]


        df = pd.read_csv(input_file)
        new_df = pd.DataFrame()

        num_rows = len(pd_dataframe.index)
        count = 0
        # print("Iterating over every row:")
        starttime = time.time()
        
        for index, row in df.iterrows():  
            userID = row['userID']
            page = row['Page'] 
            aoi_type = row['AOI_TYPE']
            numbered_aoi = AOI_STRING_TO_AOI_NUMBER[aoi_type]
            
            #Number of Fixation in the AOI
            fixation_count[numbered_aoi][page] += 1

            #Fixation Duration
            fixation_duration = row['FPOGD']
            fixation_duration_total[numbered_aoi][page] += fixation_duration
            
            #Longest Fixation Duration
            longest_fixation_duration[numbered_aoi][page] = max(longest_fixation_duration[numbered_aoi][page], fixation_duration)

            #Saccade Length
            saccade_length = row['Saccade_length']
            saccade_length_total[numbered_aoi][page] += saccade_length

            #Saccade Absolute Angle
            saccade_absolute_angle = row['Saccade_absolute_angle']
            saccade_absolute_angle_total[numbered_aoi][page] += saccade_absolute_angle

            #Saccade Relative Length
            saccade_relative_angle = row['Saccade_relative_angle']
            saccade_relative_angle_total[numbered_aoi][page] += saccade_relative_angle

            #Refixation
            refixation = row['Is_Refixation']
            refixation_total[numbered_aoi][page] += refixation

            if row['LPMMV'] == 1 and row['RPMMV'] == 1:
                valid_pupil_count[numbered_aoi][page] += 1

                left_pupil_difference = row['Left_Difference']
                left_pupil_difference_total[numbered_aoi][page] += left_pupil_difference

                right_pupil_difference = row['Right_Difference']
                right_pupil_difference_total[numbered_aoi][page] += right_pupil_difference

            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")

        ID_LIST = []
        AOI_TYPE_LIST = []
        PAGE_LIST = []
        
        FIXATION_COUNT_LIST = []

        TOTAL_FIXATION_DURATION_LIST = []
        AVERAGE_FIXATION_DURATION_LIST = []
        LONGEST_FIXATION_DURATION_LIST = []

        TOTAL_SACCADE_LENGTH_LIST = []
        AVERAGE_SACCADE_LENGTH_LIST = []

        TOTAL_SACCADE_ABSOLUTE_ANGLE_LIST = []
        AVERAGE_SACCADE_ABSOLUTE_ANGLE_LIST = []

        TOTAL_SACCADE_RELATIVE_ANGLE_LIST = []
        AVERAGE_SACCADE_RELATIVE_ANGLE_LIST = []

        TOTAL_REFIXATION_LIST = []
        REFIXATION_RATIO_LIST = []

        TOTAL_LEFT_EYE_DIFERENCE_LIST = []
        AVERAGE_LEFT_EYE_DIFERENCE_LIST = []

        TOTAL_RIGHT_EYE_DIFERENCE_LIST = []
        AVERAGE_RIGHT_EYE_DIFERENCE_LIST = []

        for i in range(NUMBER_OF_PAGES):
            for j in range(NUMBER_OF_AOI_TYPES):
                ID_LIST.append(userID)
                AOI_TYPE_LIST.append(AOI_NUMBER_TO_AOI_STRING[j])
                PAGE_LIST.append(i)

                FIXATION_COUNT_LIST.append(fixation_count[j][i])

                TOTAL_FIXATION_DURATION_LIST.append(fixation_duration_total[j][i])
                LONGEST_FIXATION_DURATION_LIST.append(longest_fixation_duration[j][i])

                TOTAL_SACCADE_LENGTH_LIST.append(saccade_length_total[j][i])

                TOTAL_SACCADE_ABSOLUTE_ANGLE_LIST.append(saccade_absolute_angle_total[j][i])

                TOTAL_SACCADE_RELATIVE_ANGLE_LIST.append(saccade_relative_angle_total[j][i])

                TOTAL_REFIXATION_LIST.append(refixation_total[j][i])

                if fixation_count[j][i] == 0:
                    AVERAGE_FIXATION_DURATION_LIST.append(0)
                    AVERAGE_SACCADE_LENGTH_LIST.append(0)
                    AVERAGE_SACCADE_ABSOLUTE_ANGLE_LIST.append(0)
                    AVERAGE_SACCADE_RELATIVE_ANGLE_LIST.append(0)
                    REFIXATION_RATIO_LIST.append(0)
                else:
                    AVERAGE_FIXATION_DURATION_LIST.append(fixation_duration_total[j][i]/fixation_count[j][i])
                    AVERAGE_SACCADE_LENGTH_LIST.append(saccade_length_total[j][i]/fixation_count[j][i])
                    AVERAGE_SACCADE_ABSOLUTE_ANGLE_LIST.append(saccade_absolute_angle_total[j][i]/fixation_count[j][i])
                    AVERAGE_SACCADE_RELATIVE_ANGLE_LIST.append(saccade_relative_angle_total[j][i]/fixation_count[j][i])
                    REFIXATION_RATIO_LIST.append(refixation_total[j][i]/fixation_count[j][i])
                    
                TOTAL_LEFT_EYE_DIFERENCE_LIST.append(left_pupil_difference_total[j][i])

                TOTAL_RIGHT_EYE_DIFERENCE_LIST.append(left_pupil_difference_total[j][i])
                
                if valid_pupil_count[j][i] == 0:
                    AVERAGE_LEFT_EYE_DIFERENCE_LIST.append(0)
                    AVERAGE_RIGHT_EYE_DIFERENCE_LIST.append(0)
                else:
                    AVERAGE_LEFT_EYE_DIFERENCE_LIST.append(left_pupil_difference_total[j][i]/valid_pupil_count[j][i])
                    AVERAGE_RIGHT_EYE_DIFERENCE_LIST.append(left_pupil_difference_total[j][i]/valid_pupil_count[j][i])

        
        fixation_duration_variance = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        saccade_length_variance = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        saccade_absolute_angle_variance = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        saccade_relative_angle_variance = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        left_pupil_difference_variance = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]
        right_pupil_difference_variance = [[0 for i in range(NUMBER_OF_PAGES)] for j in range(NUMBER_OF_AOI_TYPES)]        
        SD_FIXATION_DURATION_LIST = []
        SD_SACCADE_LENGTH_LIST = []
        SD_SACCADE_ABSOLUTE_ANGLE_LIST = []
        SD_SACCADE_RELATIVE_ANGLE_LIST = []
        SD_LEFT_EYE_DIFERENCE_LIST = []
        SD_RIGHT_EYE_DIFERENCE_LIST = []
        
        count = 0 
        for index, row in df.iterrows():   
            page = row['Page'] 
            aoi_type = row['AOI_TYPE']
            numbered_aoi = AOI_STRING_TO_AOI_NUMBER[aoi_type]

            if fixation_count[numbered_aoi][page] == 0:
                fixation_duration_variance[numbered_aoi][page] = 0
                saccade_length_variance[numbered_aoi][page] = 0
                saccade_absolute_angle_variance[numbered_aoi][page] = 0
                saccade_relative_angle_variance[numbered_aoi][page] = 0
            else:
                #Fixation Duration
                fixation_duration = row['FPOGD']
                fixation_duration_average = fixation_duration_total[numbered_aoi][page]/fixation_count[numbered_aoi][page]
                fixation_duration_variance[numbered_aoi][page] += pow(fixation_duration-fixation_duration_average, 2)
                
                #Saccade Length
                saccade_length = row['Saccade_length']
                saccade_length_average = saccade_length_total[numbered_aoi][page]/fixation_count[numbered_aoi][page]
                saccade_length_variance[numbered_aoi][page] += pow(saccade_length-saccade_length_average, 2)

                #Saccade Absolute Angle
                saccade_absolute_angle = row['Saccade_absolute_angle']
                saccade_absolute_angle_average = saccade_absolute_angle_total[numbered_aoi][page]/fixation_count[numbered_aoi][page]
                saccade_absolute_angle_variance[numbered_aoi][page] += pow(saccade_absolute_angle-saccade_absolute_angle_average, 2)

                #Saccade Relative Length
                saccade_relative_angle = row['Saccade_relative_angle']
                saccade_relative_angle_average = saccade_relative_angle_total[numbered_aoi][page]/fixation_count[numbered_aoi][page]
                saccade_relative_angle_variance[numbered_aoi][page] += pow(saccade_relative_angle-saccade_relative_angle_average, 2)

                if row['LPMMV'] == 1 and row['RPMMV'] == 1:
                    if valid_pupil_count[numbered_aoi][page] == 0:
                        left_pupil_difference_variance[numbered_aoi][page] = 0
                        right_pupil_difference_variance[numbered_aoi][page] = 0                        
                    else:
                        left_pupil_difference = row['Left_Difference']
                        left_pupil_difference_average = left_pupil_difference_total[numbered_aoi][page]/valid_pupil_count[numbered_aoi][page]
                        left_pupil_difference_variance[numbered_aoi][page] += pow(left_pupil_difference-left_pupil_difference_average, 2)

                        right_pupil_difference = row['Right_Difference']
                        right_pupil_difference_average = right_pupil_difference_total[numbered_aoi][page]/valid_pupil_count[numbered_aoi][page]
                        right_pupil_difference_variance[numbered_aoi][page] += pow(right_pupil_difference-right_pupil_difference_average, 2)

            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")
        SD_LEFT_EYE_DIFERENCE_LIST = []
        SD_RIGHT_EYE_DIFERENCE_LIST = []
        for i in range(NUMBER_OF_PAGES):
            for j in range(NUMBER_OF_AOI_TYPES):
                if fixation_count[j][i] == 0:
                    SD_FIXATION_DURATION_LIST.append(0)
                    SD_SACCADE_LENGTH_LIST.append(0)
                    SD_SACCADE_ABSOLUTE_ANGLE_LIST.append(0)
                    SD_SACCADE_RELATIVE_ANGLE_LIST.append(0)
                else:
                    SD_FIXATION_DURATION_LIST.append(math.sqrt(fixation_duration_variance[j][i]/fixation_count[j][i]))
                    SD_SACCADE_LENGTH_LIST.append(math.sqrt(saccade_length_variance[j][i]/fixation_count[j][i]))
                    SD_SACCADE_ABSOLUTE_ANGLE_LIST.append(math.sqrt(saccade_absolute_angle_variance[j][i]/fixation_count[j][i]))
                    SD_SACCADE_RELATIVE_ANGLE_LIST.append(math.sqrt(saccade_relative_angle_variance[j][i]/fixation_count[j][i]))
                
                if valid_pupil_count[j][i] == 0:
                    SD_LEFT_EYE_DIFERENCE_LIST.append(0)
                    SD_RIGHT_EYE_DIFERENCE_LIST.append(0)
                else:
                    SD_LEFT_EYE_DIFERENCE_LIST.append(math.sqrt(left_pupil_difference_variance[j][i]/valid_pupil_count[j][i]))
                    SD_RIGHT_EYE_DIFERENCE_LIST.append(math.sqrt(right_pupil_difference_variance[j][i]/valid_pupil_count[j][i]))
        
        new_df['userID'] = ID_LIST
        new_df['Page'] = PAGE_LIST
        new_df['AOI_TYPE'] = AOI_TYPE_LIST
        new_df['Total_Fixation_Count'] = FIXATION_COUNT_LIST
        new_df['Total_Fixation_Duration'] = TOTAL_FIXATION_DURATION_LIST  
        new_df['Average_Fixation_Duration'] = AVERAGE_FIXATION_DURATION_LIST  
        new_df['Fixation_Duration_SD'] = SD_FIXATION_DURATION_LIST          
        new_df['Longest_Fixation_Duration'] = LONGEST_FIXATION_DURATION_LIST
        new_df['Total_Refixation_Count'] = TOTAL_REFIXATION_LIST
        new_df['Refixation_Ratio'] = REFIXATION_RATIO_LIST
        new_df['Total_Saccade_Length'] = TOTAL_SACCADE_LENGTH_LIST  
        new_df['Average_Saccade_Length'] = AVERAGE_SACCADE_ABSOLUTE_ANGLE_LIST
        new_df['Saccade_Length_SD'] = SD_SACCADE_LENGTH_LIST        
        new_df['Total_Saccade_Absolute_Angle'] = TOTAL_SACCADE_ABSOLUTE_ANGLE_LIST  
        new_df['Average_Saccade_Absolute_Angle'] = AVERAGE_SACCADE_ABSOLUTE_ANGLE_LIST
        new_df['Saccade_Absolute_Angle_SD'] = SD_SACCADE_ABSOLUTE_ANGLE_LIST        
        new_df['Total_Saccade_Relative_Angle'] = TOTAL_SACCADE_RELATIVE_ANGLE_LIST  
        new_df['Average_Saccade_Relative_Angle'] = AVERAGE_SACCADE_RELATIVE_ANGLE_LIST
        new_df['Saccade_Relative_Angle_SD'] = SD_SACCADE_RELATIVE_ANGLE_LIST                
        new_df['Total_Left_Eye_Difference'] = TOTAL_LEFT_EYE_DIFERENCE_LIST  
        new_df['Average_Left_Eye_Difference'] = AVERAGE_LEFT_EYE_DIFERENCE_LIST
        new_df['Left_Eye_Difference_SD'] = SD_RIGHT_EYE_DIFERENCE_LIST        
        new_df['Total_Right_Eye_Difference'] = TOTAL_RIGHT_EYE_DIFERENCE_LIST  
        new_df['Average_Right_Eye_Difference'] = AVERAGE_RIGHT_EYE_DIFERENCE_LIST
        new_df['Right_Eye_Difference_SD'] = SD_RIGHT_EYE_DIFERENCE_LIST        

        new_df.to_csv(output_file, index=False)
        print("Finished exporting to {}".
              format(output_file).replace("\\", "/"))
    else:
        print("Exiting...")