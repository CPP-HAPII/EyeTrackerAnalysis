import pandas as pd
import math
import os
import time
from core import utils

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

def combine(input_file, input2_file, output_file):
    """
    Combine 2 AOI Files.

    :param input_file: Fixation AOI file
    :param input_file: Blinking AOI file    
    :param output_file: Combined AOI file    
    """
    print("Combining data per AOI...")
    
    # print("Reading Fixation AOI...")
    fixation_dataframe = pd.read_csv(input_file, sep=",", index_col=False)
    # print("Finished loading in \"{}\" file".format(input_file))

    # print("Reading Blinking AOI...")
    blinking_dataframe = pd.read_csv(input2_file, sep=",", index_col=False)
    # print("Finished loading in \"{}\" file".format(input2_file))

    all_relevances_dataframe = pd.read_csv("user_study_data/All-Relevances.csv", sep=",", index_col=False)
    all_results_dataframe = pd.read_csv("user_study_data/results.csv", sep=",", index_col=False)

    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    # if (os.path.exists(output_file)):
    #s    overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(output_file).replace("\\", "/"))

    if overwrite.lower() == "y":
        new_df = pd.DataFrame()
        new_df = pd.merge(fixation_dataframe, blinking_dataframe,  how='left', on=['AOI_TYPE','Page'])
        new_df = new_df[new_df.Page != 0]
        new_df = new_df[new_df.AOI_TYPE != "NOT_AOI"]
        #new_df = new_df[new_df.Total_Fixation_Count != 0]
        new_df = new_df[new_df.AOI_TYPE != "QUERY"]
        
        userID = new_df['userID'].iloc[0]
        user_dataframe = all_relevances_dataframe.loc[all_relevances_dataframe['userID'] == userID]

        page = 1
        counter = 0
        PAGE_LIST = []
        AOI_LIST = []
        QUERY_LANGUAGE_LIST = []

        for index, row in user_dataframe.iterrows():
            if counter == 0:
                QUERY_LANGUAGE_LIST.append(row["QueryLanguage"])                                
            if counter == 6:
                counter = 0
                QUERY_LANGUAGE_LIST.append(row["QueryLanguage"])                                
                page += 1
            PAGE_LIST.append(page)
            AOI_LIST.append(AOI_NUMBER_TO_AOI_STRING[row['Rank']+1])
            counter += 1

        user_dataframe["Page"] = PAGE_LIST
        user_dataframe["AOI_TYPE"] = AOI_LIST    

        result_df = pd.merge(user_dataframe, all_results_dataframe[['ID','Language']], left_on=['resultID'], right_on=['ID'], how='left')

        new_df = pd.merge(new_df,result_df[['Page', 'AOI_TYPE', 'Language']], on=['Page','AOI_TYPE'], how='left')
        new_df = new_df.rename(columns={"Language": "AOILanguage"})
        
        CURRENT_AOI_LANGUAGE_LIST = []
        PREVIOUS_AOI_LANGUAGE_LIST = []        
        counter = 0
        userID = 0

        for index, row in new_df.iterrows():
            userID = row["userID"]
            if row['AOI_TYPE'] == "QUERY":
                CURRENT_AOI_LANGUAGE_LIST.append(QUERY_LANGUAGE_LIST[counter])
                PREVIOUS_AOI_LANGUAGE_LIST.append("N/A")
                counter += 1
            else:
                CURRENT_AOI_LANGUAGE_LIST.append(row['AOILanguage'])
                PREVIOUS_AOI_LANGUAGE_LIST.append(CURRENT_AOI_LANGUAGE_LIST[len(CURRENT_AOI_LANGUAGE_LIST)-2])                

        new_df["AOILanguage"] = CURRENT_AOI_LANGUAGE_LIST
        new_df["PreviousAOILanguage"] = PREVIOUS_AOI_LANGUAGE_LIST

        L1 = "N/A"
        self_english = "N/A"
        test_english = "N/A"
        self_other = "N/A"
        test_other = "N/A"
        users_df = pd.read_csv("user_study_data/users.csv", sep=",", index_col=False)
        for index, row in users_df.iterrows():
            participant = row['Participant']
            if userID == participant:
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

        LANGUAGE_SWITCH_LIST = []
        SELF_AOI_PROFICIENCY_LIST = []
        TEST_AOI_PROFICIENCY_LIST = []
        IS_L1_LIST = []
        for index, row in new_df.iterrows():
            if row["AOILanguage"] == row["PreviousAOILanguage"]:
                LANGUAGE_SWITCH_LIST.append("No")                
            else:
                LANGUAGE_SWITCH_LIST.append("Yes")

            if row["AOILanguage"] == "English":
                SELF_AOI_PROFICIENCY_LIST.append(self_english)
                TEST_AOI_PROFICIENCY_LIST.append(test_english)
            else:
                SELF_AOI_PROFICIENCY_LIST.append(self_other)
                TEST_AOI_PROFICIENCY_LIST.append(test_other)

            if L1 == "Both":
                IS_L1_LIST.append("Yes")
            elif L1 == row["AOILanguage"]:
                IS_L1_LIST.append("Yes")
            else:
                IS_L1_LIST.append("No")

        new_df["LanguageSwitch"] = LANGUAGE_SWITCH_LIST
        new_df["Self AOI_Language_Prof"] = SELF_AOI_PROFICIENCY_LIST
        new_df["Test AOI_Language_Prof"] = TEST_AOI_PROFICIENCY_LIST
        new_df["Is_AOI_L1"] = IS_L1_LIST
            
        new_df.to_csv(output_file, index=False)
       
        #print(new_df.mean(axis = 0, skipna = True))
        
        print("Finished exporting to {}".
              format(output_file).replace("\\", "/"))
    else:
        print("Exiting...")