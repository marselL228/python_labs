'''Lab 01, exercise 04.'''
minutes = int(input('m: '))
pr = minutes //60
min = minutes % 60
print(f'{pr:02d}:{min:02d}')
