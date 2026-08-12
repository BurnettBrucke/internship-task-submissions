# Student Training Portal

## About Project

Student Training Portal ek Django based web application hai.

Is project ka use students, trainers aur admin ko manage karne ke liye kiya gaya hai.

## Technologies Used

- Python
- Django
- SQLite
- HTML
- Bootstrap
- Django Templates

## Main Features

### 1. Login and Logout

Users apne username aur password se login kar sakte hain.

Different users ke different roles hain:

- Admin
- Trainer
- Student

### 2. Student Management

Admin aur Trainer students ko:

- View
- Add
- Edit
- Delete

kar sakte hain.

### 3. Student Details

Student ke basic details store kiye jaate hain:

- Name
- Email
- Age
- Course
- Marks
- Joined Date
- Active Status

### 4. Search and Filter

Students ko search aur filter kar sakte hain.

Search ke through:

- Name
- Email
- Course

se student find kar sakte hain.

Different filters bhi available hain.

### 5. Pagination

Agar students bahut zyada hain, to unhe multiple pages mein display kiya jaata hai.

### 6. Feedback

Trainer students ko feedback de sakta hai.

Students feedback dekh sakte hain.

### 7. Marks

Student ke marks update kiye ja sakte hain.

Marks History ke through previous marks records dekhe ja sakte hain.

### 8. Audit Logs

Important user activities ko audit logs mein record kiya jaata hai.

### 9. Role Based Access

Har user ko uske role ke according access milta hai.

Admin:

- Students manage kar sakta hai
- Audit Logs dekh sakta hai

Trainer:

- Students dekh sakta hai
- Feedback manage kar sakta hai
- Marks update kar sakta hai

Student:

- Apna dashboard dekh sakta hai
- Allowed information access kar sakta hai

### 10. Security

Project mein:

- Login authentication
- Role based access
- Ownership restriction
- CSRF protection
- Custom 403 page
- Custom 404 page
- Custom 500 page

use kiya gaya hai.

## Form Validation

Forms mein invalid data enter karne par clear error messages show hote hain.

Example:

- Empty required field
- Invalid age
- Invalid marks

## Demo Data

Project mein demo data create karne ke liye management command available hai.

Command:

```bash
python manage.py seed_demo_data