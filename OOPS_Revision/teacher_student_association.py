"""
Docstring for OOPS_Revision.teacher_student_association
"""


class Student:
    """
    Docstring for Student
    """
    def __init__(self, student_id, name, marks):
        """
        Docstring for __init__

        :param self: Description
        :param student_id: Description
        :param name: Description
        :param marks: Description
        """
        self.student_id = student_id
        self.name = name
        self.marks = marks
        self.rank = None

    def set_rank(self, rank):
        """
        Docstring for set_rank

        :param self: Description
        :param rank: Description
        """
        self.rank = rank

    def display(self):
        """
        Docstring for display

        :param self: Description
        """
        print(f"ID: {self.student_id}, Name: {self.name}, ", end="")
        print(f"Marks: {self.marks}, Rank: {self.rank}")


class Teacher:
    """
    Docstring for Teacher
    """
    def __init__(self, teacher_id, name):
        """
        Docstring for __init__

        :param self: Description
        :param name: Description
        """
        self.name = name
        self.teacher_id = teacher_id
        self.students = []

    def hello(self):
        """
        Docstring for hello

        :param self: Description
        """
        print(f"Hai I am {self.name} and my ID is {self.teacher_id}")

    def add_student(self, student):
        """
        Docstring for add_student

        :param self: Description
        :param student: Description
        """
        self.students.append(student)

    def pop_student(self, student):
        """
        Docstring for pop_student

        :param self: Description
        :param student: Description
        """
        self.students.pop(student)

    def total_students(self):
        """
        Docstring for total_students

        :param self: Description
        :param students: Description
        """
        print(f"No. of students under {self.name} ", end="")
        print(f"{self.teacher_id} are {len(self.students)}")


    def assign_ranks(self):
        """
        Docstring for assign_ranks

        :param self: Description
        :param students: Description
        """
        ranks = ["1st", "2nd", "3rd", "fail", "restricted"]
        self.students.sort(key=lambda s: s.marks, reverse=True)

        for i in range(len(self.students)):
            if self.students[i].marks >= 60:
                self.students[i].set_rank(ranks[0])
            elif 45 <= self.students[i].marks < 60:
                self.students[i].set_rank(ranks[1])
            elif 35 <= self.students[i].marks < 45:
                self.students[i].set_rank(ranks[1])
            elif 20 <= self.students[i].marks < 35:
                self.students[i].set_rank(ranks[2])
            else:
                self.students[i].set_rank(ranks[3])

    def display_students(self):
        """
        Docstring for display_students

        :param self: Description
        """
        self.students.sort(key=lambda s: s.marks, reverse=True)

        for i in self.students:
            i.display()


if __name__ == "__main__":
    s1 = Student(101, "Thriam1", 95)
    s2 = Student(102, "Thriam2", 90)
    s3 = Student(103, "Thriam3", 85)
    s4 = Student(104, "Thriam4", 80)

    python_teacher = Teacher(1001, "Miss. Upasana")
    ml_teacher = Teacher(1002, "CEO Kavita")

    students_list = [s1, s2, s3, s4]
    python_teacher.add_student(s1)
    ml_teacher.add_student(s2)
    python_teacher.add_student(s1)
    ml_teacher.add_student(s1)
    python_teacher.assign_ranks()
    ml_teacher.assign_ranks()
    python_teacher.assign_ranks()
    ml_teacher.assign_ranks()

    python_teacher.hello()
    python_teacher.total_students()
    python_teacher.display_students()
    ml_teacher.hello()
    ml_teacher.total_students()
    ml_teacher.display_students()
