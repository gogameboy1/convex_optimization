from cvxpy import *

x1, x2 = Variable(), Variable()

constraint = [2 * x1 + 2 * x2 >= 1,
              2 * x1 + x2 >= 1,
              x1 >= 0,
              x2 >= 0]

objective = {
    '1': 4 * x1 + 5 * x2,
    '2': -x1 - x2,
    '3': x1,
    '4': max_elemwise([x1, x2]),
    '5': square(x1) + square(3 * x2),
}

index = input("input objective function index : ")

prob = Problem(Minimize(objective[index]), constraint)

prob.solve()

p_opt = prob.value
x_opt = (x1.value, x2.value)

print ("optimal value : ", prob.value)
print ("optimal var : ", x1.value, x2.value)
