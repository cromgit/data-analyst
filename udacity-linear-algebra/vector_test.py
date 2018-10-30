from math import sqrt

from decimal import Decimal

from vector import Vector

def to_vectors(this):
    return [Vector(x) for x in this]

def to_pairs(this):
    return [(this[x], this[x+1]) for x in range(0, len(this), 2)]

print 'Quiz 1'

q1a = Vector([8.218, -9.341])
q1b = Vector([-1.129, 2.111])
q1c = Vector([7.119, 8.215])
q1d = Vector([-8.223, 0.878])
q1e = Vector([1.671, -1.012, -0.318])
q1f = 7.41

print q1a + q1b
print q1c - q1d
print q1d * q1f

print 'Quiz 2'

q2a = Vector([-0.221, 7.437])
q2b = Vector([8.813, -1.331, -6.247])
q2c = Vector([5.581, -2.136])
q2d = Vector([1.996, 3.108, -4.554])

print q2a.magnitude()
print q2b.magnitude()
print q2c.normalize()
print q2d.normalize()

print 'Quiz 3'

q3v1 = Vector([7.887, 4.138])
q3v2 = Vector([-8.802, 6.776])
q3v3 = Vector([-5.955, -4.904, -1.874])
q3v4 = Vector([-4.496, -8.755, 7.103])
q3v5 = Vector([3.183, -7.627])
q3v6 = Vector([-2.668, 5.319])
q3v7 = Vector([7.35, 0.221, 5.188])
q3v8 = Vector([2.751, 8.259, 3.985])

print q3v1.dot_product(q3v2)
print q3v3.dot_product(q3v4)
print q3v5.angle(q3v6)
print q3v7.angle(q3v8, True)

print 'Quiz 4'

q4_vectors = to_pairs(to_vectors([
    [-7.579, -7.88],[22.737, 23.64],
    [-2.029, 9.97, 4.172],[-9.231, -6.639, -7.245],
    [-2.328, -7.284, -1.214],[-1.821, 1.072, -2.94],
    [2.118, 4.827],[0, 0]]))

for x in q4_vectors:
    # print x[0], x[1]
    # print x[0].normalize(), x[1].normalize()
    # print x[0].dot_product(x[1])
    print x[0].is_parallel(x[1])
    print x[0].is_orthogonal(x[1])

print 'Quiz 5'

q5_vectors = to_pairs(to_vectors([
    [3.039,1.879],[0.825,2.036],
    [-9.88,-3.264,-8.159],[-2.155,-9.353,-9.473],
    [3.009,-6.172,3.692,-2.51],[6.404,-9.144,2.759,8.718]
]))

print q5_vectors[0][0].projection(q5_vectors[0][1])
print q5_vectors[1][0].orthogonal_projection(q5_vectors[1][1])
print q5_vectors[2][0].projection(q5_vectors[2][1]), q5_vectors[2][0].orthogonal_projection(q5_vectors[2][1])

print 'Quiz 6'

q6_vectors = to_pairs(to_vectors([
    [8.462, 7.893,-8.187],[6.984,-5.975,4.778],
    [-8.987,-9.838,5.031],[-4.268,-1.861,-8.866],
    [1.5,9.547,3.691],[-6.007,0.124,5.772]
]))

print q6_vectors[0][0].cross_product(q6_vectors[0][1])
print q6_vectors[1][0].area_of_parallelogram(q6_vectors[1][1])
print q6_vectors[2][0].area_of_triangle(q6_vectors[2][1])
