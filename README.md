# EyeTrackerAnalysis
Analysis of Eye Tracking Data for the CSV files produced by Gazepoint Eyetracker

# How to Use
If any modules need to be installed, type the following into a terminal
```
python3 -m pip install -r requirements.txt
```
# How to Use
Required files:
- results.csv: csv file containing all possible search results for the user study
- users.csv: csv file containing userID, L1, and Proficiencies
- All-Relevances.csv: csv file containing all the timestamps when the user submitted a relevance judgment

- task_file.csv: individual user csv file containing timestamps of when the user move from a page to the next
- initial_file.csv: individual user csv file containing all eye gaze data (obtained from Gazepoint)
- initial_fixation.csv: individual user csv file containing eye gaze data per fixation (obtained from Gazepoint)
# How to Run
To process all users' data at once
```
python3 main.py process_all user_study_data/
```
To process one user's data at a time
```
python3 main.py process_one_user user_study_data/<User#folder>/
```
To combine the csv files produced 
```
python3 main.py combine_csv user_study_data/
```
To produce average read time based on recorded click time
```
python3 main.py compare_order_click user_study_data/combined_relevances.csv
```
To produce read time based on L1 and recorded click time
```
python3 main.py switch_penalty user_study_data/combined_duration_click.csv
```
To produce read time based on Relevance Judgement and recorded click time
```
python3 main.py compare_by_relevance user_study_data/combined_relevances.csv
```
To produce csv files based on median split instead of three-way split
```
python3 main.py median_split user_study_data/Combined_Median_Split/
```
To see the list of commands
```
python3 main.py -h
```

