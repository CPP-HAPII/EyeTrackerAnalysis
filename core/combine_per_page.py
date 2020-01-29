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

NUMBER_TO_LMH = {
    1 : "Low",
    2 : "Low",
    3 : "Low",
    4 : "Medium",
    5 : "High"
}

NUMBER_OF_AOI_TYPES = 8
NUMBER_OF_PAGES = 31

def combine(input_file, input2_file, output_file, task_file):
    """
    Combine 2 Collapsed Files into Page File.

    :param input_file: Fixation Collapsed file
    :param input_file: Blinking Collapsed file    
    :param output_file: Combined Page file    
    """
    print("Combining data per AOI...")
    
    # print("Reading Fixation Collapsed...")
    fixation_dataframe = pd.read_csv(input_file, sep=",", index_col=False)
    # print("Finished loading in \"{}\" file".format(input_file))

    # print("Reading Blinking Collapsed...")
    blinking_dataframe = pd.read_csv(input2_file, sep=",", index_col=False)
    # print("Finished loading in \"{}\" file".format(input2_file))

    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    # if (os.path.exists(output_file)):
    #    overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(output_file).replace("\\", "/"))

    if overwrite.lower() == "y":
        fixation_page_dataframe = processFixationDataframe(fixation_dataframe)
        blink_page_dataframe = processBlinkDataframe(blinking_dataframe)

        new_df = pd.DataFrame()
        new_df = pd.merge(fixation_page_dataframe, blink_page_dataframe,  how='left', on=['Page'])

        NUMBER_OF_ENGLISH_LIST = []
        userId = 0

        task_file = pd.read_csv(task_file, sep=",", index_col=False)
        for index, row in task_file.iterrows():
            order = row['Result Order']
            userId = row['userID']
            if row['Task'] >= 0:
                if order == 0:
                    NUMBER_OF_ENGLISH_LIST.append(0)
                elif order == 1:
                    NUMBER_OF_ENGLISH_LIST.append(6)
                else:
                    NUMBER_OF_ENGLISH_LIST.append(3)                                
        new_df['Number of English AOIs'] = NUMBER_OF_ENGLISH_LIST

        L1 = "N/A"
        self_english = "N/A"
        test_english = "N/A"
        self_other = "N/A"
        test_other = "N/A"
        users_df = pd.read_csv("user_study_data/users.csv", sep=",", index_col=False)
        for index, row in users_df.iterrows():
            participant = row['Participant']
            if userId == participant:
                L1 =  row['L1']
                self_english = NUMBER_TO_LMH[row['Self-English Prof']]
                test_english = row['Test-English']
                if row['Self-Chinese Prof'] > 0:
                    self_other = NUMBER_TO_LMH[row['Self-Chinese Prof']]
                    test_other = row['Test-Chinese']
                else:
                    self_other = NUMBER_TO_LMH[row['Self-Spanish Prof']]
                    test_other = row['Test-Spanish']                    
                break

        L1_LIST = [L1] * 31  
        SELF_ENG_PROF = [self_english] * 31
        TEST_ENG_PROF = [test_english] * 31
        SELF_OTHER_PROF = [self_other] * 31
        TEST_OTHER_PROF = [test_other] * 31    

        new_df['L1'] = L1_LIST    
        new_df['Eng Prof (Self)'] = SELF_ENG_PROF    
        new_df['Eng Prof (Test)'] = TEST_ENG_PROF
        new_df['Chinese/Spanish Prof (Self)'] = SELF_OTHER_PROF    
        new_df['Chinese/Spanish Prof (Test)'] = TEST_OTHER_PROF    

        new_df = new_df[new_df.Page != 0]        

        new_df.to_csv(output_file, index=False)
       
        print("Finished exporting to {}".
              format(output_file).replace("\\", "/"))
    else:
        print("Exiting...")

def processFixationDataframe(df):
    new_df = pd.DataFrame()
    
    fixation_count = [0 for i in range(NUMBER_OF_PAGES)] 
    valid_pupil_count = [0 for i in range(NUMBER_OF_PAGES)]
        
    fixation_duration_total = [0 for i in range(NUMBER_OF_PAGES)] 
    longest_fixation_duration = [0 for i in range(NUMBER_OF_PAGES)] 

    saccade_length_total = [0 for i in range(NUMBER_OF_PAGES)] 
    saccade_absolute_angle_total = [0 for i in range(NUMBER_OF_PAGES)] 
    saccade_relative_angle_total = [0 for i in range(NUMBER_OF_PAGES)] 

    refixation_total = [0 for i in range(NUMBER_OF_PAGES)]

    left_pupil_difference_total = [0 for i in range(NUMBER_OF_PAGES)]
    right_pupil_difference_total = [0 for i in range(NUMBER_OF_PAGES)]   
    
    num_rows = len(df.index)
    count = 0
    # print("Iterating over every row:")
    starttime = time.time()
    
    for index, row in df.iterrows():  
        userID = row['userID']
        page = row['Page'] 
        aoi_type = row['AOI_TYPE']
        numbered_aoi = AOI_STRING_TO_AOI_NUMBER[aoi_type]
        
        #Number of Fixation in the AOI
        if numbered_aoi > 0 and numbered_aoi < 7:
            fixation_count[page] += 1

            #Fixation Duration
            fixation_duration = row['FPOGD']
            fixation_duration_total[page] += fixation_duration
            
            #Longest Fixation Duration
            longest_fixation_duration[page] = max(longest_fixation_duration[page], fixation_duration)

            #Saccade Length
            saccade_length = row['Saccade_length']
            saccade_length_total[page] += saccade_length

            #Saccade Absolute Angle
            saccade_absolute_angle = row['Saccade_absolute_angle']
            saccade_absolute_angle_total[page] += saccade_absolute_angle

            #Saccade Relative Length
            saccade_relative_angle = row['Saccade_relative_angle']
            saccade_relative_angle_total[page] += saccade_relative_angle

            #Refixation
            refixation = row['Is_Refixation']
            refixation_total[page] += refixation

            if row['LPMMV'] == 1 and row['RPMMV'] == 1:
                valid_pupil_count[page] += 1

                left_pupil_difference = row['Left_Difference']
                left_pupil_difference_total[page] += left_pupil_difference

                right_pupil_difference = row['Right_Difference']
                right_pupil_difference_total[page] += right_pupil_difference

        curtime = time.time()
        elapsed_time = curtime - starttime
        count += 1
        progress = utils.progress_bar(count, num_rows, elapsed_time)
        print(progress, end="\r")

    print("")

    ID_LIST = []
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
        ID_LIST.append(userID)
        PAGE_LIST.append(i)

        FIXATION_COUNT_LIST.append(fixation_count[i])

        TOTAL_FIXATION_DURATION_LIST.append(fixation_duration_total[i])
        LONGEST_FIXATION_DURATION_LIST.append(longest_fixation_duration[i])

        TOTAL_SACCADE_LENGTH_LIST.append(saccade_length_total[i])

        TOTAL_SACCADE_ABSOLUTE_ANGLE_LIST.append(saccade_absolute_angle_total[i])

        TOTAL_SACCADE_RELATIVE_ANGLE_LIST.append(saccade_relative_angle_total[i])

        TOTAL_REFIXATION_LIST.append(refixation_total[i])

        if fixation_count[i] == 0:
            AVERAGE_FIXATION_DURATION_LIST.append(0)
            AVERAGE_SACCADE_LENGTH_LIST.append(0)
            AVERAGE_SACCADE_ABSOLUTE_ANGLE_LIST.append(0)
            AVERAGE_SACCADE_RELATIVE_ANGLE_LIST.append(0)
            REFIXATION_RATIO_LIST.append(0)
        else:
            AVERAGE_FIXATION_DURATION_LIST.append(fixation_duration_total[i]/fixation_count[i])
            AVERAGE_SACCADE_LENGTH_LIST.append(saccade_length_total[i]/fixation_count[i])
            AVERAGE_SACCADE_ABSOLUTE_ANGLE_LIST.append(saccade_absolute_angle_total[i]/fixation_count[i])
            AVERAGE_SACCADE_RELATIVE_ANGLE_LIST.append(saccade_relative_angle_total[i]/fixation_count[i])
            REFIXATION_RATIO_LIST.append(refixation_total[i]/fixation_count[i])
            
        TOTAL_LEFT_EYE_DIFERENCE_LIST.append(left_pupil_difference_total[i])

        TOTAL_RIGHT_EYE_DIFERENCE_LIST.append(left_pupil_difference_total[i])
        
        if valid_pupil_count[i] == 0:
            AVERAGE_LEFT_EYE_DIFERENCE_LIST.append(0)
            AVERAGE_RIGHT_EYE_DIFERENCE_LIST.append(0)
        else:
            AVERAGE_LEFT_EYE_DIFERENCE_LIST.append(left_pupil_difference_total[i]/valid_pupil_count[i])
            AVERAGE_RIGHT_EYE_DIFERENCE_LIST.append(left_pupil_difference_total[i]/valid_pupil_count[i])

    
    fixation_duration_variance = [0 for i in range(NUMBER_OF_PAGES)]
    saccade_length_variance = [0 for i in range(NUMBER_OF_PAGES)]
    saccade_absolute_angle_variance = [0 for i in range(NUMBER_OF_PAGES)]
    saccade_relative_angle_variance = [0 for i in range(NUMBER_OF_PAGES)]
    left_pupil_difference_variance = [0 for i in range(NUMBER_OF_PAGES)]
    right_pupil_difference_variance = [0 for i in range(NUMBER_OF_PAGES)]       
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

        if fixation_count[page] == 0:
            fixation_duration_variance[page] = 0
            saccade_length_variance[page] = 0
            saccade_absolute_angle_variance[page] = 0
            saccade_relative_angle_variance[page] = 0
        elif numbered_aoi > 0 and numbered_aoi < 7:
            #Fixation Duration
            fixation_duration = row['FPOGD']
            fixation_duration_average = fixation_duration_total[page]/fixation_count[page]
            fixation_duration_variance[page] += pow(fixation_duration-fixation_duration_average, 2)
            
            #Saccade Length
            saccade_length = row['Saccade_length']
            saccade_length_average = saccade_length_total[page]/fixation_count[page]
            saccade_length_variance[page] += pow(saccade_length-saccade_length_average, 2)

            #Saccade Absolute Angle
            saccade_absolute_angle = row['Saccade_absolute_angle']
            saccade_absolute_angle_average = saccade_absolute_angle_total[page]/fixation_count[page]
            saccade_absolute_angle_variance[page] += pow(saccade_absolute_angle-saccade_absolute_angle_average, 2)

            #Saccade Relative Length
            saccade_relative_angle = row['Saccade_relative_angle']
            saccade_relative_angle_average = saccade_relative_angle_total[page]/fixation_count[page]
            saccade_relative_angle_variance[page] += pow(saccade_relative_angle-saccade_relative_angle_average, 2)

            if row['LPMMV'] == 1 and row['RPMMV'] == 1:
                if valid_pupil_count[page] == 0:
                    left_pupil_difference_variance[page] = 0
                    right_pupil_difference_variance[page] = 0                        
                elif numbered_aoi > 0 and numbered_aoi < 7:
                    left_pupil_difference = row['Left_Difference']
                    left_pupil_difference_average = left_pupil_difference_total[page]/valid_pupil_count[page]
                    left_pupil_difference_variance[page] += pow(left_pupil_difference-left_pupil_difference_average, 2)

                    right_pupil_difference = row['Right_Difference']
                    right_pupil_difference_average = right_pupil_difference_total[page]/valid_pupil_count[page]
                    right_pupil_difference_variance[page] += pow(right_pupil_difference-right_pupil_difference_average, 2)

        curtime = time.time()
        elapsed_time = curtime - starttime
        count += 1
        progress = utils.progress_bar(count, num_rows, elapsed_time)
        print(progress, end="\r")

    print("")
    SD_LEFT_EYE_DIFERENCE_LIST = []
    SD_RIGHT_EYE_DIFERENCE_LIST = []
    for i in range(NUMBER_OF_PAGES):
        if fixation_count[i] == 0:
            SD_FIXATION_DURATION_LIST.append(0)
            SD_SACCADE_LENGTH_LIST.append(0)
            SD_SACCADE_ABSOLUTE_ANGLE_LIST.append(0)
            SD_SACCADE_RELATIVE_ANGLE_LIST.append(0)
        else:
            SD_FIXATION_DURATION_LIST.append(math.sqrt(fixation_duration_variance[i]/fixation_count[i]))
            SD_SACCADE_LENGTH_LIST.append(math.sqrt(saccade_length_variance[i]/fixation_count[i]))
            SD_SACCADE_ABSOLUTE_ANGLE_LIST.append(math.sqrt(saccade_absolute_angle_variance[i]/fixation_count[i]))
            SD_SACCADE_RELATIVE_ANGLE_LIST.append(math.sqrt(saccade_relative_angle_variance[i]/fixation_count[i]))
        
        if valid_pupil_count[i] == 0:
            SD_LEFT_EYE_DIFERENCE_LIST.append(0)
            SD_RIGHT_EYE_DIFERENCE_LIST.append(0)
        else:
            SD_LEFT_EYE_DIFERENCE_LIST.append(math.sqrt(left_pupil_difference_variance[i]/valid_pupil_count[i]))
            SD_RIGHT_EYE_DIFERENCE_LIST.append(math.sqrt(right_pupil_difference_variance[i]/valid_pupil_count[i]))

    new_df['userID'] = ID_LIST
    new_df['Page'] = PAGE_LIST
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

    return new_df

def processBlinkDataframe(df):
    new_df = pd.DataFrame()
    
    blink_count = [0 for i in range(NUMBER_OF_PAGES)]
    blink_duration_total = [0 for i in range(NUMBER_OF_PAGES)]

    num_rows = len(df.index)
    count = 0
    # print("Iterating over every row:")
    starttime = time.time()

    for index, row in df.iterrows():   
        page = row['Page'] 
        aoi_type = row['AOI_TYPE']
        numbered_aoi = AOI_STRING_TO_AOI_NUMBER[aoi_type]
        blink_duration = row['BKDUR']

        if numbered_aoi > 0 and numbered_aoi < 7:
            blink_count[page] += 1
            blink_duration_total[page] += blink_duration

        curtime = time.time()
        elapsed_time = curtime - starttime
        count += 1
        progress = utils.progress_bar(count, num_rows, elapsed_time)
        print(progress, end="\r")

    print("")

    PAGE_LIST = []
    BLINK_COUNT_LIST = []
    TOTAL_BLINK_DURATION_LIST = []
    AVERAGE_BLINK_DURATION_LIST = []

    for i in range(NUMBER_OF_PAGES):
        PAGE_LIST.append(i)
        BLINK_COUNT_LIST.append(blink_count[i])
        TOTAL_BLINK_DURATION_LIST.append(blink_duration_total[i])
        if blink_count[i] != 0:
            AVERAGE_BLINK_DURATION_LIST.append(blink_duration_total[i]/blink_count[i])
        else:
            AVERAGE_BLINK_DURATION_LIST.append(0)

    new_df['Page'] = PAGE_LIST
    new_df['Blink_Count'] = BLINK_COUNT_LIST
    new_df['Total_Blink_Duration'] = TOTAL_BLINK_DURATION_LIST  
    new_df['Average_Blink_Duration'] = AVERAGE_BLINK_DURATION_LIST  

    return new_df