# Define a class for the object
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Create an object
person1 = Person("John", 30)

# Create a dictionary to store the object with an ID
people = {}

# Store the object in the dictionary with an ID
people["person1_id"] = person1

# Access the object using the ID
print(people["person1_id"].name)  # Output: John
print(people["person1_id"].age)   # Output: 30