import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

MONTH_ORDER = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

st.set_page_config(
    page_title="Instructor Classroom Dashboard",
    layout="wide"
)

st.title("Your Classroom Dashboard")

#load data
posts = pd.read_csv("data/classroom_post.csv")
submissions = pd.read_csv("data/student_submissions.csv")

#conversion
posts["post_date"] = pd.to_datetime(posts["post_date"])
submissions["submit_date"] = pd.to_datetime(submissions["submit_date"])
posts["month"] = posts["post_date"].dt.month_name()
submissions["month"] = submissions["submit_date"].dt.month_name()

course = st.sidebar.selectbox(
    "Select Course",
    sorted(posts["class_id"].unique())
)

course_posts = posts[posts["class_id"] == course]
course_subs = submissions[submissions["class_id"] == course]

#KPI cards
total_assignments = course_posts[course_posts["post_type"] == "assignment"].shape[0]
total_announcements = course_posts[course_posts["post_type"] == "announcement"].shape[0]
total_submissions = course_subs.shape[0]

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Assignments Posted", total_assignments)
kpi2.metric("Announcements Posted", total_announcements)
kpi3.metric("Total Submissions", total_submissions)


monthly_posts = (
    course_posts.groupby("month")
    .size()
    .reindex(MONTH_ORDER, fill_value=0)
    .reset_index()
)

monthly_posts.columns = ["month", "posts"]

fig_posts = px.line(
    monthly_posts,
    x="month",
    y="posts",
    markers=True,
    title="Your Monthly Activity",
)

st.plotly_chart(fig_posts, use_container_width=True)

monthly_subs = (
    course_subs.groupby("month")
    .size()
    .reindex(MONTH_ORDER, fill_value=0)
    .reset_index()
)

monthly_subs.columns = ["month", "submissions"]

fig_subs = px.line(
    monthly_subs,
    x="month",
    y="submissions",
    markers=True,
    title="Student Engagement",
)

st.plotly_chart(fig_subs, use_container_width=True)

st.subheader("How difficult were the assignments you made??")

assignment_stats = (
    course_subs
    .groupby("assignment_id")
    .agg(
        avg_marks=("marks", "mean"),
        submissions=("student_id", "count")
    )
    .reset_index()
)

def safe_norm(s):
    return (s - s.min()) / (s.max() - s.min()) if s.max() != s.min() else 0.5

assignment_stats["difficulty_score"] = (
    (1 - safe_norm(assignment_stats["avg_marks"])) +
    (1 - safe_norm(assignment_stats["submissions"]))
)

fig_diff = px.bar(
    assignment_stats.sort_values("difficulty_score"),
    x="difficulty_score",
    y="assignment_id",
    orientation="h",
    title="Difficulty Ranking"
)

st.plotly_chart(fig_diff, use_container_width=True)

hardest = assignment_stats.sort_values("difficulty_score", ascending=False).iloc[0]

st.success(
    f"Hardest Assignment Goes to... {hardest['assignment_id']}  |  "
    f" The average marks scored in it were..{hardest['avg_marks']:.2f}  |  "
    f" No. of students who dared to submit it were..{int(hardest['submissions'])} students"
)

st.subheader("Insights")

instructor_monthly = (
    course_posts.groupby("month")
    .size()
    .reset_index(name="posts")
)

# Ensure correct month order
instructor_monthly["month"] = pd.Categorical(
    instructor_monthly["month"],
    categories=MONTH_ORDER,
    ordered=True
)
instructor_monthly = instructor_monthly.sort_values("month")

most_active_month = instructor_monthly.loc[
    instructor_monthly["posts"].idxmax(), "month"
]

least_active_month = instructor_monthly.loc[
    instructor_monthly["posts"].idxmin(), "month"
]

hardest_assignment = assignment_stats.sort_values(
    "difficulty_score", ascending=False
).iloc[0]

st.info(f"You were **most active** in **{most_active_month}**.")
st.info(f"You were **least active** in **{least_active_month}**.")
st.info(
    f"The **hardest assignment** of this course was **{hardest_assignment['assignment_id']}** "
    f"(Avg Marks: {hardest_assignment['avg_marks']:.2f}, "
    f"Submissions: {int(hardest_assignment['submissions'])})."
)
