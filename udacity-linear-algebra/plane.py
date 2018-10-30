from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        '''

        :param normal_vector:
        :type normal_vector: Vector
        :param constant_term:
        :type constant_term: str
        '''
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def __mul__(self, other):
        return Plane(normal_vector=self.normal_vector * other, constant_term=self.constant_term * other)

    def __add__(self, other):
        return Plane(
            normal_vector=self.normal_vector + other.normal_vector,
            constant_term=self.constant_term + other.constant_term)

    def __getitem__(self, item):
        '''
        :param item:
        :type item: int
        :return:
        :rtype: Decimal
        '''
        return self.normal_vector[item]

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)

    def get_nonzero_index(self):
        '''

        :return:
        :rtype: int
        '''
        try:
            return Plane.first_nonzero_index(self.normal_vector)
        except Exception as e:
            if (str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG):
                return -1
            else:
                raise e

    def is_parallel(self, other):
        return self.normal_vector.is_parallel(other.normal_vector)

    def __eq__(self, other):
        if self.is_parallel(other):
            if (self.normal_vector.is_zero_vector() and other.normal_vector.is_zero_vector()):
                return True
            if not self.basepoint or not other.basepoint:
                return self.normal_vector == other.normal_vector and self.constant_term == other.constant_term
            basepoint_diff = self.basepoint - other.basepoint
            return basepoint_diff.is_orthogonal(self.normal_vector)

        return False


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
