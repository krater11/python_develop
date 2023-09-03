from settings import MEDIA_LIST, IMAGE_LIST, AUDIO_LIST, VIDEO_LIST


def guess_type(filename):
    filename_list = filename.split(".")
    if filename_list[-1] in MEDIA_LIST:
        if filename_list[-1] in IMAGE_LIST:
            file_path = '/media/image'
        elif filename_list[-1] in AUDIO_LIST:
            file_path = '/media/audio'
        elif filename_list[-1] in VIDEO_LIST:
            file_path = '/media/video'
    else:
        file_path = '/file'

    return file_path