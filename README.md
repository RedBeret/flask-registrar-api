# Registrar API
This is a simplified API for a university regristrar. The database models are completed except for the validations, which you must finish. You also need to write the routes.

## Models

 - Student
    - `id`   Integer (primary key)
    - `fname` String (not null)
    - `lname` String (not null)
    - `grad_year` Integer (not null)
 - Enrollment
    - `id`        Integer (primary key)
    - `term`   String (not null)
    - `student_id` Integer (not null)
    - `course_id` Integer (not null)
 - Course
    - `id`   Integer (primary key)
    - `title` String (unique, not null)
    - `instructor` String
    - `credits` Integer (not null)
### Validation

  - Student
    - `grad_year` must be current year or later
  - Enrollment
    - `term` must start with 'S' or 'F' and end in an integer
  - Course
    - `title` must not be empty
## Routes

  - GET /students
  - GET /students/<int:id>
  - POST /enrollments
  - PATCH /courses/<int:id>
  - PATCH /students/<int:id>
  - DELETE /students/<int:id>
    

### Response Formats


- GET /students
    ```json
    [
        {
            id
            fname
            lname
            grad_year
        }
    ]
    ```
- GET /students/<int:id>
    ```json
    [
        {
            id
            fname
            lname
            grad_year
            enrollments [
                id
                term
                student_id
                course_id
                course {
                    id
                    title
                    instructor
                    credits
                }
            ]
        }
    ]
    ```
- POST /enrollments
    ```json
    [
        {
            id
            student_id
            course_id
            term
        }
    ]
    ```
- PATCH /courses/<int:id>
    ```json
    [
        {
            id
            title
            instructor
            credits
        }
    ]
    ```
- PATCH /students/<int:id>
    ```json
    [
        {
            id
            fname
            lname
            grad_year
        }
    ]
    ```
- DELETE /students/<int:id>
    ```json
    [
        {}
    ]
    ```
