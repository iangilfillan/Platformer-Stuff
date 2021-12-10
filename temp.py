from math import ceil


input_string = "ippi"

left = input_string[:ceil(len(input_string)/2)]
t_right = input_string[len(input_string)//2:]
right = ""

for i in t_right:
    right = i + right

print(left == right)