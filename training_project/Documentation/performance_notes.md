# Performance Optimization Notes

## 1. Problem Identified

The Trainer Dashboard was loading students and then querying each student's marks history separately.

This caused an N+1 query problem.

---

## 2. Before Optimization

The dashboard used:

for student in students:
    student.latest_marks_update = student.marks_history.select_related(
        'trainer'
    ).order_by('-updated_at').first()

This resulted in:

Total Queries: 16

The main problem was that a separate query was executed for marks history for each student.

### 3. Optimization Applied

Used Django Prefetch with select_related:

students = Student.objects.filter(
    courses__in=courses
).distinct().prefetch_related(
    Prefetch(
        'marks_history',
        queryset=MarksUpdateHistory.objects.select_related(
            'trainer'
        ).order_by('-updated_at'),
        to_attr='all_marks_history'
    )
)

Then the already-fetched data is reused:

for student in students:
    student.latest_marks_update = (
        student.all_marks_history[0]
        if student.all_marks_history
        else None
    )

### 4. After Optimization

After using Prefetch:

Total Queries: 2

Result
Measurement	Before	After
Database Queries	16	2
Queries Reduced	-	14
Reduction	-	87.5%

The N+1 query problem was reduced by fetching related marks history in advance.

### 5. Other Query Optimizations

The project also uses:

select_related() for ForeignKey/OneToOne relationships.
prefetch_related() for ManyToMany/reverse relationships.
count() for database-level counting.
exists() for permission/existence checks.
values_list() where only IDs are required.
distinct() where ManyToMany joins can create duplicate results.

These optimizations help reduce unnecessary database queries and improve application performance.