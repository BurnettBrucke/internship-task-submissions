from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# TEST 1 - HEALTH CHECK
# ============================================================

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "message": "Student API is running"
    }


# ============================================================
# TEST 2 - GET ALL STUDENTS
# ============================================================

def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


# ============================================================
# TEST 3 - GET STUDENT BY ID
# ============================================================

def test_get_student_by_id():
    response = client.get("/students/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert "name" in data
    assert "email" in data


# ============================================================
# TEST 4 - STUDENT NOT FOUND
# ============================================================

def test_student_not_found():
    response = client.get("/students/9999")

    assert response.status_code == 404

    assert response.json()["detail"] == "Student not found"


# ============================================================
# TEST 5 - CREATE STUDENT
# ============================================================

def test_create_student():
    student = {
        "name": "Test Student",
        "email": "teststudent@example.com",
        "age": 25,
        "marks": 85,
        "active": True
    }

    response = client.post("/students", json=student)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Student"
    assert data["email"] == "teststudent@example.com"
    assert data["age"] == 25
    assert data["marks"] == 85
    assert "id" in data


# ============================================================
# TEST 6 - INVALID EMAIL
# ============================================================

def test_invalid_email():
    student = {
        "name": "Invalid Email",
        "email": "invalid-email",
        "age": 25,
        "marks": 80,
        "active": True
    }

    response = client.post("/students", json=student)

    assert response.status_code == 422


# ============================================================
# TEST 7 - INVALID AGE
# ============================================================

def test_invalid_age():
    student = {
        "name": "Invalid Age",
        "email": "age@example.com",
        "age": 15,
        "marks": 80,
        "active": True
    }

    response = client.post("/students", json=student)

    assert response.status_code == 422


# ============================================================
# TEST 8 - INVALID MARKS
# ============================================================

def test_invalid_marks():
    student = {
        "name": "Invalid Marks",
        "email": "marks@example.com",
        "age": 25,
        "marks": 101,
        "active": True
    }

    response = client.post("/students", json=student)

    assert response.status_code == 422


# ============================================================
# TEST 9 - UPDATE STUDENT
# ============================================================

def test_update_student():
    response = client.patch(
        "/students/1",
        json={"marks": 95}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["marks"] == 95


# ============================================================
# TEST 10 - DELETE STUDENT
# ============================================================

def test_delete_student():
    # Create a student first
    student = {
        "name": "Delete Student",
        "email": "delete@example.com",
        "age": 25,
        "marks": 70,
        "active": True
    }

    create_response = client.post(
        "/students",
        json=student
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    # Delete student
    delete_response = client.delete(
        f"/students/{student_id}"
    )

    assert delete_response.status_code == 204

    # Verify student no longer exists
    get_response = client.get(
        f"/students/{student_id}"
    )

    assert get_response.status_code == 404

# ============================================================
# TEST 11: FILTER ACTIVE STUDENTS
# ============================================================

def test_filter_active_students():
    """
    Verify that the active=true filter
    returns only active students.
    """

    response = client.get("/students?active=true")

    # API should return successful response
    assert response.status_code == 200

    data = response.json()

    # At least one active student should be present
    assert len(data) >= 1

    # Every returned student must be active
    for student in data:
        assert student["active"] is True


# ============================================================
# TEST 12: FILTER INACTIVE STUDENTS
# ============================================================

def test_filter_inactive_students():
    """
    Verify that the active=false filter
    returns only inactive students.
    """

    response = client.get("/students?active=false")

    # API should return successful response
    assert response.status_code == 200

    data = response.json()

    # At least one inactive student should be present
    assert len(data) >= 1

    # Every returned student must be inactive
    for student in data:
        assert student["active"] is False


# ============================================================
# TEST 13: FILTER STUDENTS BY MINIMUM MARKS
# ============================================================

def test_filter_minimum_marks():
    """
    Verify that min_marks filter returns
    only students having marks >= given value.
    """

    response = client.get("/students?min_marks=80")

    # API should return successful response
    assert response.status_code == 200

    data = response.json()

    # Every returned student's marks
    # should be greater than or equal to 80
    for student in data:
        assert student["marks"] >= 80

# ============================================================
# TEST 14: PAGINATION USING SKIP AND LIMIT
# ============================================================

def test_students_pagination():
    """
    Verify that skip and limit parameters
    correctly control the number of students returned.
    """

    response = client.get("/students?skip=0&limit=2")

    # API should return successful response
    assert response.status_code == 200

    data = response.json()

    # Only 2 students should be returned
    assert len(data) == 2

    # Verify that the returned data is a list
    assert isinstance(data, list)

# ============================================================
# TEST 15: PAGINATION BOUNDARY CASE
# ============================================================

def test_students_pagination_boundary():
    """
    Verify that when skip value is greater than
    the available number of students, the API
    returns an empty list.
    """

    response = client.get("/students?skip=100&limit=10")

    # API should return successful response
    assert response.status_code == 200

    data = response.json()

    # No students should be available after skipping 100 records
    assert data == []

    # Response should be a list
    assert isinstance(data, list)

# ============================================================
# TEST 16: UPDATE NON-EXISTING STUDENT
# ============================================================

def test_update_student_not_found():
    """
    Verify that updating a student who does not exist
    returns a 404 Not Found response.
    """

    response = client.patch(
        "/students/9999",
        json={"marks": 90}
    )

    # Student does not exist, so API should return 404
    assert response.status_code == 404

    # Verify the error message
    assert response.json()["detail"] == "Student not found"

# ============================================================
# TEST 17: DELETE NON-EXISTING STUDENT
# ============================================================

def test_delete_student_not_found():
    """
    Verify that deleting a student who does not exist
    returns a 404 Not Found response.
    """

    response = client.delete("/students/9999")

    # Student does not exist, so API should return 404
    assert response.status_code == 404

    # Verify the error message
    assert response.json()["detail"] == "Student not found"

# ============================================================
# TEST 18: COMBINED FILTERS
# ============================================================

def test_combined_filters():
    """
    Verify that active and min_marks filters
    work correctly when used together.
    """

    response = client.get(
        "/students?active=true&min_marks=80"
    )

    # API should return successful response
    assert response.status_code == 200

    data = response.json()

    # Every returned student must be active
    # and have marks >= 80
    for student in data:
        assert student["active"] is True
        assert student["marks"] >= 80

# ============================================================
# TEST 19: INVALID SKIP VALUE
# ============================================================

def test_invalid_skip():
    """
    Verify that a negative skip value
    is rejected by the API.
    """

    response = client.get("/students?skip=-1")

    # Negative skip should fail validation
    assert response.status_code == 422

# ============================================================
# TEST 20: INVALID LIMIT VALUE
# ============================================================

def test_invalid_limit():
    """
    Verify that a zero limit value
    is rejected by the API.
    """

    response = client.get("/students?limit=0")

    # Limit must be at least 1
    assert response.status_code == 422

