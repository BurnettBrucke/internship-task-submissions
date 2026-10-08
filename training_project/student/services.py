


def update_course_marks_service(

    request,
    course,
    assigned_student,
    form,
):
    """
    Update a student's marks for a course.

    This business logic is kept outside the view so that the same
    operation can later be reused by an API, background task,
    or another interface without duplicating the database logic.
    """

    course_mark, created = CourseMark.objects.get_or_create(
        course=course,
        student=assigned_student,
    )

    old_marks = course_mark.marks
    new_marks = form.cleaned_data["marks"]
    reason = form.cleaned_data.get("reason", "")

    with transaction.atomic():

        course_mark.marks = new_marks
        course_mark.save()

        MarksHistory.objects.create(
            course_mark=course_mark,
            old_marks=old_marks,
            new_marks=new_marks,
            reason=reason,
            updated_by=request.user,
        )

        create_audit_log(
            request=request,
            action_type="UPDATE",
            description=(
                f"Updated marks for "
                f"{assigned_student.name} in "
                f"{course.course_name}: "
                f"{old_marks} -> {new_marks}. "
                f"Reason: {reason}"
            ),
            affected_object=course_mark,
        )

    return course_mark


def get_course_mark(course, assigned_student, user):
    """
    Get or create the CourseMark used by the marks form.

    Keeping this database lookup in the service layer allows
    future API endpoints to use the same CourseMark retrieval
    logic without duplicating it.
    """

    course_mark, created = CourseMark.objects.get_or_create(
        course=course,
        student=assigned_student,
        defaults={
            "marks": assigned_student.marks,
            "updated_by": user,
        },
    )

    return course_mark


