import pandas as pd

posts = pd.read_csv("data/classroom_post.csv")
submissions = pd.read_csv("data/student_submissions.csv")
students = pd.read_csv("data/students.csv")

#date conversion
posts["post_date"] = pd.to_datetime(posts["post_date"])
submissions["submit_date"] = pd.to_datetime(submissions["submit_date"])
posts["month"] = posts["post_date"].dt.month_name()
submissions["month"] = submissions["submit_date"].dt.month_name()

print("INSTRUCTOR CLASSROOM ANALYSIS")

print("Instructor Posting Summary (per course):")
post_summary = (
    posts.groupby(["class_id", "post_type"])
    .size()
    .reset_index(name="count")
)
print(post_summary)

print("\nInstructor Activity by Month:")
monthly_posts = (
    posts.groupby(["class_id", "month"])
    .size()
    .reset_index(name="posts")
)
print(monthly_posts)

print("\nStudent Activity by Month:")
monthly_submissions = (
    submissions.groupby(["class_id", "month"])
    .size()
    .reset_index(name="submissions")
)
print(monthly_submissions)

print("\nHARDEST ASSIGNMENT ANALYSIS ")

#caluclate hardest assign by the normalized avg. marks and the no. of submissions

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

# normalize marks and submission count to combine fairly

assignment_stats["norm_avg_marks"] = (
    assignment_stats.groupby("class_id")["avg_marks"]
    .transform(safe_normalize)
)

assignment_stats["norm_submission_count"] = (
    assignment_stats.groupby("class_id")["submission_count"]
    .transform(safe_normalize)
)

assignment_stats["difficulty_score"] = (
    (1 - assignment_stats["norm_avg_marks"]) +
    (1 - assignment_stats["norm_submission_count"])
)

#if tie, then judge acc to post date
assignment_dates = posts[posts["post_type"] == "assignment"][
    ["class_id", "post_id", "post_date"]
].rename(columns={"post_id": "assignment_id"})

assignment_stats = assignment_stats.merge(
    assignment_dates, on=["class_id", "assignment_id"], how="left"
)

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

for _, row in hardest_assignment.iterrows():
    print(f"\nCourse: {row['class_id']}")
    print(f"→ Hardest Assignment: {row['assignment_id']}")
    print(f"→ Average Marks: {row['avg_marks']:.2f}")
    print(f"→ Submission Count: {int(row['submission_count'])}")
    print(f"→ Difficulty Score: {row['difficulty_score']:.2f}")
    print("-" * 40)

print("\nYour Academic year looked something like this..")

for course in posts["class_id"].unique():
    print(f"\nCourse: {course}")

    course_posts = posts[posts["class_id"] == course]
    instructor_monthly = (
        course_posts.groupby("month")
        .size()
        .sort_values(ascending=False)
    )

    most_active_instructor_month = instructor_monthly.idxmax()

    print(f" Instructor was most active in {most_active_instructor_month}.")

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

