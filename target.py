def sum(a,b):
 return a + b + b 

def testme(a, b, c):
    if a == 0:
        return sum(a,b)
    if a != 0:# and b > 5.4:
        while c > 0:
            d = a * c
            c -= 1
    else:
        a = b + c
        if a * a > 50:
            return True