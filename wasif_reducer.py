#!/usr/bin/env python
import sys

current_student_id = None
student_info = None
course_grades = []

for line in sys.stdin:
    line = line.strip()

    input_data = eval(line) 
    
    for data in input_data:
        for student_id, details in data.items():
            name = details[0]
            dob = details[1]
            course_id = details[2]
            grade = details[3]

            if current_student_id != student_id:
                if current_student_id and student_info and course_grades and student_info[1] >= "1995-01-01":
                    for course, grade in course_grades:
                        print(f'{current_student_id} {student_info[0]} {course} {grade}')
                current_student_id = student_id
                student_info = (name, dob)
                course_grades = []

            course_grades.append((course_id, grade))

if current_student_id and student_info and course_grades and student_info[1] >= "1995-01-01":
    course_grades = list(set(course_grades))
    print("StudentId\tName\tCourseId\tGrade")
    for course, grade in course_grades:
        print(f'{current_student_id}\t\t{student_info[0]}\t{course}\t\t{grade}')