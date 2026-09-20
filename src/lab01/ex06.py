'''Lab 01, exercise 06'''
n = int(input('Число: '))
k = 0
m = 0
for x in range(n):
    a = input('участник лабы: ')
    if 'True' in a:
        k += 1
    else:
        m += 1
print(k,m)


