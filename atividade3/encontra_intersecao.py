
p1 = (3,2.5)
p2 = (4,0.6)

q1 = (1,2.4)
q2 = (0.6,1.1)

# m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
# m2 = (q2[1] - q1[1]) / (q2[0] - q1[0])

# h1 = p1[1] - m1*p1[0]
# h2 = q1[1] - m1*q1[0]

# print(m1,m2)
# print(h1)
# #h = y0 - mx0

# xi = (h2-h1)/(m1-m2)
# yi = m1*xi + h1

# print(xi,yi)

# def line(p1, p2):
#     A = (p1[1] - p2[1]) #delta y
#     B = (p2[0] - p1[0]) #delta x 
#     C = (p1[0]*p2[1] - p2[0]*p1[1]) #x1*y2 - x2*y1
#     return A, B, -C

# def intersection(L1, L2):
#     D  = L1[0] * L2[1] - L1[1] * L2[0]
#     Dx = L1[2] * L2[1] - L1[1] * L2[2]
#     Dy = L1[0] * L2[2] - L1[2] * L2[0]
#     if D != 0:
#         x = Dx / D
#         y = Dy / D
#         return x,y
#     else:
#         return False


p1 = (3,2.5)
p2 = (4,0.6)

q1 = (1,2.4)
q2 = (0.6,1.1)

# L1 = line(p2,p1)
# print(L1)
# L2 = line(q2,q1)

# R = intersection(L1, L2)
# print(R)


def slope(P1, P2):
    # dy/dx
    # (y2 - y1) / (x2 - x1)
    return(P2[1] - P1[1]) / (P2[0] - P1[0])

def y_intercept(P1, slope):
    # y = mx + b
    # b = y - mx
    # b = P1[1] - slope * P1[0]
    return P1[1] - slope * P1[0]

def line_intersect(m1, b1, m2, b2):
    if m1 == m2:
        print ("These lines are parallel!!!")
        return None
    # y = mx + b
    # Set both lines equal to find the intersection point in the x direction
    # m1 * x + b1 = m2 * x + b2
    # m1 * x - m2 * x = b2 - b1
    # x * (m1 - m2) = b2 - b1
    # x = (b2 - b1) / (m1 - m2)
    x = (b2 - b1) / (m1 - m2)
    # Now solve for y -- use either line, because they are equal here
    # y = mx + b
    y = m1 * x + b1
    return x,y

m1 = slope(p1,p2)
m2 = slope(q1,q2)
yint_a = y_intercept(p1, m1)
yint_b = y_intercept(q1,m2)
print(line_intersect(m1, yint_a, m2, yint_b))
# A1 = [1,1]
# A2 = [3,3]
# B1 = [1,3]
# B2 = [3,1]
# slope_A = slope(A1, A2)
# slope_B = slope(B1, B2)
# y_int_A = y_intercept(A1, slope_A)
# y_int_B = y_intercept(B1, slope_B)
# print(line_intersect(slope_A, y_int_A, slope_B, y_int_B))