from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from libs import image_helper
import traceback
import os
from schemas.image_schema import ImageSchema

image_schema = ImageSchema()
IMAGE_UPLOAD = "Image {} uploaded"
IMAGE_ILLEGAL_EXTENSION = "Illegal image extension {}"
IMAGE_ILLEGAL_FILE_NAME = "Illegal file name {} requested"
IMAGE_NOT_FOUND = "{} Not found"
IMAGE_DELETED = "{} deleted successfully"
IMAGE_DELETION_FAILED = "Internal server error! Failed to delete image"
AVATAR_DELETE_FAILED = "Internal server error! Failed to delete avatar"
AVATAR_UPLOADED = "Avatar {} successfully uploaded"
AVATAR_NOT_FOUND = "Avatar not found"


class ImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        """
        Used to upload an image to server
        It users JWT to retrieve our information and then
        saves the image to our image folder
        If there's a file name conflict, it'll append the number
        at the end

        """
        data = image_schema.load(request.files)  # {"image":FileStorage}
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"  # static/images
        try:
            image_path = image_helper.save_image(data['image'],
                                                 folder=folder)
            basename = image_helper.get_path(image_path)
            return {"message": IMAGE_UPLOAD.format(basename)}, 201

        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": IMAGE_ILLEGAL_EXTENSION.format(extension)}, 400


class Image(Resource):
    @classmethod
    @jwt_required
    def get(cls, filename: str):
        """
                    Returns the requested image if it exists.
                    Looks up inside the logged in user's folder
                    :param filename:
                    :return:
                    """

        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_helper.is_filename_safe(filename):
            return {"message": IMAGE_ILLEGAL_FILE_NAME.format(filename)}, 400

        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND.format(filename)}, 404

    @classmethod
    @jwt_required
    def delete(cls, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not image_helper.is_filename_safe(filename):
            return {"message": IMAGE_ILLEGAL_FILE_NAME.format(filename)}, 400

        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": IMAGE_DELETED.format(filename)}, 200
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND.format(filename)}, 404

        except:
            traceback.print_exc()
            return {"message": IMAGE_DELETION_FAILED}, 500


class AvatarUpload(Resource):
    @classmethod
    @jwt_required
    def put(cls):
        data = image_schema.load(request.files)
        filename = f"user_{get_jwt_identity()}"
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": AVATAR_DELETE_FAILED}, 500

        try:
            ext = image_helper.get_extension(data['image'].filename)
            avatar = filename + ext
            avatar_path = image_helper.save_image(
                data["image"], folder=folder, name=avatar
            )
            basename = image_helper.get_basename(avatar_path)
            return {"message": AVATAR_UPLOADED.format(basename)}, 200
        except UploadNotAllowed:
            extension = image_helper.get_extension(data['image'])
            return {"message": IMAGE_ILLEGAL_EXTENSION.format(extension)}, 400


class Avatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        folder = 'avatars'
        filename = f"user_{user_id}"
        avatar = image_helper.find_image_any_format(filename, folder)
        if avatar:
            return send_file(avatar)
        return {"message": AVATAR_NOT_FOUND}, 404
