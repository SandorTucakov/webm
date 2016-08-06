from multiprocessing import Pool
from time import sleep

def square(x):
  sleep(x % 3)
  print 'sq:' , x * x, x % 3
  return x * x

def cube(y):
  print 'cb:', y * y * y
  return y * y * y

pool = Pool(processes=4)

result_squares = pool.map_async(square, range(150))
result_cubes = pool.map_async(cube, range(150))
