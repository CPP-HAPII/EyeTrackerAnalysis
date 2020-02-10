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

import argparse
import sys
import json
import os

valid_commands = ["process_all", "process_one_user", "combine_csv", "split_extra"]

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

# Create parser for the process_all command
parser_combine_csv = subparsers.add_parser(valid_commands[2], help="Combine all produced csv")
parser_combine_csv.add_argument("path_to_folder", help="The path to user_study_data folder",
    metavar="path_to_user_study_folder")

# Create parser for the process_all command
parser_split_extra = subparsers.add_parser(valid_commands[3], help="Split Extra Columnd from aoi csv")
parser_split_extra.add_argument("path_to_file", help="The path to aoi csv",
    metavar="path_to_file")

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