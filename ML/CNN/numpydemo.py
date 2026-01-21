import numpy as np

list = np.array([[10, 20, 30, 40, True],[1, 2, 3, 4, None]])

list1 = np.array([10, 20, 30, 40])
list2 = np.array([10, 20, 30, 40])

list3 = list1 + list2

list2d1 = np.array(
    [[1, 2, 3, 4],
    ["T1", "Hello", "Hi", "Welcome"],
    [10, 20, 30, 40]]
)
list2d1.resize(1,12)
list2d2 = list2d1.reshape(1,12)
print(list2d1)
