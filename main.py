


student_1 = "John"
student_1_age = 16

def print_student_info(name, age):
  print(name + " ", age)


###############################################



class Student:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def print_info(self):
    print(self.name + " ", self.age)

john = Student("John", 17)
john.print_info()