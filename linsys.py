from decimal import Decimal, getcontext
from copy import deepcopy

import math

from vector import Vector, MyDecimal
from plane import Plane

getcontext().prec = 30

class Parametrization(object):

    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM = (
        'The basepoint and direction vectors should all live in the same '
        'dimension')

    def __init__(self, basepoint, direction_vectors):

        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension

        except AssertionError:
            raise Exception(self.BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM)

    def __str__(self):

        output = ''
        for coord in range(self.dimension):
            output += 'x_{} = {} '.format(coord + 1,
                                          round(self.basepoint[coord], 3))
            for free_var, vector in enumerate(self.direction_vectors):
                output += '+ {} t_{}'.format(round(vector[coord], 3),
                                             free_var + 1)
            output += '\n'
        return output


class LinearSystem(object):

    planes = None # type: List[Plane]
    dimension = None # type: int

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'


    def __init__(self, planes):
        '''

        :param planes:
        :type planes: List[Plane]
        '''
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        tmp = self[row1]
        self[row1] = self[row2]
        self[row2] = tmp

    def multiply_coefficient_and_row(self, coefficient, row):
        self[row] = self[row] * coefficient

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        self[row_to_be_added_to] = \
            self[row_to_add] * Decimal(coefficient) + self[row_to_be_added_to]

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.get_nonzero_index()
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        '''

        :param i:
        :type i: int
        :return:
        :rtype: Plane
        '''
        return self.planes[i]


    def __setitem__(self, i, x):
        '''

        :param i:
        :type i: int
        :param x:
        :type x: Plane
        :return:
        :rtype: None
        '''
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret

    def find_plane(self, func, start = 0):
        for i in range(start, len(self.planes)):
            if func(self.planes[i]):
                return i
        return None

    # x y z
    # 1 1 1 N
    # -1 1 -1 Y
    # 1 -1 -1 N
    # -1 -1 1 Y

    def find_and_swap(self, variable_index, current_index):
        '''

        :param system:
        :type system: LinearSystem
        :param variable_index:
        :type variable_index: int
        :param current_index:
        :type current_index: int
        :param nonzero_index:
        :type nonzero_index: int
        :return:
        :rtype: None
        '''
        for i in range(current_index, len(self.planes)):
            first_zero_index = self[i].get_nonzero_index()
            if first_zero_index >=0 and first_zero_index <= variable_index:
                self.swap_rows(current_index, i)
                return True

        return False

    def clear_variables(self, plane_index, variable_index, nonzero_index):
        for i in range(plane_index):
            ith_nonzero_index = self[i].get_nonzero_index()
            if (ith_nonzero_index == nonzero_index):
                row_to_add = i
                row_to_add_to = plane_index
                coefficient = (self[row_to_add_to][nonzero_index] / self[row_to_add][ith_nonzero_index]).copy_abs()
                if self[row_to_add_to][nonzero_index] * self[row_to_add][ith_nonzero_index] > 0:
                    coefficient = coefficient * -1
                self.add_multiple_times_row_to_row(coefficient, row_to_add=row_to_add, row_to_be_added_to=row_to_add_to)


    @property
    def compute_triangular_form(self):
        system = deepcopy(self) # type: LinearSystem
        plane_index = 0
        variable_index = 0
        while plane_index < len(system.planes):
            nonzero_index = system[plane_index].get_nonzero_index()
            if nonzero_index < 0:
                if not system.find_and_swap(variable_index, plane_index):
                    variable_index = variable_index + 1
                    plane_index = plane_index + 1
            elif nonzero_index > variable_index:
                if not system.find_and_swap(variable_index, plane_index):
                    variable_index = variable_index + 1
                    plane_index = plane_index + 1
            elif nonzero_index == variable_index:
                variable_index = variable_index + 1
                plane_index = plane_index + 1
            else:
                system.clear_variables(plane_index, variable_index, nonzero_index)

        return system

    # @property
    # def compute_triangular_form2(self):
    #     system = deepcopy(self)
    #
    #     current_index = 0
    #     while current_index < len(system.planes):
    #         current_zero_index = system[current_index].get_nonzero_index()
    #         if current_zero_index > current_index:
    #             # find the best fit
    #             maxindex = current_index
    #             min = current_zero_index
    #             for j in range(current_index+1, len(system.planes)):
    #                 if (system[j].get_nonzero_index() < min):
    #                     min = system[j].get_nonzero_index()
    #                     maxindex = j
    #
    #             system.swap_rows(current_index, maxindex)
    #             current_index = current_index + 1
    #         else:
    #             if not current_zero_index == current_index:
    #                 row_to_add_index = None
    #                 for j in range(0, current_index):
    #                     if system[j].get_nonzero_index() == current_zero_index:
    #                         row_to_add_index = j
    #                         break
    #
    #                 if row_to_add_index is not None:
    #                     current_factor = system[current_index][current_zero_index]
    #                     target_factor = system[row_to_add_index][current_zero_index]
    #                     coefficient = (current_factor / target_factor).copy_abs()
    #                     if target_factor * current_factor > 0:
    #                         coefficient = coefficient * -1
    #
    #                     system.add_multiple_times_row_to_row(coefficient, row_to_add_index, current_index)
    #                 else:
    #                     current_index = current_index + 1
    #             else:
    #                 current_index = current_index + 1
    #
    #     return system

    def compute_rref(self):
        '''
        reduce pivot variable coefficient to 1
        ensure pivot variable is alone in column
        :return: LinearSystem
        :rtype: LinearSystem
        '''
        tf = self.compute_triangular_form

        for i, x in enumerate(tf.indices_of_first_nonzero_terms_in_each_row()):
            if x >= 0:
                tf.reduce_pivot_variable_to_one(i, x)
                tf.clear_rows_above(i, x)

        return tf

    def reduce_pivot_variable_to_one(self, i, x):
        self.multiply_coefficient_and_row(Decimal('1') / self[i][x], i)

    def clear_rows_above(self, i, x):
        for j in range(0, i):
            if self[j][x] != 0:
                coefficient = (self[j][x] / self[i][x]).copy_abs()
                if self[j][x] * coefficient > 0:
                    coefficient = coefficient * -1
                self.add_multiple_times_row_to_row(coefficient=coefficient, row_to_add=i, row_to_be_added_to=j)

    def has_unique_solution(self):
        for x in self.planes:
            if x.get_nonzero_index() < 0 and not MyDecimal(x.constant_term).is_near_zero():
                return self.NO_SOLUTIONS_MSG

        if not len([x for x in self.indices_of_first_nonzero_terms_in_each_row() if x >= 0]) == self.dimension:
            return self.INF_SOLUTIONS_MSG

        return True

    def to_parametrization(self):
        plane_index = 0
        coefficient_index = 0
        basepoint = ['0']*self.dimension
        pivots = self.indices_of_first_nonzero_terms_in_each_row()
        number_of_direction_vectors = self.dimension - len(['0' for x in pivots if x >= 0])
        direction_vectors = [['0' for x in range(self.dimension)] for x in range(number_of_direction_vectors)]

        for i in range(0, len(self.planes)):
            pivot = self[i].get_nonzero_index()
            if pivot < 0:
                break
            basepoint[pivot] = self[i].constant_term

        for i in range(0, len(self.planes)):
            pivot = self[i].get_nonzero_index()
            if pivot < 0:
                break
            else:
                index = 0
                for j in range(pivot+1, self.dimension):
                    coefficient = self[i][j]
                    if not MyDecimal(coefficient).is_near_zero():
                        direction_vectors[index][pivot] = coefficient * Decimal('-1')
                    if j not in pivots:
                        index = index + 1

        index = 0
        for i in range(self.dimension):
            if i not in pivots:
                direction_vectors[index][i] = '1'
                index = index + 1

        return Parametrization(Vector(basepoint), map(lambda x: Vector(x), direction_vectors))

# def dot_product(vector_one, vector_two):
#     return sum([x*y for x,y in zip(vector_one, vector_two)])

# def get_row(matrix, row):
#     return matrix[row]









