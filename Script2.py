x = 1
y = 2

def addxy():
    global x
    x += 1 
    return x+y


z = addxy()
print z