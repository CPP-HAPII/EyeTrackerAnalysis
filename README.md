# EyeTrackerAnalysis
Analysis of Eye Tracking Data

# How to Use
If any modules need to be installed, type the following into a terminal
```
python3 -m pip install -r requirements.txt
```
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
To see the list of commands
```
python3 main.py -h
```