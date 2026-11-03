
"""
Student Manager — DevOps Lab 5
Module: Main Application
"""

import sys
import json
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from student import Student

DATA_FILE = "students.json"


# ==============================
# VALIDATION
# ==============================

def validate_student_id(student_id):
    return bool(student_id.strip())


def validate_name(name):
    return bool(name.strip())


def validate_age(age):
    try:
        age = int(age)
        return 1 <= age <= 120
    except ValueError:
        return False


# ==============================
# ADD STUDENT
# ==============================

def add_student(students, student_id, name, age, grade):

    if not validate_student_id(student_id):
        print("Invalid student ID!")
        return students

    if not validate_name(name):
        print("Invalid student name!")
        return students

    if not validate_age(age):
        print("Age must be between 1 and 120!")
        return students

    if not grade.strip():
        print("Grade cannot be empty!")
        return students

    for s in students:
        if s.student_id.lower() == student_id.lower():
            print("Student ID already exists!")
            return students

    student = Student(student_id, name, int(age), grade)

    students.append(student)

    print("Student added successfully!")

    return students


# ==============================
# DISPLAY STUDENTS
# ==============================

def display_students(students):

    if not students:
        print("No students found!")
        return

    print("\n========== STUDENT LIST ==========")

    for index, student in enumerate(students, start=1):
        print(f"{index}. {student}")

    print(f"\nTotal students: {len(students)}")


# ==============================
# SEARCH STUDENT
# ==============================

def search_student(students, keyword):

    results = []

    keyword = keyword.strip().lower()

    for student in students:
        if (
            keyword in student.name.lower()
            or keyword in student.student_id.lower()
        ):
            results.append(student)

    if results:
        print(f"\nFound {len(results)} student(s):")

        for student in results:
            print(student)

    else:
        print("Student not found!")

    return results


# ==============================
# UPDATE STUDENT
# ==============================

def update_student(students, student_id):

    student = next(
        (s for s in students
         if s.student_id.lower() == student_id.lower()),
        None
    )

    if student is None:
        print("Student not found!")
        return students

    print("Enter new information (leave blank to keep old value)")

    name = input(f"Name [{student.name}]: ").strip()
    age = input(f"Age [{student.age}]: ").strip()
    grade = input(f"Grade [{student.grade}]: ").strip()

    if name:
        student.name = name

    if age:
        if validate_age(age):
            student.age = int(age)
        else:
            print("Invalid age! Keeping old age.")

    if grade:
        student.grade = grade

    print("Student updated successfully!")

    return students


# ==============================
# DELETE STUDENT
# ==============================

def delete_student(students, student_id):

    for student in students:

        if student.student_id.lower() == student_id.lower():

            confirm = input(
                f"Delete {student.name}? (y/n): "
            ).strip().lower()

            if confirm == "y":
                students.remove(student)
                print("Student deleted successfully!")
            else:
                print("Delete cancelled!")

            return students

    print("Student not found!")

    return students


# ==============================
# SORT STUDENTS
# ==============================

def sort_students(students):

    print("\n1. Sort by name")
    print("2. Sort by age")
    print("3. Sort by student ID")

    choice = input("Choose: ")

    if choice == "1":
        students.sort(key=lambda s: s.name.lower())

    elif choice == "2":
        students.sort(key=lambda s: s.age)

    elif choice == "3":
        students.sort(key=lambda s: s.student_id.lower())

    else:
        print("Invalid choice!")
        return

    print("Students sorted successfully!")


# ==============================
# STATISTICS
# ==============================

def statistics(students):

    if not students:
        print("No data available!")
        return

    total = len(students)

    average_age = sum(
        s.age for s in students
    ) / total

    oldest = max(students, key=lambda s: s.age)
    youngest = min(students, key=lambda s: s.age)

    print("\n========== STATISTICS ==========")
    print(f"Total students: {total}")
    print(f"Average age: {average_age:.2f}")
    print(f"Oldest student: {oldest.name} ({oldest.age})")
    print(f"Youngest student: {youngest.name} ({youngest.age})")


# ==============================
# SAVE DATA
# ==============================

def save_data(students):

    data = [s.to_dict() for s in students]

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Data saved successfully!")

    except OSError as error:
        print(f"Cannot save data: {error}")


# ==============================
# LOAD DATA
# ==============================

def load_data():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [Student.from_dict(item) for item in data]

    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Cannot load data: {error}")
        return []


# ==============================
# MAIN MENU
# ==============================

def main():

    students = load_data()

    if not students:
        students = [
            Student("SV001", "Nguyen Van A", 20, "K20"),
            Student("SV002", "Tran Thi B", 21, "K20"),
            Student("SV003", "Le Van C", 19, "K21"),
        ]

    while True:

        print("\n" + "=" * 45)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Add Student")
        print("2. Display Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Sort Students")
        print("7. Statistics")
        print("8. Save Data")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            student_id = input("Student ID: ")
            name = input("Name: ")
            age = input("Age: ")
            grade = input("Grade: ")

            add_student(
                students,
                student_id,
                name,
                age,
                grade
            )

        elif choice == "2":
            display_students(students)

        elif choice == "3":
            keyword = input("Enter keyword: ")
            search_student(students, keyword)

        elif choice == "4":
            student_id = input("Enter student ID: ")
            update_student(students, student_id)

        elif choice == "5":
            student_id = input("Enter student ID: ")
            delete_student(students, student_id)

        elif choice == "6":
            sort_students(students)

        elif choice == "7":
            statistics(students)

        elif choice == "8":
            save_data(students)

        elif choice == "0":
            save_data(students)
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
