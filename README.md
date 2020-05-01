# EyeTrackerAnalysis
Analysis of Eye Tracking Data for the CSV files produced by Gazepoint Eyetracker

# How to Use
If any modules need to be installed, type the following into a terminal
```
python3 -m pip install -r requirements.txt
```
# How to Use
Required files:
- All-Relevances.csv 
- combined_relevances.csv
- results.csv
- users.csv
- task_file.csv
- initial_file.csv
- initial_fixation.csv 
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
To produce average read time based on fixation data
```
python3 main.py compare_order_fixation user_study_data/Combined/all_users_aoi\ all.csv
```
To produce average read time based on recorded click time
```
python3 main.py compare_order_click user_study_data/combined_relevances.csv
```
To produce average read time based on recorded click time
```
python3 main.py switch_penalty user_study_data/combined_duration_click.csv
```
To produce csv file based on median split
```
python3 main.py new_splits user_study_data/Combined_Median_Split/
```
To see the list of commands
```
python3 main.py -h
```

