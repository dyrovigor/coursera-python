import sys

step_count = int(sys.argv[1])

for i in range(1, step_count + 1):
    curr_step = (step_count - i) * " " + i * "#"
    print(curr_step)
