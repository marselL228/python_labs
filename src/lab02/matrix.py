###transpose
def transpose(mat: list[list[float | int]]) -> list[list]:
    if len(mat)==0:
        return []
    if all(len(x)==len(mat[0]) for x in mat):
        st = len(mat[0]) #2
        n = len(mat) #3
        nmat=[]
        for i in range(st):
            nrow = []
            for y in range(n):
                nrow.append(mat[y][i])
            nmat.append(nrow)
        return nmat
    else: 
        raise ValueError("Матрица рваная")  
#print(transpose([[1, 2, 3]]))          
#print(transpose([[1], [2], [3]]))      
#print(transpose([[1, 2], [3, 4]]))     
#print(transpose([]))                    
#print(transpose([[1, 2], [3]]))


#row_sums
def row_sums(mat: list[list[float | int]]) -> list[float]:
    if len(mat)==0: 
        raise ValueError("Пустой список")
    if not all(len(z)==len(mat[0]) for z in mat): 
        raise ValueError("Матрица рваная")
    else:
        return [sum(z) for z in mat]

#print(row_sums([[1, 2, 3], [4, 5, 6]]))     
#print(row_sums([[-1, 1], [10, -10]]))        
#print(row_sums([[0, 0], [0, 0]]))            
#print(row_sums([[1, 2], [3]]))                


#col_sums
def col_sums(mat: list[list[float | int]]) -> list[float]:   
    if len(mat)==0: 
        raise ValueError("Пустой список")
    if not all(len(q)==len(mat[0]) for q in mat): 
        raise ValueError("Матрица рваная")
    else:
        return [sum(st) for st in transpose(mat)] 

print(col_sums([[1, 2, 3], [4, 5, 6]]))     
print(col_sums([[-1, 1], [10, -10]]))        
print(col_sums([[0, 0], [0, 0]]))            
print(col_sums([[1, 2], [3]]))                
