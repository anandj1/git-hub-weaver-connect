"""
Python Practice Exercises
Complete these exercises to reinforce your learning
"""

# Exercise 1: Variables and Data Types
def exercise_1():
    """
    Create variables for:
    - Your name (string)
    - Your age (integer)
    - Your height in meters (float)
    - Whether you're a student (boolean)
    
    Print all variables with descriptive messages
    """
    # Your code here
    pass

# Exercise 2: Lists and Loops
def exercise_2():
    """
    Create a list of your favorite movies.
    Use a for loop to print each movie with its position number.
    Example: "1. The Matrix"
    """
    # Your code here
    pass

# Exercise 3: Functions
def calculate_area(length, width):
    """
    Calculate and return the area of a rectangle
    """
    # Your code here
    pass

def exercise_3():
    """
    Use the calculate_area function to find the area of a 5x3 rectangle
    """
    # Your code here
    pass

# Exercise 4: Dictionaries
def exercise_4():
    """
    Create a dictionary representing a book with keys:
    - title
    - author
    - year
    - pages
    
    Print the book information in a formatted way
    """
    # Your code here
    pass

# Exercise 5: List Comprehensions
def exercise_5():
    """
    Create a list of squares for numbers 1-10 using list comprehension
    Then create another list with only even squares
    """
    # Your code here
    pass

# Exercise 6: File Handling
def exercise_6():
    """
    Write a function that:
    1. Creates a file called "my_notes.txt"
    2. Writes 3 lines of text to it
    3. Reads the file and prints its contents
    """
    # Your code here
    pass

# Exercise 7: Classes
class Student:
    """
    Create a Student class with:
    - name and grade attributes
    - a method to display student info
    - a method to update the grade
    """
    def __init__(self, name, grade):
        # Your code here
        pass
    
    def display_info(self):
        # Your code here
        pass
    
    def update_grade(self, new_grade):
        # Your code here
        pass

def exercise_7():
    """
    Create a Student object and test its methods
    """
    # Your code here
    pass

# Exercise 8: Error Handling
def safe_divide(a, b):
    """
    Create a function that safely divides two numbers
    Handle division by zero and invalid input types
    """
    # Your code here
    pass

def exercise_8():
    """
    Test the safe_divide function with various inputs
    """
    # Your code here
    pass

# Exercise 9: Advanced - Password Validator
def validate_password(password):
    """
    Create a password validator that checks:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character (!@#$%^&*)
    
    Return True if valid, False otherwise
    """
    # Your code here
    pass

def exercise_9():
    """
    Test the password validator with different passwords
    """
    test_passwords = [
        "password",
        "Password1",
        "Password1!",
        "Pass1!",
        "MySecurePassword123!"
    ]
    
    for pwd in test_passwords:
        result = validate_password(pwd)
        print(f"'{pwd}' is {'valid' if result else 'invalid'}")

# Exercise 10: Mini Project - To-Do List
class TodoList:
    """
    Create a simple to-do list manager with methods to:
    - Add tasks
    - Remove tasks
    - Mark tasks as complete
    - Display all tasks
    """
    def __init__(self):
        # Your code here
        pass
    
    def add_task(self, task):
        # Your code here
        pass
    
    def remove_task(self, task):
        # Your code here
        pass
    
    def complete_task(self, task):
        # Your code here
        pass
    
    def display_tasks(self):
        # Your code here
        pass

def exercise_10():
    """
    Create a TodoList and test all its methods
    """
    # Your code here
    pass

if __name__ == "__main__":
    print("Python Practice Exercises")
    print("=" * 30)
    
   
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    exercise_7()
    exercise_8()
    exercise_9()
    exercise_10()
    
    print("\nComplete the exercises by filling in the code!")