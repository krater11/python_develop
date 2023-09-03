def dict_zip(a, b):
    dict_zip = []
    row_dict = dict(zip(b, [x for x in a]))
    dict_zip.append(row_dict)
    result = dict_zip[0]
    return result


def dict_zip_multiple(a, b):
    dict_zip = []
    for i in a:
        row_dict = dict(zip(b, [x for x in i]))
        dict_zip.append(row_dict)
    return dict_zip