from math import sqrt

import math

from decimal import Decimal

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

class Vector(object):

    ZERO_MSG = 'ZERO_VECTOR'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __getitem__(self, item):
        return self.coordinates[item]

    def __add__(self, other):
        return Vector([x + y for x,y in zip(self.coordinates, other.coordinates)])

    def __sub__(self, other):
        return Vector([x - y for x,y in zip(self.coordinates, other.coordinates)])

    def __mul__(self, other):
        return Vector([x * Decimal(other) for x in self.coordinates])

    def __div__(self, other):
        return Vector([x / Decimal(other) for x in self.coordinates])

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def magnitude(self):
        return Decimal.sqrt(reduce(lambda x,y: x+y, map(lambda x: pow(x, 2), self.coordinates), Decimal('0')))

    def normalize(self):
        try:
            return Vector(self.coordinates) / self.magnitude()
        except ZeroDivisionError:
            raise Exception(self.ZERO_MSG)


    def dot_product(self, other):
        return reduce(lambda x, y: x+y, map(lambda x,y: x*y, self.coordinates, other.coordinates), 0)

    def angle(self, other, in_degrees = False):

        angle =  math.acos(self.dot_product(other) / (self.magnitude() * other.magnitude()))

        if in_degrees:
            return math.degrees(angle)
        else:
            return angle

    def is_zero_vector(self):
        return self.is_zero(self.magnitude())

    def is_zero(self, value, tolerance = 1e-10):
        return math.fabs(value) < tolerance

    def within_tolerance(self, value1, value2, tolerance = 1e-10):
        return value1 - tolerance < value2 and value1 + tolerance > value2

    def is_orthogonal(self, other):
        return self.is_zero_vector() or \
               other.is_zero_vector() or \
                self.is_zero(self.dot_product(other))

    def is_parallel(self, other):
        return self.is_zero_vector() or \
            other.is_zero_vector() or \
            reduce(lambda x,y: x and y,
                   map(lambda x,y: self.within_tolerance(math.fabs(x), math.fabs(y)),
                       self.normalize().coordinates,
                       other.normalize().coordinates),
                   True)

    def projection(self, other):
        other_normalized = other.normalize()
        proj_magnitude = self.dot_product(other_normalized)
        return other_normalized * proj_magnitude

    def orthogonal_projection(self, other):
        return self - self.projection(other)

    def cross_product(self, other):
        v = self.coordinates
        w = other.coordinates

        return Vector([v[1]*w[2] - w[1]*v[2], -1*(v[0]*w[2] - w[0]*v[2]), v[0]*w[1] - w[0]*v[1]])

    def area_of_parallelogram(self, other):
        return self.cross_product(other).magnitude()

    def area_of_triangle(self, other):
        return self.area_of_parallelogram(other) / 2

    def __eq__(self, v):
        return self.coordinates == v.coordinates
