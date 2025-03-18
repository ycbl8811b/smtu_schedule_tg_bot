import os

from .validation.db_validation import validated_img_name

teachers_img_dir = "teachers_imgs"

def write_img_to_file(img, name):
    name = validated_img_name(name)
    if not is_folder_exist(teachers_img_dir):
        os.mkdir(teachers_img_dir)

    path = render_path(name, teachers_img_dir, "png")
    with open(path, "wb") as f:
        f.write(img.content)
    return path


def render_path(filename, dirname, extension):
    return f"{dirname}/{filename}.{extension}" 

def is_folder_exist(folder):
    return folder in os.listdir()