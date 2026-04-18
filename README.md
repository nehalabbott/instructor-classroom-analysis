# Instructor Classroom Analytics Dashboard

An instructor-oriented analytics project that analyzes classroom activity and student engagement across multiple courses.  
The project provides insights into teaching workload, student participation trends, and assignment difficulty using structured classroom data.

# Project Overview

This project is designed from an instructor’s point of view and focuses on answering questions such as: (similar to spotify wrapped)
- How frequently did I post assignments and announcements?
- During which months was teaching activity the highest?
- When were students most active?
- Which assignments were the most challenging for students?

The analytics are presented through a dashboard built using Streamlit and Plotly.

# Key Features

# Instructor Activity Analysis
- Total assignments and announcements posted per course
- Monthly teaching workload trends

# Student Engagement Analysis
- Monthly submission patterns
- Identification of peak and low engagement periods

# Assignment Difficulty Analysis
- Difficulty score based on:
  - Average marks
  - Number of student submissions
- Handling of edge cases (ties, uniform values)

# Dashboard Visualization
- KPI cards for quick summary
- Interactive line charts for trends
- Ranking of hardest assignments
- Course-wise filtering

# Tech Stack

- Python
- Pandas – data processing
- Streamlit– dashboard framework
- Plotly – for visualizations
  
# How to Run
1. Clone the Repository
git clone https://github.com/your-username/instructor-classroom-analytics.git
cd instructor-classroom-analytics
2. Create a Virtual Environment 
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install pandas streamlit plotly

4. Run the Application
streamlit run app.py
6. Open in Browser

Once the app starts, it will automatically open in your browser.

6. Provide Dataset
Place your dataset file(s) inside the project directory (e.g., data/)
Ensure the file format matches the expected schema used in the code


