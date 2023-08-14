def dict_zip(a, b):
    dict_zip = []
    row_dict = dict(zip(b, [x for x in a]))
    dict_zip.append(row_dict)
    result = dict_zip[0]
    return result
