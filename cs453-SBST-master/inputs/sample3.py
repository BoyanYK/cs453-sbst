def test_me(x):
    z = 0
    if x == 2:
        print("1")
        return z
    for i in range(x):
        print("2")
        z += 1
    else:
        print("3")
        if z == 0:
            print("4")
            return x
        while z > 0:
            print("5")
            z -= 1
    return z
