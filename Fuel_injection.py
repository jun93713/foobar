def answer(n):
  n = long(n)
  count = 0

  if n == 0:
    return 1
  while not n == 1:
    count += 1
    #if its odd
    if n % 2:
        #n & 2 ==> two results:
        #n compare to 2 in binary which is 10
        #if bin(n) ends in 01, result is 00
        #if bin(n) end in 11, result is 10 (in binary, compare 11 and 10 you get 10)
        #so if n & 2 == 0, n is 1 more than multiple of 4
        #n & 2 == 2, n is 1 less than multiple of 4
      if n == 3 or n & 2 == 0:
        n -= 1
      else:
        n += 1
    else:
      n = n >> 1
  return count

print(answer(15))
