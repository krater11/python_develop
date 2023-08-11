def dict_zip(a, b):
    dict_zip = []
    for i in a:
        row_dict = dict(zip(b,i))
        dict_zip.append(row_dict)
    result = dict_zip[0]
    return result
