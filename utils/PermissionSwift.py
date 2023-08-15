def permission_swift(a):
    permissionlist = []
    for i in a:
        row_list = []
        for x in i:
            if x == "1":
                row_list.append("True")
            elif x == "0":
                row_list.append("False")
            else:
                row_list.append(x)
            row_tuple = tuple(row_list)
        permissionlist.append(row_tuple)

    return permissionlist