import math

def answer(total_lambs):
    if total_lambs < 4:
        return 0
    return most(total_lambs) - least(total_lambs)

#sum of fib numbers = F(n+2) - F(2)
def most(total_lambs):
    for i,f  in enumerate(fibonacci()):
        if f > total_lambs + 1:
            return i - 2

#least men 1, 2, 4, 8, 16...2^n
def least(num):
  for j, t in enumerate(twoPower()):
    if 2**(j+1)-1 > num:
      if num - 2**j + 1 >= 2**(j-2) + 2**(j-1):
        return j + 1
      else:
        return j

#most men 1, 1, 2, 3, 5, 8, 13...fib
def fibonacci():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def twoPower():
  a = 2
  while True:
    yield a
    a = a * 2



