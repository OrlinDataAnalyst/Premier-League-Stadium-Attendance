import pandas as pd
import numpy as np

# Load data
matches = pd.read_csv('data/matches.csv', encoding='latin1')
stadiums = pd.read_csv('data/stadiums.csv', encoding='latin1')
performance = pd.read_csv('data/team_performance.csv', encoding='latin1')

# Cleaning & standardizing key columns
performance = performance[performance["season_end_year"] >= 2017].copy()    # Keep data from 2017 onwards and ensure safe, independent manipulation (copy)
performance = performance.rename(columns={                                  # Rename columns for clarity
    'team': 'Team', 'position': 'Position', 'played': 'Played',
    'won': 'Won', 'drawn': 'Drawn', 'lost': 'Lost', 'gf': 'Goals_For',
    'ga': 'Goals_Against', 'gd': 'Goal_Difference', 'points': 'Points',
    'season_end_year': 'Season_End_Year'}
)

performance = performance.drop(columns=['notes'])   # Drop unnecessary columns
stadiums = stadiums[stadiums['Country'].str.contains('England', case=False, na=False)].copy()   # Keep only English stadiums
stadiums['Stadium'] = stadiums['Stadium'].replace('White Hart Lane', 'Tottenham Hotspur Stadium')   # Update stadium name
matches['Match_Date'] = pd.to_datetime(matches['Date'], errors='coerce')    # Parse dates and handle errors as NoT (Not a Time)
matches = matches.dropna(subset=['Match_Date'])   # Remove rows where date failed to parse
matches = matches[(matches['Match_Date'] < '2020-03-01') | (matches['Match_Date'] > '2021-08-01')].copy()   # Remove matches during COVID-19 restrictions
matches = matches.rename(columns={'Venue': 'Stadium'})  # Standardize to 'Stadium'
matches['Score'] = matches['Score'].str.replace(r'\D+', ':', regex=True).str.strip(':')   # Fix encoding issue in 'Score'

# Standardize text columns for merging
def clean_text(series):
    return (
        series.astype(str)
        .str.lower()
        .str.strip()
        .str.replace("&", "and", regex=False)   
        .str.replace("-", " ", regex=False)
    )

matches["Stadium"] = clean_text(matches["Stadium"])
stadiums["Stadium"] = clean_text(stadiums["Stadium"])
matches["Home_Team"] = clean_text(matches["Home_Team"])
performance["Team"] = clean_text(performance["Team"])

# Fix various misspellings of Nottingham Forest
forest_fix = {      
    "nott'ham forest": "nottingham forest",
    "nott'm forest": "nottingham forest",
    "nott ham forest": "nottingham forest"
}

matches["Home_Team"] = matches["Home_Team"].replace(forest_fix)
performance["Team"] = performance["Team"].replace(forest_fix)

# Merge stadium capacity
matches_stadiums = matches.merge(
    stadiums[["Stadium", "Capacity"]].drop_duplicates('Stadium'),   # Prevent potential data inflation from duplicate stadium entries
    on="Stadium",
    how="left"
)

# Extract date features
matches_stadiums["Day_of_Week"] = matches_stadiums["Match_Date"].dt.day_name()
matches_stadiums["Is_Weekend"] = matches_stadiums["Day_of_Week"].isin(["Saturday", "Sunday"]).astype(int)

# Create Season column from match date (e.g., 2022/2023)
def get_season(date):
    year, month = date.year, date.month
    return f"{year}/{year+1}" if month >= 8 else f"{year-1}/{year}"

matches_stadiums["Season"] = matches_stadiums["Match_Date"].apply(get_season)

# Create Season column from performance year (e.g., 2017/2018)
def format_season(year):
    return f"{int(year)-1}/{int(year)}"

performance['Season'] = performance['Season_End_Year'].apply(format_season)

# Merge team performance data
matches_perf = matches_stadiums.merge(
    performance,
    left_on=["Home_Team", "Season"],
    right_on=["Team", "Season"],
    how="left" 
).drop(columns=['Team']).copy()   # Remove the redundant 'Team' column

# Fill missing attendance with the average of that team's other home games that season
matches_perf['Attendance'] = matches_perf['Attendance'].fillna(
    matches_perf.groupby(['Home_Team', 'Season'])['Attendance'].transform('mean')
)

# Fill missing capacities with the median if any stadiums didn't match
matches_perf['Capacity'] = matches_perf['Capacity'].fillna(matches_perf['Capacity'].median())

# Convert numeric columns to integers
matches_perf['Attendance'] = matches_perf['Attendance'].round(0).astype('int64')
matches_perf['Capacity'] = matches_perf['Capacity'].round(0).astype('int64')

# Select relevant performance columns
performance_cols = [
    'Points', 'Position', 'Goal_Difference'
]

# FINAL DATASET
matches_perf.to_csv('matches_perf_cleaned.csv', index=False, encoding='utf-8-sig')

# EXPLORATORY DATA ANALYSIS
matches_perf.shape
matches_perf.info()
matches_perf.describe()
matches_perf.head()

# 01. Visualize Attendance Distribution
import matplotlib.pyplot as plt

plt.hist(matches_perf['Attendance'], bins=30)
plt.title("Distribution of Match Attendance")
plt.xlabel("Attendance")
plt.ylabel("Number of Matches")
plt.show()

# 02. Compare Attendance: Weekend vs Weekday
avg_attendance = matches_perf.groupby('Is_Weekend')['Attendance'].mean().round(0).astype(int)
avg_attendance.index = ['Weekday', 'Weekend']
print("Average Attendance by Match Day Type:")
print(avg_attendance)

# Boxplot Visualization
matches_perf.boxplot(
    column='Attendance',
    by='Is_Weekend'
)
plt.title("Attendance: Weekday vs Weekend")
plt.suptitle("")
plt.show()

# 03. Scatter Plot: Attendance vs Stadium Capacity
plt.scatter(
    matches_perf['Capacity'],
    matches_perf['Attendance'],
    alpha=0.5
)
plt.xlabel("Stadium Capacity")
plt.ylabel("Attendance")
plt.title("Attendance vs Stadium Capacity")
plt.show()

# 04. Scatter Plot: Attendance vs Team Performance (Points)
plt.scatter(
    matches_perf['Points'],
    matches_perf['Attendance'],
    alpha=0.5
)
plt.xlabel("Season Points")
plt.ylabel("Attendance")
plt.title("Attendance vs Team Performance")
plt.show()

# 05. Correlation Analysis
features = [
    'Attendance',
    'Capacity',
    'Points',
    'Is_Weekend'
]

matches_perf[features].corr()

# 06. Calculate Capacity Fill Rate
matches_perf['Capacity_Fill_Rate'] = (
    matches_perf['Attendance'] / matches_perf['Capacity']
).clip(upper=1.0)   # Cap at 100%

matches_perf['Capacity_Fill_Rate'].describe()

# 07. Top 10 Teams by Average Capacity Fill Rate
matches_perf.groupby('Home_Team')['Capacity_Fill_Rate'].mean() \
    .sort_values(ascending=False).head(10)



