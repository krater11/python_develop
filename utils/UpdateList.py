def update_list(a, b, c):
    try:
        count = 0
        for i in a:
            if i == b:
                a[count] = c
            else:
                count += 1
        return a
    except Exception:
        print("error")


def tuple_list(a):
    count = 0
    for i in a:
        a[count] = list(i)
        count += 1
    return a