# Create a marks dictionary and find the highest scorer, lowest scorer and average

marks = {
    "Riya": 85,    
    "Priya": 90,
    "pihu": 99,
    "mahi": 96
}

if not marks:
    print("Marks dictionary is empty.")
    exit()

highest_scorer = max(marks, key=marks.get)
lowest_scorer = min(marks, key=marks.get)
average = sum(marks.values()) / len(marks)

print(f"Highest scorer: {highest_scorer} with {marks[highest_scorer]} marks")
print(f"Lowest scorer: {lowest_scorer} with {marks[lowest_scorer]} marks")
print(f"Average marks: {average}")