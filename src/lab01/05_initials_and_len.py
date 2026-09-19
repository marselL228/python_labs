'''Lab 01, exercise 05.'''
a = input('ФИО: ').split()
name = ' '.join(a)
initials = a[0][0] + a[1][0] + a[2][0]
print(f'Инициалы: {initials.upper()}.')
print(f'Длина (символов): {len(name)}')

