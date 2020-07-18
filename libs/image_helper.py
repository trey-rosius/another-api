import os
import re
from typing import Union

from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Take image and save to folder"""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """Take image name and folder and return full path"""
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """
    Given a format-less filename, try to find the file by appending each of the allowed formats to the given
    filename and check if the file exists
    :param filename: formatless filename
    :param folder: the relative folder in which to search
    :return: the path of the image if exists, otherwise None
    """
    for _format in IMAGES:  # look for existing avatar and delete it
        avatar = f"{filename}.{_format}"
        avatar_path = IMAGE_SET.path(filename=avatar, folder=folder)
        if os.path.isfile(avatar_path):
            return avatar_path
    return None



def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Take Filestorage and return the file name"""
    if isinstance(file, FileStorage):
        return file.filename
    return file

    pass


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    filename = _retrieve_filename(file)
    allowed_format = "|".join(IMAGES)  # png?svg?jpg?jpeg
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """Return full name of image in the path"""
    """get_basename('some/folder/image.jpg') returns 'image.jpg"""
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
