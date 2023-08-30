from settings import MEDIA_LIST, IMAGE_LIST, AUDIO_LIST, VIDEO_LIST
def guess_type(filename):

    filename_list = filename.split(".")
    if filename_list[-1] == ''