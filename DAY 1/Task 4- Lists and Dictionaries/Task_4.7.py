# Create a marks dictionary and find the highest scorer, lowest scorer and average.
marks = {
    "Python" : 78,
    "Java" : 67,
    "SQL" : 88,
    "ML" : 56,
    "React" : 77
}

for sub,mark in marks.items():
    print(f"{sub} : {mark}")

highest_score = max(marks.values())
print("Highest Score : ",highest_score)

lowest_score = min(marks.values())
print("Lowest Score : ",lowest_score)

average = sum(marks.values())/len(marks.values())
print("Average of marks : ",average)