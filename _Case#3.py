from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
from typing import Dict, List, Union


# Abstract Base Class for Person
class Person(ABC):
    def __init__(self, name: str, email: str, contact_number: str, address: str):
        self.__name = name
        self.__email = email
        self._contact_number = contact_number
        self._address = address

    @property
    def name(self) -> str:
        """Get or set the person's name."""
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self.__name = value

    @property
    def email(self) -> str:
        """Get or set the person's email."""
        return self.__email

    @email.setter  # Corrected to email.setter
    def email(self, value: str):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address.")
        self.__email = value

    @property
    def contact_number(self) -> str:
        """Get or set the person's contact number."""
        return self._contact_number

    @contact_number.setter
    def contact_number(self, value: str):
        if not value.isdigit() or len(value) < 10:
            raise ValueError("Contact number must be at least 10 digits.")
        self._contact_number = value

    @property
    def address(self) -> str:
        """Get or set the person's address."""
        return self._address

    @address.setter
    def address(self, value: str):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        self._address = value

    @abstractmethod
    def display_info(self) -> str:
        """Abstract method to display information about the person."""
        pass


class Student(Person):
    def __init__(self, name, email, contact_number, address, student_id, year_level, program, gpa=0.0, birth_date=None,
                 enrolled_courses=None, role="Student"):
        super().__init__(name, email, contact_number, address)
        self.__student_id = student_id
        self.__year_level = year_level
        self.__program = program
        self.__gpa = gpa
        self.__birth_date = birth_date
        self.role = role
        self.__enrolled_courses = enrolled_courses if enrolled_courses is not None else []
        self.course = []
        self.grades = []

    def to_dict(self):
        """Convert the Student object to a dictionary."""
        return {
            'name': self.name,
            'email': self.email,
            'contact_number': self.contact_number,  # Use the getter method
            'address': self.address,  # Use the getter method
            'student_id': self.student_id,
            'year_level': self.year_level,
            'program': self.program,
            'gpa': self.gpa,
            'birth_date': self.birthdate,  # Use the getter method
            'enrolled_courses': [course.to_dict() for course in self.enrolled_courses]
            # Assumes Course has a to_dict method
        }

    @classmethod
    def from_dict(cls, data, all_courses):
        """
        Create a Student object from a dictionary.
        :param data: A dictionary containing student details.
        :param all_courses: A list of Course objects to map enrolled courses.
        :return: A Student object.
        """
        student = cls(
            data['name'],
            data['email'],
            data['contact_number'],
            data['address'],
            data['student_id'],
            data['year_level'],
            data['program'],
            gpa=data.get('gpa', 0.0),
            birth_date=data.get('birth_date')
        )
        # Map enrolled_courses to actual Course objects
        for course_data in data.get('enrolled_courses', []):
            course = next((c for c in all_courses if c.course_code == course_data['course_code']), None)
            if course:
                student.enroll(course)

        return student

    @property
    def student_id(self):
        return self.__student_id

    @property
    def year_level(self):
        return self.__year_level

    @property
    def program(self):
        return self.__program

    @property
    def birthdate(self):
        return self.__birth_date

    @birthdate.setter
    def birthdate(self, value):
        self.__birth_date = value

    @property
    def enrolled_courses(self):
        return self.__enrolled_courses

    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        if 0 <= value <= 4.0:
            self.__gpa = value
        else:
            raise ValueError("GPA must be between 0 and 4.0")

    def add_grade(self, course, grade):
        """Add a grade for a specific course."""
        self.grades.append({
            'course_name': course.course_name,
            'course_code': course.course_code,
            'grade': grade
        })

    def enroll(self, course):
        """
        Enroll the student in a course.
        :param course: A Course object to enroll in.
        """
        if course not in self.__enrolled_courses:  # Avoid duplicates
            self.__enrolled_courses.append(course)

    def display_info(self):
        """
        Display basic student information.
        :return: A formatted string with student details.
        """
        return (
            f"ID: {self.student_id}\n"
            f"Student: {self.name}\n"
            f"Year Level: {self.year_level}\n"
            f"Program: {self.program}\n"
            f"Email: {self.email}\n"
            f"Contact#: {self.contact_number}\n"
            f"Address: {self.address}"
        )


# Ensure Instructor class is properly defined, inherits from Person class
class Instructor(Person):
    def __init__(self, name: str, email: str, contact_number: str, address: str, instructor_id: str, role="Instructor"):
        # Initialize the Person class
        super().__init__(name, email, contact_number, address)
        self.__instructor_id = instructor_id  # Private attribute for instructor ID
        self.role = role  # Role of the instructor
        self._courses_taught = []  # List to store courses taught by the instructor
        self._assignments = []  # List to store assignments assigned by the instructor
        self.course = []

    @property
    def instructor_id(self) -> str:
        return self.__instructor_id

    @property
    def courses_taught(self) -> list:
        return self._courses_taught

    @property
    def assignments(self) -> list:
        return self._assignments

    def to_dict(self) -> dict:
        """Convert instructor details to a dictionary."""
        return {
            'instructor_id': self.instructor_id,
            'name': self.name,
            'email': self.email,
            'contact_number': self.contact_number,  # Using getter
            'address': self.address,  # Using getter
            'role': self.role,
            'courses_taught': [course.course_code for course in self._courses_taught],
            # Course codes for taught courses
        }

    def teach_course(self, course) -> None:
        """Add a course to the list of courses taught by the instructor."""
        if course not in self._courses_taught:  # Avoid duplicates
            self._courses_taught.append(course)
            print(f"Course '{course.course_name}' added to instructor '{self.name}'.")
        else:
            print(f"Instructor '{self.name}' is already teaching the course '{course.course_name}'.")

    def assign_assignment(self, assignment) -> None:
        """Assign an assignment to a course taught by the instructor."""
        if assignment.course not in self._courses_taught:
            print(f"Cannot assign '{assignment.title}' to instructor '{self.name}': course not taught by instructor.")
        else:
            if assignment not in self._assignments:  # Avoid duplicates
                self._assignments.append(assignment)
                print(f"Assignment '{assignment.title}' assigned to instructor '{self.name}'.")
            else:
                print(f"Assignment '{assignment.title}' is already assigned.")

    def display_info(self) -> str:
        """Display detailed information about the instructor."""
        courses = ', '.join(
            course.course_name for course in self._courses_taught) if self._courses_taught else "No courses taught"
        return (f"ID: {self.instructor_id} \nInstructor: {self.name} \nRole: {self.role} "
                f"\nEmail: {self.email} \nContact#: {self.contact_number} \nAddress: {self.address} "
                f"\nCourses Taught: {courses}")


class Course:

    def __init__(self, course_name: str, course_code: str, instructor: 'Instructor', units: int):
        self.__course_name = course_name
        self.__course_code = course_code
        self.__instructor = instructor
        self._students: List['Student'] = []  # List to hold students
        self._units = units
        self.assignments: List['Assignment'] = []  # Initialize assignments list
        self.grades = {}  # Store grades in a dictionary
        self.enrolled_students = []
        self.discussion_threads = []  # List to store discussion threads for the course

    def add_student(self, student: 'Student') -> None:
        """Adds a student to the course."""
        if student not in self._students:
            self._students.append(student)
            print(f"Student {student.name} has been added to the course {self.course_name}.")
        else:
            print(f"Student {student.name} is already enrolled in {self.course_name}.")

    def add_grade(self, grade: 'Grade') -> None:
        """Add a grade for the course."""
        key = (grade.student.student_id, grade.assignment.title)
        if key in self.grades:
            print(f"Grade for student {grade.student.name} on assignment {grade.assignment.title} already exists.")
            return
        self.grades[key] = grade
        print(f"Grade for {self.course_name} added: {grade}")

    def to_dict(self) -> dict:
        """Convert course details to a dictionary."""
        return {
            'course_name': self.course_name,
            'course_code': self.course_code,
            'instructor_id': self.instructor.instructor_id,
            'units': self._units
        }

    def assign_assignment(self, title: str, description: str, due_date: str) -> None:
        """Create and assign a new assignment to the course."""
        try:
            due_datetime = datetime.fromisoformat(due_date)
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DDTHH:MM:SS.")
            return

        if due_datetime <= datetime.now():
            print("Error: The due date must be in the future.")
            return

        if any(a.title == title and a.due_date == due_datetime for a in self.assignments):
            print(f"An assignment with title '{title}' and due date '{due_date}' already exists.")
            return

        new_assignment = Assignment(title, description, due_datetime, self)  # Pass self as course
        self.assignments.append(new_assignment)
        print(f"Assignment '{title}' added to course '{self.course_name}'.")

    def input_grades(self) -> None:
        """Input grades for a specific assignment."""
        assignment_title = input("Enter the assignment title: ")
        assignment = next((a for a in self.assignments if a.title == assignment_title), None)

        if assignment:
            student_id = input("Enter the student's ID: ")
            student = next((s for s in self._students if s.student_id == student_id), None)

            if student:
                self._handle_grade_input(student, assignment)
            else:
                print("Student not found. Please check the ID and try again.")
        else:
            print("Assignment not found. Please check the title and try again.")

    def _handle_grade_input(self, student: Student, assignment: 'Assignment') -> None:
        """Helper method to handle grade input for a specific student."""
        try:
            score = float(input("Enter the grade: "))
            feedback = input("Enter feedback: ")
            grade = Grade(student, assignment, score, feedback)  # Create a Grade instance
            assignment.add_grade(score)  # Assuming add_grade accepts score
            self.add_grade(grade)  # Store the grade in the course
            print(f"Grade for student '{student.name}' added to assignment '{assignment.title}'.")
        except ValueError:
            print("Invalid score. Please enter a numeric value.")

    @property
    def course_name(self) -> str:
        return self.__course_name

    @property
    def course_code(self) -> str:
        return self.__course_code

    @property
    def instructor(self) -> 'Instructor':
        return self.__instructor

    def display_info(self) -> str:
        """Display course information."""
        return (f"Course: {self.course_name} \n"
                f"Code: {self.course_code} \n"
                f"Units: {self._units} \n"
                f"Instructor: {self.instructor.name}")

    def display_grades(self) -> None:
        """Display grades for all assignments in the course."""
        for (student_id, assignment_title), grade in self.grades.items():
            print(f"Student ID: {student_id}, Assignment: {assignment_title}, Grade: {grade.score}")

    def remove_student(self, student):
        pass


class Enrollment:
    def __init__(self):
        self._enrollments: List[Dict[str, Union[Student, Course]]] = []  # List to track enrollments

    def enroll_student(self, student: Student, course: Course) -> None:
        """
        Enroll a student in a course if they are not already enrolled.
        """
        if not self.is_student_enrolled(student, course):
            course.add_student(student)  # Assuming the 'Course' class has a method to add students
            self._enrollments.append({'student': student, 'course': course})
            print(f"{student.name} has been enrolled in {course.course_name}.")
        else:
            print(f"{student.name} is already enrolled in {course.course_name}.")

    def is_student_enrolled(self, student: Student, course: Course) -> bool:
        """
        Check if a student is already enrolled in a specific course.
        """
        return any(
            enrollment['student'] == student and enrollment['course'] == course for enrollment in self._enrollments)

    def unenroll_student(self, student: Student, course: Course) -> None:
        """
        Unenroll a student from a course if they are enrolled.
        """
        for enrollment in self._enrollments:
            if enrollment['student'] == student and enrollment['course'] == course:
                course.remove_student(student)  # Assuming the 'Course' class has a method to remove students
                self._enrollments.remove(enrollment)
                print(f"{student.name} has been unenrolled from {course.course_name}.")
                return
        print(f"{student.name} is not enrolled in {course.course_name}.")

    def get_enrollment_list(self) -> List[str]:
        """
        Return a list of all enrollments in a readable format.
        """
        if not self._enrollments:
            return ["No enrollments found."]
        return [
            f"{enrollment['student'].name} enrolled in {enrollment['course'].course_name}"
            for enrollment in self._enrollments
        ]

    def display_enrollments(self) -> None:
        """
        Display all enrollments in a user-friendly format.
        """
        enrollments = self.get_enrollment_list()
        print("Current Enrollments:")
        for enrollment in enrollments:
            print(f"- {enrollment}")

    def get_courses_by_student(self, student: Student) -> List[Course]:
        """
        Get a list of courses a specific student is enrolled in.
        """
        return [enrollment['course'] for enrollment in self._enrollments if enrollment['student'] == student]

    def get_students_by_course(self, course: Course) -> List[Student]:
        """
        Get a list of students enrolled in a specific course.
        """
        return [enrollment['student'] for enrollment in self._enrollments if enrollment['course'] == course]


class Grade:
    def __init__(self, student: 'Student', assignment: 'Assignment', score: float, feedback: str = None):
        self.__student = student  # The student associated with the grade
        self.__assignment = assignment  # The assignment associated with the grade
        self.__score = score  # The score for the assignment
        self.__feedback = feedback  # Optional feedback from the instructor
        self.validate_score()  # Ensure score is valid upon initialization

    @property
    def student(self) -> 'Student':
        return self.__student

    @property
    def assignment(self) -> 'Assignment':
        return self.__assignment

    @property
    def score(self) -> float:
        return self.__score

    @score.setter
    def score(self, value: float) -> None:
        """Update and validate the score."""
        self.__score = value
        self.validate_score()

    @property
    def feedback(self) -> str:
        return self.__feedback

    @feedback.setter
    def feedback(self, value: str) -> None:
        """Update the feedback."""
        self.__feedback = value

    def validate_score(self) -> None:
        """Validate that the score is between 0 and 100."""
        if not (0 <= self.__score <= 100):
            raise ValueError("Score must be between 0 and 100.")

    def display_grade_info(self) -> str:
        """Return a formatted string displaying the grade information."""
        feedback_display = self.feedback if self.feedback else 'No feedback'
        return (f"Student: {self.student.name} \n"
                f"Assignment: {self.assignment.title} \n"
                f"Score: {self.score:.2f} \n"
                f"Feedback: {feedback_display}")

    def to_dict(self) -> dict:
        """Convert the grade to a dictionary for serialization."""
        return {
            'student_id': self.student.student_id,
            'assignment_title': self.assignment.title,
            'score': self.score,
            'feedback': self.feedback
        }

    @classmethod
    def from_dict(cls, data: dict, students: list[Student], assignments: list[assignment]) -> 'Grade':
        """Create a Grade object from a dictionary."""
        student = next((s for s in students if s.student_id == data['student_id']), None)
        assignment = next((a for a in assignments if a.title == data['assignment_title']), None)

        if not student:
            raise ValueError(f"Student with ID {data['student_id']} not found.")
        if not assignment:
            raise ValueError(f"Assignment titled '{data['assignment_title']}' not found.")

        return cls(student, assignment, data['score'], data.get('feedback'))


class Schedule:
    def __init__(self, course: Course, day: str, time: str):
        """
        Initialize a schedule entry.
        :param course: A Course object associated with the schedule.
        :param day: The day of the week (e.g., "Monday").
        :param time: The time of the class (e.g., "09:00 AM - 11:00 AM").
        """
        self.__course = course
        self.__day = day
        self.__time = time

    @property
    def course(self) -> Course:
        """Return the associated course."""
        return self.__course

    @property
    def day(self) -> str:
        """Return the day of the schedule."""
        return self.__day

    @property
    def time(self) -> str:
        """Return the time of the schedule."""
        return self.__time

    def to_dict(self) -> dict:
        """
        Convert the schedule to a dictionary format.
        :return: A dictionary representing the schedule.
        """
        return {
            "course": self.course.course_code,  # Assuming Course has a unique course_code
            "day": self.day,
            "time": self.time,
        }

    @classmethod
    def from_dict(cls, data: dict, all_courses: list[Course]):
        """
        Create a Schedule object from a dictionary.
        :param data: A dictionary containing schedule details.
        :param all_courses: A list of available Course objects to match the course_code.
        :return: A Schedule object.
        """
        # Look up the course based on the course_code from the list of all courses
        course = next((c for c in all_courses if c.course_code == data["course"]), None)
        if not course:
            raise ValueError(f"Course with code {data['course']} not found.")
        # Return the newly created Schedule object
        return cls(course, data["day"], data["time"])

    def display_schedule(self) -> str:
        """
        Display the schedule details in a formatted string.
        :return: A string with course name, day, and time.
        """
        return f"Course: {self.course.course_name} (Code: {self.course.course_code}), Day: {self.day}, Time: {self.time}"

    def __repr__(self) -> str:
        """
        Provide a string representation for the Schedule object.
        :return: A formatted string representing the schedule.
        """
        return f"<Schedule(course={self.course.course_name}, day={self.day}, time={self.time})>"


class Assignment:
    def __init__(self, title: str, description: str, due_date: datetime, course):
        self.__title = title
        self.__description = description
        self.__due_date = due_date  # Expecting a datetime object
        self.__course = course  # The course to which this assignment belongs
        self.grades = []  # Initialize grades list

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def due_date(self) -> datetime:
        return self.__due_date

    @property
    def course(self):
        return self.__course

    def is_overdue(self) -> bool:
        """Check if the assignment is overdue."""
        return datetime.now() > self.__due_date

    def display_info(self) -> str:
        """Display information about the assignment."""
        course_name = self.course.course_name if hasattr(self.course, 'course_name') else "Unknown Course"
        return (f"Assignment: {self.title} \n"
                f"Description: {self.description} \n"
                f"Due Date: {self.due_date.strftime('%Y-%m-%d %H:%M:%S')} \n"
                f"Course: {course_name}")

    def add_grade(self, grade: float, feedback: str = '', student_id: str = '') -> None:
        """Add a grade to the assignment, along with optional feedback."""
        if not (0 <= grade <= 100):
            print("Error: Grade must be between 0 and 100.")
            return
        if any(g['student_id'] == student_id for g in self.grades):
            print(f"Grade for student {student_id} already exists for this assignment.")
            return
        self.grades.append({'score': grade, 'student_id': student_id, 'feedback': feedback})
        print(f"Grade of {grade} added for student {student_id} to '{self.title}'.")

    def average_grade(self) -> float:
        """Calculate and return the average grade for the assignment."""
        valid_grades = [grade['score'] for grade in self.grades if
                        grade['score'] >= 0]  # Example of excluding invalid grades
        if not valid_grades:
            return 0.0
        return sum(valid_grades) / len(valid_grades)

    def grade_count(self) -> int:
        """Return the number of grades entered for this assignment."""
        return len(self.grades)

    def display_grades(self):
        """Display all grades for this assignment."""
        if not self.grades:
            print("No grades entered yet.")
        for idx, grade in enumerate(self.grades, start=1):
            print(
                f"Grade {idx}: {grade['score']} - Feedback: {grade['feedback']} - Student: {grade.get('student_id', 'Unknown')}")


class Announcement:
    def __init__(self, title, content, date, recipient_groups):
        self.title = title
        self.content = content
        self.date = date
        self.recipient_groups = recipient_groups

    def __str__(self):
        return f"{self.date}: {self.title} - {self.content} (Recipients: {', '.join(self.recipient_groups)})"

    def add_recipient_group(self, group: str) -> None:
        """Adds a new recipient group to the announcement with validation."""
        if not group.isalnum():  # Example: Check if group name is alphanumeric
            print(f"Error: Group name '{group}' is not valid. Please use alphanumeric characters only.")
            return
        if group not in self.recipient_groups:
            self.recipient_groups.append(group)
            print(f"Group '{group}' added to recipients.")
        else:
            print(f"Group '{group}' is already a recipient.")

    def remove_recipient_group(self, group: str) -> None:
        """Removes a recipient group from the announcement."""
        if group in self.recipient_groups:
            self.recipient_groups.remove(group)
            print(f"Group '{group}' removed from recipients.")
        else:
            print(f"Group '{group}' not found in recipients.")

    def add_recipient_groups(self, groups: List[str]) -> None:
        """Adds multiple recipient groups at once."""
        for group in groups:
            self.add_recipient_group(group)

    def is_recipient(self, group: str) -> bool:
        """Checks if a specific group is a recipient."""
        return group in self.recipient_groups


class DiscussionThread:
    def __init__(self, course: 'Course', title: str, creator: 'Person'):
        self.course = course  # The course associated with this discussion thread
        self.title = title
        self.creator = creator  # Person (could be Student or Instructor)
        self.posts = []  # List of posts (messages) in this thread
        self.timestamp = datetime.now()

    def display_thread(self) -> None:
        """Display the thread details with all posts."""
        print(f"Discussion Thread: {self.title}")
        print(f"Created by: {self.creator.name} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Course: {self.course.course_name} (Code: {self.course.course_code})")
        print("Posts:")
        for post in self.posts:
            print(f"- {post['person']} ({post['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}): {post['message']}")

    def add_post(self, person: 'Person', message: str) -> None:
        """Add a post to the thread."""
        if not message.strip():
            print("Cannot post an empty message.")
            return
        post = {
            'person': person.name,
            'timestamp': datetime.now(),
            'message': message
        }
        self.posts.append(post)
        print(f"Post added by {person.name}: {message}")


class PlatformAdmin:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = []
        self.enrollments = []  # Handles enrollments

    @staticmethod
    def admin_login():
        """Authenticate admin user."""
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")

        try:
            if os.path.exists("data.json"):
                with open("data.json", "r") as file:
                    data = json.load(file)

                admins = data.get("admins", [])
                if any(admin["email"] == email and admin["password"] == password for admin in admins):
                    print("Login successful. Welcome, Admin!")
                    return True
                else:
                    print("Invalid email or password. Access denied.")
                    return False
            else:
                print("Error: data.json file not found.")
                return False

        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def load_data(self, filename='data.json'):
        """
        Load data from a JSON file and initialize the platform's entities.
        :param filename: Path to the JSON file.
        """
        try:
            if not os.path.exists(filename):
                print(f"File '{filename}' not found. Starting with empty data.")
                return

            with open(filename, 'r') as f:
                data = json.load(f)

            # Load instructors
            self.instructors = [
                Instructor(**inst_data)
                for inst_data in data.get('instructors', [])
            ]

            # Load courses
            self.courses = []
            for course_data in data.get('courses', []):
                instructor_id = course_data.get('instructor_id')
                instructor_obj = next((i for i in self.instructors if i.instructor_id == instructor_id), None)

                if not instructor_obj:
                    print(
                        f"Warning: Instructor ID {instructor_id} not found for course '{course_data.get('course_name', 'Unknown')}'. Skipping.")
                    continue

                course_obj = Course(
                    course_data['course_name'],
                    course_data['course_code'],
                    instructor_obj,
                    course_data['units']
                )
                self.courses.append(course_obj)

            # Load students
            self.students = [
                Student.from_dict(student_data, self.courses)
                for student_data in data.get('students', [])
            ]

            # Load enrollments
            self.enrollments = []
            for enrollment_data in data.get('enrollments', []):
                student_obj = next((s for s in self.students if s.student_id == enrollment_data['student_id']), None)
                course_obj = next((c for c in self.courses if c.course_code == enrollment_data['course_code']), None)

                if student_obj and course_obj:
                    student_obj.enroll(course_obj)
                    course_obj.enrolled_students.append(student_obj)
                else:
                    if not student_obj:
                        print(f"Warning: Student ID {enrollment_data['student_id']} not found.")
                    if not course_obj:
                        print(f"Warning: Course code {enrollment_data['course_code']} not found.")

            # Load schedules
            schedules = data.get('schedules', [])
            for schedule_data in schedules:
                course_obj = next((c for c in self.courses if c.course_code == schedule_data['course_code']), None)
                if course_obj:
                    # Ensure to use the correct class name 'Schedule' instead of 'schedules'
                    schedule_obj = Schedule(course_obj, schedule_data['day'], schedule_data['time'])
                    course_obj.schedule = schedule_obj
                else:
                    print(f"Warning: Course code {schedule_data['course_code']} not found for schedule.")

        except json.JSONDecodeError:
            print("Error decoding JSON. Please ensure the file is formatted correctly.")
        except FileNotFoundError:
            print(f"File '{filename}' not found. Ensure the file exists in the correct path.")
        except Exception as e:
            print(f"An unexpected error occurred while loading data: {e}")

    def save_data(self, filename='data.json'):
        """
        Save the current platform data to a JSON file.
        :param filename: Path to the JSON file.
        """
        try:
            data = {
                "students": [student.to_dict() for student in self.students],
                "instructors": [instructor.to_dict() for instructor in self.instructors],
                "courses": [course.to_dict() for course in self.courses],
                "enrollments": [
                    {"student_id": student.student_id, "course_code": course.course_code}
                    for student in self.students for course in student.enrolled_courses
                ],
                "schedules": [
                    {"course_code": course.course_code, "day": course.schedule.day, "time": course.schedule.time}
                    for course in self.courses if hasattr(course, 'schedule') and course.schedule
                ]
            }

            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Data successfully saved to {filename}.")

        except Exception as e:
            print(f"Error saving data: {e}")


class E_Learning_Environment:
    mission = "To provide quality education through innovative technology."
    vision = "To become a leading platform fostering accessible learning for all."

    def __init__(self):
        self.current_admin = None
        self.platform_admin = PlatformAdmin()
        self.platform_admin.load_data()  # Load data on startup
        self.courses = self.platform_admin.courses
        self.students = self.platform_admin.students
        self.instructors = self.platform_admin.instructors
        self.announcements = []
        self.discussions = []
        self.enrollments = []

    def set_courses(self, courses):
        self.courses = courses

    @classmethod
    def display_mission(cls):
        """Class method to display the mission statement."""
        print("\n🌟 Mission:")
        print(f"   {cls.mission}")

    @classmethod
    def display_vision(cls):
        """Class method to display the vision statement."""
        print("\n🌟 Vision:")
        print(f"   {cls.vision}")

    def main_menu(self):
        while True:
            print("=" * 50)
            print("🎓 Welcome to the E-Learning Environment 🎓".center(50))
            print("=" * 50)
            # Display mission and vision using class methods
            E_Learning_Environment.display_mission()
            E_Learning_Environment.display_vision()
            print("-" * 50)
            print("\nSign in as? Student(1) or Instructor(2)")
            print("1. Student")
            print("2. Instructor")
            print("3. Sign in as Admin")
            print("4. Exit")
            print("-" * 50)
            choice = input("Select an option: ")

            if choice == "1":
                self.student_menu()
            elif choice == "2":
                self.instructor_menu()
            elif choice == "3":
                if self.platform_admin.admin_login():  # Static method call
                    self.admin_menu()
            elif choice == "4":
                self.platform_admin.save_data()  # Save data on exit
                print("Exiting the platform. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def student_menu(self):
        student = self.get_student_by_name()
        if not student:
            print("Student not found.")
            return

        while True:
            print(f"\nWelcome, {student.name}")
            print("1. View My Grades")
            print("2. Submit Assignment")
            print("3. Enroll in Courses")
            print("4. View All Enrolled Courses")
            print("5. View Discussion Threads")
            print("6. Display All Schedule")
            print("7. View Announcements")
            print("8. Logout")
            choice = input("Select an option: ")

            if choice == "1":
                self.view_student_grades(student)
            elif choice == "2":
                self.submit_assignment(student)
            elif choice == "3":
                self.enroll_in_courses(student)
            elif choice == "4":
                self.view_student_courses(student)
            elif choice == "5":
                self.view_discussion_threads(student)
            elif choice == "6":
                self.display_all_schedules()
            elif choice == "7":
                self.view_announcements(student)
            elif choice == "8":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def get_student_by_name(self):
        name = input("Enter your name: ")
        return next((s for s in self.platform_admin.students if s.name == name), None)

    def view_student_grades(self, student):
        print(f"\nGrades for {student.name}:")
        found_grades = False

        # Check the student's own grades
        for grade_info in student.grades:
            found_grades = True
            print(
                f"Course: {grade_info['course_name']} (Code: {grade_info['course_code']}), Grade: {grade_info['grade']}")

        # Alternatively, check enrollments if needed
        for enrollment in self.enrollments:
            if enrollment.get('student_id') == student.student_id:
                found_grades = True
                print(
                    f"Course: {enrollment['course_name']} (Code: {enrollment['course_code']}), Grade: {enrollment.get('grade', 'N/A')}")

        if not found_grades:
            print("No grades found.")

    def submit_assignment(self, student):
        print("\nYour Courses:")
        for course in student.enrolled_courses:
            print(f"- {course.course_name}")

        course_name = input("Enter the course name for which you want to submit an assignment: ").strip()
        course = next((c for c in student.enrolled_courses if c.course_name == course_name), None)

        if not course:
            print("You are not enrolled in this course.")
            return

        assignment_title = input("Enter the assignment title: ").strip()
        assignment = next((a for a in course.assignments if a.title == assignment_title), None)

        if not assignment:
            print("Assignment not found in this course.")
            return

        submission_content = input("Enter your submission content: ").strip()
        print(f"Assignment '{assignment_title}' submitted successfully for course '{course_name}'.")
        print(f"Submission Content: {submission_content}")

    def enroll_in_courses(self, student):
        print("\nAvailable Courses:")
        for course in self.platform_admin.courses:
            print(f"{course.course_name} (Instructor: {course.instructor.name})")

        course_name = input("Enter the course name to enroll in: ")
        course = next((c for c in self.platform_admin.courses if c.course_name == course_name), None)

        if course:
            # Check if the student is already enrolled
            if course in student.enrolled_courses:
                print(f"You are already enrolled in {course_name}.")
            else:
                self.platform_admin.enrollments.enroll_student(student, course)
                print(f"Enrolled in {course_name} successfully!")
        else:
            print("Course not found.")

    def view_student_courses(self, student):
        print(f"\nEnrolled Courses for {student.name}:")
        if not student.enrolled_courses:
            print("You are not enrolled in any courses.")
            return

        for course in student.enrolled_courses:
            print(f"{course.course_name} (Instructor: {course.instructor.name})")

    def display_all_schedules(self):
        print("All schedules:")
        for course in self.courses:
            if hasattr(course, 'schedule') and course.schedule:  # Ensure the course has a schedule
                print(course.schedule.display_schedule())
            else:
                print(f"Course: {course.course_name} has no schedule assigned.")

    def instructor_menu(self):
        instructor = self.get_instructor_by_name()
        if not instructor:
            print("Instructor not found.")
            return

        while True:
            print(f"\nWelcome, {instructor.name}")
            print("1. Assign Assignments")
            print("2. Input Grades")
            print("3. View Enrolled Students")
            print("4. View Courses Taught")
            print("5. Create Announcements")
            print("6. View Announcements")
            print("7. Logout")
            choice = input("Select an option: ")

            if choice == "1":
                self.assign_assignments(instructor)
            elif choice == "2":
                self.input_grades(instructor)
            elif choice == "3":
                self.view_enrolled_students(instructor)
            elif choice == "4":
                self.view_courses_taught(instructor)
            elif choice == "5":
                title = input("Enter announcement title: ")
                content = input("Enter announcement content: ")
                date = input("Enter announcement date (YYYY-MM-DD): ")
                recipient_groups = input("Enter recipient groups (e.g., Student, Instructor, Admin): ").split(", ")
                self.create_announcement(title, content, date, recipient_groups)
            elif choice == "6":
                self.view_announcements(instructor)
            elif choice == "7":
                print(f"Goodbye, {instructor.name}!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def get_instructor_by_name(self):
        name = input("Enter your name: ")
        return next((i for i in self.platform_admin.instructors if i.name == name), None)

    def assign_assignments(self, instructor):
        print("Available Courses:")
        for course in self.platform_admin.courses:
            if course.instructor.instructor_id == instructor.instructor_id:
                print(f"- {course.course_name} ({course.course_code})")

        course_code = input("Enter the course code to assign an assignment: ")
        course = next((c for c in self.platform_admin.courses if c.course_code == course_code), None)

        if course:
            title = input("Enter assignment title: ")
            description = input("Enter assignment description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            course.assign_assignment(title, description, due_date)
        else:
            print("Course not found.")

    def input_grades(self, instructor):
        # Get the course code and find the corresponding course taught by the instructor
        course_code = input("Enter the course code: ")
        course = next(
            (c for c in self.platform_admin.courses if c.course_code == course_code and c.instructor == instructor),
            None
        )

        if course:
            # Proceed to input grades for the students in this course
            student_id = input("Enter the student ID: ")
            grade = input("Enter the grade: ")

            # Add grade for the student (assuming the course has a list of enrolled students)
            student = next((s for s in course.enrolled_students if s.student_id == student_id), None)
            if student:
                student.add_grade(course, grade)  # Assuming there's a method to add grades to the student
                print(f"Grade for student {student.name} in course {course.course_name} is {grade}.")

                # Now call view_student_grades to show the updated grades
                self.view_student_grades(student)  # Pass the student object to display their grades
            else:
                print(f"Student with ID {student_id} is not enrolled in this course.")
        else:
            print(f"Course with code {course_code} not found.")

    def view_enrolled_students(self, instructor):
        """Display a list of students enrolled in the courses taught by the instructor."""
        print("\nCourses Taught:")
        instructor_courses = [course for course in self.platform_admin.courses if
                              course.instructor.instructor_id == instructor.instructor_id]

        if not instructor_courses:
            print("You are not teaching any courses.")
            return

        for course in instructor_courses:
            print(f"\nCourse: {course.course_name} (Code: {course.course_code})")
            if not course.enrolled_students:
                print("  No students are currently enrolled in this course.")
            else:
                print("  Enrolled Students:")
                for student in course.enrolled_students:
                    print(f"  - {student.name} (ID: {student.student_id})")

    def view_courses_taught(self, instructor):
        """Return a list of course names taught by this instructor."""
        instructor_courses = [course for course in self.platform_admin.courses if
                              course.instructor.instructor_id == instructor.instructor_id]

        for course in instructor_courses:
            print(f"\nCourse: {course.course_name} (Code: {course.course_code})")
            if not instructor_courses:
                print("You are not teaching any courses.")
                return

    def view_discussion_threads(self, creator):
        print("\nAvailable Discussion Threads:")

        # Check if the user is a student or instructor and display courses accordingly
        if isinstance(creator, Student):
            courses_to_display = creator.enrolled_courses
        elif isinstance(creator, Instructor):
            courses_to_display = creator._courses_taught  # Instructor teaches courses
        else:
            print("Invalid user type.")
            return

        # Display discussion threads for the courses
        for course in courses_to_display:
            print(f"\nCourse: {course.course_name}")
            for thread in course.discussion_threads:
                thread.display_thread()

        # Option to add a post to a discussion thread
        add_post_choice = input("\nDo you want to add a post? (yes/no): ")
        if add_post_choice.lower() == "yes":
            self.add_post_to_thread(creator)

    def add_post_to_thread(self, creator):
        """Allow user to add a post to a discussion thread."""
        course_name = input("Enter the course name for the thread you want to post in: ")
        course = next((c for c in creator.course if c.course_name().strip().lower() == course_name.lower()), None)

        # if not course:
        #     print("Course not found.")
        #     return

        thread_title = input("Enter the title of the thread you want to post in: ")
        thread = next((t for t in course.discussion_threads if t.title.strip().lower() == thread_title), None)

        if not thread:
            print("Discussion thread not found.")
            return

        message = input("Enter your message: ")
        thread.add_post(creator, message)
        print("Post added successfully!")

    def create_announcement(self, title, content, date, recipient_groups):
        try:
            announcement = Announcement(title, content, date, recipient_groups)
            self.announcements.append(announcement)
            print("Announcement created.")
        except Exception as e:
            print(f"Error creating announcement: {e}")

    def view_announcements(self, user):
        """Method to view announcements for the given user."""
        print("\nAnnouncements:")
        for announcement in self.announcements:
            if user.role in announcement.recipient_groups:  # Assuming user has a role attribute
                print(f"- {announcement.title} ({announcement.date}): {announcement.content}")
        if not any(user.role in announcement.recipient_groups for announcement in self.announcements):
            print("No announcements available.")

    def admin_menu(self):
        """Display the admin menu options."""
        print("Admin Menu:")
        print("1. View Users")
        print("2. Create Announcement")
        print("3. Log Out")

        choice = input("Select an option: ")
        if choice == "1":
            self.view_users()
        elif choice == "2":
            title = input("Enter announcement title: ")
            content = input("Enter announcement content: ")
            date = input("Enter announcement date (YYYY-MM-DD): ")
            recipient_groups = input("Enter recipient groups (e.g., Student, Instructor, Admin): ").split(", ")
            self.create_announcements_admin(title, content, date, recipient_groups)
        elif choice == "3":
            self.log_out()
        else:
            print("Invalid choice, please try again.")

    def view_users(self):
        """Logic to view users."""
        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                try:
                    data = json.load(file)

                    students = data.get("students", [])
                    instructors = data.get("instructors", [])

                    print("Displaying Users:")
                    print("\nStudents:")
                    if students:
                        for student in students:
                            print(f"Email: {student['email']}, Name: {student['name']}")
                    else:
                        print("No students found.")

                    print("\nInstructors:")
                    if instructors:
                        for instructor in instructors:
                            print(f"Email: {instructor['email']}, Name: {instructor['name']}")
                    else:
                        print("No instructors found.")

                except json.JSONDecodeError:
                    print("Error: Could not decode JSON data.")
        else:
            print("No data file found.")

    def create_announcements_admin(self, title, content, date, recipient_groups):
        try:
            announcement = Announcement(title, content, date, recipient_groups)
            self.announcements.append(announcement)
            print("Announcement created.")
        except Exception as e:
            print(f"Error creating announcement: {e}")

    def log_out(self):
        """Logic to log out."""
        print("Logging out...")


if __name__ == "__main__":
    try:
        # Initialize the PlatformAdmin and load data
        platform_admin = PlatformAdmin()

        # Check if load_data method exists
        if hasattr(platform_admin, 'load_data'):
            platform_admin.load_data('data.json')  # Load data from JSON
        else:
            raise AttributeError("PlatformAdmin does not have a 'load_data' method.")
        # Initialize the E-Learning Environment
        e_learning_system = E_Learning_Environment()

        # Ensure platform_admin can be set in E-Learning system
        if hasattr(e_learning_system, 'platform_admin'):
            e_learning_system.platform_admin = platform_admin
        else:
            raise AttributeError("E_Learning_Environment does not have a 'platform_admin' property or method.")

        # Ensure the set_courses method exists and passes the courses to E-Learning system
        if hasattr(e_learning_system, 'set_courses'):
            # Check if platform_admin has 'courses', adjust if it's a method
            if hasattr(platform_admin, 'courses'):
                e_learning_system.set_courses(platform_admin.courses)  # Assuming platform_admin has a courses attribute
            elif hasattr(platform_admin, 'get_courses'):
                e_learning_system.set_courses(platform_admin.get_courses())  # Call if it's a method
            else:
                raise AttributeError("PlatformAdmin does not have a 'courses' attribute or 'get_courses' method.")
        else:
            raise AttributeError("E_Learning_Environment does not have a 'set_courses' method.")

        # Start the main menu
        e_learning_system.main_menu()

    except AttributeError as e:
        print(f"AttributeError: {e}")  # More specific error handling
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")  # Handle missing file
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Generic error for all other cases