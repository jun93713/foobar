from fractions import Fraction
# m = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

# m = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
# m = [[0, 1, 1],[1, 0, 1], [0, 0, 0]]
m = [[0, 1], [0, 0]]

def answer(m):
  if len(m) ==2 :
    return [1, 1]
  markov = []
  markovDict = {}
  indexToLetter = { 0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J"}

  #save locations of state transform count using letters
  #    A  B  C  D  E  F
  # A  0  1  0  0  0  1
  # B  4  0  0  3  2  0
  # C  0  0  0  0  0  0
  # D  0  0  0  0  0  0
  # E  0  0  0  0  0  0
  # F  0  0  0  0  0  0
  #save in dict 'AB': 1/2 which helps relocate them after reform the matrix
  for i in range(len(m)):
    for j in range(len(m)):
      if m[i][j]:
        frac = Fraction(m[i][j], sum(m[i]))
        markovDict[indexToLetter[i]+indexToLetter[j]] = Fraction(m[i][j], sum(m[i]))

  #find the moving pattern of reforming the matrix
  order = ""
  for i in range(len(m)):
    if not sum(m[i]):
      markovDict[indexToLetter[i] + indexToLetter[i]] = 1
      order += indexToLetter[i]
  divider = len(order)
  alpha = "ABCDEFGHIJ"
  for i in range(len(m)):
    if not alpha[i] in order:
      order += alpha[i]

  #According to https://www.youtube.com/watch?v=BsOkOaB8SFk
  #the reformed matrix should look like this
  #    C  D  E  F | A  B
  # C  1  0  0  0 | 0  0
  # D  0  1  0  0 | 0  0
  # E  0  0  1  0 | 0  0
  # F  0  0  0  1 | 0  0
  #---------------+-----
  # A  0  0  0  1 | 0  1
  # B  0  3  2  0 | 4  0
  # all I need is this part with non-zero numbers to coresponding fractions/floats as prabability like this
  #    C    D    E    F   |  A   B
  # A  0    0    0   1/2  |  0  1/2
  # B  0   3/9  2/9   0   | 4/9  0
  #where left part is R and right part is Q
  R, Q = [], []
  for i in range(divider, len(m)):
    row_R, row_Q = [], []
    for j in range(len(m)):
      key = order[i] + order[j]
      if key in markovDict:
        row_R.append(markovDict[key]) if j < divider else row_Q.append(markovDict[key])
      else:
        row_R.append(0) if j < divider else row_Q.append(0)
    R.append(row_R)
    Q.append(row_Q)


  # the output is the first row of FR
  # where F = (I - Q)^-1
  # 1. find I - Q  
  # 2. inverse it to get F
  F = inverse_matrix(i_mines_q(make_matrix_i(len(Q)), Q))
  # 3. multiply F and R
  FR = matrix_mult(F, R)
  print(FR[0])
  # the fisrt row of FR is the result but need a bit reform to the requirement
  #find the least common multiple among the denominators, then multiply FR[0] with lcm
  lcm = lcm_in_arr(list(map(lambda x: x.denominator, FR[0])))
  
  return list(map(lambda x: int(x * lcm), FR[0])) + [lcm]

def gcd(a, b):
  return a if not b else gcd(b, a%b)

def lcm(a, b):
  return a*b//gcd(a, b)

def lcm_in_arr(arr):
  for i in range(1, len(arr)):
    arr[i] = lcm(arr[i], arr[i - 1])
  return arr[len(arr) - 1]

def matrix_mult(a,b):
  zip_b = zip(*b)
  return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
            for col_b in zip_b] for row_a in a]

def make_matrix_i(size):
  return [[1 if i == j else 0 
  for j in range(size)]
  for i in range(size)]

#only for I-Q
def i_mines_q(a, b):
  l = len(b)

  res = [[ 0 for j in range(l)]
  for i in range(l)]

  for i in range(l):
    for j in range(l):
      res[i][j] = a[i][j] - b[i][j]

  return res


def transpose_matrix(m):
  return map(list,zip(*m))

def get_matrix_of_minors(m,i,j):
  return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def get_matrix_of_deternminant(m):
  #base case for 2x2 matrix
  if len(m) == 2:
      return m[0][0]*m[1][1]-m[0][1]*m[1][0]

  determinant = 0
  for c in range(len(m)):
      determinant += ((-1)**c)*m[0][c]*get_matrix_of_deternminant(get_matrix_of_minors(m,0,c))
  return determinant

def inverse_matrix(m):
  determinant = get_matrix_of_deternminant(m)
  #special case for 2x2 matrix:
  if len(m) == 2:
      return [[m[1][1]/determinant, -1*m[0][1]/determinant],
              [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
  cofactors = []
  for r in range(len(m)):
      cofactorRow = []
      for c in range(len(m)):
          minor = get_matrix_of_minors(m,r,c)
          cofactorRow.append(((-1)**(r+c)) * get_matrix_of_deternminant(minor))
      cofactors.append(cofactorRow)
  cofactors = transpose_matrix(cofactors)
  for r in range(len(cofactors)):
      for c in range(len(cofactors)):
          cofactors[r][c] = cofactors[r][c]/determinant
  return cofactors
  
print(answer(m))

