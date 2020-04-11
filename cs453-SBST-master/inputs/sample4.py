def test_me(x, y, z):
    a = 0
    b = 0
    c = 0

    if x == 4:
        print("1")
        a += 1
        if x + y == 100:
            print("2")
            a += 1
            if z > 112831829389:
                print("3")
                a += 1
            else:
                print("4") 
        elif x + y == 40:
            print("5")