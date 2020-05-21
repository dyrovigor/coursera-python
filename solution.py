import sys

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])

discriminant = pow(b, 2) - 4 * a * c

print(int((-b + pow(discriminant, 0.5)) / (2 * a)))
print(int((-b - pow(discriminant, 0.5)) / (2 * a)))
