import numpy as np

myarray = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

print(myarray.shape)
print(myarray)

newarray = myarray.reshape(int(myarray.shape[0] / 3), 3)

print(newarray.shape)
print(newarray)