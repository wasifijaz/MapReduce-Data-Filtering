#!/usr/bin/env python
import sys

def is_date(string):
    try:
        year, month, day = map(int, string.split('-'))
        return True
    except ValueError:
        return False

def map_grades(parts):
    student_id, course_id, grade = parts
    return {student_id: [course_id, grade]}

def map_students(parts):
    student_id, name, dob = parts
    return {student_id: [name, dob]}

def read_csv(file_path, data_type):
    data_list = []
    with open(file_path, 'r') as file:
        first_line = True
        for line in file:
            if first_line:
                first_line = False
                continue
            line = line.strip()
            parts = line.split(',')
            if data_type == 'grades':
                data_list.append(map_grades(parts))
            elif data_type == 'students':
                data_list.append(map_students(parts))
    return data_list

def main(grades_file, students_file):
    studentList = read_csv(students_file, 'students')
    gradesList = read_csv(grades_file, 'grades')
    
    student_dict = {list(student.keys())[0]: list(student.values())[0] for student in studentList}
    combined_list = []
    for grade in gradesList:
        for student_id, grade_details in grade.items():
            if student_id in student_dict:
                student_details = student_dict[student_id] + grade_details
                combined_list.append({student_id: student_details})

    print(combined_list)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python mapper.py <grades_file.csv> <students_file.csv>")
    else:
        main(sys.argv[1], sys.argv[2])
