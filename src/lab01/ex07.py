'''Lab 01, exercise 07'''
n = input()
k = []

for x in range(len(n)):
    if n[x].isupper():
        k.append(n[x])
        m = x
        break

for x in range(len(n)):
    if n[x].isdigit():
        step = x + 1 - m
        break

x = m + step
while x < len(n):
    k.append(n[x])
    if n[x] == '.':
        break
    x += step

print(''.join(k))
