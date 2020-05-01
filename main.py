import core.convert_ratio as convert_ratio
import core.add_label as add_label
import core.fixations as fixations
import core.blinks as blinks
import core.calculations as calculations
import core.refixation as refixation
import core.pupil as pupil
import core.fixation_aoi as fixation_aoi
import core.blink_aoi as blink_aoi
import core.combine_per_aoi as combine_per_aoi
import core.combine_per_page as combine_per_page
import core.combine_per_aoipage as combine_per_aoipage
import core.combine_csv as combine_csv
import core.split_extra as split_extra
import core.compare_order_by_fixation as compare_order_by_fixation
import core.compare_order_by_click as compare_order_by_click
import core.calculate_switch as calculate_switch

import pandas as pd

import argparse
import sys
import json
import os

valid_commands = ["process_all", "process_one_user", "combine_csv", "split_extra", "compare_order_fixation", "compare_order_click", "switch_penalty", "drop_total", "median_split"]

# Start the command line arguments
s = "Various functions to calculate things relating to eye gaze, such as saccade calculations or\n\
Area of Interest (AOI) calculation. The valid commands are:\n\
{}".format(", ".join(valid_commands))
parser = argparse.ArgumentParser(description=s, formatter_class=argparse.RawDescriptionHelpFormatter)

subparsers = parser.add_subparsers(title="Valid commands", description="For additional help with \
these commands, type into the terminal:\n\
    python main.py command_name -h\n\
For example,\n\
    python main.py {} -h".format(valid_commands[0]), dest="command_name")

# Create parser for the process_all command
parser_process_all = subparsers.add_parser(valid_commands[0], help="Process all users")
parser_process_all.add_argument("path_to_folder", help="The path to user_study_data folder",
    metavar="path_to_user_study_folder")

# Create parser for the process_one_user command
parser_process_one_user = subparsers.add_parser(valid_commands[1], help="Process one user")
parser_process_one_user.add_argument("path_to_folder", help="The path to user folder",
    metavar="path_to_user_folder")

# Create parser for the combine_csv command
parser_combine_csv = subparsers.add_parser(valid_commands[2], help="Combine all produced csv")
parser_combine_csv.add_argument("path_to_folder", help="The path to user_study_data folder",
    metavar="path_to_user_study_folder")

# Create parser for the split_extra command
parser_split_extra = subparsers.add_parser(valid_commands[3], help="Split Extra Columnd from aoi csv")
parser_split_extra.add_argument("path_to_file", help="The path to aoi csv",
    metavar="path_to_file")

# Create parser for the compare_order_fixation command
parser_compare_order_fixation = subparsers.add_parser(valid_commands[4], help="compare_order_fixation")
parser_compare_order_fixation.add_argument("path_to_file", help="The path to combined aoi file",
    metavar="path_to_file")

# Create parser for the compare_order_click command
parser_compare_order_click = subparsers.add_parser(valid_commands[5], help="compare_order_click")
parser_compare_order_click.add_argument("path_to_file", help="The path to combined relevance result file",
    metavar="path_to_file")
    
# Create parser for the switch_penalty command
parser_switch_penalty = subparsers.add_parser(valid_commands[6], help="switch_penalty")
parser_switch_penalty.add_argument("path_to_file", help="The path to combined click result file",
    metavar="path_to_file")

# Create parser for the drop_total command
parser_switch_penalty = subparsers.add_parser(valid_commands[7], help="drop_total")
parser_switch_penalty.add_argument("path_to_file", help="The path to file",
    metavar="path_to_file")

# Create parser for the new_splits command
parser_new_split = subparsers.add_parser(valid_commands[8], help="Assign user differently")
parser_new_split.add_argument("path_to_folder", help="The path to user_study_data folder",
    metavar="path_to_user_study_folder")

# Compile all the command line parser and subparsers
args = parser.parse_args()

# If no outputs are supplied, print help
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

def process_one_user(folder_name):
    path_to_initial_file = folder_name + "initial_file.csv"
    path_to_collapsed_fixation_file = folder_name + "initial_fixation.csv"    
    path_to_task_file = folder_name + "task_file.csv"
    path_to_collapsed_blink_file = folder_name + "collapsed_blink.csv"
    path_to_fixation_per_AOI_file = folder_name + "fixation_aoi.csv"
    path_to_blink_per_AOI_file = folder_name + "blink_aoi.csv"
    path_to_combined_AOI_file = folder_name + "combined_aoi.csv"
    path_to_combined_page_file = folder_name + "combined_page.csv"
    path_to_combined_AOIpage_file = folder_name + "combined_aoipage.csv"
    
    convert_ratio.convert_ratio_to_pixel(path_to_initial_file)
    add_label.add_label(path_to_initial_file, path_to_task_file)
    blinks.collapse_to_blinks(path_to_initial_file, path_to_collapsed_blink_file)

    convert_ratio.convert_ratio_to_pixel(path_to_collapsed_fixation_file)
    add_label.add_label(path_to_collapsed_fixation_file, path_to_task_file)

    calculations.calculate(path_to_collapsed_fixation_file)
    refixation.calculate(path_to_collapsed_fixation_file)
    pupil.calculate_pupil(path_to_collapsed_fixation_file, path_to_task_file)

    fixation_aoi.calculate_fixation_per_aoi(path_to_collapsed_fixation_file, path_to_fixation_per_AOI_file)
    blink_aoi.calculate_blink_per_aoi(path_to_collapsed_blink_file, path_to_blink_per_AOI_file)
    
    combine_per_aoi.combine(path_to_fixation_per_AOI_file, path_to_blink_per_AOI_file, path_to_combined_AOI_file)
    combine_per_page.combine(path_to_collapsed_fixation_file, path_to_collapsed_blink_file, path_to_combined_page_file, path_to_task_file)    
    combine_per_aoipage.combine(path_to_combined_AOI_file, path_to_combined_page_file, path_to_combined_AOIpage_file)

# Process all users at once
if args.command_name == valid_commands[0]:
    root = args.path_to_folder
    dirlist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    dirlist = [x for x in dirlist if "NAH" not in x]
    dirlist = [x for x in dirlist if "User" in x]
    
    for x in dirlist:
        folder_name = args.path_to_folder + x + "/"
        process_one_user(folder_name)        

# Process one user
if args.command_name == valid_commands[1]:
    process_one_user(args.path_to_folder)

# Combine all csv files
if args.command_name == valid_commands[2]:
    combine_csv.combine_csv(args.path_to_folder)

# Split Extra column
if args.command_name == valid_commands[3]:
    split_extra.process_csv(args.path_to_file)

# Calculate order result by fixation
if args.command_name == valid_commands[4]:
    compare_order_by_fixation.compare_order_by_fixation(args.path_to_file)

# Calculate order result by click
if args.command_name == valid_commands[5]:
    compare_order_by_click.compare_order_by_click(args.path_to_file)

# Calculate switch penalty
if args.command_name == valid_commands[6]:
    calculate_switch.calculate_switch_prep(args.path_to_file)

if args.command_name == valid_commands[7]:
    input_file = args.path_to_file
    pd_dataframe = pd.read_csv(input_file, sep=",", index_col=False)
    cols = [c for c in pd_dataframe.columns if c.lower()[:4] != 'tota']
    pd_dataframe = pd_dataframe[cols]
    pd_dataframe.to_csv(input_file, index=False)

if args.command_name == valid_commands[8]:
    root = args.path_to_folder + "original"
    dirlist = [item for item in os.listdir(root) if os.path.isfile(os.path.join(root, item))]
    
    low_chinese_self_median = [5385,1338,671]
    high_chinese_self_median = [3545,132,1586,2068,2591]
    low_chinese_test_median = [5385,1338,671]
    high_chinese_test_median = [3545,132,1586,2068,2591]
    low_chinese_cefr_median = [5385,1338,671,2591]
    high_chinese_cefr_median = [3545,132,1586,2068]
    low_chinese_paper_median = [5385,1338,671,2591]
    high_chinese_paper_median = [3545,132,1586,2068]

    low_spanish_self_median = [5890,2899,6673,7734,6515,6965,1855,1699,2934,452,6853,1572,2929]
    high_spanish_self_median = [2128,2156,5492,3816,4799,5689]
    low_spanish_test_median = [5890,2899,7734,6515,3816,1855,1699,452,1572,2929]
    high_spanish_test_median = [2128,2156,5492,6673,6965,2934,4799,5689,6853]
    low_spanish_cefr_median = [5890,2899,1855,1699,452,1572,2929,6965]
    high_spanish_cefr_median = [2128,2156,6515,5492,6673,2934,4799,5689,6853,7734,3816]
    low_spanish_paper_median = [5890,2899,1855,1699,452,1572,2929,6965]
    high_spanish_paper_median = [2128,2156,6515,5492,6673,2934,4799,5689,6853,7734,3816]

    low_english_self_median = [3545,132,1586,6515,2591,671]
    high_english_self_median = [5890,2128,2156,5492,2899,6673,7734,2068,5385,6965,1338,3816,1855,1699,2934,4799,5689,452,6853,1572,2929]
    low_english_test_median = [3545,132,1586,2591,671,2156,5492,2899,2068,1338,3816,5689,2929]
    high_english_test_median = [5890,2128,6673,7734,5385,6965,1855,1699,2934,4799,452,6853,1572,6515]
    low_english_cefr_median = [3545,132,1586,6515,2591,671,6965,3816,4799,5689,6853]
    high_english_cefr_median = [5890,2128,2156,5492,2899,6673,7734,2068,5385,1338,1855,1699,2934,452,1572,2929]
    low_english_paper_median = [3545,1586,2591,671,6853]
    high_english_paper_median = [5890,2128,2156,5492,2899,6673,7734,2068,5385,1338,1855,1699,2934,452,1572,2929,132,6965,6515,3816,4799,5689]

    for item in dirlist:
        self_median_list = []
        test_median_list = []
        cefr_median_list = []
        paper_median_list = []        
        if "chinese" in item:
            df = pd.read_csv(root + "/" + item, sep=",", index_col=False)
            for index, row in df.iterrows():
                if row["userID"] in low_chinese_self_median:
                    self_median_list.append("Low")
                else:
                    self_median_list.append("High")

                if row["userID"] in low_chinese_test_median:
                    test_median_list.append("Low")
                else:
                    test_median_list.append("High")

                if row["userID"] in low_chinese_cefr_median:
                    cefr_median_list.append("Low")
                else:
                    cefr_median_list.append("High")
                
                if row["userID"] in low_chinese_paper_median:
                    paper_median_list.append("Low")
                else:
                    paper_median_list.append("High")
            
            cols = [c for c in df.columns if c.lower()[:4] != 'tota']
            df = df[cols]
            df = df.drop(columns=['userID'])
            
            if "aoipage" in item:
                df = df.drop(columns=['Page'])
                for i in range (1,7):
                    df = df.drop(columns=['Is_AOI_L1_AOI'+str(i)])
                    df = df.drop(columns=['Self_AOI_Language_Proficiency_AOI'+str(i)])
                    df = df.drop(columns=['Test_AOI_Language_Proficiency_AOI'+str(i)])

            df["Self Median"] = self_median_list
            name = item.replace("chinese", "chinese median self")
            df.to_csv(args.path_to_folder + "/medianself/" + name, index=False)            
            df = df.drop(columns=['Self Median'])

            df["Test Median"] = test_median_list
            name = item.replace("chinese", "chinese median test")
            df.to_csv(args.path_to_folder + "/mediantest/" + name, index=False)     
            df = df.drop(columns=['Test Median'])

            df["CEFR Median"] = cefr_median_list
            name = item.replace("chinese", "chinese median cefr")
            df.to_csv(args.path_to_folder + "/mediancefr/" + name, index=False)     
            df = df.drop(columns=['CEFR Median'])

            df["Paper Median"] = paper_median_list
            name = item.replace("chinese", "chinese median paper")
            df.to_csv(args.path_to_folder + "/medianpaper/" + name, index=False)                 
        elif "spanish" in item:
            df = pd.read_csv(root + "/" + item, sep=",", index_col=False)
            for index, row in df.iterrows():
                if row["userID"] in low_spanish_self_median:
                    self_median_list.append("Low")
                else:
                    self_median_list.append("High")

                if row["userID"] in low_spanish_test_median:
                    test_median_list.append("Low")
                else:
                    test_median_list.append("High")

                if row["userID"] in low_spanish_cefr_median:
                    cefr_median_list.append("Low")
                else:
                    cefr_median_list.append("High")
                
                if row["userID"] in low_spanish_paper_median:
                    paper_median_list.append("Low")
                else:
                    paper_median_list.append("High")
            
            cols = [c for c in df.columns if c.lower()[:4] != 'tota']
            df = df[cols]
            df = df.drop(columns=['userID'])
            
            if "aoipage" in item:
                df = df.drop(columns=['Page'])
                for i in range (1,7):
                    df = df.drop(columns=['Is_AOI_L1_AOI'+str(i)])
                    df = df.drop(columns=['Self_AOI_Language_Proficiency_AOI'+str(i)])
                    df = df.drop(columns=['Test_AOI_Language_Proficiency_AOI'+str(i)])

            df["Self Median"] = self_median_list
            name = item.replace("spanish", "spanish median self")
            df.to_csv(args.path_to_folder + "/medianself/" + name, index=False)            
            df = df.drop(columns=['Self Median'])

            df["Test Median"] = test_median_list
            name = item.replace("spanish", "spanish median test")
            df.to_csv(args.path_to_folder + "/mediantest/" + name, index=False)     
            df = df.drop(columns=['Test Median'])

            df["CEFR Median"] = cefr_median_list
            name = item.replace("spanish", "spanish median cefr")
            df.to_csv(args.path_to_folder + "/mediancefr/" + name, index=False)     
            df = df.drop(columns=['CEFR Median'])

            df["Paper Median"] = paper_median_list
            name = item.replace("spanish", "spanish median paper")
            df.to_csv(args.path_to_folder + "/medianpaper/" + name, index=False) 
        elif "english" in item:
            df = pd.read_csv(root + "/" + item, sep=",", index_col=False)
            for index, row in df.iterrows():
                if row["userID"] in low_english_self_median:
                    self_median_list.append("Low")
                else:
                    self_median_list.append("High")

                if row["userID"] in low_english_test_median:
                    test_median_list.append("Low")
                else:
                    test_median_list.append("High")

                if row["userID"] in low_english_cefr_median:
                    cefr_median_list.append("Low")
                else:
                    cefr_median_list.append("High")
                
                if row["userID"] in low_english_paper_median:
                    paper_median_list.append("Low")
                else:
                    paper_median_list.append("High")
            
            cols = [c for c in df.columns if c.lower()[:4] != 'tota']
            df = df[cols]
            df = df.drop(columns=['userID'])
            
            if "aoipage" in item:
                df = df.drop(columns=['Page'])
                for i in range (1,7):
                    df = df.drop(columns=['Is_AOI_L1_AOI'+str(i)])
                    df = df.drop(columns=['Self_AOI_Language_Proficiency_AOI'+str(i)])
                    df = df.drop(columns=['Test_AOI_Language_Proficiency_AOI'+str(i)])

            df["Self Median"] = self_median_list
            name = item.replace("english", "english median self")
            df.to_csv(args.path_to_folder + "/medianself/" + name, index=False)            
            df = df.drop(columns=['Self Median'])

            df["Test Median"] = test_median_list
            name = item.replace("english", "english median test")
            df.to_csv(args.path_to_folder + "/mediantest/" + name, index=False)     
            df = df.drop(columns=['Test Median'])

            df["CEFR Median"] = cefr_median_list
            name = item.replace("english", "english median cefr")
            df.to_csv(args.path_to_folder + "/mediancefr/" + name, index=False)     
            df = df.drop(columns=['CEFR Median'])

            df["Paper Median"] = paper_median_list
            name = item.replace("english", "english median paper")
            df.to_csv(args.path_to_folder + "/medianpaper/" + name, index=False) 