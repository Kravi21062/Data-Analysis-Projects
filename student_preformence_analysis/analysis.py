import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv("data.csv")

print(" Student Performance Data Analysis")
print("-----------------------------------")

# Show first few rows
print("\n Data Preview:")
print(data.head())

# Show basic statistics
print("\n Summary Statistics:")
print(data.describe())

# Average marks of all subjects
print("\n Average Marks:")
print(data[['Math', 'Science', 'English']].mean())

# Add total marks column
data['Total'] = data['Math'] + data['Science'] + data['English']

# Find the topper
topper = data.loc[data['Total'].idxmax()]
print("\n Topper of the class:")
print(topper[['Name', 'Total']])

# Save updated data
data.to_csv("result.csv", index=False)
print("\n File saved as 'result.csv'")


# Visualization Section
# Bar chart - Total marks by student
plt.figure(figsize=(8,5))
plt.bar(data["Name"], data["Total"], color="skyblue")
plt.title("Total Marks by Student")
plt.xlabel("Student Name")
plt.ylabel("Total Marks")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Line chart - Subject comparison
plt.figure(figsize=(8,5))
plt.plot(data["Name"], data["Math"], marker="o", label="Math")
plt.plot(data["Name"], data["Science"], marker="o", label="Science")
plt.plot(data["Name"], data["English"], marker="o", label="English")
plt.title("Subject-wise Performance")
plt.xlabel("Student Name")
plt.ylabel("Marks")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Gender-Based Analysis
print("\n Average Marks by Gender:")
gender_avg = data.groupby("Gender")[["Math", "Science", "English", "Total"]].mean()
print(gender_avg)

# Pie Chart - Average Total Marks by Gender
plt.figure(figsize=(5,5))
plt.pie(
    gender_avg["Total"],
    labels=gender_avg.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=["pink", "lightblue"]
)
plt.title("Average Total Marks (Boys vs Girls)")
plt.tight_layout()
plt.show()

# Bar Chart - Subject Comparison by Gender
plt.figure(figsize=(7,5))
gender_avg[["Math", "Science", "English"]].plot(
    kind="bar",
    figsize=(7,5),
    color=["#f4a261", "#2a9d8f", "#e76f51"]
)
plt.title("Average Subject Marks by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Marks")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()