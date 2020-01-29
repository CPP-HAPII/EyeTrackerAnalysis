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

import argparse
import sys
import json

valid_commands = ["convert_ratio", "add_label", "fixation_collapse", "blink_collapse", "saccade_calc", 
                    "refix_calc", "calculate_fixation_per_aoi", "calculate_blink_per_aoi", "combine_per_aoi", "pupil_calc",
                    "combine_per_page", "process_all"]

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

# Create parser for the convert_ratio command
parser_convert_ratio = subparsers.add_parser(valid_commands[0], help="Convert the fixation ratio \
    into pixel values")
parser_convert_ratio.add_argument("initial_file", help="The path to initial file", metavar="init_file")

# Create parser for the add_label command
parser_add_label = subparsers.add_parser(valid_commands[1], help="Add AOI and Page Label")
parser_add_label.add_argument("initial_file", help="The path to initial file", metavar="init_file")
parser_add_label.add_argument("task_file", help="The path to the task file", metavar="task_file")

# Create parser for the fixation_collapse command
parser_fixation_collapse = subparsers.add_parser(valid_commands[2], help="Collapse a fixation file \
    into a smaller fixation file with one fixation per line")
parser_fixation_collapse.add_argument("init_fixation_file", help="The path to the initial fixation file",
    metavar="init_file")
parser_fixation_collapse.add_argument("collapsed_fixation_file", help="The path to the smaller, \
    collapsed fixation file", metavar="collapsed_file")

# Create parser for the blink_collapse command
parser_blink_collapse = subparsers.add_parser(valid_commands[3], help="Collapse a gaze file \
    into a blink file")
parser_blink_collapse.add_argument("init_fixation_file", help="The path to the initial file",
    metavar="init_file")
parser_blink_collapse.add_argument("collapsed_blink_file", help="The path to the smaller, \
    collapsed blink file", metavar="collapsed_file")    

# Create parser for the saccade calculation command
parser_saccade_calc = subparsers.add_parser(valid_commands[4], help="Calculate saccades based on \
    the fixations")
parser_saccade_calc.add_argument("collapsed_fixation_file", help="The path to the collapsed fixation file.",
    metavar="collapsed_file")

# Create parser for the refixation calculation command
parser_refixation_calc = subparsers.add_parser(valid_commands[5], help="Calculate refixation based on \
    the fixations")
parser_refixation_calc.add_argument("collapsed_fixation_file", help="The path to the collapsed fixation file.",
    metavar="collapsed_file")

# Create parser for the calculate_fixation_per_aoi command
parser_calc_fixation_per_aoi = subparsers.add_parser(valid_commands[6], help="Collapse a fixation file \
    per AOI")
parser_calc_fixation_per_aoi.add_argument("collapsed_fixation_file", help="The path to the collapsed fixation file",
    metavar="collapsed_fixation_file")
parser_calc_fixation_per_aoi.add_argument("fixation_aoi_file", help="The path to the fixation per AOI file", 
    metavar="fixation_aoi_file")

# Create parser for the calculate_blink_per_aoi command
parser_calc_blink_per_aoi = subparsers.add_parser(valid_commands[7], help="Collapse a blink file \
    per AOI")
parser_calc_blink_per_aoi.add_argument("collapsed_blink_file", help="The path to the collapsed blinking file",
    metavar="collapsed_blink_file")
parser_calc_blink_per_aoi.add_argument("blink_aoi_file", help="The path to the blink per AOI file", 
    metavar="blink_aoi_file")

# Create parser for the combine_per_aoi command
parser_aoi_combine = subparsers.add_parser(valid_commands[8], help="Combine fixation AOI and blinking AOI \
    files")
parser_aoi_combine.add_argument("fixation_aoi_file", help="The path to AOI fixation file",
    metavar="fixation_aoi_file")
parser_aoi_combine.add_argument("blink_aoi_file", help="The path to AOI Blink file", 
    metavar="blink_aoi_file")
parser_aoi_combine.add_argument("combined_aoi_file", help="The path to the combined file",
    metavar="combined_file")

# Create parser for the pupil_calc command
parser_pupil_calc = subparsers.add_parser(valid_commands[9], help="Calculate the difference of pupil diameter \
    from baseline")
parser_pupil_calc.add_argument("collapsed_fixation_file", help="The path to the collapsed fixation file",
    metavar="collapsed_fixation_file")
parser_pupil_calc.add_argument("task_file", help="The path to the task file", metavar="task_file")

# Create parser for the combine_per_page command
parser_page_combine = subparsers.add_parser(valid_commands[10], help="Combine fixation & blink into per page")
parser_page_combine.add_argument("collapsed_fixation_file", help="The path to collapsed",
    metavar="collapsed_fixation_file")
parser_page_combine.add_argument("collapsed_blink_file", help="The path to AOI Blink file", 
    metavar="collapsed_blink_file")
parser_page_combine.add_argument("combined_page_file", help="The path to the combined file",
    metavar="combined_page_file")

# Create parser for the process_all command
parser_process_all = subparsers.add_parser(valid_commands[11], help="Combine all commmands")
parser_process_all.add_argument("path_to_folder", help="The path to user folder",
    metavar="path_to_folder")

# Compile all the command line parser and subparsers
args = parser.parse_args()

# If no outputs are supplied, print help
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

# Handle Convert Ratio
if args.command_name == valid_commands[0]:
    convert_ratio.convert_ratio_to_pixel(args.initial_file)

# Handle Add Label 
if args.command_name == valid_commands[1]:
    add_label.add_label(args.initial_file, args.task_file)

# Handle Fixation Collapse
if args.command_name == valid_commands[2]:
    fixations.collapse_to_fixations(args.init_fixation_file, args.collapsed_fixation_file)

# Handle Blink Collapse
if args.command_name == valid_commands[3]:
    blinks.collapse_to_blinks(args.init_fixation_file, args.collapsed_blink_file)

# Handle Saccade calculation
if args.command_name == valid_commands[4]:
    calculations.calculate(args.collapsed_fixation_file)

# Handle Refixation calculation
if args.command_name == valid_commands[5]:
    refixation.calculate(args.collapsed_fixation_file)

# Handle Fixation AOI calculation
if args.command_name == valid_commands[6]:
    fixation_aoi.calculate_fixation_per_aoi(args.collapsed_fixation_file, args.fixation_aoi_file)

# Handle Blink AOI calculation
if args.command_name == valid_commands[7]:
    blink_aoi.calculate_blink_per_aoi(args.collapsed_blink_file, args.blink_aoi_file)

# Handle Combine AOI
if args.command_name == valid_commands[8]:
    combine_per_aoi.combine(args.fixation_aoi_file, args.blink_aoi_file, args.combined_aoi_file)

# Handle Pupil AOI calculation
if args.command_name == valid_commands[9]:
    pupil.calculate_pupil(args.collapsed_fixation_file, args.task_file)

# Handle Combine Page
if args.command_name == valid_commands[10]:
    combine_per_page.combine(args.collapsed_fixation_file, args.collapsed_blink_file, args.combined_page_file, ".")

# Handle all commands at once
if args.command_name == valid_commands[11]:
    folder_name = args.path_to_folder

    path_to_initial_file = folder_name + "initial_file.csv"
    path_to_collapsed_fixation_file = folder_name + "initial_fixation.csv"    
    path_to_task_file = folder_name + "task_file.csv"
    path_to_collapsed_blink_file = folder_name + "collapsed_blink.csv"
    path_to_fixation_per_AOI_file = folder_name + "fixation_aoi.csv"
    path_to_blink_per_AOI_file = folder_name + "blink_aoi.csv"
    path_to_combined_AOI_file = folder_name + "combined_aoi.csv"
    path_to_combined_page_file = folder_name + "combined_page.csv"
    
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
