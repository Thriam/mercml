"""
Docstring for employee_adv
"""


class Employee:
    """
    Docstring for Employee
    """
    def __init__(self, _id, name, salary):
        """
        Docstring for __init__

        :param self: Description
        :param id: Description
        :param name: Description
        :param salary: Description
        """
        self.__id = _id
        self.__name = name
        self.__salary = salary

    def get_id(self):
        """
        Docstring for get_id

        :param self: Description
        """
        return f"The id is {self.__id}"

    def show_details(self):
        """
        Docstring for show_details

        :param self: Description
        """
        print(self.__id, self.__name, self.__salary)


class Manager(Employee):
    """
    Docstring for Manager
    """
    def __init__(self, _id, name, salary, no_of_teams):
        """
        Docstring for __init__

        :param self: Description
        :param id: Description
        :param name: Description
        :param salary: Description
        :param no_of_teams: Description
        """
        super().__init__(_id, name, salary)
        self.__no_of_teams = no_of_teams

    def get_id(self):
        """
        Docstring for get_id

        :param self: Description
        """
        print(super().get_id())

    def show_details(self):
        """
        Docstring for show_details

        :param self: Description
        """
        super().show_details()
        print(self.__no_of_teams)


if __name__ == "__main__":
    emp = Employee(1001, "xyz", 1234567)
    emp.show_details()
    mgr = Manager(101, "abc", 12345678, 10)
    mgr.show_details()
