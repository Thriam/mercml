"""
Docstring for employee
"""


class Employee:
    """
    Docstring for Employee
    """
    def __init__(self, _id, name, salary):
        """
        Docstring for __init__

        :param self: Description
        :param name: Description
        :param salary: Description
        """
        self.id = _id
        self.name = name
        self.salary = salary

    def hello(self):
        """
        Docstring for hello

        :param self: Description
        """
        print(f"Hello from Employee DB row with person id {self.id}, ", end="")
        print(f"and his name is {self.name}")

    def other_details(self):
        """
        Docstring for other_details

        :param self: Description
        """
        print(f"Mr/Mrs {self.name} gets a salary of {self.salary}")


if __name__ == "__main__":
    print("Enter no. of employees: ", end="")
    num = int(input())
    emp_list = []
    unique = []
    for i in range(num):
        _id = ""
        _list = []
        while 1:
            print("Enter employee ID: ", end="")
            _id = input()
            if _id in unique:
                print("ID already available in DB")
                continue
            unique.append(id)
            break
        print("Enter employee name: ", end="")
        _list.append(input())
        print("Enter employee salary: ", end="")
        _list.append(int(input()))
        e = Employee(_id, _list[0], _list[1])
        emp_list.append(e)

    set_emp = set(emp_list)
    dict_emp = dict(zip(unique, emp_list))

    for i in dict_emp.values():
        i.hello()
        i.other_details()
