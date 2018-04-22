from cvxpy import *

x, y, z = Variable(), Variable(), Variable()

# for constraint d, construct t = max(x, 1), m = max(y, 2) and k = (3x + y) ** 2
t, m, k = Variable(), Variable(), Variable()


constraint = {
    # The DCP rule ask affine == affine only, but the right side of original (a)
    # is not affine.
    # The original form is sqrt(square(x + 2y) + square(x - y)) == 0. Thus x + 2y == 0,
    # x - y == 0. This is equal to x = y = 0.
    'a': [x == y, x == 0],
    # This form can pass, ask Professor?
    'b': [square(square(x + y)) <= x - y],
    # The DCP rule only valid for convex <= concave, this is not valid.
    # Also, 1/x + 1/y is invalid because only scalar can be divided.
    # To satisfy 1/x + 1/y <= 1, x and y must > 1.
    'c': [x >= 1, y >= 1],
    # Cannot evaluate the truth value of a constraint or chain constraints.
    # for constraint (d), construct t = max(x, 1), m = max(y, 2) and k = (3x + y) ** 2
    # Thus, square(t) + square(m) <= k, let t = 1 and m = 2, k >= 5.
    'd': [square(t) + square(m) <= k, t >= 1, m >= 2, k >= 5],
    # xy in 'UNKNOWN' curvature in CVXPY, not in the valid DCP rule.
    # for constraint (e), construct t = xy. Because x >= 0 and y >= 0, thus t must >= 0.
    'e': [t >= 1],
    # DCP rule says that only scalar can be divided. (x + y) ^ 2 / sqrt(y) is invalid.
    # Use quad_over_lin in CVXPY to change the original (x + y) ** 2 / sqrt(y)
    'f': [quad_over_lin((x+y), sqrt(y)) <= x - y + 5],
    # This can be solved directly. Ask Professor?
    'g': [x ** 3 + y ** 3 <= 1, x >= 0, y >= 0],
    # The right side of (h) is 'UNKNOWN' to CVXPY.
    # Construct t = xy. Open the original, we get (x + z - 1) ** 2 <= xy - z**2
    # then (x + z - 1) ** 2 + z ** 2 <= xy = t.
    # Because x and y >=0, thus t >= 0.
    'h': [(x + z - 1) ** 2 + z ** 2 <= t, t >= 0]
}

objective = x + y - z

prob = Problem(Minimize(objective), constraint['f'])

prob.solve(solver=SCS)

p_opt = prob.value
x_opt = (x.value, y.value, z.value)

print ("optimal value : ", prob.value)
print ("optimal var : ", x.value, y.value, z.value)
