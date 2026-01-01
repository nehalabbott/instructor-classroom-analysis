import pandas as pd

#loading data
posts = pd.read_csv("data/classroom_post.csv")
submissions = pd.read_csv("data/student_submissions.csv")
students = pd.read_csv("data/students.csv")

#date conversion
posts["post_date"] = pd.to_datetime(posts["post_date"])
submissions["submit_date"] = pd.to_datetime(submissions["submit_date"])

posts["month"] = posts["post_date"].dt.month_name()
submissions["month"] = submissions["submit_date"].dt.month_name()


print("INSTRUCTOR CLASSROOM ANALYSIS")

#instructors posting summary
print("Instructor Posting Summary (per course):")
post_summary = (
    posts.groupby(["class_id", "post_type"])
    .size()
    .reset_index(name="count")
)
print(post_summary)

#monthly activity
print("\nInstructor Activity by Month:")
monthly_posts = (
    posts.groupby(["class_id", "month"])
    .size()
    .reset_index(name="posts")
)
print(monthly_posts)

#student activity summary
print("\nStudent Activity by Month:")
monthly_submissions = (
    submissions.groupby(["class_id", "month"])
    .size()
    .reset_index(name="submissions")
)
print(monthly_submissions)

#hardest assignment analysis
print("\nHARDEST ASSIGNMENT ANALYSIS ")

assignment_stats = (
    submissions
    .groupby(["class_id", "assignment_id"])
    .agg(
        avg_marks=("marks", "mean"),
        submission_count=("student_id", "count")
    )
    .reset_index()
)

def safe_normalize(series):
    if series.max() == series.min():
        return 0.5
    return (series - series.min()) / (series.max() - series.min())

# Normalize per course
assignment_stats["norm_avg_marks"] = (
    assignment_stats.groupby("class_id")["avg_marks"]
    .transform(safe_normalize)
)

assignment_stats["norm_submission_count"] = (
    assignment_stats.groupby("class_id")["submission_count"]
    .transform(safe_normalize)
)

# Combined difficulty score
assignment_stats["difficulty_score"] = (
    (1 - assignment_stats["norm_avg_marks"]) +
    (1 - assignment_stats["norm_submission_count"])
)

# Bring assignment post dates (tie-breaker)
assignment_dates = posts[posts["post_type"] == "assignment"][
    ["class_id", "post_id", "post_date"]
].rename(columns={"post_id": "assignment_id"})

assignment_stats = assignment_stats.merge(
    assignment_dates, on=["class_id", "assignment_id"], how="left"
)

# Pick hardest assignment per course
hardest_assignment = (
    assignment_stats
    .sort_values(
        ["difficulty_score", "post_date"],
        ascending=[False, True]  # earlier assignment wins tie
    )
    .groupby("class_id")
    .first()
    .reset_index()
)

#output
for _, row in hardest_assignment.iterrows():
    print(f"\nCourse: {row['class_id']}")
    print(f"→ Hardest Assignment: {row['assignment_id']}")
    print(f"→ Average Marks: {row['avg_marks']:.2f}")
    print(f"→ Submission Count: {int(row['submission_count'])}")
    print(f"→ Difficulty Score: {row['difficulty_score']:.2f}")
    print("-" * 40)

#monthly insights
print("\nMONTHLY INSIGHTS")

for course in posts["class_id"].unique():
    print(f"\nCourse: {course}")

    # Instructor activity
    course_posts = posts[posts["class_id"] == course]
    instructor_monthly = (
        course_posts.groupby("month")
        .size()
        .sort_values(ascending=False)
    )

    most_active_instructor_month = instructor_monthly.idxmax()

    print(f" Instructor was most active in {most_active_instructor_month}.")

    # Student activity
    course_submissions = submissions[submissions["class_id"] == course]

    if not course_submissions.empty:
        student_monthly = (
            course_submissions.groupby("month")
            .size()
            .sort_values(ascending=False)
        )

        most_active_student_month = student_monthly.idxmax()
        least_active_student_month = student_monthly.idxmin()

        print(f"Students were most active in {most_active_student_month}.")
        print(f"Lowest student engagement was in {least_active_student_month}.")
    else:
        print("No student submission data available.")

