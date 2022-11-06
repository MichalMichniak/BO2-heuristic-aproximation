from typing import Callable, List, Tuple, Dict
from Func import Func
from Func_f import Func_f
from Func_g import Func_g


class Objective_Function:
    def __init__(self, func_vect: List[List[Tuple[int]]], lut: Dict[int, Func],
                 metryka: Callable[[float, float], float]):
        """
        bounds func_vect  and lut to class
        """
        self.func_vector = func_vect
        self.lut = lut
        self.metryka = metryka

    def calculate_error_single(self, argument: List[float], desired_function: Callable[[List[float]], float]):
        """
        Calculates objective function for 1 argument, metrics is set in __init__
        args:
        argument : for  f:R^N->R list of size N
        desired_function : approximated function
        """
        current_layer_ind = 0
        last_layer_values = argument
        while current_layer_ind < len(self.func_vector):
            current_layer_values = [None for i in range(len(self.func_vector[current_layer_ind]))]
            for j in range(len(self.func_vector[current_layer_ind])):
                c_func = self.func_vector[current_layer_ind][j]
                if c_func is not None:
                    if len(c_func) == 2:
                        current_layer_values[j] = self.lut[c_func[0]].f_(last_layer_values[c_func[1]])
                    if len(c_func) == 3:
                        current_layer_values[j] = self.lut[c_func[0]].g_(last_layer_values[c_func[1]],
                                                                         last_layer_values[c_func[2]])
            print(current_layer_values)
            last_layer_values = current_layer_values
            current_layer_ind += 1

        vv = None
        for v in last_layer_values:
            if v is not None:
                vv = v
                break
        if vv is None:
            raise Exception("cos nie dziala, same nony w ostatniej warstwie")
        print(argument)
        print(desired_function(argument))
        print(vv)
        return self.metryka(vv, desired_function(argument))

    def calculate_for_all(self, dimension: int, steps: int, desired_function: Callable[[List[float]], float]):
        """
        Creates space of arguments and sum errors
        """
        arguments = generate_N_space(dimension, steps)
        obj_function = 0
        for arg in arguments:
            obj_function += self.calculate_error_single(arg, desired_function)
        return obj_function

    def calculate_for_all_normalized(self, dimension: int, steps: int, desired_function: Callable[[List[float]], float]):
        """
        Returns normalized oj function
        """
        return self.calculate_for_all(dimension, steps, desired_function)/steps**dimension


def generate_N_space(N: int, steps) -> List[List[float]]:
    '''
    Generates arguments space
    N from 1 to 5
            """
    args:
    N: dimension
    steps : result will be steps^N values
    return:
        List[List[floatxN]]: combination of all values from [-5,5]
    '''
    points = []
    if N == 1:
        points = [-5 + 10 / steps * i for i in range(steps)]
    if N == 2:
        points = [[-5 + 10 / steps * i, -5 + 10 / steps * j] for i in range(steps) for j in range(steps)]
    if N == 3:
        points = [[-5 + 10 / steps * i, -5 + 10 / steps * j, -5 + 10 / steps * k] for i in range(steps) for j in
                  range(steps) for k in range(steps)]
    if N == 4:
        points = [[-5 + 10 / steps * i, -5 + 10 / steps * j, -5 + 10 / steps * k, -5 + 10 / steps * m] for i in range(steps) for j in
                  range(steps) for k in range(steps) for m in range(steps)]
    if N == 5:
        points = [[-5 + 10 / steps * i, -5 + 10 / steps * j, -5 + 10 / steps * k, -5 + 10 / steps * m, -5 + 10 / steps * n] for i in range(steps) for j in
                  range(steps) for k in range(steps)  for m in range(steps) for n in range(steps)]
    return points

def example_for_test():
    print(generate_N_space(2, 3))
    f = Func_f(lambda x: x ** (1 / 2), 0)
    g = Func_g(lambda x, y: x + y, 0)
    lut = {1: f, 2: g}
    arg = [2, 1]
    vect = [
        [(1, 0), (2, 0, 1), (1, 1)],  ##warstwa 1
        [None, (2, 0, 2), (1, 2)],  ##warstwa 2
        [None, (1, 1), (1, 2)],  ##warstwa 3
        [None, (2, 1, 2), None]  ##warstwa 4
    ]

    of = Objective_Function(vect, lut, lambda x, y: (x ** 2 - y ** 2) ** (1 / 2))

    print(of.calculate_error_single([2, 1], lambda x: x[0] ** x[1]))
    print(of.calculate_for_all(2, 2, lambda x: x[0] ** abs(x[1])))
    print(generate_N_space(2,2))