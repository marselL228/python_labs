'''Lab 01, exercise 06'''
n = int(input('in_1: '))
k = 0
m = 0
for x in range(n):
    a = input(f'in_{x+2}: ')
    if 'True' in a:
        k += 1
    else:
        m += 1
print(k,m)


