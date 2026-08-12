# PYTHON AND DJANGO TRAINING - DAY 3 Intern Task Workbook Answers
**Topic:** Django CRUD, Relationships, ORM, Authentication, and Templates  
**Page:** 7  

---

### 1. What is CRUD?
**CRUD** stands for **Create, Read, Update, and Delete**. These are the four basic operations of persistent storage in web development and databases:
* **Create:** Adding new records to the database (HTTP POST / Django `Model.objects.create()`).
* **Read:** Retrieving or viewing existing records (HTTP GET / Django `Model.objects.all()`, `.get()`, `.filter()`).
* **Update:** Modifying existing records (HTTP PUT/PATCH / Django updating object attributes and calling `.save()` or `.update()`).
* **Delete:** Removing records from the database (HTTP DELETE / Django `instance.delete()`).

---

### 2. What is `get_object_or_404()`?
`get_object_or_404()` is a shortcut function in `django.shortcuts`.  
* **Purpose:** It calls `get()` on a given model manager or QuerySet. If the requested object exists, it returns the object. If the object does not exist (raises `DoesNotExist`), it catches the exception and immediately raises Django's `Http404` exception instead of allowing a 500 Server Error.
* **Example:**
  ```python
  from django.shortcuts import get_object_or_404
  from .models import Student

  def student_detail(request, pk):
      student = get_object_or_404(Student, pk=pk)
      return render(request, 'student_detail.html', {'student': student})
  ```

---

### 3. Why should we redirect after a successful POST request?
Redirecting after a successful POST request implements the **Post/Redirect/Get (PRG)** design pattern.
* **Prevents Duplicate Submissions:** If a user refreshes the page after submitting a POST request, the browser would re-submit the POST data, resulting in duplicate database inserts, duplicate payments, or repeated actions.
* **Safe Navigation & Bookmarking:** A redirect converts the browser's current state to an HTTP GET request (e.g., redirecting to a success page or detail page), which can safely be refreshed, back-navigated, or bookmarked.

---

### 4. What is a ModelForm?
A **ModelForm** (`django.forms.ModelForm`) is a helper class in Django that automatically creates an HTML form bound directly to a Django ORM `Model`.
* **Key Advantages:**
  * Automatically maps model field types to corresponding form fields and HTML widgets.
  * Inherits model validation rules (e.g., `max_length`, `unique`, `blank`, `null`).
  * Includes a built-in `.save()` method to create or update model instances in the database directly from validated form data.

---

### 5. What is a ForeignKey?
A `ForeignKey` (`models.ForeignKey`) defines a **Many-to-One** relationship between Django models.
* **Explanation:** Multiple records in the defining model (child) can link to a single record in the referenced model (parent).
* **Database Level:** Django creates a foreign key database column on the child table appending `_id` (e.g., `course_id`) containing the primary key value of the parent record.

---

### 6. What is a one-to-one relationship?
A one-to-one relationship is created using `models.OneToOneField`.
* **Explanation:** Each record in Model A corresponds to exactly one record in Model B, and vice-versa.
* **Common Use Cases:** Extending the default Django `User` model with a `UserProfile` model.
* **Database Level:** Similar to a `ForeignKey`, but with a `UNIQUE` database constraint enforced on the column to ensure only one relationship per record exists.

---

### 7. What is a many-to-many relationship?
A many-to-many relationship is created using `models.ManyToManyField`.
* **Explanation:** Multiple records in Model A can be related to multiple records in Model B (e.g., a `Student` can enroll in multiple `Course`s, and a `Course` can have multiple `Student`s).
* **Database Level:** Relational databases cannot directly store arrays of keys, so Django automatically creates an intermediate junction/join table behind the scenes containing pair mappings of foreign keys from both tables.

---

### 8. What is the purpose of `related_name`?
`related_name` is an optional parameter on relational fields (`ForeignKey`, `OneToOneField`, `ManyToManyField`).
* **Purpose:** It specifies the attribute name used for the **reverse relationship** from the target/parent model back to the defining model.
* **Example:**
  ```python
  class Student(models.Model):
      course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
  ```
  With `related_name='students'`, you can retrieve all students for a course instance using `course.students.all()`, rather than using the default fallback syntax `course.student_set.all()`.

---

### 9. What does `on_delete` do?
`on_delete` is a mandatory argument for `ForeignKey` and `OneToOneField` attributes in Django models.
* **Purpose:** It instructs Django and the database engine on what action to take regarding child records when the referenced parent object is deleted.

---

### 10. What is the difference between CASCADE and PROTECT?
* **`models.CASCADE`:** Cascade deletion. When the referenced parent object is deleted, all child objects linked to it are automatically deleted as well.
* **`models.PROTECT`:** Protection from deletion. If any child objects reference the parent, Django raises a `ProtectedError` and prevents the parent object from being deleted until the child references are removed or reassigned.

---

### 11. What is a QuerySet?
A **QuerySet** is a collection of database queries representing objects retrieved from the database via Django's ORM model managers (e.g., `Student.objects.all()`).
* QuerySets allow filtering, slicing, ordering, and chaining methods before producing an executed database SQL statement.

---

### 12. Why are Django QuerySets lazy?
Django QuerySets are **lazy** because creating or chaining a QuerySet does not immediately invoke a database hit or execute SQL.
* **Why:**
  1. **Performance Optimization:** Allows chaining multiple operations (such as `.filter()`, `.exclude()`, `.order_by()`) into a single combined SQL query rather than hitting the database multiple times.
  2. **Efficiency:** SQL is only executed when the QuerySet is explicitly **evaluated** (e.g., iterating over it in a `for` loop, calling `list()`, checking boolean truth `if queryset:`, or slicing with a step).

---

### 13. What is the difference between `get()` and `filter()`?

| Feature | `filter(**kwargs)` | `get(**kwargs)` |
| :--- | :--- | :--- |
| **Return Type** | Returns a **QuerySet** (list-like object). | Returns a **single model instance**. |
| **Matching Count** | Works for 0, 1, or multiple matching records. | Expects **exactly 1** matching record. |
| **0 Matches** | Returns an empty QuerySet (`<QuerySet []>`). | Raises `DoesNotExist` exception. |
| **>1 Matches** | Returns QuerySet with all matching records. | Raises `MultipleObjectsReturned` exception. |
| **Evaluation** | Lazy (evaluated when used). | Immediate (hits database right away). |

---

### 14. What is the purpose of Q objects?
`django.db.models.Q` objects are used to construct complex database queries involving logical operators (**OR `|`**, **AND `&`**, and **NOT `~`**).
* Standard `filter(key1=val1, key2=val2)` only supports `AND` logic.
* **Example using `Q`:**
  ```python
  from django.db.models import Q
  # Search for students whose first name starts with 'A' OR whose age is >= 20
  students = Student.objects.filter(Q(first_name__startswith='A') | Q(age__gte=20))
  ```

---

### 15. What is aggregation?
**Aggregation** (`.aggregate()`) calculates a single summary statistic over an **entire QuerySet**.
* **Return Type:** Returns a standard Python **dictionary** of key-value pairs containing summary totals (using functions like `Avg`, `Count`, `Max`, `Min`, `Sum`).
* **Example:**
  ```python
  from django.db.models import Avg
  Student.objects.aggregate(average_age=Avg('age'))
  # Output: {'average_age': 21.5}
  ```

---

### 16. What is annotation?
**Annotation** (`.annotate()`) calculates summary statistics for **each individual object** in a QuerySet (similar to SQL `GROUP BY`).
* **Return Type:** Returns a **QuerySet** where each object has a new dynamic attribute appended to it.
* **Example:**
  ```python
  from django.db.models import Count
  courses = Course.objects.annotate(total_students=Count('students'))
  for course in courses:
      print(course.name, course.total_students)
  ```

---

### 17. What is the difference between `select_related()` and `prefetch_related()`?
Both functions are performance optimizations designed to solve the **N+1 query problem**.

* **`select_related()`:**
  * Works via a **SQL JOIN** (INNER / LEFT OUTER JOIN) in a **single database query**.
  * Used for single-valued relationships: **`ForeignKey`** and **`OneToOneField`**.
* **`prefetch_related()`:**
  * Executes **separate SQL queries** for each table and joins the results together using Python.
  * Used for multi-valued relationships: **`ManyToManyField`** and **reverse `ForeignKey`** (One-to-Many).

---

### 18. What is user authentication?
**User authentication** is the process of verifying the **identity** of a user attempting to access a system (answering "Who are you?").
* It verifies provided credentials (such as username/password, authentication tokens, or OTPs) against stored user credentials.

---

### 19. What is the difference between authentication and authorization?
* **Authentication:** Verifying **who** the user is (Identity Verification).  
  * *Example:* Logging into a web application with a valid username and password.
* **Authorization:** Determining **what actions** an authenticated user is permitted to perform (Permissions & Access Control).  
  * *Example:* Checking if a logged-in student has permission to delete a course or access the admin dashboard.

---

### 20. What does `login_required` do?
`login_required` is a view decorator (`django.contrib.auth.decorators.login_required`).
* **Functionality:** It restricts access to a view function so that only authenticated (logged-in) users can view it.
* **Behavior:** If an unauthenticated user attempts to visit the protected URL, `login_required` intercepts the request and redirects the user to the login URL (defined by `LOGIN_URL` in `settings.py`) with a `next` query string parameter pointing back to the requested page.

---

### 21. What is the purpose of Django messages?
The Django **messages framework** (`django.contrib.messages`) allows views to create lightweight, one-time notifications ("flash messages") during an HTTP request and display them to the user in the subsequent rendered HTTP response (most commonly after form handling and POST-redirects).
* **Built-in Message Levels:** `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`.

---

### 22. What is template inheritance?
**Template inheritance** is a core Django template feature that allows developers to define a base layout ("skeleton") template and mark specific areas with `{% block block_name %}` tags. Child templates can extend the base template using `{% extends "base.html" %}` and override only the specified block sections without rewriting the entire page structure.

---

### 23. What is the purpose of a base template?
A **base template** (typically `base.html`) acts as the parent master layout for an application.
* **Purpose:**
  1. Promotes the **DRY (Don't Repeat Yourself)** principle by placing common boilerplate HTML structure (head tags, meta tags, CSS/JS includes, navbar header, footer) in one central place.
  2. Ensures visual consistency across all pages.
  3. Allows global UI layout changes to be made in a single file across the entire web application.

---

### 24. What is reverse URL resolution?
**Reverse URL resolution** is the mechanism of generating URL paths dynamically from their logical name defined in `urls.py`, rather than hard-coding absolute URL paths.
* **In Python Code:** `reverse('student-detail', kwargs={'pk': 1})` or `redirect('student-detail', pk=1)`
* **In Django Templates:** `{% url 'student-detail' student.id %}`

---

### 25. Why should URLs not be hard-coded in templates?
URLs should never be hard-coded (e.g., `<a href="/students/detail/5/">`) in templates because:
1. **Maintainability:** If a URL structure changes in `urls.py` (e.g., changing `/students/detail/5/` to `/academic/students/view/5/`), every hard-coded URL reference across all templates would break and require manual updating.
2. **DRY & Decoupling:** Using dynamic reverse lookup (`{% url 'student-detail' student.id %}`) decouples template hyperlinking from URL routing. Changing the URL path pattern in `urls.py` automatically updates every link across the entire application instantly without touching HTML templates.
