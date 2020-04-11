def test_me(x, y, z):
    if y > 13:
        print("1")
        if x < 2:
            print("2")
            z = 3
            if x < -1:
                print("3")
                z = 1
    else:
        print("4")
        x = 2
    y = 50
    if z == 4:
        print("5")
        z = 1
    else:
        print("6")
        while x < 5:
            print("7")
            x += 1
            z = z + 1
    y = 0
