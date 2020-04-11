def test_me(a, b, c):
    d = 0
    if a > b + c:
        print("1")
        if b != c:
            print("2")
            d += 1
        else:
            print("3")
            d += 2
    else:
        print("4")
        d = d - 1
    
    if d > 0:
        print("5")
        if a > 0:
            print("6")
            return 1
        else:
            print("7")
            return 2
    else:
        print("8")
        return 3