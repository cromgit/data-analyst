

from line import Line, MyDecimal
from plane import Plane
from vector import Vector
import unittest

print 'Quiz 1'

def tdv(array):
    return Vector(map(lambda x: MyDecimal(x), array))

def td(value):
    return MyDecimal(value)

q1_array = [
    Line(tdv(['4.046','2.836']), td('1.21')),
    Line(tdv(['10.115','7.09']), td('3.025')),
    Line(tdv(['7.204','3.182']), td('8.68')),
    Line(tdv(['8.172','4.114']), td('9.883')),
    Line(tdv(['1.182','5.562']), td('6.744')),
    Line(tdv(['1.773','8.343']), td('9.525'))
]

print q1_array[0].intercept(q1_array[1])
print q1_array[2].intercept(q1_array[3])
print q1_array[4].intercept(q1_array[5])

print 'Quiz 2'

q2_array = [
    Plane(tdv(['-0.412', '3.806','0.728']), td('-3.46')),
    Plane(tdv(['1.03','-9.515','-1.82']), td('8.65')),
    Plane(tdv(['2.611','5.528','0.283']), td('4.6')),
    Plane(tdv(['7.715','8.306','5.342']), td('3.76')),
    Plane(tdv(['-7.926','8.625','-7.212']), td('-7.952')),
    Plane(tdv(['-2.642','2.875','-2.404']), td('-2.443'))
]

print q2_array[0].is_parallel(q2_array[1]), q2_array[0] == q2_array[1]
print q2_array[2].is_parallel(q2_array[3]), q2_array[2] == q2_array[3]
print q2_array[4].is_parallel(q2_array[5]), q2_array[4] == q2_array[5]


# -x + y + z + x - 4y + 4z = -2 + 21
# -3y + 5z = 19
# 7(-x + y + z) + (7x - 5y - 11z) = 7*-2 + 0
# 2y - 4z = -14
# -3y + 5z + 3/2(2y - 4z) = 19 + 3/2(-14)
# 5z + - 6z = 19 - 21
# -z = -2
# z = 2
# -3y + 5z = 19
#  -3y + 10 = 19
# -3y = 9
# y = -3
# -x + y + z = -2
# -x + -3 + 2 = -2
# -x - 3 = -4
# -x = -1
#  x = 1


# x - 2y + z = -1,  2y - 3z = 3
# x       -2z = 2
# -x + 4y - 4z = 0, 2y -3z = -1

# x - 2y + z = -1
# x      - 2z = 2,      2y - 3z = 3
# -x + 4y - 4z = 0,     2y - 3z = -1, 0 = -4
#

#      y - z = 2, -3z = -3, z = 1
# x -  y + z = 2, x + 3 + 1 = 2, x = 2 -3 -1 = -2
# 3x - 4y + z = 1, -y - 2z = -5, y = -5 + 2z, y = -5 + 2 = -3

# x + 2y + z = -1, x + 2y - 4 = -1, x + 2y = 3, x = 3 - 2y
# 3x + 6y + 2z = 1, 0 + 0 - z = 4, z = -4
# -x - 2y - z = 1, 0 = 0

# [ 3 - 2y ]
# [ y ]
# [ -4 ]
# [3, 0, -4] + y[-2, 1, 0]

# x + 2y + z = -1, x + 2y - 4 = -1, x + 2y = 3, x = 3 - 2y
# 3x + 6y + 2z = 1, 0 + 0 - z = 4, z = -4
# -x - 2y - z = 1, 0 = 0