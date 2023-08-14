def get_file_filename(content_type, data):
    boundary = content_type.split('; ')[1].split('=')[1]
    parts = data.split(b'--' + boundary.encode())
    for part in parts:
        if b'filename=' in part:
            # 获取文件名
            filename_start = part.find(b'filename=')
            filename_end = part.find(b'\r\n', filename_start)
            image_name = part[filename_start + 10:filename_end - 1].decode()
            content_start = part.find(b'\r\n\r\n')
            image_file = part[content_start + 4:-2]

    return image_file, image_name