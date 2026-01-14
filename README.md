# Stadium Attendance Analysis (Premier League)
## Project Overview

This project analyzes Premier League stadium attendance patterns across multiple seasons, focusing on how stadium capacity, team performance, and match scheduling influence demand.

The goal is to demonstrate a full data analytics workflow:

- Data cleaning & feature engineering (Python)
- Exploratory Data Analysis (EDA)
- Interactive dashboarding (Power BI)
- Business-focused insights and storytelling

The project is designed for portfolio and interview use, targeting junior data analyst roles.

## Key Business Questions

- Are stadiums operating at full capacity, or is demand underutilized?
- Does better team performance lead to higher attendance?
- Do weekend matches attract more fans than weekdays?
- Which teams consistently sell out their stadiums?
- How did attendance patterns change across seasons?

## Files Included
├── data/
│   ├── matches.csv
│   ├── stadiums.csv
│   └── team_performance.csv
│
├── notebooks/
│   └── stadium_attendance_analysis.py
│
├── powerbi/
│   └── Stadium_Attendance_Dashboard.pbix
│
├── presentation/
│   └── Stadium_Attendance_Insights.pptx
│
├── matches_perf_cleaned.csv
│
└── README.md

## File Descriptions

- Premier_League_Stadium_Attendance_Analysis.py
Python script for data cleaning, feature engineering, and exploratory data analysis

- Premier_League_Stadium_Attendance_Dashboard.pbix
Interactive Power BI dashboard with filters and drill-downs

- Premier_League_Stadium_Attendance_Insights.pdf
Stakeholder-ready presentation with key insights and recommendations

## Key Insights You Can Explore
1️⃣ Attendance & Capacity Utilization

- Average stadium fill rate is ~91%
- Many top teams operate near or at full capacity
- Attendance is often supply-constrained, not demand-constrained

2️⃣ Capacity vs Demand

- Strong relationship between stadium capacity and attendance
- Larger stadiums do not always guarantee higher utilization

3️⃣ Team Performance Impact

- Better-performing teams generally show higher fill rates
- Some teams sell out regardless of league position

4️⃣ Scheduling Effects

- Weekend matches have slightly higher average attendance
- The difference is modest, indicating loyal fanbases

5️⃣ Seasonality

- Attendance dipped during COVID-affected seasons
- Recovery observed in post-COVID seasons

## Data Sources

- Match Data: Historical Premier League match records
- Stadium Data: Stadium capacities and locations
- Team Performance Data: League position, points, and goal statistics
- All datasets are publicly available and used for educational purposes only.

## Database & Compatibility

- Data Format: CSV
- Processing: Python (Pandas, NumPy, Matplotlib)
- Visualization: Power BI Desktop

## OS Compatibility

- Windows: ✅ Full support
- macOS / Linux: Python supported; Power BI requires VM or Power BI Service

## How to Run This Project
### Step 1: Python Analysis

1. Clone the repository
2. Install required libraries:

pip install pandas numpy matplotlib

3. Run the script:

python stadium_attendance_analysis.py

4. This generates matches_perf_cleaned.csv

### Step 2: Power BI Dashboard

1. Open Power BI Desktop
2. Load Stadium_Attendance_Dashboard.pbix
3. Ensure the data source path points to matches_perf_cleaned.csv
4. Use season slicers and filters to explore insights

## Skills Demonstrated

- Data Cleaning & Feature Engineering
- Exploratory Data Analysis (EDA)
- Data Modeling & Joins
- Statistical Thinking
- Data Visualization Best Practices
- Power BI (DAX, measures, slicers, dashboards)
- Business Insight & Data Storytelling
- Portfolio-Ready Documentation

## License

This project is licensed under the MIT License.
You are free to use, modify, and share this project with attribution.

## Author

Orlin
Aspiring Data Analyst

Skills: Python · Pandas · Power BI · Data Visualization

This project was created for portfolio and junior data analyst role applications.
