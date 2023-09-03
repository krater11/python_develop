def get_file_information(data):
    imagename = []
    imagefile = []
    if type(data) == type(imagename):
        for i in data:
            image_file = i.file.read()
            image_name = i.filename
            imagefile.append(image_file)
            imagename.append(image_name)
    else:
        imagefile.append(data.file.read())
        imagename.append(data.filename)

    return imagename, imagefile