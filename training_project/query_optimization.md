# Query Optimization Review

## 1. Purpose

This document records the query and performance review performed for the Student Training Portal.

The goal was to identify unnecessary database queries and reduce N+1 query patterns in important dashboard and list pages.

---

## 2. Before Optimization — Student List

The student list originally used:

```python
students = Student.objects.all()