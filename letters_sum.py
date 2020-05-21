import sys

digit_string = sys.argv[1]

result_sum = 0

for letter in digit_string:
    result_sum += int(letter)

print(result_sum)
