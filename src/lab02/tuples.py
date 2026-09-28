def format_record(rec: tuple[str, str, float]) -> str:
    """Форматирует запись студента."""
    
    if type(rec) != tuple: #Проверка на кортеж 
        raise TypeError("Входные данные должны быть кортежем")
#-------------------------
    if len(rec) < 3: #недополнение
        raise ValueError("Неполный формат входных данных")
    if len(rec) > 3: #переполнение
        raise IndexError("Слишком много входных данных")
#---------------------------
    if not isinstance(rec[0], str) or not isinstance(rec[1], str) \
    or not isinstance(rec[2], (int, float)): 
        raise TypeError("Некорректный тип входных данных")

#---------------------------

    if not rec[0].strip(): raise ValueError("Пустое ФИО")
    if not rec[1].strip(): raise ValueError("Пустая группа")
    if not isinstance(rec[2], (int, float)) : raise TypeError("некооректный тип GPA")
    if rec[2] < 0 or rec[2] > 5:
        raise ValueError("GPA должен быть от 0 до 5")
    
    

    # name
    FIO = rec[0]
    FIOsplited = FIO.split()

    if len(FIOsplited) < 2: #проверка имени
        raise ValueError("ФИО должно содержать минимум фамилию и имя")

    initials = ''.join([name[0] for name in FIOsplited]).upper()

    if len(FIOsplited) == 3:
        name = FIOsplited[0][0].upper() + FIOsplited[0][1:] + " " + initials[1] + "." + initials[2] + "."
    if len(FIOsplited) == 2:
        name = FIOsplited[0][0].upper() + FIOsplited[0][1:] + " " + initials[1] + "."
    
    # group
    group = rec[1]
    # gpa
    gpa = rec[2]

    return f"{name}, гр. {group}, GPA {gpa:.2f}"

print(format_record(("Иванов Иван Иванович", "BIVT-25", 4.6)))  
 #Иванов И.И., гр. BIVT-25, GPA 4.60

print(format_record(("Петров Петр ", "IKBO-12", 5.0)))  
 #Петров П., гр. IKBO-12, GPA 5.00

print(format_record(("Петров Пётр Петрович", "IKBO-12" , 5.0)))  
 #Петров П.П., гр. IKBO-12, GPA 5.00

print(format_record(("  сидорова  анна  сергеевна ", "ABB-01", 3.9999)))  
 #Сидорова А.С., гр. ABB-01, GPA 4.00