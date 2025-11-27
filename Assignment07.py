# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Jett Magnuson,11/24/2025,Created Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the data variables
students: list = []
menu_choice: str = ''

class Person:
    """A class representing person data """

    def __init__(self, first_name: str = '' , last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def last_name(self):
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self):
        return f'{self.first_name},{self.last_name}'

class Student(Person):
    """A class representing student data """

    def __init__(self, first_name: str = '' , last_name: str = '', course_name: str = ''):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'

class FileProcessor:
    """A collection of processing layer functions that work with Json files"""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """Reads data from a json file and loads it into a list of student objects"""
        file = None
        try:
            file = open(file_name, "r")
            json_data = json.load(file)
            file.close()

            for student in json_data:
                student_object = Student(first_name=student["FirstName"],
                                         last_name=student["LastName"],
                                         course_name=student["CourseName"])
                student_data.append(student_object)

        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!.", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error when reading the file!",e)
        finally:
            if file and not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name:str,  student_data: list):
        """Writes data to json file with data from a list of student objects"""
        file = None
        try:
            list_of_dictionary_data = []
            for student in student_data:
                student_json = {"FirstName": student.first_name,
                                "LastName": student.last_name,
                                "CourseName": student.course_name}
                list_of_dictionary_data.append(student_json)

            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file, indent=2)
            file.close()
            IO.output_student_courses(student_data=student_data)
        except Exception as e:
            if file and not file.closed:
                file.close()
            IO.output_error_messages("There was a problem writing to the file!", e)

class IO:
    """A collection of presentation layer functions that manage user input and output """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Displays a custom error message"""
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu:str):
        """Displays the menu of choices to the user"""
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """Gets a menu choice from the user"""
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """Displays the student and course names to the user"""
        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} '
                f'{student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """Gets the student's first name and last name, with a course name from the user"""
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")

            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Please enter the name of the course: ")

            student = Student(first_name=student_first_name,
                            last_name=student_last_name,
                            course_name=course_name)
            student_data.append(student)

            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was not correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data!", error=e)
        return student_data

# start of main body
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while True:
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":
        break

    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended")